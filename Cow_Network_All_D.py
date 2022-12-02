import pandas as pd
import numpy as np
import datetime
import itertools

# Change date to minutes
def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2020,1,1)
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

    network=Calc_Network(start_time, kor, time)
    print_network(network, cut)

def Robot_Milkings(farm_name, time, cut):
    data = pd.read_csv(farm_name)
    data['MilkingStartDateTime']=data['MilkingStartDateTime'].map(time_calc)
    data = data.sort_values(by=['MilkingStartDateTime'])
    data = data.reset_index(drop=True)
    start_time=data['MilkingStartDateTime']
    kor=data["Gigacow_Cow_Id"] 

    network=Calc_Network(start_time, kor, time)
    print_network(network, cut)

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
def Calc_Network(start_time, kor, time):
    hold=[]
    cow_dict={}

    for i in range(len(kor)-1):

        hold.append(int(kor[i]))
        if not abs((start_time[i]-start_time[i+1])) <= time or len(hold) > 4:
            if len(hold) > 1:
                h = cow_groups(hold)

                for group in h:

                    if group not in cow_dict: 
                        cow_dict[group]=1
                    else:
                        cow_dict[group]+=1
            hold=[]
    
    return cow_dict

# Print network
def print_network(cow_dict, cut):
    new_dict = {}
    for (key, value) in cow_dict.items():
        if value > cut:
            new_dict[key] = value

    sort = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse= False))
    for (key, value) in sort.items():
        print('Cows: '+ str(key) + '\tNumber: ' + str(value))


### -------------------------------------------------------------------------------------------------------------
### Run code ----------------------------------------------------------------------------------------------------
### -------------------------------------------------------------------------------------------------------------

# (Farm data, time cut off, value cut off)

Waitroom_Traffic('Waitroom_Traffic_A6.csv', 1, 150)
#Waitroom_Traffic('Waitroom_Traffic_F4.csv', 1, 150)

Robot_Milkings('RobotMilkings_A6.csv', 5, 40)
#Robot_Milkings('RobotMilkings_F4.csv', 5, 40)