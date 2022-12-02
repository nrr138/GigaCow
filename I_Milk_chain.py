import pandas as pd
import numpy as np
import datetime
import itertools
import math
import matplotlib.pyplot as plt

def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2022,1,1)
    return int(t.total_seconds()//60)

#data = pd.read_csv('RobotMilkings_A6_traffic.csv')
data = pd.read_csv('RobotMilkings_A6.csv')
#data = pd.read_csv('test.csv')
data['MilkingStartDateTime']=data['MilkingStartDateTime'].map(time_calc)
data = data.sort_values(by=['MilkingStartDateTime'])
data = data.reset_index(drop=True)

star_time=data['MilkingStartDateTime']
kor=data["Gigacow_Cow_Id"]
milk=data["TotalYield"]


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
time=5
cow_dict={}
cow_dict2={}
cow_dict3={}
cow_dict4={}

def cow_groups(lst):
    combs = []
    for r in range(len(lst)+1):
        for comb in itertools.combinations(set(lst), r):
            if len(comb) == 2:
                combs.append(tuple(sorted(comb)))
    return combs

for i in range(len(kor)-1):

    hold.append(int(kor[i]))
    k=milk[i].item()
    h=int(kor[i])

    if not math.isnan(k):
        if h not in cow_dict3:
            cow_dict4[h]=1
            cow_dict3[h]=k
        else:
            cow_dict4[h]+=1
            cow_dict3[h]+=k
    
    
    if not abs((star_time[i]-star_time[i+1])) <= time or len(hold) == 2:
        
        if len(hold) > 1:
            
            h=hold[1]
        
             
            k=milk[i-1].item()
            if not math.isnan(k):
                if h not in cow_dict: 
                    cow_dict[h]=1
                    cow_dict2[h]=k
      
                else:
                    cow_dict[h]+=1
                    cow_dict2[h]+=k
            
            h=hold[0]
            
             

            

                
                

        hold=[]


new_dict = {}
for (key, value) in cow_dict.items():
    if key in cow_dict4:
        if value >50:
            new_dict[key] = [cow_dict2[key]/value, value , cow_dict3[key]/cow_dict4[key], cow_dict4[key]]

printx = []
printy = []
sorted = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse= False))
for (key, value) in sorted.items():
    print('Cow: '+ f'{key} \t' + 'milk produced: ' + str(round(value[2],2)) + '\tdata points: ' +  f'{str(value[3])} \t' + 'milk produced for cow ahead: ' + f'{str(round(value[0],2))} \t'+ 'data points: ' +  str(value[1]))
    
    printx.append(value[0])
    printy.append(value[2])

plt.bar(printx,printy, color = 'g', width = 0.05)
plt.show()



































































































































































