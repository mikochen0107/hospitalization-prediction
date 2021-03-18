import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

### Demographics
file_path = r"M:\UCSF_ARS\cc_data_cleaning\Data\Demographics\Demographics_MC.csv"
df = pd.read_csv(file_path)

# hispanic and race
# replace whatever value in race with "HISPANIC" if hispanic=1
pd.crosstab(df['race'], df['hispanic'])
hisp = df.hispanic==1
df.loc[hisp, 'race'] = 'HISPANIC'

# language
# take the top 6 languages (> 1000): english, spanish, chinese (cantonese, mandarin), russian, vietnamese, tagalog
# all other languages are binned as "others"
df['language'].str.strip()
df.loc[(df.language == 'CANTONESE'),'language']='CHINESE'
df.loc[(df.language == 'MANDARIN'),'language']='CHINESE'
df.loc[(df.language != 'ENGLISH') & 
       (df.language != 'SPANISH') & 
       (df.language != 'CHINESE') &
       (df.language != 'RUSSIAN') &
       (df.language != 'VIETNAMESE') &
       (df.language != 'TAGALOG'),'language']='OTHERS'
df['language'].value_counts()

# finclass (insurance)
# categorize into 5 classes: medicare, medi-cal, commercial, other, HSF/None
df['finclass'].str.strip()

# medicare 
df.loc[(df.finclass == 'MEDICARE [1]') | 
       (df.finclass == 'MEDICARE MANAGED CARE HMO [Z]') |
       (df.finclass == 'PSYCH. MEDICARE [D]') |
       (df.finclass == 'INPT MEDICARE WITH MEDI-CAL [N]') |
       (df.finclass == 'MEDICARE BAD DEBT [8]'),'finclass'] = 'MEDICARE'

# medi-cal 
df.loc[(df.finclass == 'CHN CAPITATED PLANS [A]') | 
       (df.finclass == 'MEDI-CAL [2]') |
       (df.finclass == 'MEDI-CAL MANAGED CARE [X]') |
       (df.finclass == 'PSYCH. MEDI-CAL SHORT-DOYLE [E]'),'finclass'] = 'MEDI-CAL'

# commercial
df.loc[(df.finclass == 'COMMERCIAL NON-HMO OR PPO [5]') | 
       (df.finclass == 'COMMERCIAL MANAGED CARE HMO [Y]') |
       (df.finclass == "WORKER'S COMP. (CCSF ONLY) [W]") |
       (df.finclass == 'PSYCH - COMMERCIAL [S]') |
       (df.finclass == 'PSYCH MEDI-CAL PENDING [P]'),'finclass'] = 'COMMERCIAL'

# other 
df.loc[(df.finclass == 'SFHN CONTRACTS CAP NON MEDI-CAL [H]') | 
       (df.finclass == 'LIHP / SF PATH [M]') |
       (df.finclass == 'OTHER GOVT. [B]') |
       (df.finclass == 'SP. ACCTS. - HLTH.CTR.&SATEL. (No Pymts)(OuOpt Only) (Post Inpt to Outpt) [K]') |
       (df.finclass == 'Ward 18 [L]') |
       (df.finclass == 'PSYCH SHORT DOYLE [7]') |
       (df.finclass == 'SP ACCT, Health Center and Satellites [J]'), 'finclass'] = 'OTHER'

# HSF 
df.loc[(df.finclass == 'HEALTHY SAN FRANCISCO W/O HCCI [U]') |
       (df.finclass == 'PATIENT PAY [4]') | 
       (df.finclass == 'CMAP [C]') |
       (df.finclass == 'JAIL [6]') |
       (df.finclass == 'SP ACCTS, RESEARCH [G]') |
       (df.finclass == 'SPECIAL PACKAGE PROGRAM [9]') |
       (df.finclass == 'PSYCH - JAIL [T]') |
       (df.finclass == 'PSYCH - PATIENT PAY [R]') |
       (df.finclass == 'MEDI-CAL PENDING [3]'), 'finclass'] = 'HEALTHY SF'

