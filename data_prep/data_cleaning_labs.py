### Chem lab

file_path = r"M:\UCSF_ARS\RITM0152990\Data\Labs\Chem_Lab.csv"
df = pd.read_csv(file_path)

# create a new dataframe for each type of chem lab, remove the spaces in the name, and export as csv
new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"

for t in df.TRM_NAME.unique():
    new_df = df[df['TRM_NAME'] == t]
    new_df.index = np.arange(0,len(new_df))
    cleaned_name = t.replace(' ', '')
    new_df.to_csv(os.path.join(new_path,r'chem_lab_{}.csv'.format(cleaned_name)))

# calculate eGFR with CKD-Epi equation
# based on https://www.mdcalc.com/ckd-epi-equations-glomerular-filtration-rate-gfr#evidence

# requires sex, age, race from demographics
# requires serum creatinine

df_demo = pd.read_csv(r"M:\UCSF_ARS\michael_thesis\cleaned_data\demo.csv")
df_scre = pd.read_csv(r"M:\UCSF_ARS\michael_thesis\cleaned_data\chem_lab_Creatinine(CR).csv")

df_scre = df_scre.drop(columns=['Unnamed: 0', 'OBSV_PT_HASH_NO', 'OBSV_TRM_NO', 'TRM_NAME'])
df_demo = df_demo.drop(columns=['Unnamed: 0'])

df_scre = pd.merge(df_scre, df_demo, on=['ActiveMRN'])
df_scre = df_scre.drop(columns=['DOD', 'language', 'homeless', 'finclass', 'zip'])

df_scre.head()

df_scre['age'] = np.floor((pd.to_datetime(df_scre['OBSV_DATE']) - pd.to_datetime(df_scre['DOB'])) / np.timedelta64(1, 'Y'))

df_scre['black'] = np.where(df_scre['race'] == 'BLACK', 1, 0)

def epi_eGFR_female_smaller(scre, age, black):
    A = 144
    B = 0.7
    C = -0.329
    if black == 1:
        eGFR = A * ((scre/B)**C) * (0.993**age) * (1.159)
    else:
        eGFR = A * ((scre/B)**C) * (0.993**age)
    return(eGFR)
    
def epi_eGFR_female_bigger(scre, age, black):
    A = 144
    B = 0.7
    C = -1.209
    if black == 1:
        eGFR = A * ((scre/B)**C) * (0.993**age) * (1.159)
    else:
        eGFR = A * ((scre/B)**C) * (0.993**age) 
    return(eGFR)

def epi_eGFR_male_smaller(scre, age, black):
    A = 141
    B = 0.9
    C = -0.411
    if black == 1:
        eGFR = A * ((scre/B)**C) * (0.993**age) * (1.159)
    else:
        eGFR = A * ((scre/B)**C) * (0.993**age) 
    return(eGFR)

def epi_eGFR_male_bigger(scre, age, black):
    A = 141
    B = 0.9
    C = -1.209
    if black == 1:
        eGFR = A * ((scre/B)**C) * (0.993**age) * (1.159)
    else:
        eGFR = A * ((scre/B)**C) * (0.993**age) 
    return(eGFR)

conditions = [(df_scre['female'] == 1) & (df_scre['OBSV_RSLT_NO_VAL'] <= 0.7), 
              (df_scre['female'] == 1) & (df_scre['OBSV_RSLT_NO_VAL'] > 0.7),
              (df_scre['female'] == 0) & (df_scre['OBSV_RSLT_NO_VAL'] <= 0.9),
              (df_scre['female'] == 0) & (df_scre['OBSV_RSLT_NO_VAL'] > 0.9)]
choices = [df_scre.apply(lambda x: epi_eGFR_female_smaller(x.OBSV_RSLT_NO_VAL, x.age, x.black), axis=1),
           df_scre.apply(lambda x: epi_eGFR_female_bigger(x.OBSV_RSLT_NO_VAL, x.age, x.black), axis=1), 
           df_scre.apply(lambda x: epi_eGFR_male_smaller(x.OBSV_RSLT_NO_VAL, x.age, x.black), axis=1), 
           df_scre.apply(lambda x: epi_eGFR_male_bigger(x.OBSV_RSLT_NO_VAL, x.age, x.black), axis=1)]

