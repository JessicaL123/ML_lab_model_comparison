# -*- coding: utf-8 -*-
"""6375 Lab.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wzQ0JHsspYKgDGBqdIsY8lk3SMwXfa5m
"""

import numpy as np
import pandas as pd

np.random.seed(1)

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')

data_set_path = 'https://archive.ics.uci.edu/ml/machine-learning-databases/car/car.data'
headers = ['buying','maint','doors','persons','lug_boot', 'safety', 'label']
df = pd.read_csv(data_set_path, header=None, names=headers)

df

from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
for col in df.columns:
    df[col] = label_encoder.fit_transform(df[col])

df

X = df.iloc[:, 0:-1]
y = df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

# normailize
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

models = {
            'DT':DecisionTreeClassifier(), 
            'NN': MLPClassifier(),
            'SVM': SVC(), 
            'GaussianNB': GaussianNB(), 
            'LR': LogisticRegression(),
            'KNN': KNeighborsClassifier(), 
            'Bagging': BaggingClassifier(),
            'RF': RandomForestClassifier(), 
            'AdaBoost': AdaBoostClassifier(),
            'GB': GradientBoostingClassifier(), 
            'XGB': XGBClassifier()}

hyperparameters = {
    'DT':{'max_depth':[None, 5, 10], 'min_samples_split': [2, 4, 8], 'max_features': [None, 3, 5], 'min_impurity_decrease': [0, 0.1, 0.5]},
    'NN': {'hidden_layer_sizes':[[4], [2, 4], [10, 10, 10]], 'activation':['logistic', 'relu', 'tanh'], 'learning_rate' : ['constant', 'adaptive'], 'max_iter':[100, 1000]},
    'SVM': {'kernel': ['linear', 'poly'], 'gamma': [1e-3, 1e-6], 'C': [1, 100], 'max_iter': [1000, 5000]},
    'GaussianNB': {'priors':[None, [0.25, 0.25, 0.25, 0.25], [0.1, 0.2, 0.3, 0.4]]},
    'LR': {'penalty': ['l1', 'l2'], 'tol': [1e-2, 1e-4, 1e-6], 'fit_intercept':[True, False], 'max_iter': [1000, 5000]},
    'KNN': {'n_neighbors': [3, 6, 9], 'weights':['uniform', 'distance'], 'algorithm': ['auto', 'brute', 'ball_tree'], 'p': [1, 2]},
    'Bagging': {'n_estimators': [10, 30], 'max_samples': [1.0, 0.5], 'max_features': [1.0, 0.5], 'random_state': [None, 1]},
    'RF': {'n_estimators': [10, 100], 'criterion': ['gini', 'entropy'], 'max_depth': [None, 2, 4], 'min_samples_split': [2, 4, 8]},
    'AdaBoost': {'n_estimators': [50, 100], 'learning_rate':[0.2, 1], 'algorithm': ['SAMME', 'SAMME.R'], 'random_state': [None, 1]},
    'GB': {'loss': ['deviance'], 'learning_rate': [0.1, 0.01], 'max_depth': [3, 5], 'min_impurity_decrease': [0, 0.1]},
    'XGB': {'learning_rate': [0.1, 0.01], 'n_estimators': [100, 300], 'seed': [None, 1], 'booster': ['gblinear', 'gbtree']}}

# Commented out IPython magic to ensure Python compatibility.
scores = ['accuracy']

for classifier in models.keys():
    print('================================== Classifier: %s ==================================' % classifier)

    print()
    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(models[classifier], hyperparameters[classifier], cv=5,
                           scoring='%s' % score)
        clf.fit(X_train, y_train)

        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r"
#                   % (mean, std * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(X_test)
        print('*' * 30)
        print(y_pred)
        print(classification_report(y_true, y_pred))
        print("Detailed confusion matrix:")
        print(confusion_matrix(y_true, y_pred))
        print("Accuracy Score: \n")
        print(accuracy_score(y_true, y_pred))

        print()

