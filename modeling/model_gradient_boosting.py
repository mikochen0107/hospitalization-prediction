import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# import training data
X_train = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_train_knn.csv", delimiter=',')
y_train = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\y_train.csv", delimiter=',')
y_train = y_train[1:,1]

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import GradientBoostingClassifier

# Number of trees in gradient boosting classifier
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Learning rate
learning_rate = [0.0001, 0.001, 0.01, 0.1, 1.0]
# Maximum number of levels in tree
max_depth = [3, 5, 7, 9]
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'learning_rate': learning_rate,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}

rbc = GradientBoostingClassifier()
rbc_random = RandomizedSearchCV(estimator = rbc, param_distributions = random_grid, n_iter=100, cv=5, 
                               scoring=['roc_auc', 'precision'], refit='precision',
                               verbose=3, random_state=7, n_jobs = -1)

rbc_random.fit(X_train, y_train)

# CV results: best params, best score, and the cv results
print(rbc_random.best_params_)
print(rbc_random.best_score_)
cv_results = pd.DataFrame(rbc_random.cv_results_)

# ranking based on roc auc
cv_results.sort_values(by=['rank_test_roc_auc'])['params']
cv_results.sort_values(by=['rank_test_roc_auc'])['mean_test_roc_auc']

# ranking based on precision
cv_results.sort_values(by=['rank_test_precision'])
cv_results.sort_values(by=['rank_test_precision'])['mean_test_precision']

cv_results.to_csv(r'M:\UCSF_ARS\michael_thesis\cross_validation\gradient_boosting_CV.csv')

# use the best hyperparams to train the model
# {'n_estimators': 800, 'min_samples_split': 5, 'min_samples_leaf': 1, 'max_depth': 7, 'learning_rate': 0.001}
rbc = GradientBoostingClassifier(n_estimators=800, min_samples_split=5, min_samples_leaf=1, max_depth=7, learning_rate=0.001,
                                 verbose=3, random_state=7)

rbc.fit(X_train, y_train)

# model calibration
from sklearn.calibration import CalibratedClassifierCV
calibrated_clf = CalibratedClassifierCV(base_estimator=rbc1, cv=5, method='isotonic')
calibrated_clf.fit(X_train, y_train)

y_pred_rbc = rbc.predict(X_train) # get the predictions (0/1)
y_prob_rbc = calibrated_clf.predict_proba(X_train)[:, 1] # get the prob for predicting 1s

model_metrics(y_train, y_pred_rbc, y_prob_rbc)

# evaluate with test set
X_test = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_test_knn.csv", delimiter=',')
y_test = np.genfromtxt(r"M:\UCSF_ARS\michael_thesis\processed_data\y_test.csv", delimiter=',')
y_test = y_test[1:,1]

y_pred_rbc_test = rbc1.predict(X_test) # get the predictions (0/1)
y_prob_rbc_test = calibrated_clf.predict_proba(X_test)[:, 1] # get the prob for predicting 1s

model_metrics(y_test, y_pred_rbc_test, y_prob_rbc_test)
