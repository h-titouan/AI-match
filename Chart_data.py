import pandas as pd
from Nettoyage_donnees import model_ready

data = model_ready

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


# Mean of each variable for each condition
dict = {"int_corr": [0.315267, 0.299630],
            "sinc_o": [0.847308, 0.650555],
            "diff_age": [3.178344, 3.799305],
            "diff_date": [1.661765, 1.601048],
            "diff_go_out": [0.902752, 1.120491],
            "attr_o": [0.726390, 0.404404],
            "diff_intel": [6.794465, 6.774984],
            "fun_o": [0.555163, 0.246688],
            "diff_sinc": [6.658629, 7.107700],
            "diff_shar": [6.802592, 6.642148],
            "diff_amb": [6.946236, 7.043938],
            "diff_attr": [13.346743, 12.326343],
            "diff_fun": [6.391057, 6.217810],
            "intel_o": [0.667255, 0.452023]
            }

dataG = pd.DataFrame(dict)
