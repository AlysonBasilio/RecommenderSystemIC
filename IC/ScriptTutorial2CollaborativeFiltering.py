import pandas as pd
import math

#column headers for the dataset
data_cols = ['user id','movie id','rating','timestamp']
item_cols = ['movie id','movie title','release date','video release date','IMDb URL','unknown','Action','Adventure','Animation','Childrens','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance ','Sci-Fi','Thriller','War' ,'Western']
user_cols = ['user id','age','gender','occupation','zip code']

#importing the data files onto dataframes
users = pd.read_csv('ml-100k/u.user', sep='|', names=user_cols, encoding='latin-1')
item = pd.read_csv('ml-100k/u.item', sep='|', names=item_cols, encoding='latin-1')
data = pd.read_csv('ml-100k/u.data', sep='\t', names=data_cols, encoding='latin-1')

#Separando dataset para treino e para teste.
utrain = (data.sort_values('user id'))[:99832]
# print(utrain.tail())
utest = (data.sort_values('user id'))[99833:]
# print(utest)

#Transformando dataset em matriz para facilitar manipulação
utrain = utrain.as_matrix(columns = ['user id', 'movie id', 'rating'])
# print(utrain)
utest = utest.as_matrix(columns = ['user id', 'movie id', 'rating'])
# print(utest)

#Para cada usuário, é iniciado um vetor de suas classificações.
users_list = []
for i in range(1,943):
    list = []
    for j in range(0,len(utrain)):
        if utrain[j][0] == i:
            list.append(utrain[j])
        else:
            break
    utrain = utrain[j:]
    users_list.append(list)

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

#Calcula-se então os Eucledians Score de todos os usuários em relação ao usuário de teste.
score_list = []
for i in range(0,942):
    score_list.append([i+1,EucledianScore(users_list[i], utest)])

#Aqui descobre-se qual usuário é mais similar ao usuário de teste.
score = pd.DataFrame(score_list, columns = ['user id','Eucledian Score'])
score = score.sort_values(by = 'Eucledian Score')
print(score)
score_matrix = score.as_matrix()

#Aqui pega o usuário mais similar e o usuário de teste, compara para ver quais filmes eles têm em
#comum. Descarta-se então esses filmes e recomenda-se apenas os filmes que o usuário similar
#viu e que o usuário de teste não viu.
user= int(score_matrix[0][0])
common_list = []
full_list = []
for i in utest:
    for j in users_list[user-1]:
        if(int(i[1])== int(j[1])):
            common_list.append(int(j[1]))
        full_list.append(j[1])

common_list = set(common_list)
full_list = set(full_list)
recommendation = full_list.difference(common_list)

#Para finalizar, organiza-se a saída do programa para mostrar os filmes que foram recomendados.
item_list = (((pd.merge(item,data).sort_values(by =
                'movie id')).groupby('movie title')))['movie id', 'movie title', 'rating']
item_list = item_list.mean()
item_list['movie title'] = item_list.index
item_list = item_list.as_matrix()

recommendation_list = []
for i in recommendation:
    recommendation_list.append(item_list[i - 1])

recommendation = (pd.DataFrame(recommendation_list, columns=['movie id', 'mean rating', 'movie title'])).sort_values(
    by='mean rating', ascending=False)
print(recommendation[['mean rating', 'movie title']])
