import pandas as pd
from math import log
import time

# column headers for the dataset
ratings_cols = ['user id', 'movie id', 'rating', 'timestamp']
movies_cols = ['movie id', 'movie title', 'genres']
user_cols = ['user id', 'gender', 'age', 'occupation', 'zip code']

# importing the data files onto dataframes
users = pd.read_csv('ml-1m/users.dat', sep='::',
                    names=user_cols, encoding='latin-1', engine='python')
# print(users.head())

movies = pd.read_csv('ml-1m/movies.dat', sep='::',
                     names=movies_cols, encoding='latin-1', engine='python')
# print(movies.head())

ratings = pd.read_csv('ml-1m/ratings.dat', sep='::',
                      names=ratings_cols, encoding='latin-1', engine='python')
# print(ratings.head())

# Create one data frame from the three
dataset1 = pd.merge(pd.merge(movies[['movie id', 'genres']], ratings[['user id', 'movie id', 'rating']]),
                    users[['user id', 'gender', 'age', 'occupation']])
print("Head of Dataset1")
print(dataset1.head())

# Create one data frame of how many times a movie was rated
ratings_total1 = dataset1.groupby('movie id').size()
print("Head of Total Number of Ratings per Each Movie")
print(ratings_total1.head())

# Create one data frame with the mean rate for each movie
ratings_mean1 = (dataset1.groupby('movie id'))['movie id', 'rating'].mean()
print("Mean Rate")
print(ratings_mean1.head())


class Node():
    def __init__(self, atributo):
        self.atributo = atributo
        self.filhos = {}

    def incluirFilhos(self, valor, node):
        self.filhos[valor] = node

def getEntropia(exemplos):
    m = (exemplos.groupby('rating'))['rating'].size()
    soma = m.sum(0)
    entropia = 0
    for i in range(len(m)):
        if m.iloc[i] == 0:
            continue
        entropia -= (m.iloc[i] / soma) * (log(m.iloc[i] / soma) / log(2))
    return entropia

def escolherAtributo(atributos, exemplos):
    entropiaInicial = getEntropia(exemplos)
    # print("Entropia Inicial: ", entropiaInicial)
    informacao = 0
    atributoEscolhido = atributos[0]
    numElementos = len(exemplos)
    for atributo in atributos:
        values = list(exemplos[atributo].unique())
        entropia = 0
        for elem in values:
            particao = exemplos[exemplos[atributo]==elem]
            entropia += (len(particao)/numElementos)*getEntropia(particao)
        # print("atributo: ", atributo, " entropia: ", entropia)
        if (entropiaInicial-entropia) > informacao:
            informacao = entropiaInicial-entropia
            atributoEscolhido = atributo
    if informacao == 0:
        return None
    else:
        return atributoEscolhido

def getDecisionTree(exemplos, atributos, padrao):
    # print('Exemplos:', len(exemplos))
    # print('Atributos:',atributos)
    tree = None
    if len(exemplos) < 1000:
        return padrao
    else:
        m = int(exemplos.iloc[0, 3])
        b = True
        for i in exemplos.iloc[:, 3]:
            if m != int(i):
                b = False
                break
        if b:
            return m
        else:
            if len(atributos) == 0:
                m = (exemplos.groupby('rating'))['rating'].size()
                m = m.sort_values(ascending=False)
                return m.index[0]
            else:
                melhor = escolherAtributo(atributos, exemplos)
                if melhor is None:
                    return padrao
                else:
                    tree = Node(melhor)
                    m = (exemplos.groupby('rating'))['rating'].size()
                    m = m.sort_values(ascending=False)
                    m = m.index[0]
                    # print('m = ', m)
                    for v in list(exemplos[melhor].unique()):
                        e = exemplos[exemplos[melhor] == v]
                        # print("Num Exemplos:",len(e))
                        i = atributos[:]
                        del i[i.index(melhor)]
                        sub_arvore = getDecisionTree(e, i, m)
                        tree.incluirFilhos(v, sub_arvore)
    return tree

print("Separando DataSets")
dataset1.sample(frac=1).reset_index(drop=True)
dataset_train = dataset1[:int(len(dataset1) * 2 / 3)]
dataset_test = dataset1[int(len(dataset1) * 2 / 3):]

print("Construir Arvore")
# print(escolherAtributo(['gender', 'age', 'occupation', 'genres'], dataset_train))
inicio = time.time()
t = getDecisionTree(dataset_train, ['genres', 'age', 'gender', 'occupation'], 1)
fim = time.time()
print("Tempo de Execução:",fim-inicio)

def printDecisionTree(node):
    print("Atributo:",node.atributo)
    for f in node.filhos.keys():
        print("Key:",f)
        v = node.filhos[f]
        if str(v.__class__.__name__)=='Node':
            printDecisionTree(node.filhos[f])
        else:
            print("Value:", v)

printDecisionTree(t)
