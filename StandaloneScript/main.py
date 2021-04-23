import time

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from FinalProject.CeleryUtils import CeleryUtils
from FinalProject.CeleryUtils.CeleryUtils import group_tasks
from FinalProject.CeleryWorkerTask import train_worker, compare_models


def run_pc():
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
    for model_lib in [LogisticRegression, DecisionTreeClassifier, RandomForestClassifier, AdaBoostClassifier,
                      MLPClassifier,
                      KNeighborsClassifier, SVC]:
        model = model_lib()
        model.fit(X, y)
        y_pred = model.predict(X_test)
        result.update({model_lib: roc_auc_score(y_test, y_pred, multi_class="ovr")})
    print(time.time() - start)
    print(result)


def run_worker():
    payload = [{'model': '{}', 'class_name': 'ScikitSolver', 'model_name': 'LogisticRegression'},
               {'model': '{}', 'class_name': 'ScikitSolver', 'model_name': 'DecisionTreeClassifier'},
               {'model': '{}', 'class_name': 'ScikitSolver', 'model_name': 'RandomForestClassifier'},
               {'model': '{}', 'class_name': 'ScikitSolver', 'model_name': 'AdaBoostClassifier'},
               {'model': '{}', 'class_name': 'ScikitSolver', 'model_name': 'MLPClassifier'},
               {'model': '{}', 'class_name': 'ScikitSolver', 'model_name': 'KNeighborsClassifier'},
               {'model': '{}', 'class_name': 'ScikitSolver', 'model_name': 'SVC'}]
    dataset_name = 'titanic2_data'
    group = group_tasks(train_worker, payload, dataset_name)
    agent = CeleryUtils.create_chords(group, compare_models, dataset_name=dataset_name)
    agent.apply_async(queue='test')


run_worker()
