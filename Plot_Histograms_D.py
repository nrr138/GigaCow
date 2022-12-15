import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Change date to weeks
def time_calc(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10]), int(list[11:13]), int(list[14:16])) - datetime.datetime(2020,1,1)
    return int(t.days)//7

# Change date to weeks (for lactation)
def time_calc_lact(list):
    t = datetime.datetime(int(list[0:4]), int(list[5:7]),int(list[8:10])) - datetime.datetime(2020,1,1)
    return int(t.days)//7
### -------------------------------------------------------------------------------------------------------------
### Traffic events ----------------------------------------------------------------------------------------------
### -------------------------------------------------------------------------------------------------------------
def traffic_event(farm_name):
    traffic = pd.read_csv('Traffic.csv')

    data = traffic[['TrafficEventDateTime','FarmName_Pseudo','TrafficDeviceName']]
    g = data[(data ['FarmName_Pseudo']==farm_name)] 

    time=g['TrafficEventDateTime'].map(time_calc)

    dict = {}
    for i in time:
        if i not in dict:
            dict[i] = 1
        else: 
            dict[i] += 1

    plt.figure()
    plt.title('All traffic events per week. Farm: '+farm_name)
    plt.ylabel('Events')
    plt.xlabel('Weeks (after 2020-01-01)')
    plt.bar(list(dict.keys()), dict.values(), color='g')

### -------------------------------------------------------------------------------------------------------------
### Milk events -------------------------------------------------------------------------------------------------
### -------------------------------------------------------------------------------------------------------------
def milk_event(farm_name):
    robot = pd.read_csv('RobotMilkings.csv')

    data = robot[['MilkingStartDateTime','FarmName_Pseudo']]
    g = data[(data ['FarmName_Pseudo']==farm_name)]

    time=g['MilkingStartDateTime'].map(time_calc)

    dict = {}
    for i in time:
        if i not in dict:
            dict[i] = 1
        else: 
            dict[i] += 1

    plt.figure()
    plt.title('Milk Robot data per week. Farm: '+farm_name)
    plt.ylabel('Events')
    plt.xlabel('Weeks (after 2020-01-01)')
    plt.bar(list(dict.keys()), dict.values(), color='g')

### -------------------------------------------------------------------------------------------------------------
### Cows per week and difference --------------------------------------------------------------------------------
### -------------------------------------------------------------------------------------------------------------
def cow_count_week(farm_name):    
    traffic = pd.read_csv('RobotMilkings.csv')

    data = traffic[['FarmName_Pseudo','Gigacow_Cow_Id','MilkingStartDateTime']]

    cow =data['Gigacow_Cow_Id']
    time=data['MilkingStartDateTime'].map(time_calc)

    # Extract cows from specified farm per week
    dict = {}
    for i in range(len(time)-1):
        if data['FarmName_Pseudo'][i] == farm_name:
            cowtime = (time[i], cow[i])
            if cowtime not in dict:
                dict[cowtime] = 1

    time = {}
    for (key, value) in dict.items():
        print(key[0])
        if key[0] not in time:
            time[key[0]] = 1
        else:
            time[key[0]] += 1
    print(time)

    time_cowdiff = {}
    k = -1
    for (key, value) in sorted(time.items()):

        time_cowdiff[key] = value - k
        if k == -1:
            time_cowdiff[key] = 0
        k = value 
    plt.figure()
    plt.title('Number of cows, Farm: ' + farm_name)
    plt.ylabel('Cows')
    plt.xlabel('Weeks')
    plt.bar(list(time.keys()), time.values(), color='g')

    plt.figure()
    plt.title('Cow difference (from previous week), Farm: ' + farm_name)
    plt.ylabel('Cows')
    plt.xlabel('Weeks')
    plt.bar(list(time_cowdiff.keys()), time_cowdiff.values(), color='g')


### -------------------------------------------------------------------------------------------------------------
### Lactation_events --------------------------------------------------------------------------------------------
### -------------------------------------------------------------------------------------------------------------
def lactation_event(farm_name):
    robot = pd.read_csv('Lactations.csv', sep=';')

    data = robot[['LactationInfoDate','FarmName_Pseudo']]
    g = data[(data ['FarmName_Pseudo']==farm_name)]

    time=g['LactationInfoDate'].map(time_calc_lact)
    dict = {}
    for i in time:
        if i not in dict:
            dict[i] = 1
        else: 
            dict[i] += 1

    plt.figure()
    plt.title('Lactation data per week. Farm: '+farm_name)
    plt.ylabel('Data amount')
    plt.xlabel('Weeks (after 2020-01-01)')
    plt.bar(list(dict.keys()), dict.values(), color='g')

### -------------------------------------------------------------------------------------------------------------
### Plots -------------------------------------------------------------------------------------------------------
### -------------------------------------------------------------------------------------------------------------

# Traffic event histogram
traffic_event('a624fb9a')
traffic_event('f454e660')
plt.show()

# Milk event histogram
milk_event('a624fb9a')
milk_event('f454e660')
plt.show()

# Cows per week and difference histogram
cow_count_week('a624fb9a')
cow_count_week('f454e660')
plt.show()

# Lactation events
lactation_event('a624fb9a')
lactation_event('f454e660')
plt.show()