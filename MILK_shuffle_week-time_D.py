import pandas as pd
import numpy as np
import datetime
import random


# Change date to minutes
def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2020,1,1)
    t = int(t.total_seconds()//60)
    t = random.randint(t-180, t+180) 
    return t

### -------------------------------------------------------------------------------------------------------------
### Import Waitroom or Robot Milking data -----------------------------------------------------------------------
### -------------------------------------------------------------------------------------------------------------

data = pd.read_csv('RobotMilkings_A6.csv')
data['MilkingStartDateTime']=data['MilkingStartDateTime'].map(time_calc)

data = data.sort_values(by=['MilkingStartDateTime'])
data = data.reset_index(drop=True)

week = 1
d = data.to_numpy()
data_shuffle = np.array([])
hold = np.array([])

def shuffle(lst):
    lstuniq=list(dict.fromkeys(lst))

    for i in range(len(lst)):
        lst[i] = random.choice(lstuniq)
    return np.array(lst)

for i in range(len(d)):
    if abs(d[i,2]-d[0,2]) > 10080*week:
        print(week)
        if hold.size != 0:
            if hold.ndim != 1:
                hold[:,0] = shuffle(list(hold[:,0]))
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
        hold[:,0] = shuffle(list(hold[:,0]))
    if data_shuffle.size == 0:
        data_shuffle = hold
    else:
        data_shuffle = np.vstack([data_shuffle, hold])


random = pd.DataFrame(data_shuffle, columns= ['Gigacow_Cow_Id','SE_Number','MilkingStartDateTime','FarmName_Pseudo'])
random.to_csv('RobotMilkings_A6_random.csv', index=False)