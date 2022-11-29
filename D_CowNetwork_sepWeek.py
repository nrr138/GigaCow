import pandas as pd
import numpy as np
import datetime
import itertools
import random

def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2015,1,1)
    return int(t.total_seconds()//60)

data = pd.read_csv('RobotMilkings_A6_traffic.csv')
#data = pd.read_csv('RobotMilkings_F4_traffic.csv')

data['TrafficEventDateTime']=data['TrafficEventDateTime'].map(time_calc)
data = data.sort_values(by=['TrafficEventDateTime'])
data = data.reset_index(drop=True)
star_time=data['TrafficEventDateTime']
kor=data["Gigacow_Cow_Id"]

""" data = pd.read_csv('RobotMilkings_A6.csv')
#data = pd.read_csv('RobotMilkings_F4.csv')

data['MilkingStartDateTime']=data['MilkingStartDateTime'].map(time_calc)
data = data.sort_values(by=['MilkingStartDateTime'])
data = data.reset_index(drop=True)
star_time=data['MilkingStartDateTime']
kor=data["Gigacow_Cow_Id"] """


print('-----Time Data-----')
print(star_time)
print('------Cow Data-----')
print(kor)
print('\n------------Data info---------------')
print('Number of cows in farm:', len(np.unique(np.array(kor))))
print('------------------------------------\n')
hold=[]
time=1
cow_dict={}
print_csv = []



def save_plot(cow_dict,w):
    cut_off= 1
    new_dict = {}
    for (key, value) in cow_dict.items():
        if value >= cut_off:
            new_dict[key] = value


    sortedd = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse= False))
    for (key, value) in sortedd.items():
        print('Cows: '+ str(key) + '\tNumber: ' + str(value))
        if value >= cut_off:
            print_csv.append([key[0],key[1], value, w])


def cow_groups(lst):
    combs = []
    for r in range(len(lst)+1):
        for comb in itertools.combinations(set(lst), r):
            if len(comb) == 2:
                combs.append(tuple(sorted(comb)))
    return combs
week = 1


for i in range(len(kor)-1):
    if abs(star_time[i]-star_time[0]) > 10080*week:
        save_plot(cow_dict, week)
        week += 1
        cow_dict={}

    hold.append(int(kor[i]))
    if not abs((star_time[i]-star_time[i+1])) <= time or len(hold) > 5:
        if len(hold) > 1:
            h = cow_groups(hold)

            for group in h:

                if group not in cow_dict: 
                    cow_dict[group]=1
                else:
                    cow_dict[group]+=1
        hold=[]




# Print export
""" import csv

header = ['cow1', 'cow2','num','week']
with open('plot.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(print_csv) """


    
    
from pyvis.network import Network
import matplotlib.pyplot as plt
def network_graph(lst,w):
    # To create an empty undirected graph
    G = Network(height="1000px", width="1200px", bgcolor="#222222", font_color="white",select_menu=True, neighborhood_highlight=True)
    G.barnes_hut(gravity=-550, central_gravity=0.2)

    for pc in lst:

        if pc[2] > 6 and pc[3] == w:
            G.add_node(str(pc[0]), title=str(pc[0]))
            G.add_node(str(pc[1]), title=str(pc[1]))
            G.add_edge(str(pc[0]), str(pc[1]), value=pc[2])

    neighbor_map = G.get_adj_list()

    # add neighbor data to node hover data
    for node in G.nodes:
                    node["title"] += " Neighbors:\n" + "\n".join(neighbor_map[node["id"]])
                    node["value"] = len(neighbor_map[node["id"]])



    G.show_buttons(filter_=['physics'])
    G.toggle_physics(False)
    G.show('network_week_'+str(w)+'.html')


network_graph(print_csv, 50)
#network_graph(print_csv, 51)

def dictcor(d1, d2):
    diff=0
    tot=0
    for (key) in d1:
        if key in d2:
            tot += (d1[key]+d2[key])
            diff+= (d1[key]+d2[key])-abs(d1[key]-d2[key])
        else:
            tot+= d1[key]
    if tot == 0:
        return 0
    return diff/tot

""" def dictcor(d1,d2):
    hold=0
    
    for (key) in d1:
        if d1[key] > 5:
            if key in d2:
                hold+=1
    if len(d2) == 0:
        return 0
    return hold/len(d2) """

def to_dict(lst1, w):
    dict1 = {}
    dict2 = {}
    for lst in lst1:
        if lst[3] == w:
            dict1[(lst[0], lst[1])] = lst[2]
    for lst in lst1:
        if lst[3] == w+1:
            dict2[(lst[0], lst[1])] = lst[2]
    return (dict1, dict2)


week_cor = {}
for i in range(print_csv[-1][3]):
    dw= to_dict(print_csv, i)
    cor = dictcor(dw[0], dw[1])
    week_cor[i] = cor

rand_week_cor = {}
for i in range(print_csv[-1][3]):
    lst_rand = []
    for n in range(len(print_csv)):
        if print_csv[n][3] == i:
            lst_rand.append(print_csv[n][2])
    random.shuffle(lst_rand)
    k = 0
    for n in range(len(print_csv)):
        if print_csv[n][3] == i:
            print_csv[n][2] = lst_rand[k]
            k += 1
    dw= to_dict(print_csv, i)
    cor = dictcor(dw[0], dw[1])
    rand_week_cor[i] = cor


plt.figure(1)
plt.ylabel('Week correlation')
plt.xlabel('Weeks')
plt.bar(list(week_cor.keys()), week_cor.values(), color='g')

plt.figure(2)
plt.title('Random')
plt.ylabel('Week correlation')
plt.xlabel('Weeks')
plt.bar(list(rand_week_cor.keys()), rand_week_cor.values(), color='g')
plt.show()
