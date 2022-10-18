# visit http://127.0.0.1:8050/ in your web browser.

# Imports
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from Chart_data import dataG
from Nettoyage_donnees import model_ready
from dash.dependencies import Input, Output
import Dash_functions as dashF
import plotly.graph_objects as go

app = Dash(__name__)

# Usefull datasets
data = model_ready
dataG = dataG
colonnes = list(dataG.columns)

# Image directory
EasyDate = 'EasyDate.png'
AI_match = 'AI_match.png'

#Mise en place du html
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    # Show images
    html.Img(src=dashF.b64_image(EasyDate),style={'width':"20%"}),
    html.Img(src=dashF.b64_image(AI_match),style={'width':"10%"}),

    # Create Multipage on App
    dcc.Tabs([
        dcc.Tab(label='Page 1', children=[

    # Columns Selector
    html.Div([

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
    ]),

    # Barplot
    html.Div([
        dcc.Graph(id='barplot')], style = {"width" : '100%'}),

    # Radar
    html.Div([

        # Checklist du radar
        dcc.Checklist(id = "checklist", className="radar",
                options=colonnes,
                value=colonnes,
                labelStyle={'display': 'block'},
                style={'float': 'right','margin': 'auto'}
                      ),
        # Graphique du radar
        dcc.Graph(id='radar', className="radar",  style={'float': 'left','margin': 'auto'})], style ={"width" : "100%"})

        # Close Page 1
        ]),
        dcc.Tab(label='Page 2', children=[

        # Close Page 2
        ])
    # Close Tabs
    ])
])

#---------------------------------------------------------------
# Connecting the Dropdown values to the graph

# Barplot Callback
@app.callback(
    Output(component_id='barplot', component_property='figure'),
    Input(component_id='select_cols', component_property='value')
    )

# Barplot reactive function
def build_bar(column_chosen):
    df = dashF.interactive_bar(column_chosen)
    fig = px.bar(df, x=column_chosen, y="Taux_match", color_discrete_sequence= ["#E0115F"])
    return fig

# Radar Callback
@app.callback(
    Output(component_id='radar', component_property='figure'),
    Input(component_id='checklist', component_property='value')
     )

# Radar reactive function
def build_radar(cols):
    radar = dashF.radar_fig(cols)
    return radar

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)