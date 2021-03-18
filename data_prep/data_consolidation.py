import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

import datetime as dt
from dateutil.relativedelta import *
from datetime import datetime

from sklearn.linear_model import LinearRegression


class DataConsolidation():
    '''
    The function of this class is to consolidate the cleaned data from data_cleaning to create "rectangular" datasets 
    that are ready to be inputted into models to be trained.  

    The procedures are as follows:

        1. Start at a time point t
        2. Inclusion/exclusion criteria: determine who is alive and has CKD, only include those pt
        3. Label outcome: Look forward 6 months from t to see who is admitted, mark them as 1; otherwise, 0
        4. Extract predictors: Look backward to extract the predictors that would be available at t
        5. Repeat steps 1-4 for all time points between 2009-2018 to make the full dataset
        6. Randomly split the data into train (80%) and test set (20%)
    '''
    
    def __init__(self, demo_file_path, adm_file_path, 
                 interval, forward_window, backward_window):
        '''
        Initialize the important attributes of the class
        '''
        self.demo_file_path = demo_file_path
        self.adm_file_path = adm_file_path
        
        self.og_data = pd.read_csv(demo_file_path).drop(columns=['Unnamed: 0', 'Unnamed: 0.1']) # don't touch this!
        self.data = self.og_data # ever-changing df for manipulation purposes
        self.data_store = [] # stores the dataset from each time point in the list
        self.data_out = np.nan # ultimately the merged rectangular dataset we want
        
        self.interval = interval # expressed in months
        self.forward_window = forward_window 
        self.backward_window = backward_window #maybe depends on var
    
    def inclusionCriteria(self, time): # might need more parameters about inclusion criteria
        '''
        
        '''
        self.vitalAgeStatus(time)
        self.ckdStatus(time)
        
    def vitalAgeStatus(self, time):
        '''
        run this before ckdStatus
        nested in inclusionCriteria
        '''
       
        # born before the date
        self.data = self.og_data[self.og_data['DOB'] < time]
        # not dead (DOD is NA or DOD is after date)
        self.data = self.data[(self.data['DOD'].isna()) | (self.data['DOD'] > '2008-01-01')]
        # calculate age
        self.data['age'] = np.floor((pd.to_datetime(time) - pd.to_datetime(self.data['DOB'])) / np.timedelta64(1, 'Y'))
        # reset index
        self.data.index = np.arange(0,len(self.data))
        
    def ckdStatus(self, time):
        '''
        run this after vitalAgeStatus 
        nested in inclusionCriteria
        
        include only patients with CKD
        
        '''
        # include patients who have been diagnosed with CKD
        self.data = self.data[self.data['CKD_date'] < time]
        # reset index
        self.data.index = np.arange(0,len(self.data))
        
    def createLabel(self, time):
        '''
        Import the admissions csv and label the data
        '''
        # import admissions csv
        df_adm = pd.read_csv(self.adm_file_path)
        
        # find the encounters in the time window, drop any duplicates
        time_endpoint = str(dt.datetime.strptime(time, "%Y-%m-%d").date() + relativedelta(months=+self.forward_window))
        df_adm = df_adm[(df_adm['AdmitDate'] > time) & (df_adm['AdmitDate'] < time_endpoint)]
        df_adm = df_adm[['ActiveMRN', 'admit']]
        
        self.data = pd.merge(self.data, df_adm, how = 'left', on=['ActiveMRN'])
        self.data.loc[self.data['admit'].isna(), 'admit'] = 0
     
    def defineComorbidity(self, time, var_file_path, var_name):
        '''
        
        '''
        
        # import predictor csv
        df = pd.read_csv(var_file_path)
        
        df['OBSV_DATE'] = pd.to_datetime(df.OBSV_DATE)      
        df = df[(df['OBSV_DATE'] < time)]
        df = df.drop_duplicates(subset=['ActiveMRN'], keep= 'last')
        df[var_name] = 1
        df = df[['ActiveMRN', var_name]]

        self.data = pd.merge(self.data, df, how = 'left', on=['ActiveMRN'])
        self.data.loc[self.data[var_name].isna(), var_name] = 0
        
    def getMostRecentValue(self, time, var_file_path, var_name):
        '''
        quick way to add predictors
        restricted to most recent
        make sure the column of interest is called "OBSV_RSLT_NO_VAL"
        
        gets the most recent value within the last 2 years
        works for all chem labs, urine labs, hemoglobin,  pth, vitals
        
        ''' 
        # import predictor csv
        df = pd.read_csv(var_file_path)
        two_years_prior = str(dt.datetime.strptime(time, "%Y-%m-%d").date() + relativedelta(months=-self.backward_window))
        
        df['OBSV_DATE'] = pd.to_datetime(df.OBSV_DATE)      
        df = df[(df['OBSV_DATE'] < time) & (df['OBSV_DATE'] > two_years_prior)]
        df = df.sort_values(by='OBSV_DATE')
        df = df.drop_duplicates(subset=['ActiveMRN'], keep= 'last')
        df = df[['ActiveMRN','OBSV_RSLT_NO_VAL']]
        df = df.rename({'OBSV_RSLT_NO_VAL': var_name}, axis=1)

        self.data = pd.merge(self.data, df, how = 'left', on=['ActiveMRN'])

    def getEvent(self, time, var_file_path, var_name):
        '''
        colonoscopy, fecal occult, pcp, immunization, etc. comorb
        var_name is the column name (change this in data_cleaning)
        '''
        df = pd.read_csv(var_file_path)
        two_years_prior = str(dt.datetime.strptime(time, "%Y-%m-%d").date() + relativedelta(months=-self.backward_window))
        
        df['OBSV_DATE'] = pd.to_datetime(df.OBSV_DATE)
        df = df[(df['OBSV_DATE'] < time) & (df['OBSV_DATE'] > two_years_prior)]
        df = df.sort_values(by='OBSV_DATE')
        df = df.drop_duplicates(subset=['ActiveMRN'], keep='last')
        df = df[['ActiveMRN', var_name]]

        self.data = pd.merge(self.data, df, how = 'left', on=['ActiveMRN'])
        self.data.loc[self.data[var_name].isna(), var_name] = 0
    
    def timeSinceEvent(self, time, var_file_path, var_name):
        '''
        time since last inpt, outpt, and ED encounter
        '''
        
        df = pd.read_csv(var_file_path)
        #two_years_prior = str(dt.datetime.strptime(time, "%Y-%m-%d").date() + relativedelta(months=-self.backward_window))

        df['OBSV_DATE'] = pd.to_datetime(df.OBSV_DATE)
        df = df[(df['OBSV_DATE'] < time)]

        df = df.sort_values(by='OBSV_DATE')
        df = df.drop_duplicates(subset=['ActiveMRN'], keep= 'last')

        df['time'] = datetime.strptime(time, '%Y-%m-%d')
        df[var_name]=(df['time'] - df['OBSV_DATE']).astype('timedelta64[D]')
        df = df[['ActiveMRN', var_name]]
        
        self.data = pd.merge(self.data, df, how = 'left', on=['ActiveMRN'])
        #self.data.loc[self.data[var_name].isna(), var_name] = np.nan

    def countEvent(self, time, var_file_path, var_name):
        '''
        # of inpt, outpt, and ED encounters in the last 2 years
        '''

        df = pd.read_csv(var_file_path)
        two_years_prior = str(dt.datetime.strptime(time, "%Y-%m-%d").date() + relativedelta(months=-self.backward_window))    
        
        df['OBSV_DATE'] = pd.to_datetime(df.OBSV_DATE)
        df = df[(df['OBSV_DATE'] < time) & (df['OBSV_DATE'] > two_years_prior)]

        df[var_name] = df.groupby(['ActiveMRN'])['ActiveMRN'].transform('count')
        df = df.drop_duplicates(subset=['ActiveMRN'])
        df = df[['ActiveMRN', var_name]]
        
        self.data = pd.merge(self.data, df, how = 'left', on=['ActiveMRN'])
        self.data.loc[self.data[var_name].isna(), var_name] = 0
    
    def linreg(self, df):
        '''
        for calculateSlope() below
        requires sklearn linear regression
        '''
        y = df[['OBSV_RSLT_NO_VAL']].values
        X = df[['X']].values
        return np.squeeze(LinearRegression().fit(X, y).coef_*365)
    
    def calculateSlope(self, time, var_file_path, var_name):
        '''
        '''
        
        df = pd.read_csv(var_file_path)
        two_years_prior = str(dt.datetime.strptime(time, "%Y-%m-%d").date() + relativedelta(months=-self.backward_window))    
        
        df['OBSV_DATE'] = pd.to_datetime(df.OBSV_DATE)
        df = df[(df['OBSV_DATE'] < time) & (df['OBSV_DATE'] > two_years_prior)]

        df['start'] = datetime.strptime(two_years_prior, '%Y-%m-%d')
        df['X'] = (df['OBSV_DATE'] -  df['start']).astype('timedelta64[D]')

        df = df[df['OBSV_RSLT_NO_VAL'].isnull() == False]
        df = df.groupby(['ActiveMRN']).apply(self.linreg).reset_index()
        df = df.rename({0: var_name}, axis=1)
        
        self.data = pd.merge(self.data, df, how = 'left', on=['ActiveMRN'])
        self.data.loc[self.data[var_name].isna(), var_name] = 0
        
    def consolidate(self, time):
        '''
        Pulling everything together in 1 time point
        '''
        self.inclusionCriteria(time)
        self.createLabel(time)
        
        file_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
        
        chem_labs = ['chem_lab_alb', 'chem_lab_bun', 'chem_lab_ca', 'chem_lab_chol', 'chem_lab_gluc', 'chem_lab_hdl', 
                     'chem_lab_a1c','chem_lab_ldl', 'chem_lab_p', 'chem_lab_k', 'chem_lab_na', 'chem_lab_egfr', 
                     'chem_lab_crea']
        for cl in chem_labs:
            print(cl)
            name = cl
            path = os.path.join(file_path, cl + '.csv')
            self.getMostRecentValue(time, var_file_path=path, var_name=name)
        
        urine_labs = ['urine_lab_prot', 'urine_lab_occult', 'urine_lab_pcr', 'urine_lab_acr']
        for ul in urine_labs:
            print(ul)
            name = ul
            path = os.path.join(file_path, ul + '.csv')
            self.getMostRecentValue(time, var_file_path=path, var_name=name)
        
        other_labs = ['other_lab_col', 'other_lab_hemo', 'other_lab_fecal', 'other_lab_pth']
        for ol in other_labs:
            print(ol)
            name = ol
            path = os.path.join(file_path, ol + '.csv')
            if (name == 'other_lab_col') | (name == 'other_lab_fecal'):
                self.getEvent(time, var_file_path=path, var_name=name)
            else: 
                self.getMostRecentValue(time, var_file_path=path, var_name=name)
        
        immunizations = ['iz_hepb', 'iz_pneumovax', 'iz_prevnar']
        for iz in immunizations:
            print(iz)
            name = iz
            path = os.path.join(file_path, iz + '.csv')
            self.getEvent(time, var_file_path=path, var_name=name)
        
        comorbidities = ['cm_chf', 'cm_ast', 'cm_dm', 'cm_hyp', 'cm_chd', 'cm_dem', 'cm_pain', 'cm_sub']
        for cm in comorbidities:
            print(cm)
            name = cm
            path = os.path.join(file_path, cm + '.csv')
            self.defineComorbidity(time, var_file_path=path, var_name=name)
        
        pcp_path = os.path.join(file_path, 'pcp.csv')
        self.getEvent(time, var_file_path=pcp_path, var_name='pcp')
        
        encounters = ['enc_inpt', 'enc_outpt', 'enc_ed']
        for enc in encounters:
            print(enc)
            name = enc
            path = os.path.join(file_path, enc + '.csv')
            self.countEvent(time=time, var_file_path=path, var_name=name+'_count')
            self.timeSinceEvent(time=time, var_file_path=path, var_name=name+'_timesince')
            
        vitals = ['vit_sys', 'vit_dia'] # 'vit_hgt', 'vit_wgt', 'vit_bmi' not added
        for v in vitals:
            print(v)
            name = v
            path = os.path.join(file_path, v + '.csv')
            self.getMostRecentValue(time, var_file_path=path, var_name=name)
        
        
        self.data['pred_date'] = time
        
        return self.data
    
    def consolidateAll(self, start_date, end_date, interval):
        '''
        For all time points
        '''
        # loop through all the time points from start to end, run the thing above
        t = start_date
        times = []
        
        # create a list of points in time given the start and end
        while t <= end_date:
            times.append(t)
            t = str(dt.datetime.strptime(t, "%Y-%m-%d").date() + relativedelta(months=+interval))
        
        # consolidate data for each of the point in time
        for time in times:
            print('Processing:', time)
            df = self.consolidate(time)
            self.data_store.append(df)
        
        # merge the datasets from diff times
        self.data_out = pd.concat(self.data_store)
        self.data_out.index = np.arange(0,len(self.data_out))

# use the created class to consolidate data
dc = DataConsolidation(demo_file_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data\demo_ckd.csv",
                          adm_file_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data\admit.csv", 
                          interval = 6, forward_window=6, backward_window=24)

dc.consolidateAll(start_date='2008-01-01', end_date='2018-12-31', interval=6)

path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
dc.data_out.to_csv(os.path.join(path, r'consolidated_data.csv'))
