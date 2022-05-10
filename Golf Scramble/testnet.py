
Dic = {'Joakim': 67.16, 'Johan': 63.99, 'Karl': 49.27, 'Petrus': 56.25, 'Erika': 32.93, 'Adam': 12.15, 'Gustav': 18.82, 'Robert': 10.55, 'Nils': 2.65, 'Leisel': 3.01, 'Jesper': 48.67, 'Andreas': 46.17, 'Jakob': 44.5, 'Edwin': 43.67, 'Dennis': 31.17, 'Bertil': 4.5, 'Ceasar': 47.83}
list1 = (67.16, 49.27, 2.65, 3.01, 63.99, 32.93, 12.15, 18.82, 56.25, 46.17, 4.5, 10.55, 48.67, 47.83, 44.5, 43.67, 31.17)
new = []
teams = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]


def get_key(val,Dict):
    for key, value in Dict.items():
         if val == value:
             return key

#new = [k for k, v in Dic.items() if v in list]
for i in range(len(list1)):
    new.append(get_key(list1[i],Dic))

co = 0
for i in range(len(teams)):
    for j in range(len(teams[i])):
        teams[i][j] = new[co]
        co +=1
print(new)
print(teams)