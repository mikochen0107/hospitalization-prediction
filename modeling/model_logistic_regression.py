import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# import training data
X_train = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_train_knn.csv", delimiter=',')
y_train = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\y_train.csv", delimiter=',')
y_train = y_train[1:,1]

# hyperparameter tuning with CV

# C: np.logspace(-2, 2, 5), penalty: l1, l2
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

parameters = {'penalty' : ['l1', 'l2'],
              'C' : np.logspace(-2, 2, 5)}
regr = LogisticRegression(solver='liblinear')

clf = GridSearchCV(estimator=regr, param_grid=parameters, scoring=['roc_auc', 'precision'], refit='precision', 
                   verbose=3, n_jobs=-1)
clf.fit(X_train, y_train)

# CV results: best params, best score, and the cv results
print(clf.best_params_)
print(clf.best_score_)
cv_results = pd.DataFrame(clf.cv_results_)
cv_results

# ranking based on roc auc
cv_results.sort_values(by=['rank_test_roc_auc'])['params']
cv_results.sort_values(by=['rank_test_roc_auc'])['mean_test_roc_auc']

# ranking based on precision
cv_results.sort_values(by=['rank_test_precision'])['params']
cv_results.sort_values(by=['rank_test_precision'])['mean_test_precision']

cv_results.to_csv(r'M:\UCSF_ARS\michael_thesis\cross_validation\logistic_CV.csv')

# selecting the best hyperparams from CV to train model
# C = 0.01, penalty=l2
from sklearn.linear_model import LogisticRegression

regr = LogisticRegression(solver='liblinear', C=0.01, penalty='l2', random_state=7) # liblinear
regr.fit(X_train, y_train)

from joblib import dump, load
dump(regr, 'lr.joblib') 

y_pred_lr = regr.predict(X_train) # get the predictions (0/1)
y_prob_lr = regr.predict_proba(X_train)[:, 1] # get the prob for predicting 1s

# train set metrics
model_metrics(y_train, y_pred_lr, y_prob_lr)

# get mean coefs
print('Coef:', regr.coef_)

(regr.coef_[0])

x = np.random.choice(np.arange(len(y_train)), size=len(y_train), replace=True)
boot_X = X_train[x]

# bootstrap to get the 95% CI for coefs
from sklearn.linear_model import LogisticRegression

iterations = 1000
storage = []
for i in range(iterations):
    if i%10 == 0:
        print(i)
    boot_idx = np.random.choice(np.arange(len(y_train)), size=len(y_train), replace=True)
    boot_X = X_train[boot_idx]
    boot_y = y_train[boot_idx]
    regr = LogisticRegression(solver='liblinear', C=0.01, penalty='l2', random_state=7) 
    regr.fit(boot_X, boot_y)
    storage.append(regr.coef_[0].tolist())

storage_95CI = np.percentile(storage, [2.5, 97.5], axis=0) # axis=0 means we do this for every coef

### evaluate with the test set
X_test = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_test_knn.csv", delimiter=',')
y_test = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\y_test.csv", delimiter=',')
y_test = y_test[1:,1]

y_pred_lr_test = regr.predict(X_test) # get the predictions (0/1)
y_prob_lr_test = regr.predict_proba(X_test)[:, 1] # get the prob for predicting 1s

model_metrics(y_test, y_pred_lr_test, y_prob_lr_test)
