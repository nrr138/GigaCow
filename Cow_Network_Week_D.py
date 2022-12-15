import pandas as pd
import numpy as np
import datetime
import itertools
import random
from pyvis.network import Network
import matplotlib.pyplot as plt
import networkx as nx


# Change date to minutes
def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2020,1,1)
    return int(t.total_seconds()//60)

# Change date to minutes (for lactation)
def time_calc_lact(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10])) - datetime.datetime(2020,1,1)
    return int(t.total_seconds()//60)
### -------------------------------------------------------------------------------------------------------------
### Import Waitroom or Robot Milking data -----------------------------------------------------------------------
### -------------------------------------------------------------------------------------------------------------
def Waitroom_Traffic(farm_name, time, cut):
    data = pd.read_csv(farm_name)

    data['TrafficEventDateTime']=data['TrafficEventDateTime'].map(time_calc)
    data = data.sort_values(by=['TrafficEventDateTime'])
    data = data.reset_index(drop=True)
    start_time=data['TrafficEventDateTime']
    kor=data["Gigacow_Cow_Id"]

    network=Calc_Network(start_time, kor, time, cut)
    return network, start_time[0]

def Waitroom_Traffic_shuffle(farm_name, time, cut):
    data = pd.read_csv(farm_name)

    start_time=data['TrafficEventDateTime']
    kor=data["Gigacow_Cow_Id"]

    network=Calc_Network(start_time, kor, time, cut)
    return network

def Robot_Milkings(farm_name, time, cut):
    data = pd.read_csv(farm_name)
    data['MilkingStartDateTime']=data['MilkingStartDateTime'].map(time_calc)
    data = data.sort_values(by=['MilkingStartDateTime'])
    data = data.reset_index(drop=True)
    start_time=data['MilkingStartDateTime']
    kor=data["Gigacow_Cow_Id"] 

    network=Calc_Network(start_time, kor, time, cut)
    return network, start_time[0]

def Robot_Milkings_shuffle(farm_name, time, cut):
    data = pd.read_csv(farm_name)

    start_time=data['MilkingStartDateTime']
    kor=data["Gigacow_Cow_Id"] 

    network=Calc_Network(start_time, kor, time, cut)
    return network
### -------------------------------------------------------------------------------------------------------------
### Cow network -------------------------------------------------------------------------------------------------
### -------------------------------------------------------------------------------------------------------------

# Extract pairs from cow groups
def cow_groups(lst):
    combs = []
    for r in range(len(lst)+1):
        for comb in itertools.combinations(set(lst), r):
            if len(comb) == 2:
                combs.append(tuple(sorted(comb)))
    return combs

# Calculate network
def Calc_Network(start_time, kor, time, cut):
    
    hold=[]
    week_network = []
    cow_dict={}
    week = 1
    
    for i in range(len(kor)-1):
        if abs(start_time[i] - start_time[0]) > 10080*week:
            week_network = week_network + save_network(cow_dict, week, cut)
            week += 1
            cow_dict={}

        hold.append(int(kor[i]))
        if not abs((start_time[i]-start_time[i+1])) <= time or len(hold) > 2:
            if len(hold) > 1:
                h = cow_groups(hold)

                for group in h:

                    if group not in cow_dict: 
                        cow_dict[group]=1
                    else:
                        cow_dict[group]+=1
            hold=[]
    return week_network

# Save network in list
def save_network(cow_dict,w,cut):
    print_csv = []
    cut_off= cut
    new_dict = {}
    for (key, value) in cow_dict.items():
        if value >= cut_off:
            new_dict[key] = value

    sortedd = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse= False))
    for (key, value) in sortedd.items():
        #print('Cows: '+ str(key) + '\tNumber: ' + str(value))
        if value >= cut_off:
            print_csv.append([key[0],key[1], value, w])
    return print_csv


