### Blood Pressure

#### eCW

# eCW BP data
file_path_ecw = r"M:\UCSF_ARS\RITM0152990\Data\Vitals\eCW\BloodPressure.csv"
df = pd.read_csv(file_path_ecw)

df['ResultValue'].isnull().sum()
# get rid of the 2 NAs
df = df.dropna(subset=['ResultValue'])

# get rid of values without the slash (195)
noslash = df[~df['ResultValue'].str.contains('/', regex=False)]
len(noslash)
# drop values with no '/'
df = df[df['ResultValue'].str.contains('/', regex=False)]
df.index = np.arange(0,len(df))

# IF THERE IS TIME!
# from the noslash df, we want the space (120 80), backward slash (120\80),
# no space (12080), dash (120-80), just sys (sys: 120)

# cleaning the ones with slash

df['Processed'] = df['ResultValue'].str.findall( '\d{1,3}\/\d{1,3}')
df['Processed_Sys'] = df['ResultValue'].str.findall( '\d{1,3}\/')
df['Processed_Dia'] = df['ResultValue'].str.findall( '/\d{1,3}')
df['len'] = df['Processed'].str.len()

df[df['len'] >1].head()

# calculate the average Sys and Dia when there are multiple measurements
df['Sys_BP'] = np.nan
df['Dia_BP'] = np.nan
for p in range(len(df)):
    
    sys = df['Processed_Sys'][p]
    dia = df['Processed_Dia'][p]
    s2 = 0
    d2 = 0
    
    if len(sys) > 0:
        for i in range(len(sys)):
            # sys
            s1 = sys[i][:-1]
            s2 += int(s1)
        df['Sys_BP'][p] = s2 / len(sys)
        
    if len(dia) > 0:
        for j in range(len(dia)):
        # dia
            d1 = dia[j][1:]
            d2 += int(d1)
        
        df['Dia_BP'][p] = d2 / len(dia)

df_sys = df[df['Sys_BP'].isna() == False]
df_sys = df_sys[['ActiveMRN', 'EncounterDate', 'Sys_BP']]
df_sys = df_sys.rename(columns={"Sys_BP": "OBSV_RSLT_NO_VAL", "EncounterDate": "OBSV_DATE"})

df_dia = df[df['Dia_BP'].isna() == False]
df_dia = df_dia[['ActiveMRN', 'EncounterDate', 'Dia_BP']]
df_dia = df_dia.rename(columns={"Dia_BP": "OBSV_RSLT_NO_VAL", "EncounterDate": "OBSV_DATE"})

print(len(df))
print(len(df_sys))
print(len(df_dia))

# export as csv
new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_sys.to_csv(os.path.join(new_path,r'vit_sys.csv'))
df_dia.to_csv(os.path.join(new_path,r'vit_dia.csv'))
