import pandas as pd
from scipy import stats
from random import *

#column headers for the dataset
data_cols = ['user id','movie id','rating','timestamp']
item_cols = ['movie id','movie title','release date','video release date','IMDb URL','unknown','Action','Adventure','Animation','Childrens','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance ','Sci-Fi','Thriller','War' ,'Western']
user_cols = ['user id','age','gender','occupation','zip code']

#importing the data files onto dataframes
users = pd.read_csv('ml-100k/u.user', sep='|', names=user_cols, encoding='latin-1')
item = pd.read_csv('ml-100k/u.item', sep='|', names=item_cols, encoding='latin-1')
utrain = pd.read_csv('ml-100k/u1.base', sep='\t', names=data_cols, encoding='latin-1')
utest = pd.read_csv('ml-100k/u1.test', sep='\t', names=data_cols, encoding='latin-1')

#Transformando dataset em matriz para facilitar manipulação
utrain = utrain.as_matrix(columns = ['user id', 'movie id', 'rating'])
# print(utrain)
utest = utest.as_matrix(columns = ['user id', 'movie id', 'rating'])
# print(utest)

#Calcular quantidade de usuários utilizados para treinamento.
usersN = 0
for row in utrain:
    if usersN!=row[0]:
        usersN = usersN+1
print("Quantidade de usuarios para treinamento: "+str(usersN))

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
print("Tamanho do vetor de classificação de filmes: "+str(len(users_train_list)))

#A função PearsonCoef calcula a similaridade entre dois usuários
#Quanto mais em comum, mais próximo de 1 o valor do coeficiente
#Quanto menos em comum, mais próximo de -1 o valor do coeficiente
#Se os usuários tiverem menos de 4 filmes em comum, o coeficiente será -1.
def PearsonCoef(train_user, test_user):
    v1 = []
    v2 = []
    count = 0
    for i in test_user:
        for j in train_user:
            if(int(i[1]) == int(j[1])):
                v1.append(i[2])
                v2.append(j[2])
                count = count + 1
    if(count<4):
        sum = -1
    else:
        sum = stats.pearsonr(v1,v2)[0]
    #print("Coef. de Pearson = "+str(sum))
    return(sum)

#Função que gera um vetor de tamanho numUsers com os valores de usuários.
def RandomVector(numUsers, totalUsers):
    vector = []
    for i in range(0, numUsers):
        vector.append(randint(0,totalUsers-1))
    return vector

#Calcula-se então os coeficientes de Pearson de todos os usuários em relação a
#N usuários aleatórios da base de dados.
#Escolhe todos usuários dentre os N que têm o coeficiente de Pearson maior que
#delta
N=5
delta=0.7
similar_users_list = []
for i in range(0,usersN):
    list = []
    v = RandomVector(N,usersN)
    for j in v:
        # print(j)
        if i!=j:
            #print("i = "+str(i)+"| j = "+str(j))
            e = PearsonCoef(users_train_list[i], users_train_list[j])
            if e>delta:
                list.append([i+1, j+1, e, users_train_list[j]])
    similar_users_list.append(list)
print("Tamanho da lista de coeficientes de pearson: " + str(len(similar_users_list)))

#Calcular quantidade de usuários utilizados para teste.
usersNt = 0
for row in utest:
    if usersNt!=row[0]:
        usersNt = usersNt+1
print("Quantidade de usuários de teste: "+str(usersNt))

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
    users_test_list.append([i, list])
print("Tamanho do vetor de classificações de cada usuário: "+str(len(users_test_list)))

# print(users_test_list)
#Aqui pega os usuários mais similares de acordo com o delta escolhido anteriormente
#e o usuário de teste, a partir disso vamos tentar prever o rating de cada filme que o
#usuário de teste assistiu fazendo uma média ponderada das notas dadas pelos
#usuários similares para aquele filme.
#Se a nota prevista estiver dentro de um intervalo de +/- op da nota que foi dada pelo
#usuário de teste, vamos marcar como uma recomendação correta. Se estiver fora do intervalo,
#vamos marcar como uma recomendação incorreta.
recommendation = []
op=0.5
rate_base = 3
acerto = 0
total = 0
for i in range(0,usersNt):
    userID = users_test_list[i][0]
    similar_users = similar_users_list[userID-1]
    #print(str(i)+" - Similar user: "+str(similar_users))
    if(len(similar_users)>0):
        for j in users_test_list[i][1]:#Para cada filme que o usuário i+1 vai assistir
            # print("j - "+str(j))
            numerador = 0
            denominador = 0
            for k in similar_users:#Para cada usuário similar ao usuário i+1
                for l in k[3]:#Verificar se o usuário similar também assistiu o filme j
                    if(int(j[1])== int(l[1])):
                        numerador = numerador + k[2]*l[2]#k[2] = coeficiente, l[2] rating
                        denominador = denominador + k[2]
                        break
            if(denominador!=0):
                predicted_rating = numerador/denominador
                if(predicted_rating>rate_base):
                    # result = j[2]-predicted_rating
                    # if(result>(-1*op) and result<op):
                    acerto = acerto+1
                total = total + 1
print("Percentual de acerto: "+str(acerto*100/total)+"%")