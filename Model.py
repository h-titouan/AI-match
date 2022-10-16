
# Importer les librairies
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score, confusion_matrix, classification_report
from sklearn.model_selection import learning_curve

# Ouvrir les données
data = pd.read_csv("model_ready.csv", sep = ";")

# Splitter avec X_train, X_test
X_train, X_test = train_test_split(data, test_size=0.20, random_state=0)

# Fonction de suppression des valeurs manquantes
def imputation(data):
    data = data.dropna(axis=0)
    return data

# Fonction de preprocessing sur les données
def preprocessing(data):
    data = imputation(data)

    X = data.drop("match", axis=1)
    y = data['match']

    print(y.value_counts(normalize=True))
    return X, y

X_train, y_train = prepocessing(X_train)

# Définition de l'instance SMOTE
sm = SMOTE(k_neighbors=3, sampling_strategy=0.80)

# Application du SMOTE aux données
X_train, y_train = sm.fit_resample(X_train, y_train)

# Preprocessing sur l'échantillon test
X_test, y_test = preprocessing(X_test)

# Modèle KNN Classifier
knn = KNeighborsClassifier(n_neighbors=1)

# Tester le modèle
knn.fit(X_train, y_train)

# Prédiction
y_pred = knn.predict(X_test)

# Fonction d'évaluation du modèle
def evaluation(model):
    model.fit(X_train, y_train)
    ypred = model.predict(X_test)

    print(pd.DataFrame(confusion_matrix(y_test, ypred),
                       columns=['pred_0', 'pred_1'],
                       index=['obs_0', 'obs_1']))
    print(classification_report(y_test, ypred))

    N, train_score, val_score = learning_curve(model, X_train, y_train,
                                               cv=5, scoring="f1", train_sizes=np.linspace(0.1, 1, 10))

    plt.figure(figsize=(8, 6))
    plt.plot(N, train_score.mean(axis=1), label="train score")
    plt.plot(N, val_score.mean(axis=1), label="validation score")
    plt.legend()

evaluation(KNN)

y_pred = model_final(KNN, X_test)

# Ouvrir les données submission
submission = pd.read_csv("submissions.csv", sep = ";", on_bad_lines='skip')
iid_pid = submission.iid_pid


def submission_process(data):
    data = data.replace(",", ".", regex=True)
    data = data.apply(pd.to_numeric, downcast="float", errors="coerce")

    # Gérer les outliers sur la catégorie gaming et reading
    data.loc[data["gaming"] > 10] = data.loc[data["gaming"] == 10]
    data.loc[data["reading"] > 10] = data.loc[data["reading"] == 10]

    iid = data[['iid', "goal", "date", "go_out", "sports", "tvsports", 'exercise', 'dining', 'museums', 'art', 'hiking',
                'gaming',
                'clubbing', 'reading', 'tv', 'theater', 'movies', 'concerts', 'music', 'shopping', 'yoga', "exphappy"]]
    iid = iid.drop_duplicates("iid")
    iid = iid.rename(columns={"iid": "pid"})
    data = data.merge(iid, on="pid", how="left")

    # Toutes les différences
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

    not_in_submission = ["partner", "idg", 'gender', 'condtn', "iid_pid", "iid", "id", "pid"]
    data = data.drop(columns=not_in_submission)
    data = data.fillna(data.mean())

    data["intel_o"] = [1 if el > 7.5 else 0 for el in data["intel_o"]]
    data["fun_o"] = [1 if el > 7.5 else 0 for el in data["fun_o"]]
    data["attr_o"] = [1 if el > 6.5 else 0 for el in data["attr_o"]]
    data["sinc_o"] = [1 if el > 6.5 else 0 for el in data["sinc_o"]]
    return data

submission = submission_process(submission)

model_var = ["int_corr", "diff_age", "diff_date", "diff_go_out", "sinc_o", "attr_o", "fun_o",
           "diff_intel", "diff_sinc", "diff_shar", "diff_amb", "diff_attr", "diff_fun", "intel_o"]

submission = submission[model_var]
pred = KNN.predict(submission)
dict = {"iid_pid" : iid_pid, "target" : pred}
prediction = pd.DataFrame(dict)

prediction = prediction.astype(int)

prediction.target.value_counts(normalize=True)