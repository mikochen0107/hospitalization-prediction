### Admission (inpt encounters)

df_adm1 = pd.read_csv(r"M:\UCSF_ARS\RITM0152990\Data\Encounters\InpatientEnc\mj_RITM0152990_Velasquez_InPtEncDx_2002_2014.csv")
df_adm2 = pd.read_csv(r"M:\UCSF_ARS\RITM0152990\Data\Encounters\InpatientEnc\mj_RITM0152990_Velasquez_InPtEncDx_2015_2018.csv")

# extract relevant data and drop duplicates
df_adm1 = df_adm1[['ActiveMRN', 'AdmitDate']]
df_adm1 = df_adm1.drop_duplicates(keep='last')
df_adm2 = df_adm2[['ActiveMRN', 'AdmitDate']]
df_adm2 = df_adm2.drop_duplicates(keep='last')

df_adm = pd.concat([df_adm1, df_adm2])

df_adm.index = np.arange(0,len(df_adm))
df_adm['admit'] = 1

# export csv
new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_adm.to_csv(os.path.join(new_path, r'admit.csv'))
