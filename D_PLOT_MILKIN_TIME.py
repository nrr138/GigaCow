import pandas as pd
import datetime
import matplotlib.pyplot as plt
def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2020,1,1)
    return int(t.days)

robot = pd.read_csv('RobotMilkings.csv', low_memory=False)
d2 = robot[['MilkingStartDateTime','FarmName_Pseudo']]

# Dela upp respektive gård
g1 = d2[(d2 ['FarmName_Pseudo']=='a624fb9a')]
g2 = d2[(d2 ['FarmName_Pseudo']=='f454e660')]

time=g2['MilkingStartDateTime'].map(time_calc)
#data['TrafficEventDateTime']=data['TrafficEventDateTime']
#time = time.sort_values(by=['TrafficEventDateTime'])
#time = time.reset_index(drop=True)

dict = {}
for i in time:
    if i not in dict:
        dict[i] = 1
    else: 
        dict[i] += 1

#data.to_csv('test')
#print(dict)

plt.ylabel('Events')
plt.xlabel('Days')
plt.bar(list(dict.keys()), dict.values(), color='g')
plt.show()