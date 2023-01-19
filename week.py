import pandas as pd
import numpy as np
import datetime
import itertools
import random
import matplotlib.pyplot as plt
def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2015,1,1)
    return int(t.total_seconds()//60)


#use the outher data set f4
""" data = pd.read_csv('RobotMilkings_F4_traffic.csv')
#data = pd.read_csv('RobotMilkings_F4_traffic.csv')

data['TrafficEventDateTime']=data['TrafficEventDateTime'].map(time_calc)
data = data.sort_values(by=['TrafficEventDateTime'])
data = data.reset_index(drop=True)
star_time=data['TrafficEventDateTime']
kor=data["Gigacow_Cow_Id"] """

#use the outher data set A6
data = pd.read_csv('RobotMilkings_A6.csv')
#data = pd.read_csv('RobotMilkings_F4.csv')

data['MilkingStartDateTime']=data['MilkingStartDateTime'].map(time_calc)
data = data.sort_values(by=['MilkingStartDateTime'])
data = data.reset_index(drop=True)
star_time=data['MilkingStartDateTime']
kor=data["Gigacow_Cow_Id"]

#prints relevent information
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

#used to save the right varibles
def save_plot(cow_dict,w):
    cut_off= 1
    new_dict = {}
    for (key, value) in cow_dict.items():
        if value >= cut_off:
            new_dict[key] = value


    sortedd = dict(sorted(new_dict.items(), key=lambda item: item[1], reverse= False))
    for (key, value) in sortedd.items():

        if value >= cut_off:
            print_csv.append([key[0],key[1], value, w])

#used to create the right groups
def cow_groups(lst):
    combs = []
    for r in range(len(lst)+1):
        for comb in itertools.combinations(set(lst), r):
            if len(comb) == 2:
                combs.append(tuple(sorted(comb)))
    return combs
week = 1

newcow=[[]]
newcow[0]=[]
cowinout=[]
hold2=[]
save=[]

#used so only the new cows are saved
def newcowfunc(l1,l2):
    weekcow=[[],[]]
    for i in l1:
        if i not in l2: 
            weekcow[0].append(i)
    for i in l2:
        if i not in l1: 
            weekcow[1].append(i)
    return weekcow

#For loop that gose through the whole data set and takes out all the unique cows. 
for i in range(len(kor)-1):
    if kor[i] not in hold2:
        hold2.append(kor[i]) 

    if abs(star_time[i]-star_time[0]) > 10080*week:
        save_plot(cow_dict, week)
        cow_dict={}
        newcow.append(hold2)
        save=hold2
        hold2=[]
        cowinout.append(newcowfunc(newcow[week-1],newcow[week]))
        week += 1



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

#used to normalize the data
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

#conver to dic
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

#creats the dictionary to plot the data
week_cor = {}
for i in range(print_csv[-1][3]):
    dw= to_dict(print_csv, i)
    cor = dictcor(dw[0], dw[1])
    week_cor[i] = cor

test1=[]
test2=[]

for i in cowinout:
    test1.append(-len(i[0]))
    test2.append(len(i[1]))


#Calculates the the amount of cows in the start and at the end
k=0
for i in save:
    if i in newcow[1]:
        k+=1
    
print(f'cows at end {len(save)}')
print(f'cows at start {len(newcow[1])}')
print (f'unique cows from the start to the end {k}')


#plots
plt.figure(1)
plt.title('Cow difference, Farm: f454e660')
plt.ylabel('Number of cows')
plt.xlabel('Weeks')

plt.bar(list(week_cor.keys())[1:],test1[1:] , color='r')
plt.bar(list(week_cor.keys())[1:],test2[1:], color='g')
plt.legend(["Cows leaving","New cows"])
plt.show()

