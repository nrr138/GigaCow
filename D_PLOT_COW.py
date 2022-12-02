import pandas as pd
import datetime
import matplotlib.pyplot as plt
def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2020,1,1)
    return int(t.days)//7

traffic = pd.read_csv('Traffic.csv')

data = traffic[['FarmName_Pseudo','Gigacow_Cow_Id','TrafficEventDateTime']]

g1 = data[(data ['FarmName_Pseudo']=='a624fb9a')] # Sorteringsgrind 2 Trevägsgrind
g2 = data[(data ['FarmName_Pseudo']=='f454e660')] # Ingångsgrind


cow =g1['Gigacow_Cow_Id']
time=g1['TrafficEventDateTime'].map(time_calc)

#data['TrafficEventDateTime']=data['TrafficEventDateTime']
#time = time.sort_values(by=['TrafficEventDateTime'])
#time = time.reset_index(drop=True)

dict = {}
for i in range(len(time)-1):
    #if data['FarmName_Pseudo'][i] == 'f454e660':
    if data['FarmName_Pseudo'][i] == 'a624fb9a':
        cowtime = (time[i], cow[i])
        print(i)
        if cowtime not in dict:
            dict[cowtime] = 1
        else: 
            dict[cowtime] += 1
    

time = {}
for (key, value) in dict.items():
    print(key)
    if key[0] not in time:
        time[key[0]] = 1
    else:
        time[key[0]] += 1

""" time_cowdiff = {}
k = -1
for (key, value) in sorted(time.items()):

    time_cowdiff[key] = value - k
    if k == -1:
        time_cowdiff[key] = 0
    k = value """

#data.to_csv('test')
#print(dict)
plt.figure()
plt.title('Number of cows, Farm: f454e660')
plt.ylabel('Cows')
plt.xlabel('Weeks')
plt.bar(list(time.keys()), time.values(), color='g')
plt.show()
""" plt.figure()
plt.title('Cow difference (from previous week )')
plt.ylabel('Cows')
plt.xlabel('Weeks')
plt.bar(list(time_cowdiff.keys()), time_cowdiff.values(), color='g')
plt.show() """