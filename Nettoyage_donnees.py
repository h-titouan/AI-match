
# Importer les librairies
import pandas as pd
import numpy as np

data = pd.read_csv("train.csv", sep = ";")

# Fonction de nettoyage et de création des nouvelles variables
def exploratory_process(data):

# Remplacer les données avec virgule par des points
    data = data.replace(",", ".", regex=True)
    data = data.apply(pd.to_numeric, downcast="float", errors="coerce")

# Supprimer les colonnes > à 5% de données manquantes
    missing = (data.isnull().sum().sort_values(ascending=False) / data.shape[0]) * 100
# Garder les colonnes qui contiennent plus de 5% de valeurs manquantes
    missing = missing[missing > 5]
    missing = list(missing.index)
    data = data.drop(columns=missing)

# Gérer les outliers sur la catégorie gaming et reading
    data.loc[data["gaming"] > 10] = data.loc[data["gaming"] == 10]
    data.loc[data["reading"] > 10] = data.loc[data["reading"] == 10]

# Mettre les infos de la deuxième personne sur la même ligne que la rencontre
    iid = data[
    ['iid', "goal", "date", "go_out", "sports", "tvsports", 'exercise', 'dining', 'museums', 'art', 'hiking', 'gaming',
     'clubbing', 'reading', 'tv', 'theater', 'movies', 'concerts', 'music', 'shopping', 'yoga', "exphappy"]]
    iid = iid.drop_duplicates("iid")
    iid = iid.rename(columns={"iid": "pid"})
    data = data.merge(iid, on="pid", how="left")

# Créer toutes les variables de différences
    data["diff_attr"] = abs(data["attr1_1"] - data["pf_o_att"])
    data["diff_sinc"] = abs(data["sinc1_1"] - data["pf_o_sin"])
    data["diff_intel"] = abs(data["intel1_1"] - data["pf_o_int"])
    data["diff_fun"] = abs(data["fun1_1"] - data["pf_o_fun"])
    data["diff_amb"] = abs(data["amb1_1"] - data["pf_o_amb"])
    data["diff_shar"] = abs(data["shar1_1"] - data["pf_o_sha"])
    data["diff_age"] = abs(data["age"] - data["age_o"])
    data["int_corr"] = abs(data["int_corr"])

    data["diff_go_out"] = abs(data["go_out_x"] - data["go_out_y"])
    data["diff_date"] = abs(data["date_x"] - data["date_y"])
    data["diff_sports"] = abs(data["sports_x"] - data["sports_y"])
    data["diff_tvsports"] = abs(data["tvsports_x"] - data["tvsports_y"])
    data["diff_exercise"] = abs(data["exercise_x"] - data["exercise_y"])
    data["diff_dining"] = abs(data["dining_x"] - data["dining_y"])
    data["diff_museums"] = abs(data["museums_x"] - data["museums_y"])
    data["diff_art"] = abs(data["art_x"] - data["art_y"])
    data["diff_hiking"] = abs(data["hiking_x"] - data["hiking_y"])
    data["diff_gaming"] = abs(data["gaming_x"] - data["gaming_y"])
    data["diff_clubbing"] = abs(data["clubbing_x"] - data["clubbing_y"])
    data["diff_reading"] = abs(data["reading_x"] - data["reading_y"])
    data["diff_tv"] = abs(data["tv_x"] - data["tv_y"])
    data["diff_theater"] = abs(data["theater_x"] - data["theater_y"])
    data["diff_movies"] = abs(data["movies_x"] - data["movies_y"])
    data["diff_concerts"] = abs(data["concerts_x"] - data["concerts_y"])
    data["diff_music"] = abs(data["music_x"] - data["music_y"])
    data["diff_shopping"] = abs(data["shopping_x"] - data["shopping_y"])
    data["diff_yoga"] = abs(data["yoga_x"] - data["yoga_y"])
    data["diff_exphappy"] = abs(data["exphappy_x"] - data["exphappy_y"])

# Enlever les variables non présentes dans le prédicition ou inutiles
    not_in_submission = ["position", "round", "dec_o", "order", "wave", "partner",
                     "idg", 'gender', 'condtn', "iid_pid", "iid", "id", "pid"]
    data = data.drop(columns=not_in_submission)

# Recoder certaines variables
    data["intel_o"] = [1 if el > 7.5 else 0 for el in data["intel_o"]]
    data["fun_o"] = [1 if el > 7.5 else 0 for el in data["fun_o"]]
    data["attr_o"] = [1 if el > 6.5 else 0 for el in data["attr_o"]]
    data["sinc_o"] = [1 if el > 6.5 else 0 for el in data["sinc_o"]]

    return data

data = exploratory_process(data)

match = ["match"]

# Nom des colonnes conservées pour le modèle

model_var = ["sinc_o", "attr_o", "fun_o", "intel_o", "diff_age", "diff_date", "diff_go_out",
           "diff_intel", "diff_sinc", "diff_shar", "diff_amb", "diff_attr", "diff_fun", "int_corr"]


#Dataframe nettoyé
model_ready = data[model_var + match]

dict = {"Sincérité partenaire": [0.847308, 0.650555],
        "Attirance partenaire": [0.726390, 0.404404],
        "Fun partenaire": [0.555163, 0.246688],
        "Intelligence partenaire": [0.667255, 0.452023],
        "Différence d'âge": [3.178344, 3.799305],
        "Différence date": [1.661765, 1.601048],
        "Différence sortie": [0.902752, 1.120491],
        "Différence d'intelligence": [6.794465, 6.774984],
        "Différence sincérité": [6.658629, 7.107700],
        "Différence centre intérêts": [6.802592, 6.642148],
        "Différence ambition": [6.946236, 7.043938],
        "Différence attirance": [13.346743, 12.326343],
        "Différence fun": [6.391057, 6.217810],
        "Coefficient de match": [0.315267, 0.299630]
        }

dataG = pd.DataFrame(dict)
