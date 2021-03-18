import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### Random forest importance plot
rf1 = load('rf.joblib')

rf1.feature_importances_

var_names = ['Female', 'Homeless', 'Age', 'Albumin', 'BUN',
       'Calcium', 'Cholesterol', 'Glucose', 'HDL',
       'A1C', 'LDL', 'Phosphorus', 'Potassium',
       'Sodium', 'eGFR', 'Creatinine', 'Urine PCR',
       'Urine ACR', 'Colonoscopy', 'Hemoglobin', 'Fecal occult',
       'PTH', 'HepB', 'Pneumovax', 'Prevnar', 'CHF',
       'Asthma', 'Diabetes', 'Hypertension', 'CHD', 'Dementia', 'Chronic pain', 'SAD',
       'PCP', 'Inpt count', 'Inpt since', 'Outpt count',
       'Outpt since', 'ED count', 'ED since', 'SBP',
       'DBP', 'Race - American Indian Alaska Native', 'Race - Asian', 'Race - black',
       'Race - Hispanic', 'Race - Native Hawaiian Pacific Islander', 'Race - other', 'Race - white',
       'Language - Chinese', 'Language - English', 'Language - other', 'Language - Russian', 
        'Language - Spanish', 'Language - Tagalog','Language - Vietnamese', 
        'Insurance - Commercial', 'Insurance - Healthy SF', 'Insurance - Medi-Cal', 'Insurance - Medicare',
        'Insurance - other', 'Urine protein 1+', 'Urine protein 2+', 'Urine protein 3+', 'Urine protein 4+', 
        'Urine protein NEGATIVE', 'Urine protein TRACE', 'Urine occult 1+', 'Urine occult 2+', 'Urine occult 3+', 
        'Urine occult NEGATIVE', 'Urine occult TRACE']


def plot_feature_importance(importance,names,model_type):

    #Create arrays from feature importance and feature names
    feature_importance = np.array(importance)
    feature_names = np.array(names)

    #Create a DataFrame using a Dictionary
    data={'feature_names':feature_names,'feature_importance':feature_importance}
    fi_df = pd.DataFrame(data)

    #Sort the DataFrame in order decreasing feature importance
    fi_df.sort_values(by=['feature_importance'], ascending=False,inplace=True)

    #Define size of bar plot
    plt.figure(figsize=(15,7))
    #Plot Searborn bar chart

    b= sns.barplot(x=fi_df['feature_importance'][:15], y=fi_df['feature_names'][:15], palette="Oranges_r")
    b.set_ylabel("Y Label",fontsize=12)
    b.set_xlabel("X Label",fontsize=12)
    #Add chart labels
    plt.xlabel('Feature Importance')
    plt.ylabel('Predictors')
    plt.show()
plot_feature_importance(rf1.feature_importances_, var_names, 'random forest')

np.sort(rf1.feature_importances_)

def plot_feature_importance(importance,names,model_type):

    #Create arrays from feature importance and feature names
    feature_importance = np.array(importance)
    feature_names = np.array(names)

    #Create a DataFrame using a Dictionary
    data={'feature_names':feature_names,'feature_importance':feature_importance}
    fi_df = pd.DataFrame(data)

    #Sort the DataFrame in order decreasing feature importance
    fi_df.sort_values(by=['feature_importance'], ascending=False,inplace=True)

    #Define size of bar plot
    plt.figure(figsize=(20,30))
    #Plot Searborn bar chart

    b= sns.barplot(x=fi_df['feature_importance'], y=fi_df['feature_names'], palette="Oranges_r")
    b.set_ylabel("Y Label",fontsize=15)
    b.set_xlabel("X Label",fontsize=15)
    #Add chart labels
    plt.xlabel('Feature Importance')
    plt.ylabel('Predictors')
    plt.show()
plot_feature_importance(rf1.feature_importances_, var_names, 'random forest')

