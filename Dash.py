# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from Nettoyage_donnees import model_ready
from dash.dependencies import Input, Output
import Dash_functions as dashF
import seaborn as sns

app = Dash(__name__)

#rearrangement du dataframe pour le plot
data = model_ready
colonnes = list(data.columns)

# Emplacement des images
EasyDate = 'C:/Users/houde/PycharmProjects/pythonProject2/Easy Date/EasyDate.png'
AI_match = 'C:/Users/houde/PycharmProjects/pythonProject2/Easy Date/AI_match.png'

#Mise en place du html
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.Img(src=dashF.b64_image(EasyDate),style={'width':"20%"}),
    html.Img(src=dashF.b64_image(AI_match),style={'width':"10%"}),

html.Div([

        html.Br(),

        html.Label(['Choisissez une variable :'],
        style={'font-weight': 'bold', "text-align": "center"}),

        dcc.Dropdown(id='select_cols',
            options = colonnes,
            #options=[{'label': "Différence d'âge", 'value': colonnes[0]}],
            optionHeight=35,
            value= colonnes[0],               #dropdown value selected automatically when page loads
            multi=False,                        #allow multiple dropdown values to be selected
            style={'width':"30%"},             #use dictionary to define CSS styles of your dropdown

            ),
    ],className='three columns'),

    html.Div([
        dcc.Graph(id='our_graph')        ], style = {"width" : '70%'}),

    ])

#---------------------------------------------------------------
# Connecting the Dropdown values to the graph
@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='select_cols', component_property='value')])

def build_graph(column_chosen):
    df = dashF.interactive_bar(column_chosen)
    fig = px.bar(df, x=column_chosen, y="Taux_match", color_discrete_sequence= ["#E0115F"])
    return fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)