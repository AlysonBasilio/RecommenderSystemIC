import pandas as pd
import math
from random import *

#column headers for the dataset
data_cols = ['user id','movie id','rating','timestamp']
item_cols = ['movie id','movie title','release date','video release date','IMDb URL','unknown','Action','Adventure','Animation','Childrens','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance ','Sci-Fi','Thriller','War' ,'Western']
user_cols = ['user id','age','gender','occupation','zip code']

#importing the data files onto dataframes
users = pd.read_csv('ml-100k/u.user', sep='|', names=user_cols, encoding='latin-1')
item = pd.read_csv('ml-100k/u.item', sep='|', names=item_cols, encoding='latin-1')
utrain = pd.read_csv('ml-100k/u4.base', sep='\t', names=data_cols, encoding='latin-1')
utest = pd.read_csv('ml-100k/u4.test', sep='\t', names=data_cols, encoding='latin-1')

#Transformando dataset em matriz para facilitar manipulação
utrain = utrain.as_matrix(columns = ['user id', 'movie id', 'rating'])
# print(utrain)
utest = utest.as_matrix(columns = ['user id', 'movie id', 'rating'])
# print(utest)

#Calcular quantidade de usuários utilizados para treinamento.
usersN = 0
for row in utrain:
    if usersN!=row[0]:
        usersN = row[0]
print(usersN)

#Para cada usuário, é iniciado um vetor de suas classificações.
users_train_list = []
for i in range(1,usersN+1):
    list = []
    for j in range(0,len(utrain)):
        if utrain[j][0] == i:
            list.append(utrain[j])
        else:
            break
    utrain = utrain[j:]
    users_train_list.append(list)
print(len(users_train_list))

#A função EucledianScore calcula a similaridade entre dois usuários
#Quanto mais em comum, mais próximo de 0 o valor de sum
#Se os usuários tiverem menos de 4 filmes em comum, sum será muito alto(1000000).
def EucledianScore(train_user, test_user):
    sum = 0
    count = 0
    for i in test_user:
        score = 0
        for j in train_user:
            if(int(i[1]) == int(j[1])):
                score= ((float(i[2])-float(j[2]))*(float(i[2])-float(j[2])))
                count= count + 1
            sum = sum + score
    if(count<4):
        sum = 1000000
    return(math.sqrt(sum))

def RandomVector(numUsers, totalUsers):
    vector = []
    for i in range(1, numUsers):
        vector.append(randint(0,totalUsers))
    return vector

#Calcula-se então os Eucledians Score de todos os usuários em relação a todos os usuários.
score_list = []
for i in range(0,usersN):
    list = []
    aux = 1001.0
    v = RandomVector(50,len(users_train_list)-1)
    for j in v:
        # print(j)
        if i!=j:
            e = EucledianScore(users_train_list[i], users_train_list[j])
            if e<aux:
                list = [i+1, j+1, e]
                aux = e
                if e==0.0:
                    break
    # print(list)
    score_list.append(list)
# print(score_list)

#Calcular quantidade de usuários utilizados para teste.
usersNt = 0
for row in utest:
    if usersNt!=row[0]:
        usersNt = row[0]
print(usersNt)

#Para cada usuário, é iniciado um vetor de suas classificações.
users_test_list = []
for i in range(1,usersNt+1):
    list = []
    for j in range(0,len(utest)):
        if utest[j][0] == i:
            list.append(utest[j])
        else:
            break
    utest = utest[j:]
    users_test_list.append(list)
print(len(users_test_list))

#Aqui pega o usuário mais similar e o usuário de teste, compara para ver quais filmes eles têm em
#comum. Descarta-se então esses filmes e recomenda-se apenas os filmes que o usuário similar
#viu e que o usuário de teste não viu.
recommendation = []
for i in range(0,usersNt):
    similar_user = score_list[i][1]
    print(str(i)+" - Similar user: "+str(similar_user))
    differ_list = []
    for j in users_train_list[similar_user-1]:
        abc = 0
        for k in users_train_list[i]:
            if(int(j[1])== int(k[1])):
                abc = 1
                break
        if(abc == 0):
            differ_list.append(j)
    recommendation.append(differ_list)
# print(recommendation)

#Vamos recomendar apenas o filme, dentre as recomendações, que tiver maior rating
final_recommender =[]
for i in recommendation:
    print(i)
    r = 0
    item = []
    for j in i:
        if(j[2]>r):
            r = j[2]
            item = j
    final_recommender.append(item)

#Para finalizar, organiza-se a saída do programa para mostrar o percentual de acerto
acerto = 0
total = 0
for i in range(0,usersNt):
    for j in users_test_list[i]:
        # print(k)
        if(int(j[1])== int(final_recommender[i][1])):
            acerto = acerto+1
    total = total+1
print("Percentual de acerto: "+str(acerto*100/total)+"%")