df_scre['eGFR'] = np.select(conditions, choices, default=np.nan)

df_scre = df_scre.drop(columns=['OBSV_RSLT_NO_VAL', 'DOB', 'female', 'race', 'age', 'black'])

df_scre['G_stage'].value_counts()

conditions1 = [(df_scre['eGFR'] >= 90),
              (df_scre['eGFR'] >= 60) & (df_scre['eGFR'] < 90),
              (df_scre['eGFR'] >= 45) & (df_scre['eGFR'] < 60),
              (df_scre['eGFR'] >= 30) & (df_scre['eGFR'] < 45),
              (df_scre['eGFR'] < 30)]
values1 = ['G1', 'G2', 'G3a', 'G3b', 'G4-5']
df_scre['G_stage'] = np.select(conditions1, values1)

conditions2 = [(df_scre['eGFR'] >= 60), (df_scre['eGFR'] < 60)]
values2 = [False, True]
df_scre['CKD_flag'] = np.select(conditions2, values2)

df_scre = df_scre.rename({'eGFR': 'OBSV_RSLT_NO_VAL'}, axis=1)

new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_scre.to_csv(os.path.join(new_path, r'chem_lab_egfr.csv'))

### Urine lab

file_path = r"M:\UCSF_ARS\RITM0152990\Data\Labs\RITM152990_Chu_Urine_20191028_1500.csv"
df = pd.read_csv(file_path)

df.OBSV_TRM_NAME.value_counts()

# create a new dataframe for each type of chem lab, extract useful columns, and export as csv
new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"

for t in df.OBSV_TRM_NAME.unique():
    new_df = df[df['OBSV_TRM_NAME'] == t]
    cleaned_name = t.replace(' ', '')
    new_df.to_csv(os.path.join(new_path,r'urine_lab_{}.csv'.format(cleaned_name)))

# calculate ACR and PCR 

df_cre = pd.read_csv(r"M:\UCSF_ARS\michael_thesis\cleaned_data\urine_lab_CREATININE,URINE.csv")
df_alb = pd.read_csv(r"M:\UCSF_ARS\michael_thesis\cleaned_data\urine_lab_URINARYALBUMIN,QUANT.(LAB).csv")
df_pro = pd.read_csv(r"M:\UCSF_ARS\michael_thesis\cleaned_data\urine_lab_PROTEIN,URINE.csv")

df_cre = df_cre.drop(columns=['Unnamed: 0'])
df_alb = df_alb.drop(columns=['Unnamed: 0'])
df_pro = df_pro.drop(columns=['Unnamed: 0'])

df_cre = df_cre.rename({'OBSV_RSLT_NO_VAL': 'CREATININE,URINE'}, axis=1)
df_cre = df_cre.drop(columns=['OBSV_PT_HASH_NO', 'OBSV_TRM_NO', 'OBSV_TRM_NAME'])
df_cre = df_cre.drop_duplicates(subset=['ActiveMRN', 'OBSV_DATE', 'OBSV_TIME'], keep='first')

df_alb = df_alb.rename({'OBSV_RSLT_NO_VAL': 'ALBUMIN,URINE'}, axis=1)
df_alb = df_alb.drop(columns=['OBSV_PT_HASH_NO', 'OBSV_TRM_NO', 'OBSV_TRM_NAME'])
df_alb = df_alb.drop_duplicates(subset=['ActiveMRN', 'OBSV_DATE', 'OBSV_TIME'], keep='first')

df_pro = df_pro.rename({'OBSV_RSLT_NO_VAL': 'PROTEIN,URINE'}, axis=1)
df_pro = df_pro.drop(columns=['OBSV_PT_HASH_NO', 'OBSV_TRM_NO', 'OBSV_TRM_NAME'])
df_pro = df_pro.drop_duplicates(subset=['ActiveMRN', 'OBSV_DATE', 'OBSV_TIME'], keep='first')

# calculate ACR
df_acr = pd.merge(df_cre, df_alb, on=['ActiveMRN', 'OBSV_DATE', 'OBSV_TIME'])

