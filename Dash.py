# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from Nettoyage_donnees import model_ready
from dash.dependencies import Input, Output
app = Dash(__name__)

#rearrangement du dataframe pour le plot

#rearrangement du dataframe pour le plot
data = model_ready
colonnes = list(data.columns)
#Mise en place du html
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.Div([
        dcc.Graph(id='our_graph')
    ],className='nine columns'),

    html.Div([

        html.Br(),
        html.Div(id='output_data'),
        html.Br(),

        html.Label(['Choose column:'],style={'font-weight': 'bold', "text-align": "center"}),

        dcc.Dropdown(id='select_cols',
            options = colonnes,
            #options=[{'label': "Différence d'âge", 'value': colonnes[0]}],
            optionHeight=35,                    #height/space between dropdown options
            value= colonnes[0],               #dropdown value selected automatically when page loads
            multi=False,                        #allow multiple dropdown values to be selected
            style={'width':"40%"},             #use dictionary to define CSS styles of your dropdown
            # className='select_box',           #activate separate CSS document in assets folder
            # persistence=True,                 #remembers dropdown value. Used with persistence_type
            # persistence_type='memory'         #remembers dropdown value selected until...
            ),                                  #'memory': browser tab is refreshed
                                                #'session': browser tab is closed
                                                #'local': browser cookies are deleted
    ],className='three columns'),

])

#---------------------------------------------------------------
# Connecting the Dropdown values to the graph
@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='select_cols', component_property='value')]
)

def build_graph(column_chosen):
    # df prenant la somme des matchs par différence d'âge
    df_m = data
    cols = [column_chosen, 'match']
    df_m = df_m[cols]
    df_m = df_m.loc[df_m["match"] == 1.0]
    df_m = df_m.groupby([column_chosen]).count()
    df_m = df_m.reset_index()

    df_u = data
    cols = [column_chosen, 'match']
    df_u = df_u[cols]
    df_u = df_u.loc[df_u["match"] == 0.0]
    df_u = df_u.groupby([column_chosen]).count()
    df_u = df_u.reset_index()
    df_u.columns = [column_chosen, 'unmatch']

    # Concaténation des différences d'âge plus grandes que 10

    m_ad = pd.merge(df_m, df_u, on=column_chosen, how="outer").fillna(value=0).reset_index(drop=True)
    m_ad["Taux_match"] = m_ad.match / (m_ad.match + m_ad.unmatch)
    df = m_ad
    fig = px.bar(df, x = column_chosen, y = "Taux_match", color=column_chosen, barmode="relative")

    return fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)