# drop the unnecessary columns: SSN, hispanic, city, state 
df = df.drop(columns=['ssn', 'hispanic', 'city', 'state'])


# identify the date CKD was first diagnosed
df = pd.read_csv(r"M:\UCSF_ARS\michael_thesis\cleaned_data\demo.csv")
eGFR = pd.read_csv(r"M:\UCSF_ARS\michael_thesis\cleaned_data\eGFR.csv")
ACR = pd.read_csv(r"M:\UCSF_ARS\michael_thesis\cleaned_data\ACR.csv")
PCR = pd.read_csv(r"M:\UCSF_ARS\michael_thesis\cleaned_data\PCR.csv")
dip = pd.read_csv(r"M:\UCSF_ARS\michael_thesis\cleaned_data\urine_protein.csv")

#process the lab files
eGFR['OBSV_DATE'] = pd.to_datetime(eGFR.OBSV_DATE)
ACR['OBSV_DATE'] = pd.to_datetime(ACR.OBSV_DATE)
PCR['OBSV_DATE'] = pd.to_datetime(PCR.OBSV_DATE)
dip['OBSV_DATE'] = pd.to_datetime(dip.OBSV_DATE)

eGFR = eGFR.drop(eGFR[eGFR['CKD_flag'] == False].index)
ACR = ACR.drop(ACR[ACR['CKD_flag'] == False].index)
PCR = PCR.drop(PCR[PCR['CKD_flag'] == False].index)
dip = dip.drop(dip[dip['CKD_flag'] == False].index)

proteinuria = pd.concat([ACR, PCR, dip])

# CKD can be diagnosed by eGFR or urine protein
# as long as the criteria is met for one of them, CKD is diagnosed

# initialize CKD diagnosis date
df['CKD_date'] = np.nan

for i in range(len(df)):
    # get measurements for the pt
    eGFR_temp = eGFR[eGFR['ActiveMRN'] == df['ActiveMRN'][i]]
    proteinuria_temp = proteinuria[proteinuria['ActiveMRN'] == df['ActiveMRN'][i]]
    
    eGFR_temp = eGFR_temp.sort_values(by='OBSV_DATE',ascending=True)
    proteinuria_temp = proteinuria_temp.sort_values(by='OBSV_DATE',ascending=True)
    
    eGFR_temp.index = np.arange(0,len(eGFR_temp))
    proteinuria_temp.index = np.arange(0,len(proteinuria_temp))

    # if abnormal values are observed 90 days apart for EITHER eGFR or proteinuria, CKD is determined
    # add CKD stages (G, A), eGFR trend, most recent eGFR, ACR, PCR, and dipstick

    # initialize ckd status
    ckd_status = False
    ckd_date = np.nan

    if len(eGFR_temp) > 1:
        for j in range(1, len(eGFR_temp)):
            diff = (eGFR_temp['OBSV_DATE'][j] - eGFR_temp['OBSV_DATE'][0]).days
            
            if diff >= 90:
                ckd_status = True
                ckd_date = eGFR_temp['OBSV_DATE'][j]
                break
    
    if len(proteinuria_temp) > 1:
        for k in range(1, len(proteinuria_temp)):
            diff = (proteinuria_temp['OBSV_DATE'][k] - proteinuria_temp['OBSV_DATE'][0]).days
            if diff >= 90:
                if ckd_status == True: # if already diagnosed by eGFR
                    ckd_date = min(ckd_date, proteinuria_temp['OBSV_DATE'][k])
                break
    
    
    if ckd_date:
        df.loc[i, 'CKD_date'] = ckd_date
        
# drop those who were never diagnosed with CKD
df_new = df[df['CKD_date'].isnull() == False]
df_new.index = np.arange(0,len(df_new))

# export csv
new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_new.to_csv(os.path.join(new_path, r'demo_ckd.csv'))



