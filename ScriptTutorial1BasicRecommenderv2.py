import pandas as pd

#column headers for the dataset
data_cols = ['user id','movie id','rating','timestamp']
item_cols = ['movie id','movie title','release date',
'video release date','IMDb URL','unknown','Action',
'Adventure','Animation','Childrens','Comedy','Crime',
'Documentary','Drama','Fantasy','Film-Noir','Horror',
'Musical','Mystery','Romance ','Sci-Fi','Thriller',
'War' ,'Western']
user_cols = ['user id','age','gender','occupation','zip code']

#importing the data files onto dataframes
users = pd.read_csv('ml-100k/u.user', sep='|', names=user_cols, encoding='latin-1')
item = pd.read_csv('ml-100k/u.item', sep='|', names=item_cols, encoding='latin-1')
data1 = pd.read_csv('ml-100k/u1.base', sep='\t', names=data_cols, encoding='latin-1')
testdata1 = pd.read_csv('ml-100k/u1.test', sep='\t', names=data_cols, encoding='latin-1')

#Create one data frame from the three
dataset1 = pd.merge(pd.merge(item, data1),users)
print("Head of Dataset1")
print(dataset1.head())

#Transformando dataset em matriz para facilitar manipulação
data1 = data1.as_matrix(columns = ['user id', 'movie id', 'rating'])
# print(utrain)
testdata1 = testdata1.as_matrix(columns = ['user id', 'movie id', 'rating'])

#Create one data frame of how many times a movie was rated
ratings_total1 = dataset1.groupby('movie id').size()
print("Head of Total Number of Ratings per Each Movie")
print(ratings_total1.head())

#Create one data frame with the mean rate for each movie
ratings_mean1 = (dataset1.groupby('movie id'))['movie id','rating'].mean()
print("Mean Rate")
print(ratings_mean1.head())

#modify the dataframes so that we can merge the two
ratings_total1 = pd.DataFrame({'movie id':ratings_total1.index,
'total ratings': ratings_total1.values})
# print(ratings_total1['total ratings'])
ratings_mean1['movie id'] = ratings_mean1.index
print(ratings_mean1.head())

#final1 has rating, movie title and total ratings.
final = pd.merge(ratings_mean1, ratings_total1).sort_values(by = 'total ratings',
ascending= False)
print(final.head())

# print(final1.describe())

#Calcular quantidade de usuários utilizados para teste.
usersNt = 0
for row in testdata1:
    if usersNt!=row[0]:
        usersNt = usersNt+1
print("Quantidade de usuários de teste: "+str(usersNt))

#Para cada usuário, é iniciado um vetor de suas classificações.
users_test_list = []
for i in range(1,usersNt+1):
    list = []
    for j in range(0,len(testdata1)):
        if testdata1[j][0] == i:
            list.append(testdata1[j])
        else:
            break
    testdata1 = testdata1[j:]
    users_test_list.append(list)
print("Tamanho do vetor de classificações de cada usuário: "+str(len(users_test_list)))

#Organize by mean rate the 1 more rated movies
number_of_recommended_movies = 8
number_of_rated_movies = 50
final1 = final[:number_of_rated_movies].sort_values(by = 'rating', ascending = False)
final1 = final1[:number_of_recommended_movies]
print(final1.head())

#Now we want to test the Recommender System
acertos=0
total = usersNt
for user in users_test_list:
    for movie in user:
        movieID = movie[1]
        x = 0
        for i in final1.index:
            if final1['movie id'][i] == movieID:
                acertos = acertos+1
                x = 1
                break
        if x!=0:
            break
print("Percentual de Acerto: "+str((acertos/total)*100)+"%")