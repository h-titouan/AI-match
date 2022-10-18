import base64
from Nettoyage_donnees import model_ready, dataG
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import confusion_matrix
import plotly.figure_factory as ff
from Model import y_pred, y_test

# Afficher les images
def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()

    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

data = model_ready

# Function for interactive barplot
def interactive_bar(column):

    df_m = data
    cols = [column, 'match']
    df_m = df_m[cols]
    df_m = df_m.loc[df_m["match"] == 1.0]
    df_m = df_m.groupby([column]).count()
    df_m = df_m.reset_index()

    df_u = data
    cols = [column, 'match']
    df_u = df_u[cols]
    df_u = df_u.loc[df_u["match"] == 0.0]
    df_u = df_u.groupby([column]).count()
    df_u = df_u.reset_index()
    df_u.columns = [column, 'unmatch']

    # Concaténation des différences d'âge plus grandes que 10

    m_ad = pd.merge(df_m, df_u, on=column, how="outer").fillna(value=0).reset_index(drop=True)
    m_ad["Taux_match"] = m_ad.match / (m_ad.match + m_ad.unmatch)
    df = m_ad

    return df

# Function for interactive radar plot
def radar_fig(colonnes):

    categories = list(colonnes)
    first = list(dataG[colonnes].iloc[0])
    second = list(dataG[colonnes].iloc[1])

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=first,
        theta=categories,
        name='Match'
    ))

    radar.add_trace(go.Scatterpolar(
        r=second,
        theta=categories,
        name='No Match'
    ))

    return radar

# Function for confusion matrix
def conf_matrix():
    z = confusion_matrix(y_test, y_pred)
    z = z.astype(int)
    print(z)
    x = ['pred_0', 'pred_1']
    y = ['obs_0', 'obs_1']
    z_text = [[str(y) for y in x] for x in z]
    print(z_text)
    fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale=[(0,"#FFC0CB"), (1,"hotpink")])
    return fig

conf_matrix()