# ACR is in mg/g, albumin: mg/L, creatinine mg/dL
# thus, (mg/L)/(mg/dL) = (mg/L)/(10mg/L) = (1000mg/L)/(10g/L) = 100*mg/g
df_acr['ACR'] = df_acr['ALBUMIN,URINE']*100/df_acr['CREATININE,URINE']

# cap it at 20000mg/g
df_acr.loc[df_acr['ACR'] >= 20000, 'ACR'] = 20000

conditions = [(df_acr['ACR'] >= 30), 
             (df_acr['ACR'] < 30)]
values = [True, False]
df_acr['CKD_flag'] = np.select(conditions, values)

conditions = [(df_acr['ACR'] > 300),
             (df_acr['ACR'] <= 300) & (df_acr['ACR'] >= 30),
             (df_acr['ACR'] < 30)]
values = ['A3', 'A2', 'A1']
df_acr['A_stage'] = np.select(conditions, values)

df_acr = df_acr.rename({'ACR': 'OBSV_RSLT_NO_VAL'}, axis=1)

df_acr = df_acr.drop(columns=['OBSV_TIME', 'CREATININE,URINE', 'ALBUMIN,URINE'])

new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_acr.to_csv(os.path.join(new_path, r'urine_lab_acr.csv'))

# calculate PCR
df_pcr = pd.merge(df_cre, df_pro, on=['ActiveMRN', 'OBSV_DATE', 'OBSV_TIME'])
# PCR is in mg/g, urine protein mg/dL , creatinine mg/dL
df_pcr['PCR'] = df_pcr['PROTEIN,URINE']*1000/df_pcr['CREATININE,URINE']

# cap it at 20g/g = 20000mg/g; anything above it is 20
df_pcr.loc[df_pcr['PCR'] >= 20000, 'PCR'] = 20000

conditions = [(df_pcr['PCR'] > 150), 
             (df_pcr['PCR'] <= 150)]
values = [True, False]
df_pcr['CKD_flag'] = np.select(conditions, values)

df_pcr = df_pcr.rename({'PCR': 'OBSV_RSLT_NO_VAL'}, axis=1)
df_pcr = df_pcr.drop(columns=['OBSV_TIME', 'CREATININE,URINE', 'PROTEIN,URINE'])


new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_pcr.to_csv(os.path.join(new_path, r'urine_lab_pcr.csv'))

### Urine protein

file_path = r"M:\UCSF_ARS\RITM0152990\Data\Labs\UrProtein.csv"
df = pd.read_csv(file_path)

# get rid of white spaces
df['TRM_NAME'] = df['TRM_NAME'].str.strip()
df['OBSV_RSLT_TEXT'] = df['OBSV_RSLT_TEXT'].str.strip()

# deal with UPRT
df1 = df[df['TRM_NAME'] == 'Urine Protein--UPRT']

# only taking the NEGATIVE, TRACE, 1+, 2+, 3+, 4+, discarding everything else
df1 = df1[(df1['OBSV_RSLT_TEXT'] == 'NEGATIVE')
          | (df1['OBSV_RSLT_TEXT'] == 'UA DIP NEGATIVE')
          | (df1['OBSV_RSLT_TEXT'] == 'DIP UA NEGATIVE')
          | (df1['OBSV_RSLT_TEXT'] == 'TRACE')
          | (df1['OBSV_RSLT_TEXT'] == '1+') 
          | (df1['OBSV_RSLT_TEXT'] == '2+')
          | (df1['OBSV_RSLT_TEXT'] == '3+')
          | (df1['OBSV_RSLT_TEXT'] == '4+')]

df1['OBSV_RSLT_TEXT'] = df1['OBSV_RSLT_TEXT'].replace(['UA DIP NEGATIVE', 'DIP UA NEGATIVE'], 
                                                      ['NEGATIVE', 'NEGATIVE'])

# deal with POCT
df2 = df[df['TRM_NAME'] == 'Ur Protein POCT']

# make the naming consistent with Ur Protein UPRT: Normal and Neg -> NEGATIVE; so on
df2['OBSV_RSLT_TEXT'] = df2['OBSV_RSLT_TEXT'].replace(['Normal', 'Neg', 'Trace', '+', '++', '+++'], 
                                                      ['NEGATIVE', 'NEGATIVE', 'TRACE', '1+', '2+', '3+'])

