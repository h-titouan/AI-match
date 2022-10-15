import pandas as pd

data = pd.read_csv("data.csv")

data.diff_age = round(data.diff_age)

df = data[["diff_age","match"]]

#df prenant la somme des matchs par différence d'âge
df_m = df
df_m = df_m.loc[df_m["match"]==1.0]
df_m = df_m.groupby(['diff_age']).count()
df_m = df_m.reset_index()

#df prenant la somme des non-matchs par différence d'âge
df_u = df
df_u = df_u.loc[df_u["match"]==0.0]
df_u = df_u.groupby(['diff_age']).count()
df_u = df_u.reset_index()
df_u.columns = ['diff_age','unmatch']

#Concaténation des différences d'âge plus grandes que 10
m_ad = pd.merge(df_m,df_u,on='diff_age',how='outer').fillna(value = 0).sort_values(by = "diff_age").reset_index(drop=True)
m_ad["diff_age"] = m_ad["diff_age"].apply(int).apply(str)
m_ad["match"] = m_ad["match"].apply(int)
c10 = m_ad[-11:]
c10 = pd.DataFrame(c10.sum(axis=0)).T
c10['diff_age']= "10+"
m_ad.drop(m_ad.tail(11).index,inplace = True)
m_ad = pd.concat([m_ad,c10], ignore_index=True)
m_ad["Taux_match"]= m_ad.match/m_ad.unmatch


#Création d'une fonction pour importer le df sur le main
def match_diff_age(df = m_ad):
    return df
