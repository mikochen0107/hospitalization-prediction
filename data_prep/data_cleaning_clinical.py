### Primary care provider (PCP)

df_pcp_ed = pd.read_csv(r"M:\UCSF_ARS\RITM0152990\Data\PCP\EDpatientEncPCP\mj_RITM0152990_Velasquez_EDPtEncPCP_20190423.csv")
df_pcp_in = pd.read_csv(r"M:\UCSF_ARS\RITM0152990\Data\PCP\InpatientEncPCP\mj_RITM0152990_Velasquez_InPtEncPCP_20190423.csv")
df_pcp_out = pd.read_csv(r"M:\UCSF_ARS\RITM0152990\Data\PCP\OutpatientEncPCP\mj_RITM0152990_Velasquez_OutPtEncPCP_20190423.csv")

df_pcp_ed = df_pcp_ed[['ActiveMRN', 'AdmitDate', 'PCP']]
df_pcp_in = df_pcp_in[['ActiveMRN', 'AdmitDate', 'PCP']]
df_pcp_out = df_pcp_out[['ActiveMRN', 'VisitDate', 'PCP']]

df_pcp_ed = df_pcp_ed.rename(columns={"AdmitDate": "OBSV_DATE"})
df_pcp_in = df_pcp_in.rename(columns={"AdmitDate": "OBSV_DATE"})
df_pcp_out = df_pcp_out.rename(columns={"VisitDate": "OBSV_DATE"})

df_pcp = pd.concat([df_pcp_ed, df_pcp_in, df_pcp_out])

df_pcp = df_pcp[df_pcp['PCP'].isna() == False]
df_pcp['pcp'] = 1

df_pcp.index = np.arange(0,len(df_pcp))

df_pcp

# export csv
new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_pcp.to_csv(os.path.join(new_path, r'pcp.csv'))

### Encounters

# encounters in the last period of time
# time since last encounter
df_in1 = pd.read_csv(r"M:\UCSF_ARS\RITM0152990\Data\Encounters\InpatientEnc\mj_RITM0152990_Velasquez_InPtEncDx_2002_2014.csv")
df_in2 = pd.read_csv(r"M:\UCSF_ARS\RITM0152990\Data\Encounters\InpatientEnc\mj_RITM0152990_Velasquez_InPtEncDx_2015_2018.csv")
df_in = pd.concat([df_in1, df_in2])

# just extract useful col: ActiveMRN, AdmitDate
# remove duplicates
df_in = df_in.drop_duplicates(subset=['ActiveMRN', 'AdmitDate'])
df_in = df_in.rename(columns={"AdmitDate": "OBSV_DATE"})
df_in = df_in[['ActiveMRN', 'OBSV_DATE']]

new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_in.to_csv(os.path.join(new_path, r'enc_inpt.csv'))

df_ed = pd.read_csv(r"M:\UCSF_ARS\RITM0152990\Data\Encounters\EDpatientEnc\mj_RITM0152990_Velasquez_EdPtEncDx_2002_2018.csv")

df_ed = df_ed.drop_duplicates(subset=['ActiveMRN', 'AdmitDate'])
df_ed = df_ed.rename(columns={"AdmitDate": "OBSV_DATE"})
df_ed = df_ed[['ActiveMRN', 'OBSV_DATE']]

new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_ed.to_csv(os.path.join(new_path, r'enc_ed.csv'))

path = r'M:\UCSF_ARS\RITM0152990\Data\Encounters\OutpatientEnc\csv format'
df_store = []
for file in os.listdir(path):
    df = pd.read_csv(os.path.join(path, file))
    df = df[['ActiveMRN', 'VisitDate', 'ICDCode', 'ICDType']]
    df_store.append(df)
df_out = pd.concat(df_store)

df_out = df_out.drop_duplicates(subset=['ActiveMRN', 'VisitDate'])
df_out = df_out.rename(columns={"VisitDate": "OBSV_DATE"})
df_out = df_out[['ActiveMRN', 'OBSV_DATE']]

new_path = r"M:\UCSF_ARS\michael_thesis\cleaned_data"
df_out.to_csv(os.path.join(new_path, r'enc_outpt.csv'))