### Gradient boosting importance plot
from joblib import dump, load
rbc1 = load('rbc.joblib')

rbc1.feature_importances_

var_names = ['Female', 'Homeless', 'Age', 'Albumin', 'BUN',
       'Calcium', 'Cholesterol', 'Glucose', 'HDL',
       'A1C', 'LDL', 'Phosphorus', 'Potassium',
       'Sodium', 'eGFR', 'Creatinine', 'Urine PCR',
       'Urine ACR', 'Colonoscopy', 'Hemoglobin', 'Fecal occult',
       'PTH', 'HepB', 'Pneumovax', 'Prevnar', 'CHF',
       'Asthma', 'Diabetes', 'Hypertension', 'CHD', 'Dementia', 'Chronic pain', 'SAD',
       'PCP', 'Inpt count', 'Inpt since', 'Outpt count',
       'Outpt since', 'ED count', 'ED since', 'SBP',
       'DBP', 'Race - American Indian Alaska Native', 'Race - Asian', 'Race - black',
       'Race - Hispanic', 'Race - Native Hawaiian Pacific Islander', 'Race - other', 'Race - white',
       'Language - Chinese', 'Language - English', 'Language - other', 'Language - Russian', 
        'Language - Spanish', 'Language - Tagalog','Language - Vietnamese', 
        'Insurance - Commercial', 'Insurance - Healthy SF', 'Insurance - Medi-Cal', 'Insurance - Medicare',
        'Insurance - other', 'Urine protein 1+', 'Urine protein 2+', 'Urine protein 3+', 'Urine protein 4+', 
        'Urine protein NEGATIVE', 'Urine protein TRACE', 'Urine occult 1+', 'Urine occult 2+', 'Urine occult 3+', 
        'Urine occult NEGATIVE', 'Urine occult TRACE']

import seaborn as sns

def plot_feature_importance(importance,names,model_type):

    #Create arrays from feature importance and feature names
    feature_importance = np.array(importance)
    feature_names = np.array(names)

    #Create a DataFrame using a Dictionary
    data={'feature_names':feature_names,'feature_importance':feature_importance}
    fi_df = pd.DataFrame(data)

    #Sort the DataFrame in order decreasing feature importance
    fi_df.sort_values(by=['feature_importance'], ascending=False,inplace=True)

    #Define size of bar plot
    plt.figure(figsize=(15,7))
    #Plot Searborn bar chart

    b= sns.barplot(x=fi_df['feature_importance'][:15], y=fi_df['feature_names'][:15], palette="Greens_r")
    b.set_ylabel("Y Label",fontsize=12)
    b.set_xlabel("X Label",fontsize=12)
    #Add chart labels
    plt.xlabel('Feature Importance')
    plt.ylabel('Predictors')
    plt.show()
plot_feature_importance(rbc1.feature_importances_, var_names, '')

np.sort(rbc1.feature_importances_)

import seaborn as sns

def plot_feature_importance(importance,names,model_type):

    #Create arrays from feature importance and feature names
    feature_importance = np.array(importance)
    feature_names = np.array(names)

    #Create a DataFrame using a Dictionary
    data={'feature_names':feature_names,'feature_importance':feature_importance}
    fi_df = pd.DataFrame(data)

    #Sort the DataFrame in order decreasing feature importance
    fi_df.sort_values(by=['feature_importance'], ascending=False,inplace=True)

    #Define size of bar plot
    plt.figure(figsize=(20,30))
    #Plot Searborn bar chart

    b= sns.barplot(x=fi_df['feature_importance'], y=fi_df['feature_names'], palette="Greens_r")
    b.set_ylabel("Y Label",fontsize=15)
    b.set_xlabel("X Label",fontsize=15)
    #Add chart labels
    plt.xlabel('Feature Importance')
    plt.ylabel('Predictors')
    plt.show()
plot_feature_importance(rbc1.feature_importances_, var_names, '')
