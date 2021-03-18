import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# import training data
X_train = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_train_knn.csv", delimiter=',')
y_train = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\y_train.csv", delimiter=',')
y_train = y_train[1:,1]

# hyperparameter optimization with CV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

rf = RandomForestClassifier()
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter=100, cv=5, 
                               scoring=['roc_auc', 'precision'], refit='precision',
                               verbose=3, random_state=7, n_jobs = -1)

rf_random.fit(X_train, y_train)

# CV results: best params, best score, and the cv results
cv_results = pd.DataFrame(rf_random.cv_results_)

# ranking based on roc auc
cv_results.sort_values(by=['rank_test_roc_auc'])['params']

cv_results.sort_values(by=['rank_test_roc_auc'])['mean_test_roc_auc']

# ranking based on precision
cv_results.sort_values(by=['rank_test_precision'])['params']
cv_results.sort_values(by=['rank_test_precision'])['mean_test_precision']

cv_results.to_csv(r'M:\UCSF_ARS\michael_thesis\cross_validation\random_forest_CV.csv')

# selecting the 'best' hyperparams from CV to train model
# 36 from the hyperparams cv results
rf = RandomForestClassifier(n_estimators=1400, min_samples_split=5, min_samples_leaf=4,
                            max_depth=None, bootstrap=True, random_state=7, n_jobs=-1) 
rf.fit(X_train, y_train)

# model calibration
from sklearn.calibration import CalibratedClassifierCV
calibrated_clf = CalibratedClassifierCV(base_estimator=rf, cv=5)
calibrated_clf.fit(X_train, y_train)

y_pred_rf = rf.predict(X_train) # get the predictions (0/1)
y_prob_rf = calibrated_clf.predict_proba(X_train)[:, 1] # get the prob for predicting 1s

# metrics for training set
model_metrics(y_train, y_pred_rf, y_prob_rf)

# evaluate with test set
X_test = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_test_knn.csv", delimiter=',')
y_test = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\y_test.csv", delimiter=',')
y_test = y_test[1:,1]

y_pred_rf_test = rf.predict(X_test) # get the predictions (0/1)
y_prob_rf_test = calibrated_clf.predict_proba(X_test)[:, 1] # get the prob for predicting 1s

model_metrics(y_test, y_pred_rf_test, y_prob_rf_test)
