import time

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

start = time.time()
df = pd.read_csv('csv_files/train.csv')
df = df.dropna()
X = df.drop('target', axis=1)[['bin_0', 'bin_1', 'bin_2']]
X[['bin_3', 'bin_4', 'bin_5']] = df[['bin_0', 'bin_1', 'bin_2']]
y = df['target']
df_test = pd.read_csv('csv_files/train.csv')
df_test = df_test.dropna()
X_test = df_test.drop('target', axis=1)[['bin_0', 'bin_1', 'bin_2']]
X_test[['bin_3', 'bin_4', 'bin_5']] = df_test[['bin_0', 'bin_1', 'bin_2']]
y_test = df_test['target']
result = dict()
for model_lib in [LogisticRegression, DecisionTreeClassifier, RandomForestClassifier, AdaBoostClassifier, MLPClassifier,
                  KNeighborsClassifier, SVC]:
    model = model_lib()
    model.fit(X, y)
    y_pred = model.predict(X_test)
    result.update({model_lib: roc_auc_score(y_test, y_pred, multi_class="ovr")})
print(time.time() - start)
print(result)
