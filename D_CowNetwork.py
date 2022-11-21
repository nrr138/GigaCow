import pandas as pd
import numpy as np
import datetime
import itertools

def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2015,1,1)
    return int(t.total_seconds()//60)

#data = pd.read_csv('RobotMilkings_A6_traffic.csv')
data = pd.read_csv('RobotMilkings_F4_traffic.csv')

data['TrafficEventDateTime']=data['TrafficEventDateTime'].map(time_calc)
data = data.sort_values(by=['TrafficEventDateTime'])
data = data.reset_index(drop=True)
star_time=data['TrafficEventDateTime']
kor=data["Gigacow_Cow_Id"]

""" #data = pd.read_csv('RobotMilkings_A6.csv')
data = pd.read_csv('RobotMilkings_F4.csv')
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

def cow_groups(lst):
    combs = []
    for r in range(len(lst)+1):
        for comb in itertools.combinations(set(lst), r):
            if len(comb) == 2:
                combs.append(tuple(sorted(comb)))
    return combs

for i in range(len(kor)-1):

    hold.append(int(kor[i]))
    if not abs((star_time[i]-star_time[i+1])) <= time or len(hold) > 4:
        if len(hold) > 1:
            h = cow_groups(hold)

            for group in h:

                if group not in cow_dict: 
                    cow_dict[group]=1
                else:
                    cow_dict[group]+=1
        hold=[]

new_dict = {}
for (key, value) in cow_dict.items():
   if value > 1:
       new_dict[key] = value

print_csv = []
sorted = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse= False))
for (key, value) in sorted.items():
    print('Cows: '+ str(key) + '\tNumber: ' + str(value))
    if value > 150:
        print_csv.append([key[0],key[1], value])


# Print export
import csv

header = ['cow1', 'cow2','num']
with open('super_network_plot.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(print_csv)


# To import package
from pyvis.network import Network
import matplotlib.pyplot as plt

# To create an empty undirected graph
G = Network(height="1000px", width="1200px", bgcolor="#222222", font_color="white",select_menu=True, neighborhood_highlight=True)
G.barnes_hut(gravity=-550, central_gravity=0.2)

for (key, value) in sorted.items():

    if value > 150:
        G.add_node(str(key[0]), title=str(key[0]))
        G.add_node(str(key[1]), title=str(key[1]))
        G.add_edge(str(key[0]), str(key[1]), value=value)

neighbor_map = G.get_adj_list()

# add neighbor data to node hover data
for node in G.nodes:
                node["title"] += " Neighbors:\n" + "\n".join(neighbor_map[node["id"]])
                node["value"] = len(neighbor_map[node["id"]])



G.show_buttons(filter_=['physics'])
G.toggle_physics(False)
G.show('nx_milk.html')
