import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

import datetime as dt
from dateutil.relativedelta import *
from datetime import datetime

### Train/test split

# train/test split (patients are uniquely partitioned to either, but not both, groups)
# randomly split dataset into train and test sets

path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
data = pd.read_csv(os.path.join(path, r'consolidated_data.csv'))

# generate a list of unique patients
unique_pt = data['ActiveMRN'].unique()

# randomly split the patients into train and test sets 
from sklearn.model_selection import train_test_split
idx_train,idx_test = train_test_split(unique_pt,test_size=0.2, random_state=7)

data_train = data[data['ActiveMRN'].isin(idx_train)]
data_test = data[data['ActiveMRN'].isin(idx_test)]

print(len(data_train))
print(len(data_test))

X_train = data_train.drop('admit', axis=1)
y_train = data_train['admit']
X_test = data_test.drop('admit', axis=1)
y_test = data_test['admit']

X_train.index = np.arange(0,len(X_train))
X_test.index = np.arange(0,len(X_test))
y_train.index = np.arange(0,len(y_train))
y_test.index = np.arange(0,len(y_test))

# export train/test sets and DON'T TOUCH
new_path = r"M:\UCSF_ARS\michael_thesis\processed_data"
X_train.to_csv(os.path.join(new_path, r'X_train_raw.csv'))
y_train.to_csv(os.path.join(new_path, r'y_train.csv'))
X_test.to_csv(os.path.join(new_path, r'X_test_raw.csv'))
y_test.to_csv(os.path.join(new_path, r'y_test.csv'))

### Data preprocessing 

#### train set

# preprocess train set (encoding categorical, imputing missing)
path = r"M:\UCSF_ARS\michael_thesis\processed_data"
X_train_2 = pd.read_csv(os.path.join(path, r'X_train_raw.csv'))

X_train_2.head()

X_train_2.columns

race = pd.get_dummies(X_train_2['race'])
lang = pd.get_dummies(X_train_2['language'])
finclass = pd.get_dummies(X_train_2['finclass'])
zip_ = pd.get_dummies(X_train_2['zip'])
ul_prot = pd.get_dummies(X_train_2['urine_lab_prot'])
ul_occu = pd.get_dummies(X_train_2['urine_lab_occult'])

X_train_2 = X_train_2.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'DOB', 'DOD', 'CKD_date', 'pred_date',
                                    'ActiveMRN', 'race', 'language', 'finclass', 'zip', 
                                    'urine_lab_prot', 'urine_lab_occult'])
X_train_2 = pd.concat([X_train_2, race, lang, finclass, ul_prot, ul_occu], axis=1)
X_train_2_zip = pd.concat([X_train_2, race, lang, finclass, ul_prot, ul_occu, zip_], axis=1)

# mean imputer
from sklearn.impute import SimpleImputer

imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
imp_mean.fit(X_train_2)
X_train_imp_mean = imp_mean.transform(X_train_2)

new_path = r"M:\UCSF_ARS\michael_thesis\processed_data"
np.savetxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_train_mean.csv", X_train_imp_mean, delimiter=",")

# knn imputer
from sklearn.impute import KNNImputer
imp_knn = KNNImputer(n_neighbors=5, weights="uniform")
imp_knn.fit(X_train_2)
X_train_imp_knn = imp_knn.transform(X_train_2)

X_train_imp_knn.shape

# export processed train set for model dev
new_path = r"M:\UCSF_ARS\michael_thesis\processed_data"
np.savetxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_train_processed.csv", X_train_imp_knn, delimiter=",")

#### test set

# use the same method to preprocess test set
path = r"M:\UCSF_ARS\michael_thesis\processed_data"
X_test_2 = pd.read_csv(os.path.join(path, r'X_test_raw.csv'))

race = pd.get_dummies(X_test_2['race'])
lang = pd.get_dummies(X_test_2['language'])
finclass = pd.get_dummies(X_test_2['finclass'])
#zip_ = pd.get_dummies(X_test_2['zip'])
ul_prot = pd.get_dummies(X_test_2['urine_lab_prot'])
ul_occu = pd.get_dummies(X_test_2['urine_lab_occult'])

X_test_2 = X_test_2.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'DOB', 'DOD', 'CKD_date', 'pred_date',
                                    'ActiveMRN', 'race', 'language', 'finclass', 'zip', 
                                    'urine_lab_prot', 'urine_lab_occult'])
X_test_2 = pd.concat([X_test_2, race, lang, finclass, ul_prot, ul_occu], axis=1)

X_test_imp_knn = imp_knn.transform(X_test_2)

# export processed test set for model eval
np.savetxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_test_knn.csv", X_test_imp_knn, delimiter=",")

X_test_imp_mean = imp_mean.transform(X_test_2)

# export processed test set for model eval
np.savetxt(r"M:\UCSF_ARS\michael_thesis\processed_data\X_test_mean.csv", X_test_imp_mean, delimiter=",")
