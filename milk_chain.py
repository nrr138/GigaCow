import pandas as pd
import numpy as np
import datetime
import itertools
import math
import matplotlib.pyplot as plt

#function to calculate time in total minutes.
def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2015,1,1)
    return int(t.total_seconds()//60)

#function to calculate Milk of cow ahead.
def milk_chain(farm,type,farmname,Bool):
    data = pd.read_csv(farm)
    if Bool:
        data = data[(data ["EquipmentName"]==type)]
    data['MilkingStartDateTime']=data['MilkingStartDateTime'].map(time_calc)
    data = data.sort_values(by=['MilkingStartDateTime'])
    data = data.reset_index(drop=True)
    star_time=data['MilkingStartDateTime']
    kor=data["Gigacow_Cow_Id"]
    milk=data["TotalYield"]


   

    print('-----Time Data-----')
    print(star_time)
    print('------Cow Data-----')
    print(kor)
    print('\n------------Data info---------------')
    print('Number of cows in farm:', len(np.unique(np.array(kor))))
    print('------------------------------------\n')
    time=30
    cow_dict={}
    cow_dict2={}
    cow_dict3={}
    cow_dict4={}
    #Calculates the total milk and the milk ahead. 
    for i in range(len(kor)):
        #calculates milk per session.
        k=milk[i].item()
        h=int(kor[i])

        if not math.isnan(k):

            if h not in cow_dict3:
                cow_dict4[h]=1
                cow_dict3[h]=k
            else:
                cow_dict4[h]+=1
                cow_dict3[h]+=k
    #Calculates Milk for cow ahead.
    for i in range(len(kor)-1): 

        if abs((star_time[i]-star_time[i+1])) <= time: 

            if kor[i]!=kor[i+1]:

                h=kor[i+1]  
                k=milk[i]

                if not math.isnan(k):

                    if h not in cow_dict: 

                        cow_dict[h]=1
                        cow_dict2[h]=k
        
                    else:

                        cow_dict[h]+=1
                        cow_dict2[h]+=k
                
                
                
                

                





    #Filters out all the values that are over 50. 
    new_dict = {}
    for (key, value) in cow_dict.items():

        if value >= 50:
            new_dict[key] = [cow_dict2[key]/value, value , cow_dict3[key]/cow_dict4[key], cow_dict4[key]]

    #Printing the data
    printx = []
    printy = []
    sort = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse= False))
    for (key, value) in sort.items():
        print('Cow: '+ f'{key} \t' + 'milk produced: ' + f'{str(round(value[2],2))} \t\t' + 'data points: ' +  f'{str(value[3])} \t' + 'milk produced for cow ahead: ' + f'{str(round(value[0],2))} \t'+ 'data points: ' +  str(value[1]))
        
        printy.append(value[0])
        printx.append(value[2])

    #Using a polyfit function to fit a line to the histogram
    a=np.polyfit(printx,printy,1, rcond=None, full=False, w=None, cov=False)
    print(f'polyfit k value = {a[0]} m value = {a[1]}' )
    def func(x,a,b):
        hold=[]
        for i in x:
            hold.append(a*i+b)
        return hold

    #Plots the data. 
    plt.plot(printx,func(printx,a[0],a[1]))
    plt.ylim([10,14])
    plt.bar(printx,printy, color = 'g', width = 0.3)

    if Bool:
        plt.title("Average milk produced per session farm " + farmname + " for robot " + type)
    else:
        plt.title("Average milk produced per session farm " + farmname)
    plt.xlabel('Milk produced')
    plt.ylabel('Milk produced for cow ahead')
    plt.show()



#milk_chain(Farm data,Milkin robot, farm, If True look at spesifit milking robot if False look at the total dataset)
milk_chain('RobotMilkings_A6.csv','VMS2', 'f454e660',True)