### ----------------------------------------------------------------------------------------------------------------------------------
### Networks -------------------------------------------------------------------------------------------------------------------------
### ----------------------------------------------------------------------------------------------------------------------------------

# Network visulisation
def network_graph(lst,w,name):
    # To create an empty undirected graph
    G = Network(height="1000px", width="1200px", bgcolor="#222222", font_color="white",select_menu=True, neighborhood_highlight=True)
    G.barnes_hut(gravity=-500, central_gravity=0.3)

    for pc in lst:

        if pc[2] > 2 and pc[3] == w:
            G.add_node(str(pc[0]), title=str(pc[0]))
            G.add_node(str(pc[1]), title=str(pc[1]))
            G.add_edge(str(pc[0]), str(pc[1]), value=pc[2])

    neighbor_map = G.get_adj_list()

    # add neighbor data to node hover data
    for node in G.nodes:
                    node["title"] += " Neighbors:\n" + "\n".join(neighbor_map[node["id"]])
                    node["value"] = len(neighbor_map[node["id"]])



    G.show_buttons(filter_=['physics'])
    G.toggle_physics(True)
    G.show(name+'_'+str(w)+'.html')


# Networkx graph
def networkx_graph(lst,w):
    G = nx.Graph()
    for pc in lst:
        if pc[2] > 2 and pc[3] == w:
            G.add_node(pc[0], label=str(pc[0]))
            G.add_node(pc[1], label=str(pc[1]))
            G.add_edge(pc[0], pc[1], value=pc[2] )    

    # Degree/Eigenvector centrality (connected a node is to other nodes)
    de_cent = nx.degree_centrality(G)

    # Average shortest path (how many edges on average we need to go through between two nodes)
    try:
        avg_path = nx.average_shortest_path_length(G)
    except:
        avg_path = None

    # Maximum shortest path
    try:
        max_path = nx.diameter(G)
    except:
        max_path = None

    # Transistivity (how likely nodes cluster in a network, how likely to form groups)
    transistivity = nx.transitivity(G)

    # Connectivity (how many edges are needed to be removed for the graph to become disconnected)
    try:
        L = nx.normalized_laplacian_matrix(G)
        e = np.linalg.eigvals(L.toarray())
        e = np.sort(e)
        # Spectral radius (approximetly average amount of edged node has)
        spec_rad = max(e)
        # Fiedler value (algebraic connectivity)
        Fiedler = e[1]
    except:
        spec_rad = None
        Fiedler = None

    try:
        adj_m= nx.adjacency_matrix(G)
        adj_eig = np.linalg.eigvals(adj_m.toarray())
        adj_eig = np.sort(adj_eig)
    except:
        adj_eig = np.array([])
    #adj_eig = nx.spectrum.laplacian_spectrum(G)

    return de_cent, avg_path, max_path, transistivity, spec_rad, Fiedler, adj_eig

