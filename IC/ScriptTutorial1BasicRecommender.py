import pandas as pd

#column headers for the dataset
data_cols = ['user id','movie id','rating','timestamp']
item_cols = ['movie id','movie title','release date',
'video release date','IMDb URL','unknown','Action',
'Adventure','Animation','Childrens','Comedy','Crime',
'Documentary','Drama','Fantasy','Film-Noir','Horror',
'Musical','Mystery','Romance ','Sci-Fi','Thriller',
'War' ,'Western']
user_cols = ['user id','age','gender','occupation',
'zip code']

#importing the data files onto dataframes
users = pd.read_csv('ml-100k/u.user', sep='|',
names=user_cols, encoding='latin-1')

item = pd.read_csv('ml-100k/u.item', sep='|',
names=item_cols, encoding='latin-1')

data1 = pd.read_csv('ml-100k/u1.base', sep='\t',
names=data_cols, encoding='latin-1')
testdata1 = pd.read_csv('ml-100k/u1.test', sep='\t',
names=data_cols, encoding='latin-1')

#Create one data frame from the three
dataset1 = pd.merge(pd.merge(item, data1),users)
print("Head of Dataset1")
print(dataset1.head())

#Create one data frame of how many times a movie was rated
ratings_total1 = dataset1.groupby('movie title').size()
print("Head of Total Number of Ratings per Each Movie")
print(ratings_total1.head())

#Create one data frame with the mean rate for each movie
ratings_mean1 = (dataset1.groupby('movie title'))['movie title','rating'].mean()
print("Mean Rate")
print(ratings_mean1.head())

#modify the dataframes so that we can merge the two
ratings_total1 = pd.DataFrame({'movie title':ratings_total1.index,
'total ratings': ratings_total1.values})
# print(ratings_total1.head())
ratings_mean1['movie title'] = ratings_mean1.index
# print(ratings_mean1.head())

#final1 has rating, movie title and total ratings.
final = pd.merge(ratings_mean1, ratings_total1).sort_values(by = 'total ratings',
ascending= False)
print("Mean rate | Movie Title | Total ratings")
print(final.head())

# print(final1.describe())

#Organize by mean rate the 300 more rated movies
final1 = final[:300].sort_values(by = 'rating', ascending = False)
print(final1.head())

#Now we want to test the Recommender System
#Let's recommend only movies with rate above 3.5
acertos=0
total = testdata1.size
for linha in testdata1.iterrows():
    r = 0
    movieID = linha[1][1]
    for linha1 in item.iterrows():
        if(movieID == linha1[1][0]):
            movieName = linha1[1][1]
            break
    for i in final1.index:
        if final1['movie title'][i] == movieName:
            r = final1['rating'][i]
            break
    if r>=3.5:
        acertos = acertos+1
print("Percentual de Acerto: "+(acertos/total)*100+"%")