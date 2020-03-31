from sklearn.linear_model import SGDClassifier
import random
import numpy
import pandas as pd
from time import time


def batches(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

df = pd.read_csv('perf_OH.txt' ,sep='|', nrows=10000000)
df.fillna(999, inplace=True)
print(df.drop(['dflt', 'dflt1', 'LoanID', 'RepoFlag', '24', 'Curr_Qtr'], axis=1).info())
X = df.drop(['dflt', 'dflt1', 'LoanID', 'RepoFlag', '24', 'Curr_Qtr', '14', '23'], axis=1).values
Y = df['dflt'].values

clf2 = SGDClassifier(loss='log', n_jobs=-1)

shuffledRange = list(range(len(X)))
n_iter = 5

start = time()
for n in range(n_iter):
    numpy.random.shuffle(shuffledRange)
    shuffledX = [X[i] for i in shuffledRange]
    shuffledY = [Y[i] for i in shuffledRange]
    for batch in batches(range(len(shuffledX)), 100000):
        clf2.partial_fit(shuffledX[batch[0]:batch[-1]+1], shuffledY[batch[0]:batch[-1]+1], classes=numpy.unique(Y))

end = time()

with open('output.txt', 'w') as file:
    file.write('Runtime (min): {}\n'.format((end - start)/60))