# merge UPRT and POCT
new_df = pd.concat([df1, df2])

# define CKD flag
conditions = [(new_df['OBSV_RSLT_TEXT'] == 'NEGATIVE'),
             new_df['OBSV_RSLT_TEXT'] == 'TRACE',
             new_df['OBSV_RSLT_TEXT'] == '1+',
             new_df['OBSV_RSLT_TEXT'] == '2+',
             new_df['OBSV_RSLT_TEXT'] == '3+',
             new_df['OBSV_RSLT_TEXT'] == '4+']
values = [False, False, True, True, True, True]
new_df['CKD_flag'] = np.select(conditions, values)

new_df = new_df.drop(columns=['TRM_SYS_NO', 'TRM_NAME'])

new_df = new_df.rename({'OBSV_RSLT_TEXT': 'OBSV_RSLT_NO_VAL'}, axis=1)

new_df['OBSV_DATE'] = pd.to_datetime(new_df.OBSV_DATE)

# export as csv
new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
new_df.to_csv(os.path.join(new_path, r'urine_lab_prot.csv'))

### Other labs

# colonoscopy
file_path = r"M:\UCSF_ARS\RITM0152990\Data\Labs\Colonoscopy.csv"
df = pd.read_csv(file_path)

df['other_lab_col'] = 1
df = df[['ActiveMRN', 'OBSV_DATE', 'other_lab_col']]

new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df.to_csv(os.path.join(new_path,r'other_lab_col.csv'))

# hemoglobin
file_path = r"M:\UCSF_ARS\RITM0152990\Data\Labs\Hemoglobin.csv"
df = pd.read_csv(file_path)

# no cleaning needed
new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df.to_csv(os.path.join(new_path,r'other_lab_hemo.csv'))



# occult blood
file_path = r"M:\UCSF_ARS\RITM0152990\Data\Labs\OccultBlood.csv"
df = pd.read_csv(file_path)

df['OBSV_RSLT_TEXT'] = df['OBSV_RSLT_TEXT'].str.strip()
df = df[(df['OBSV_RSLT_TEXT'] == 'POSITIVE')
       | (df['OBSV_RSLT_TEXT'] == 'NEGATIVE')]

df = df[df['OBSV_RSLT_TEXT'] == 'POSITIVE']

df['other_lab_fecal'] = 1

new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df.to_csv(os.path.join(new_path,r'other_lab_fecal.csv'))

# PTH Intact
file_path = r"M:\UCSF_ARS\RITM0152990\Data\Labs\PTHIntact.csv"
df = pd.read_csv(file_path, header=0, names = ['ActiveMRN', 'OBSV_DATE', 'OBSV_TRM_NO', 'TRM_NAME', 'OBSV_RSLT_NO_VAL_1', 'OBSV_RSLT_NO_VAL_2'])

df['TRM_NAME'] = df['TRM_NAME'].str.strip()

df1 = df[df['TRM_NAME']=='PTH']
df2 = df[df['TRM_NAME']=='PTH INTACT']

df1 = df1.drop(columns=['OBSV_RSLT_NO_VAL_1'])
df1 = df1.rename(columns={'OBSV_RSLT_NO_VAL_2': 'OBSV_RSLT_NO_VAL'})
df2 = df2.drop(columns=['OBSV_RSLT_NO_VAL_2'])
df2 = df2.rename(columns={'OBSV_RSLT_NO_VAL_1': 'OBSV_RSLT_NO_VAL'})

new_df = pd.concat([df1, df2])

new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
new_df.to_csv(os.path.join(new_path,r'other_lab_pth.csv'))

# Urine occult blood
file_path = r"M:\UCSF_ARS\RITM0152990\Data\Labs\UrOccultBlood.csv"
df = pd.read_csv(file_path)

df['OBSV_RSLT_TEXT'] = df['OBSV_RSLT_TEXT'].str.strip()