# Data from networkx graph
def networkx_data(print_csv, w1,w2):
    weeks_iter = range(w1,w2)
    avg_path = []
    transistivity = [] 
    spec_rad = []
    Fiedler = []
    max_path = []
    de_cent = pd.DataFrame([])
    adj_eig = []
    for i in weeks_iter:
        dc,a,m,t,sr,f,ae = networkx_graph(print_csv, i)
        de_cent = de_cent.append(dc,ignore_index=True)
        avg_path.append(a)
        max_path.append(m)
        transistivity.append(t)
        spec_rad.append(sr)
        Fiedler.append(f)
        adj_eig.append(ae)

    # Degree centrality
    de_cent_avg = dict(de_cent.mean())

    # Eigenvector Similarity
    def min_k(values, min_sum = 0.9):
        r_total = 0
        total = sum(values)
        if total == 0:
            return len(values)
        for i in range(len(values)):
            r_total += values[i]
            if r_total / total >= min_sum:
                return i + 1
        return len(values)

    sim = []
    for i in range(len(adj_eig)-1):
        k1 = min_k(adj_eig[i])
        k2 = min_k(adj_eig[i+1])
        k = min(k1,k2)
        sim.append(sum((adj_eig[i][:k]-adj_eig[i+1][:k])**2))

    plt.figure(5)
    plt.title('Average Degree centrality for weeks '+ str(weeks_iter[0])+'-'+str(weeks_iter[-1]))
    plt.ylabel('Centrality')
    plt.xlabel('Cows')
    plt.bar(de_cent_avg.keys(), de_cent_avg.values(),width=60)

    plt.figure(6)
    plt.title('Average shortest path for weeks '+ str(weeks_iter[0])+'-'+str(weeks_iter[-1]))
    plt.ylabel('Average shortest path')
    plt.xlabel('Weeks')
    plt.plot(weeks_iter, avg_path, 'o-')

    plt.figure(7)
    plt.title('Transistivity for weeks '+ str(weeks_iter[0])+'-'+str(weeks_iter[-1]))
    plt.ylabel('Transistivity')
    plt.xlabel('Weeks')
    plt.plot(weeks_iter, transistivity, 'o-')

    """     plt.figure(8)
    plt.title('Diameter of network')
    plt.ylabel('Diameter')
    plt.xlabel('Weeks')
    plt.plot(weeks_iter, max_path, 'o')

    plt.figure(9)
    plt.title('Spectral radius')
    plt.ylabel('Spectral radius')
    plt.xlabel('Weeks')
    plt.plot(weeks_iter, spec_rad, 'o-')

    plt.figure(10)
    plt.title('Fiedler value')
    plt.ylabel('Fiedler value')
    plt.xlabel('Weeks')
    plt.plot(weeks_iter, Fiedler, 'o-')

    plt.figure(11)
    plt.title('Eigenvector Similarity')
    plt.ylabel('Eigenvector Similarity')
    plt.xlabel('Weeks')
    plt.plot(range(w1,w2-1), sim, 'o-') """

def lactation_list(farm):
    lac_data = pd.read_csv(farm)

    lac_data['LactationInfoDate']=lac_data['LactationInfoDate'].map(time_calc_lact)
    lac_data = lac_data.sort_values(by=['LactationInfoDate'])
    lac_data = lac_data.reset_index(drop=True)

    return lac_data

def network_lactation(lst,lst_lac,w,name,time):
    # To create an empty undirected graph
    G = Network(height="1000px", width="1200px", bgcolor="#222222", font_color="white",select_menu=True, neighborhood_highlight=True)
    G.barnes_hut(gravity=-500, central_gravity=0.3)

    cow_id = lst_lac['Gigacow_Cow_Id']
    lactation = lst_lac['LactationNumber']
    date = lst_lac['LactationInfoDate']
    lac_value = {}

    for i in range(len(cow_id)):
        if abs(date[i]-time) <= 10080*(w+1):
            if lactation[i] == 1:
                lac_value[cow_id[i]] = '#cbd113'
            elif lactation[i] == 2:
                lac_value[cow_id[i]] = '#35d119'
            elif lactation[i] == 3:
                lac_value[cow_id[i]] = '#157fd6'
            elif lactation[i] > 3:
                lac_value[cow_id[i]] = '#bf1ba7'

    for pc in lst:
        if pc[2] > 2 and pc[3] == w:
            if pc[0] not in lac_value:
                lac_value[pc[0]] = '#ff0000'
            if pc[1] not in lac_value:
                lac_value[pc[1]] = '#ff0000'
            G.add_node(str(pc[0]), title=str(pc[0]), color=lac_value[pc[0]])
            G.add_node(str(pc[1]), title=str(pc[1]), color=lac_value[pc[1]])
            G.add_edge(str(pc[0]), str(pc[1]), value=pc[2])

    neighbor_map = G.get_adj_list()

    # add neighbor data to node hover data
    for node in G.nodes:
                    node["title"] += " Neighbors:\n" + "\n".join(neighbor_map[node["id"]])
                    node["value"] = len(neighbor_map[node["id"]])

    G.show_buttons(filter_=['physics'])
    G.toggle_physics(True)
    G.show(name+'_'+str(w)+'.html') 

