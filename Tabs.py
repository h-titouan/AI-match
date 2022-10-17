# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from Nettoyage_donnees import model_ready
from dash.dependencies import Input, Output
import Dash_functions as dashF

app = Dash(__name__)

#rearrangement du dataframe pour le plot
data = model_ready
colonnes = list(data.columns)

# Emplacement des images
EasyDate = 'EasyDate.png'
AI_match = 'AI_match.png'

#Mise en place du html
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.Img(src=dashF.b64_image(EasyDate),style={'width':"20%"}),
    html.Img(src=dashF.b64_image(AI_match),style={'width':"10%"}),

html.Div([
        
        
    html.Div([
        
     dcc.Tabs([
        dcc.Tab(label='Tab one', children=[
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
            dcc.Graph(id='our_graph')        ], style = {"width" : '70%'}),
        dcc.Tab(label='Tab two', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [1, 4, 1],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [1, 2, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        ],),
    ])
    ]),
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