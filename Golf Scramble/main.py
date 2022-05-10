import csv
import math
from itertools import combinations
import time
import os


print("---------------DAGS ATT SKAPA LAG ----------------------------")
start_time = time.time()
file = open('GolfcalcTEST.csv')
size = 3 # Ideal number of players per team
directory_name = 'Sheguara Golf '+time.strftime("%Y")
os.mkdir(directory_name)


contendersRead = []
PSIList = []
totPSI = 0

def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]


# Skapat för att konvertera CSV filen till användbar data
#

csvreader = csv.reader(file)

player = []
for row in csvreader:

        stringRow = str(row).replace(";",",")
        stringRowNoComma = stringRow
        if stringRow[-6:-2] == ",,,,":
                stringRowNoComma = stringRow.replace(',,,,','')

        stringRow = stringRowNoComma.replace(', ',".")
        arrayRow = stringRow.replace("'","")[1:-1].split(',')

        try:
                floatArray = list(map(float,arrayRow[1:]))
                floatArray.insert(0, arrayRow[0])
                player.append(floatArray)

        except ValueError:
                continue

####### Avgöra hur många grupper samt personer per grupp

antalGrupper = math.floor(int(len(player)) / size)
gruppLista = [size] * antalGrupper
for i in range(len(player)-int(size*antalGrupper)):                           # Justerar antal personer i grupperna så att det stämmer med spelarantal
        gruppLista[i] = gruppLista[i] + 1

# PSI kalkyl, aka Player Scramble Index kalkyl
for i in range(len(player)): #Används ej vet inte hur man balancerar faktorer
        distance = player[i][1]
        precision = player[i][2]
        totTee  = (distance + precision )/ 2
        irons = player[i][3]
        creativity = player[i][4]
        accuracy = player[i][5]
        totInspel = (creativity + accuracy) / 2
        putt = player[i][6]
        knowledge = player[i][7]
        hcp = player[i][8]
        player_score = totTee + irons + totInspel + putt + knowledge
        PSI = round((1.1-hcp/54)*player_score,4)   # round(sum(player[i][1:-1]) * (1.1 - hcp / 54), 2)            #Räknar ut PSI isch
        player[i].insert(len(player[i]), PSI)                         #Lägger till PSI med spelaren
        PSIList.append(PSI)
        totPSI += PSI
# Skapa lagen brute force algo --------------------------- RÖR EJ ---------------------------------

averagePSI = totPSI / antalGrupper  #Tar PSI / grupper. Sedan kollar den hur många tre grupper och vad snittet ish kommer höjas med
playerDic = {}
allowedDif = averagePSI / 5
teams = [[0 for x in range(4)] for y in range(antalGrupper)]
findTeams = True
counter = 0
contenders = []
sumContenders = []
Val = 1


for i in range(len(player)):
        playerDic[player[i][0]] = player[i][9]

for i in range(antalGrupper):
        if gruppLista[i] == 3:
                teams[i].pop(2)


for iteration in range(antalGrupper):
        for i in range(len(contenders) + Val):
                if iteration>0:

                        contenders = []
                        sumContenders = []

                        with open(directory_name + '/iteration'+str(iteration-1)+'.txt') as f:
                                for line in f:                                                                          #GÖR NÅGOT SMART HÄR.

                                        updatedPSIList = [playerD for playerD in PSIList if playerD not in eval(line)]
                                        counter += 1
                                        combi = combinations(updatedPSIList, gruppLista[iteration])
                                        if combi:
                                                for a in list(combi):
                                                        if sum(a) < averagePSI + allowedDif and sum(
                                                                a) > averagePSI - allowedDif:
                                                                if sum(a) not in sumContenders:
                                                                        contenders.append(eval(line)+a)
                                                                        sumContenders.append(sum(a))


                else:
                        updatedPSIList = PSIList

                        combi = combinations(updatedPSIList,gruppLista[iteration])
                        Val = 0
                        for a in list(combi):
                                if sum(a) < averagePSI + allowedDif and sum(a) > averagePSI - allowedDif:
                                        if sum(a) not in sumContenders:
                                                contenders.append(a)
                                                sumContenders.append(sum(a))


                #counter += 1
       # print(PSIList)
        #print(len(contenders))
        textfile = open(directory_name + "/iteration" + str(iteration) + ".txt", "w")
        for x in contenders:
                textfile.write(str(x) + "\n")
        textfile.close()


playerNames = []

try:
        for x in range(10):

                with open(directory_name + "/iteration" + str(x) + ".txt","r") as f:
                        saveVal = x

except IOError:
        pass


with open(directory_name + "/iteration" + str(saveVal) + ".txt") as f:
        for line in f:
                contendersRead.append(eval(line))
        lengthLag = len(open(directory_name + "/iteration" + str(saveVal) + ".txt").readlines())

for x in range(lengthLag):
        playerNames = []
        itercont = contendersRead[x]
        for i in range(len(itercont)):
                playerNames.append(get_keys_from_value(playerDic,itercont[i]))


        print(playerNames)
        co = 0
        for i in range(len(teams)):
                for j in range(len(teams[i])):
                        teams[i][j] = playerNames[co]
                        co +=1

        text = open(directory_name + "/Lagen"+str(x)+".txt", "w")
        for x in teams:
                text.write(str(x) + "\n")
        text.close()

print("Iterationer av gruppvarianter : " + str(counter))
print(playerDic)
print(teams)
print("--- %s seconds ---" % (time.time() - start_time))