df = df[(df['OBSV_RSLT_TEXT'] == 'NEGATIVE')
        | (df['OBSV_RSLT_TEXT'] == 'Negative')
        | (df['OBSV_RSLT_TEXT'] == 'Neg')
        | (df['OBSV_RSLT_TEXT'] == 'UA DIP NEGATIVE')
        | (df['OBSV_RSLT_TEXT'] == 'DIP UA NEGATIVE')
        | (df['OBSV_RSLT_TEXT'] == 'TRACE')
        | (df['OBSV_RSLT_TEXT'] == 'Trace')
        | (df['OBSV_RSLT_TEXT'] == '1+')
        | (df['OBSV_RSLT_TEXT'] == '2+')
        | (df['OBSV_RSLT_TEXT'] == '3+')]
# make the naming consistent
df['OBSV_RSLT_TEXT'] = df['OBSV_RSLT_TEXT'].replace(['Negative', 'Neg', 'UA DIP NEGATIVE', 'DIP UA NEGATIVE', 'Trace'], 
                                                      ['NEGATIVE', 'NEGATIVE', 'NEGATIVE', 'NEGATIVE', 'TRACE'])

df['OBSV_DATE'] = pd.to_datetime(df.OBSV_DATE)
df = df.rename({'OBSV_RSLT_TEXT': 'OBSV_RSLT_NO_VAL'}, axis=1)
df = df[['ActiveMRN', 'OBSV_DATE', 'OBSV_RSLT_NO_VAL']]

new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df.to_csv(os.path.join(new_path,r'urine_lab_occult.csv'))

### Immunization 

file_path = r"M:\UCSF_ARS\RITM0152990\Data\Immunizations\mj_RITM0152990_Velasquez_Iz_20190507.csv"

#data = pd.ExcelFile(file_path)
df = pd.read_csv(file_path)

# types of vaccines and frequency of each of them
df['IZ_Name'].value_counts()

# combining the HepB vaccines into one variable, and the pneumococcal vaccines into one variable

# prevnar remains the same
df['iz_prevnar'] = (df['IZ_Name'] == 'PCV13-Pneumococcal (Prevnar13)').astype(int)

# pneumovax includes PPV23, PCV13, and pneumovax
df['iz_pneumovax'] = ((df['IZ_Name'] == 'PPV23-Pneumococcal (Pneumovax)') 
                      | (df['IZ_Name'] == 'pneumovax')).astype(int)

# hepB includes all other vaccines in this dataset, anything that starts with HepB
df['iz_hepb'] = ((df['IZ_Name'] == 'HepB, unspecified') 
                 | (df['IZ_Name'] == 'HepB (adult)')
                 | (df['IZ_Name'] == 'HepB-Hib (Comvax)')
                 | (df['IZ_Name'] == 'HepB (dialysis 40 mcg/ml) Recombivax')
                 | (df['IZ_Name'] == 'HepB (dialysis 20mcg/ml) Engerix')).astype(int)

df = df.rename({'IzDate': 'OBSV_DATE'}, axis=1)

df_prevnar = df[df['iz_prevnar'] == 1]
df_pneumovax = df[df['iz_pneumovax'] == 1]
df_hepb = df[df['iz_hepb'] == 1]

df_prevnar = df_prevnar[['ActiveMRN', 'OBSV_DATE', 'iz_prevnar']]
df_pneumovax = df_pneumovax[['ActiveMRN', 'OBSV_DATE', 'iz_pneumovax']]
df_hepb = df_hepb[['ActiveMRN', 'OBSV_DATE', 'iz_hepb']]


# drop duplicates
df_prevnar = df_prevnar.drop_duplicates(subset=['ActiveMRN', 'OBSV_DATE'], keep='last')
df_pneumovax = df_pneumovax.drop_duplicates(subset=['ActiveMRN', 'OBSV_DATE'], keep='last')
df_hepb = df_hepb.drop_duplicates(subset=['ActiveMRN', 'OBSV_DATE'], keep='last')


# Export dataframe as csv to the cleaned_data folder in michael_thesis
new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_prevnar.to_csv(os.path.join(new_path,r'iz_prevnar.csv'))
df_pneumovax.to_csv(os.path.join(new_path,r'iz_pneumovax.csv'))
df_hepb.to_csv(os.path.join(new_path,r'iz_hepb.csv'))
