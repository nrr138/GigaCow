import pandas as pd
import numpy as np
import datetime
import random

# Change date to minutes, with a +-3h randomizer
def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2020,1,1)
    t = int(t.total_seconds()//60)
    t = random.randint(t-180, t+180) 
    return t

### Import Waitroom and Robot Milking data 
def Waitroom_Traffic(farm_name):
    data = pd.read_csv(farm_name+'.csv')
    data['TrafficEventDateTime']=data['TrafficEventDateTime'].map(time_calc)

    data = data.sort_values(by=['TrafficEventDateTime'])
    data = data.reset_index(drop=True)

    col_cow = data.columns.get_loc('Gigacow_Cow_Id')
    col_time = data.columns.get_loc('TrafficEventDateTime')
    randomizer(data, col_cow, col_time, True,farm_name)

def Robot_Milkings(farm_name):
    data = pd.read_csv(farm_name+'.csv')
    data['MilkingStartDateTime']=data['MilkingStartDateTime'].map(time_calc)

    data = data.sort_values(by=['MilkingStartDateTime'])
    data = data.reset_index(drop=True)

    col_cow = data.columns.get_loc('Gigacow_Cow_Id')
    col_time = data.columns.get_loc('MilkingStartDateTime')
    randomizer(data, col_cow, col_time, False,farm_name)

# Randomize cows in a week
def shuffle(lst):
    lstuniq=list(dict.fromkeys(lst))

    for i in range(len(lst)):
        lst[i] = random.choice(lstuniq)
    return np.array(lst)

# Randomize cows and times in every week
def randomizer(data, col_cow, col_time, traffic, farm_name):
    week = 1
    d = data.to_numpy()
    data_shuffle = np.array([])
    hold = np.array([])

    for i in range(len(d)):
        if abs(d[i,col_time]-d[0,col_time]) > 10080*week:
            print(week)
            if hold.size != 0:
                if hold.ndim != 1:
                    hold[:,col_cow] = shuffle(list(hold[:,col_cow]))
                if data_shuffle.size == 0:
                    data_shuffle = hold
                else:
                    data_shuffle = np.vstack([data_shuffle, hold])
            hold = np.array([])
            week += 1
        if hold.size == 0:
            hold = d[i]
        else: 
            hold = np.vstack([hold, d[i]])

    if hold.size != 0:  
        if hold.ndim != 1:   
            hold[:,col_cow] = shuffle(list(hold[:,col_cow]))
        if data_shuffle.size == 0:
            data_shuffle = hold
        else:
            data_shuffle = np.vstack([data_shuffle, hold])

    if traffic:
        rand = pd.DataFrame(data_shuffle, columns= ['TrafficEventDateTime','Gigacow_Cow_Id','TrafficDeviceName','FarmName_Pseudo'])
    else:
        rand = pd.DataFrame(data_shuffle, columns= ['Gigacow_Cow_Id','SE_Number','MilkingStartDateTime','FarmName_Pseudo'])
    rand.to_csv(farm_name+'_random.csv', index=False)


# Randomize data from both farm (Waitroom traffic and Milk robot)
Waitroom_Traffic('Waitroom_Traffic_A6') # Runtime ~1min 
Waitroom_Traffic('Waitroom_Traffic_F4')  # Runtime ~14min 
Robot_Milkings('RobotMilkings_A6')
Robot_Milkings('RobotMilkings_F4')