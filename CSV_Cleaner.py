import pandas as pd  
import matplotlib.pyplot as plt


### -------------------------------------------------------------------------------------------- ###
### CowIdentities ###
### -------------------------------------------------------------------------------------------- ###
cow = pd.read_csv("CowIdentities.csv")

d1 = cow[['Gigacow_Cow_Id','SE_Number', 'FarmName_Pseudo']]
g1 = d1[(d1 ['FarmName_Pseudo']=='a624fb9a')]

g1.to_csv('CowIdentities_clean.csv', index=False)


### -------------------------------------------------------------------------------------------- ###
### RobotMilkings ###
### -------------------------------------------------------------------------------------------- ###
robot = pd.read_csv('RobotMilkings.csv', low_memory=False)

# Rensa onödig data
d2 = robot[['Gigacow_Cow_Id','SE_Number','MilkingStartDateTime','FarmName_Pseudo']]
d2.drop(d2[d2['Gigacow_Cow_Id'] == -1].index, inplace = True)

# Dela upp respektive gård
g1 = d2[(d2 ['FarmName_Pseudo']=='a624fb9a')]
g2 = d2[(d2 ['FarmName_Pseudo']=='f454e660')]

g1.to_csv('RobotMilkings_A6.csv', index=False)
g2.to_csv('RobotMilkings_F4.csv', index=False)


### -------------------------------------------------------------------------------------------- ###
### Traffic ###
### -------------------------------------------------------------------------------------------- ###
traffic = pd.read_csv('Traffic.csv')

d3 = traffic[['TrafficEventDateTime','Gigacow_Cow_Id','TrafficDeviceName','FarmName_Pseudo']]
d3.drop(d3[d3['Gigacow_Cow_Id'] == -1].index, inplace = True)

# Dela upp respektive gård
g1 = d3[(d3 ['FarmName_Pseudo']=='a624fb9a')] # Sorteringsgrind 2 Trevägsgrind
g2 = d3[(d3 ['FarmName_Pseudo']=='f454e660')] # Ingångsgrind

# Sortera grind
g1 = g1[(g1 ['TrafficDeviceName']=='Sorteringsgrind 2 Trevägsgrind')]
g2 = g2[(g2 ['TrafficDeviceName']=='Ingångsgrind')]

g1.to_csv('Waitroom_Traffic_A6.csv', index=False)
g2.to_csv('Waitroom_Traffic_F4.csv', index=False)


### -------------------------------------------------------------------------------------------- ###
### Lactations ###
### -------------------------------------------------------------------------------------------- ###

Lactation = pd.read_csv('Lactations.csv', sep=';')
d4 = Lactation[['FarmName_Pseudo','Gigacow_Cow_Id','LactationInfoDate','LactationNumber']]

# Dela upp respektive gård
g1 = d4[(d4 ['FarmName_Pseudo']=='a624fb9a')] # Sorteringsgrind 2 Trevägsgrind
g2 = d4[(d4 ['FarmName_Pseudo']=='f454e660')] # Ingångsgrind

g1.to_csv('Lactations_A6.csv', index=False)
g2.to_csv('Lactations_F4.csv', index=False)


### -------------------------------------------------------------------------------------------- ###
### Insemination ###
### -------------------------------------------------------------------------------------------- ###

Insemination = pd.read_csv('Insemination.csv', sep=';')
d5 = Insemination[['FarmName_Pseudo','Gigacow_Cow_Id','InseminationDate']]

# Dela upp respektive gård
g1 = d5[(d5 ['FarmName_Pseudo']=='a624fb9a')] # Sorteringsgrind 2 Trevägsgrind
g2 = d5[(d5 ['FarmName_Pseudo']=='f454e660')] # Ingångsgrind

g1.to_csv('Insemination_A6.csv', index=False)
g2.to_csv('Insemination_F4.csv', index=False)