### ----------------------------------------------------------------------------------------------------------------------------------
### Run code -------------------------------------------------------------------------------------------------------------------------
### ----------------------------------------------------------------------------------------------------------------------------------

#- Get network list (data CSV, time cut off, value cut off)
MILK_network_list_A6, _ = Robot_Milkings('RobotMilkings_A6.csv', 30, 1)
MILK_network_list_random_A6 = Robot_Milkings_shuffle('RobotMilkings_A6_random.csv', 30, 1)
MILK_network_list_F4, _= Robot_Milkings('RobotMilkings_F4.csv', 30, 1)
MILK_network_list_random_F4 = Robot_Milkings_shuffle('RobotMilkings_F4_random.csv', 30, 1) 

TRAFFIC_network_list_A6, _ = Waitroom_Traffic('Waitroom_Traffic_A6.csv', 1, 1)
TRAFFIC_network_list_random_A6 = Waitroom_Traffic_shuffle('Waitroom_Traffic_A6_random.csv', 1, 1)
TRAFFIC_network_list_F4, _= Waitroom_Traffic('Waitroom_Traffic_F4.csv', 2, 1)
TRAFFIC_network_list_random_F4 = Waitroom_Traffic_shuffle('Waitroom_Traffic_F4_random.csv', 2, 1)

#- Plot visualisation of network (network list, week, random bool, traffic bool)
## Might need "Live Server" extension or other appropriate way to open html code
network_graph(MILK_network_list_A6, 100, 'Milk_network_A6') 
network_graph(MILK_network_list_random_A6, 100, 'Milk_network_random_A6')
network_graph(MILK_network_list_F4, 100, 'Milk_network_F4')
network_graph(MILK_network_list_random_F4, 100, 'Milk_network_random_F4') 

network_graph(TRAFFIC_network_list_A6, 80, 'Traffic_network_A6') 
network_graph(TRAFFIC_network_list_random_A6, 80, 'Traffic_network_random_A6')
network_graph(TRAFFIC_network_list_F4, 10, 'Traffic_network_F4')
network_graph(TRAFFIC_network_list_random_F4, 10, 'Traffic_network_random_F4')

def plotdata():
    plt.figure(5)
    plt.legend(["Original", "Randomized"])
    plt.figure(6)
    plt.legend(["Original", "Randomized"])
    plt.figure(7)
    plt.legend(["Original", "Randomized"])
    plt.show()

#- Plot data from network (network list, start week, end week)
networkx_data(TRAFFIC_network_list_F4,0,13)
networkx_data(TRAFFIC_network_list_random_F4,0,13)
plotdata()
networkx_data(TRAFFIC_network_list_A6,46,134)
networkx_data(TRAFFIC_network_list_random_A6,46,134)
plotdata()

""" networkx_data(MILK_network_list_A6,0,134) 
networkx_data(MILK_network_list_random_A6,0,134)
plotdata()
networkx_data(MILK_network_list_A6,0,134)
networkx_data(MILK_network_list_random_A6,0,134)
plotdata() """

#- Include lactation in network graph
network_listA6, first_trafficA6 = Waitroom_Traffic('Waitroom_Traffic_A6.csv', 1, 2)
network_listF4, first_trafficF4 = Waitroom_Traffic('Waitroom_Traffic_F4.csv', 1, 2)
network_lactation(network_listA6,lactation_list('Lactations_A6.csv'), 80, 'Traffic_network_A6_Lactation', first_trafficA6) 
network_lactation(network_listF4,lactation_list('Lactations_F4.csv'), 10, 'Traffic_network_F4_Lactation', first_trafficF4) 