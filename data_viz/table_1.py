import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# import entire raw data
path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
data = pd.read_csv(os.path.join(path, r'consolidated_data.csv'))

# get the train/test set (seed set to the same as actual split)
from sklearn.model_selection import train_test_split
unique_pt = data['ActiveMRN'].unique()
idx_train, idx_test = train_test_split(unique_pt,test_size=0.2, random_state=7)
data_train = data[data['ActiveMRN'].isin(idx_train)]
data_test = data[data['ActiveMRN'].isin(idx_test)]



# table 1: study population characteristics (overall, train, test)

# get the first instance for each pt: pred_date is already in order from earlier to later, so we keep the first instance
data_uniq =  data.drop_duplicates(subset=['ActiveMRN'], keep='first')
data_train_uniq = data_train.drop_duplicates(subset=['ActiveMRN'], keep='first')
data_test_uniq = data_test.drop_duplicates(subset=['ActiveMRN'], keep='first')

# drop the unnecessary columns
data_uniq = data_uniq.drop(columns=['Unnamed: 0', 'ActiveMRN', 'DOB', 'DOD', 'zip', 'CKD_date', 'pred_date'])

# entire population
len(data_uniq[data_uniq['homeless'] == 1])

for column in data_uniq:
    
    
    if (data_uniq[column].dtype == 'float64') and not (data_uniq[column].isin([0,1]).all()):
        print(column)
        print('mean:', np.mean(data_uniq[column]))
        print('95 CI:', np.nanpercentile(data_uniq[column], [2.5, 97.5]))
        print()
    else:
        print(column)
        print(data_uniq[column].value_counts())
        print()

len(data_train_uniq[data_train_uniq['homeless'] == 1])

# training set
data_train_uniq = data_train_uniq.drop(columns=['Unnamed: 0', 'ActiveMRN', 'DOB', 'DOD', 'zip', 'CKD_date', 'pred_date'])

for column in data_train_uniq:
    
    
    if (data_train_uniq[column].dtype == 'float64') and not (data_train_uniq[column].isin([0,1]).all()):
        print(column)
        print('mean:', np.mean(data_train_uniq[column]))
        print('95 CI:', np.nanpercentile(data_train_uniq[column], [2.5, 97.5]))
        print()
    else:
        print(column)
        print(data_train_uniq[column].value_counts())
        print()

# test set
#data_test_uniq = data_test_uniq.drop(columns=['Unnamed: 0', 'ActiveMRN', 'DOB', 'DOD', 'zip', 'CKD_date', 'pred_date'])

for column in data_test_uniq:
    
    
    if (data_test_uniq[column].dtype == 'float64') and not (data_test_uniq[column].isin([0,1]).all()):
        print(column)
        print('mean:', np.mean(data_test_uniq[column]))
        print('95 CI:', np.nanpercentile(data_test_uniq[column], [2.5, 97.5]))
        print()
    #else:
    #    print(column)
    #    print(data_test_uniq[column].value_counts())
    #    print()
