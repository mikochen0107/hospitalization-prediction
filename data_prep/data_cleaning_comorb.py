### Comorbidities

# import files
df_in1 = pd.read_csv(r"M:\UCSF_ARS\RITM0152990\Data\Encounters\InpatientEnc\mj_RITM0152990_Velasquez_InPtEncDx_2002_2014.csv")
df_in2 = pd.read_csv(r"M:\UCSF_ARS\RITM0152990\Data\Encounters\InpatientEnc\mj_RITM0152990_Velasquez_InPtEncDx_2015_2018.csv")

df_in = pd.concat([df_in1, df_in2])

df_ed = pd.read_csv(r"M:\UCSF_ARS\RITM0152990\Data\Encounters\EDpatientEnc\mj_RITM0152990_Velasquez_EdPtEncDx_2002_2018.csv")

path = r'M:\UCSF_ARS\RITM0152990\Data\Encounters\OutpatientEnc\csv format'
df_store = []
for file in os.listdir(path):
    df = pd.read_csv(os.path.join(path, file))
    df = df[['ActiveMRN', 'VisitDate', 'ICDCode', 'ICDType']]
    df_store.append(df)
df_out = pd.concat(df_store)

df_ed = df_ed[['ActiveMRN', 'AdmitDate', 'ICDCode', 'ICDType']]
df_in = df_in[['ActiveMRN', 'AdmitDate', 'ICDCode', 'ICDType']]

df_ed = df_ed.rename(columns={"Admitte": "OBSV_DATE"})
df_in = df_in.rename(columns={"AdmitDate": "OBSV_DATE"})
df_out = df_out.rename(columns={"VisitDate": "OBSV_DATE"})

df_all = pd.concat([df_in, df_ed, df_out])


# use ICD codes from inpt, outpt, and ED encounters to identify comorbidities
# congestive heart failure, asthma or COPD, diabetes, hypertension, coronary artery disease, dementia, chronic pain

# congestive heart failure ICD9 = 428.0, unspecified heart failure ICD10 = I50. 9
chf_conditions = (((df_all['ICDCode'] == '428.0') & (df_all['ICDType'] == 9)) | 
                  ((df_all['ICDCode'] == 'I50.9') & (df_all['ICDType'] == 10)))

# asthma ICD9 = 493, ICD10 = J45; COPD ICD9 = 496, ICD10 = J44.9
asthma_copd_conditions = (((df_all['ICDCode'].str.contains('493')) & (df_all['ICDType'] == 9)) | 
                          ((df_all['ICDCode'].str.contains('J45')) & (df_all['ICDType'] == 10)) |
                          ((df_all['ICDCode'].str.contains('496')) & (df_all['ICDType'] == 9)) |
                          ((df_all['ICDCode'].str.contains('J44.9')) & (df_all['ICDType'] == 10)))
                         
# T2D T1D ICD9 = 250, ICD10 = E11 ICD10 = E10
dm_conditions = (((df_all['ICDCode'].str.contains('250')) & (df_all['ICDType'] == 9)) | 
                 ((df_all['ICDCode'].str.contains('E11')) & (df_all['ICDType'] == 10)) |
                 ((df_all['ICDCode'].str.contains('E10')) & (df_all['ICDType'] == 10)))


# hypertension ICD9 = 401 - 405 , ICD10  = I10 - I16
hyp_conditions = (((df_all['ICDCode'].str.contains('401')) & (df_all['ICDType'] == 9)) | 
                  ((df_all['ICDCode'].str.contains('402')) & (df_all['ICDType'] == 9)) |
                  ((df_all['ICDCode'].str.contains('403')) & (df_all['ICDType'] == 9)) | 
                  ((df_all['ICDCode'].str.contains('404')) & (df_all['ICDType'] == 9)) |
                  ((df_all['ICDCode'].str.contains('405')) & (df_all['ICDType'] == 9)) |
                  ((df_all['ICDCode'].str.contains('I10')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('I11')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('I12')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('I13')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('I14')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('I15')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('I16')) & (df_all['ICDType'] == 10)))
                  
# coronary (ischemic) heart disease ICD9 = 410-414, ICD10 = I20 - 25
chd_conditions = (((df_all['ICDCode'].str.contains('410')) & (df_all['ICDType'] == 9)) | 
                  ((df_all['ICDCode'].str.contains('411')) & (df_all['ICDType'] == 9)) |
                  ((df_all['ICDCode'].str.contains('412')) & (df_all['ICDType'] == 9)) | 
                  ((df_all['ICDCode'].str.contains('413')) & (df_all['ICDType'] == 9)) |
                  ((df_all['ICDCode'].str.contains('414')) & (df_all['ICDType'] == 9)) |
                  ((df_all['ICDCode'].str.contains('I20')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('I21')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('I22')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('I23')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('I24')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('I25')) & (df_all['ICDType'] == 10)))

# dementia ICD9 = 290, ICD10 = F01 - F03
dem_conditions = (((df_all['ICDCode'].str.contains('290')) & (df_all['ICDType'] == 9)) | 
                  ((df_all['ICDCode'].str.contains('F01')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('F02')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('F03')) & (df_all['ICDType'] == 10)))

# chronic pain ICD9 = 338.2, ICD10 = 89.2
pain_conditions = (((df_all['ICDCode'].str.contains('338.2')) & (df_all['ICDType'] == 9)) | 
                   ((df_all['ICDCode'].str.contains('89.2')) & (df_all['ICDType'] == 10)))

# nondependent abuse of drugs (substance abuse disorder) ICD9 = 305, ICD10 = F10 - F19
sub_conditions = (((df_all['ICDCode'].str.contains('305')) & (df_all['ICDType'] == 9)) | 
                  ((df_all['ICDCode'].str.contains('F10')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('F11')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('F12')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('F13')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('F14')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('F15')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('F16')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('F17')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('F18')) & (df_all['ICDType'] == 10)) |
                  ((df_all['ICDCode'].str.contains('F19')) & (df_all['ICDType'] == 10)))

df_chf = df_all[chf_conditions]
df_ast = df_all[asthma_copd_conditions]
df_dm = df_all[dm_conditions]
df_hyp = df_all[hyp_conditions]
df_chd = df_all[chd_conditions]
df_dem = df_all[dem_conditions]
df_pain = df_all[pain_conditions]
df_sub = df_all[sub_conditions]

# export csv
new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_chf.to_csv(os.path.join(new_path, r'cm_chf.csv'))
df_ast.to_csv(os.path.join(new_path, r'cm_ast.csv'))
df_dm.to_csv(os.path.join(new_path, r'cm_dm.csv'))
df_hyp.to_csv(os.path.join(new_path, r'cm_hyp.csv'))
df_chd.to_csv(os.path.join(new_path, r'cm_chd.csv'))
df_dem.to_csv(os.path.join(new_path, r'cm_dem.csv'))
df_pain.to_csv(os.path.join(new_path, r'cm_pain.csv'))
df_sub.to_csv(os.path.join(new_path, r'cm_sub.csv'))
