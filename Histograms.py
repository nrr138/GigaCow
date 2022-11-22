import pandas as pd
import datetime
import matplotlib.pyplot as plt
def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2020,1,1)
    return int(t.days)

###                                      Traffic                                      ###
### --------------------------------------------------------------------------------- ###

traffic = pd.read_csv('Traffic.csv')
td = traffic[['TrafficEventDateTime','FarmName_Pseudo','TrafficDeviceName']]

t1 = td[(td ['FarmName_Pseudo']=='a624fb9a')] # Sorteringsgrind 2 Trevägsgrind
t2 = td[(td ['FarmName_Pseudo']=='f454e660')] # Ingångsgrind

t1time=t1['TrafficEventDateTime'].map(time_calc)
t2time=t2['TrafficEventDateTime'].map(time_calc)


###                                    RobotMilking                                   ###
### --------------------------------------------------------------------------------- ###
robot = pd.read_csv('RobotMilkings.csv', low_memory=False)
rd = robot[['MilkingStartDateTime','FarmName_Pseudo']]

# Dela upp respektive gård
r1 = rd[(rd ['FarmName_Pseudo']=='a624fb9a')]
r2 = rd[(rd ['FarmName_Pseudo']=='f454e660')]

r1time=r1['MilkingStartDateTime'].map(time_calc)
r2time=r2['MilkingStartDateTime'].map(time_calc)

### --------------------------------------------------------------------------------- ###

t1dict = {}
t2dict = {}
r1dict = {}
r2dict = {}

for i in t1time:
    if i not in t1dict:
        t1dict[i] = 1
    else: 
        t1dict[i] += 1
        
t2dict = {}
for i in t2time:
    if i not in t2dict:
        t2dict[i] = 1
    else: 
        t2dict[i] += 1    
        
r1dict = {}
for i in r1time:
    if i not in r1dict:
        r1dict[i] = 1
    else: 
        r1dict[i] += 1
        
r2dict = {}
for i in r2time:
    if i not in r2dict:
        r2dict[i] = 1
    else: 
        r2dict[i] += 1

  
# Traffic a624fb9a
plt.ylabel('Events')
plt.xlabel('Days')
plt.title('Traffic, Farm: a624fb9a')
plt.bar(list(t1dict.keys()), t1dict.values(), color='g')
plt.show()
  
# Traffic f454e660
plt.ylabel('Events')
plt.xlabel('Days')
plt.title('Traffic, Farm: f454e660')
plt.bar(list(t2dict.keys()), t2dict.values(), color='g')
plt.show()
  
# RobotMilking a624fb9a
plt.ylabel('Events')
plt.xlabel('Days')
plt.title('Milking Robot, Farm: a624fb9a')
plt.bar(list(r1dict.keys()), r1dict.values(), color='g')
plt.show()
  
# RobotMilking f454e660
plt.ylabel('Events')
plt.xlabel('Days')
plt.title('Milking Robot, Farm: f454e660')
plt.bar(list(r2dict.keys()), r2dict.values(), color='g')
plt.show()