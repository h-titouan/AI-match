import base64
from Nettoyage_donnees import model_ready, dataG
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Afficher les images
def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()

    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

data = model_ready
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

