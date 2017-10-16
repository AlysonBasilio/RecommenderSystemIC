import pandas as pd

#column headers for the dataset
ratings_cols = ['user id','movie id','rating','timestamp']
movies_cols = ['movie id','movie title','genres']
user_cols = ['user id','gender','age','occupation','zip code']

#importing the data files onto dataframes
users = pd.read_csv('ml-1m/users.dat', sep='::',
names=user_cols, encoding='latin-1', engine='python')
# print(users.head())

movies = pd.read_csv('ml-1m/movies.dat', sep='::',
names=movies_cols, encoding='latin-1', engine='python')
# print(movies.head())

ratings = pd.read_csv('ml-1m/ratings.dat', sep='::',
names=ratings_cols, encoding='latin-1', engine='python')
# print(ratings.head())

#Create one data frame from the three
dataset1 = pd.merge(pd.merge(movies[['movie id', 'genres']], ratings[['user id','movie id','rating']]),
                    users[['user id','gender','age','occupation']])
print("Head of Dataset1")
print(dataset1.head())

#Create one data frame of how many times a movie was rated
ratings_total1 = dataset1.groupby('movie id').size()
print("Head of Total Number of Ratings per Each Movie")
print(ratings_total1.head())

#Create one data frame with the mean rate for each movie
ratings_mean1 = (dataset1.groupby('movie id'))['movie id','rating'].mean()
print("Mean Rate")
print(ratings_mean1.head())

class Node():
    def __init__(self, atributo):
        self.atributo = atributo
        self.filhos = {}

    def incluirFilhos(self,valor,node):
        self.filhos[valor] =node

def escolherAtributo(atributos, exemplos):
    
    return None

def getDecisionTree(exemplos, atributos, padrao):
    tree = None
    if len(exemplos)==0:
        return padrao
    else:
        m = int(exemplos.iloc[0,3])
        b = True
        for i in exemplos.iloc[:,3]:
            if m != int(i):
                b = False
                break
        if b:
            return m
        else:
            if len(atributos)==0:
                m = (exemplos.groupby('rating'))['rating'].size()
                m = m.sort_values(ascending=False)
                return m.index[0]
            else:
                melhor = escolherAtributo(atributos,exemplos)
                tree = Node(melhor)
                m = (exemplos.groupby('rating'))['rating'].size()
                m = m.sort_values(ascending=False)
                m = m.index[0]
                print('m = ',m)
                for v in exemplos[melhor]:
                    e = exemplos[exemplos[melhor]==v]
                    sub_arvore = getDecisionTree(e,atributos-melhor,m)
                    tree.incluirFilhos(v,sub_arvore)
    return tree

dataset1.sample(frac=1).reset_index(drop=True)
dataset_train = dataset1[:int(len(dataset1)*2/3)]
dataset_test = dataset1[int(len(dataset1)*2/3):]

print(getDecisionTree(dataset_train,['genres','age','gender','occupation'],1))

# #modify the dataframes so that we can merge the two
# ratings_total1 = pd.DataFrame({'movie title':ratings_total1.index,
# 'total ratings': ratings_total1.values})
# # print(ratings_total1.head())
# ratings_mean1['movie title'] = ratings_mean1.index
# # print(ratings_mean1.head())
#
# #final1 has rating, movie title and total ratings.
# final = pd.merge(ratings_mean1, ratings_total1).sort_values(by = 'total ratings',
# ascending= False)
# print("Mean rate | Movie Title | Total ratings")
# print(final.head())
#
# # print(final1.describe())
#
# #Organize by mean rate the 300 more rated movies
# final1 = final[:300].sort_values(by = 'rating', ascending = False)
# print(final1.head())
#
# #Now we want to test the Recommender System
# #Let's recommend only movies with rate above 3.5
# acertos=0
# total = testdata1.size
# for linha in testdata1.iterrows():
#     r = 0
#     movieID = linha[1][1]
#     for linha1 in item.iterrows():
#         if(movieID == linha1[1][0]):
#             movieName = linha1[1][1]
#             break
#     for i in final1.index:
#         if final1['movie title'][i] == movieName:
#             r = final1['rating'][i]
#             break
#     if r>=3.5:
#         acertos = acertos+1
# print("Percentual de Acerto: "+(acertos/total)*100+"%")