#custom script that i made because i was lazy to do all those stupid calculations manually :)
#instructions are clearly written out throughout the code, read them carefully and enter your values respectively

import numpy as np
from prettytable import PrettyTable

#defining constants given in lab record, change accordingly if required (all units are in SI)
mBrass = 0.93278
mAluminium = 0.284345
area = 0.0123
cpBrass = float(380)
cpAluminium = float(890)
ambientTemp = float(26 + 273)
height = 0.095
sigma = 5.67e-8
epsilonBrass = 0.03
epsilonAluminium = 0.02

#enter times here in seconds
brassTimes = np.array([0, 72, 140, 222, 330, 428, 530, 638, 768, 910, 1042, 1216, 1369, 1572, 1795, 2067, 2365, 2732, 3166, 3537], dtype=np.float64)
aluminiumTimes = np.array([0, 90, 161, 230, 290, 370, 445, 540, 627, 726, 836, 960, 1014, 1227, 1380, 1557, 1746, 1972, 2234, 2580, 2945], dtype=np.float64)

#enter temperatures in celsius
brassTemps = np.array([100, 97, 94, 91, 88, 85, 82, 79, 76, 73, 70, 67, 64, 61, 58, 55, 52, 49, 46, 43], dtype=np.float64)
aluminiumTemps = np.array([100, 97, 94, 91, 88, 85, 82, 79, 76, 73, 70, 67, 64, 61, 58, 55, 52, 49, 46, 43, 40], dtype=np.float64)

brassTemps += 273 #converting to kelvin
aluminiumTemps += 273

# print(len(brassTimes), " ", len(brassTemps))
# print(len(aluminiumTimes), " ", len(aluminiumTemps))

#dT/dt ratio calculation (assuming you did the experiment for every 3 degree drop in temp (if not change the 3 below))
tempTimeRatioBrass = np.full(len(brassTemps), 3, dtype=np.float64)
for i in range(len(brassTemps)-1):
    tempTimeRatioBrass[i+1] /= brassTimes[i+1] - brassTimes[i]

tempTimeRatioAluminium = np.full(len(aluminiumTemps), 3, dtype=np.float64)
for i in range(len(aluminiumTemps)-1):
    tempTimeRatioAluminium[i+1] /= aluminiumTimes[i+1] - aluminiumTimes[i]

#Q value calculation
heatBrass = tempTimeRatioBrass * mBrass * cpBrass
heatAluminium = tempTimeRatioAluminium * mAluminium * cpAluminium

#experimental coefficient
hExpBrass = heatBrass/(area*(brassTemps-ambientTemp))
hExpAluminium = heatAluminium/(area*(aluminiumTemps-ambientTemp))

#hc and hr coefficients for convection and radiation
hCbrass = 1.42 * np.power((brassTemps-ambientTemp)/height , 0.25)
hRbrass = sigma * epsilonBrass * (np.power(brassTemps, 4) - pow(ambientTemp, 4)) / (brassTemps - ambientTemp)

hCaluminium = 1.42 * np.power((aluminiumTemps-ambientTemp)/height , 0.25)
hRaluminium = sigma * epsilonAluminium * (np.power(aluminiumTemps, 4) - pow(ambientTemp, 4)) / (aluminiumTemps - ambientTemp)

#theoretical coefficients
hTheoryBrass = hCbrass + hRbrass
hTheoryAluminium = hCaluminium + hRaluminium

#average values for reporting result
avghExpBrass = np.mean(hExpBrass[1:])
avghTheoryBrass = np.mean(hTheoryBrass[1:])
avghExpAluminium = np.mean(hExpAluminium[1:])
avghTheoryAluminium = np.mean(hTheoryAluminium[1:])

#printing output
tableBrass = PrettyTable()

tableBrass.add_column("time (s)", brassTimes[1:])
tableBrass.add_column("Temperature (K)", brassTemps[1:])
tableBrass.add_column("dT/dt (K/s)", tempTimeRatioBrass[1:].round(3))
tableBrass.add_column("hexp (W/m2-K)", hExpBrass[1:].round(3))
tableBrass.add_column("hc (W/m2-K)", hCbrass[1:].round(3))
tableBrass.add_column("hr (W/m2-K)", hRbrass[1:].round(3))
tableBrass.add_column("htheory (W/m2-K)", hTheoryBrass[1:].round(3))


tableAluminium = PrettyTable()

tableAluminium.add_column("time (s)", aluminiumTimes[1:])
tableAluminium.add_column("Temperature (K)", aluminiumTemps[1:])
tableAluminium.add_column("dT/dt (K/s)", tempTimeRatioAluminium[1:].round(3))
tableAluminium.add_column("hexp (W/m2-K)", hExpAluminium[1:].round(3))
tableAluminium.add_column("hc (W/m2-K)", hCaluminium[1:].round(3))
tableAluminium.add_column("hr (W/m2-K)", hRaluminium[1:].round(3))
tableAluminium.add_column("htheory (W/m2-K)", hTheoryAluminium[1:].round(3))

print("BRASS DATA")
print(tableBrass)
print("ALUMINIUM DATA")
print(tableAluminium)

avgTable = PrettyTable()
avgTable.add_column("Values", ["hexp", "htheory"])
avgTable.add_column("Brass", [round(avghExpBrass, 3), round(avghTheoryBrass, 3)])
avgTable.add_column("Aluminium", [round(avghExpAluminium, 3), round(avghTheoryAluminium, 3)])

print("AVERAGE VALUES")
print(avgTable)