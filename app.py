# visit http://127.0.0.1:8050/ in your web browser.

# Imports
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from Nettoyage_donnees import model_ready, dataG
from dash.dependencies import Input, Output
import Dash_functions as dashF
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# Usefull datasets
data = model_ready
dataG = dataG
radar_cols = list(dataG.columns)
bar_cols = list(data.columns)

# Image directory
EasyDate = 'Images/EasyDate.png'
AI_match = 'Images/AI_match.png'
validation = 'Images/validation.PNG'

#Mise en place du html
# ------------------------------------------------------------------------------
# App layout
app.layout = dbc.Container([
    html.Div([


    # Show images
    html.Img(src=dashF.b64_image(EasyDate),style={'width':"20%"}),
    html.Img(src=dashF.b64_image(AI_match),style={'width':"10%"}),

    # Create Multipage on App
    dcc.Tabs([
        # Start Page 1
        dcc.Tab(label='Analyses exploratoires', children=[

    # Columns Selector
    html.Div([

        html.Label(['Choisissez une variable :'],
        style={'font-weight': 'bold', "text-align": "center"}),

        dcc.Dropdown(id='select_cols',
                     options=[
                         {'label': "Sincérité partenaire", 'value': bar_cols[0]},
                         {'label': "Attirance partenaire", 'value': bar_cols[1]},
                         {'label': "Fun partenaire", 'value': bar_cols[2]},
                         {'label': "Intelligence partenaire", 'value': bar_cols[3]},
                         {'label': "Différence d'âge", 'value': bar_cols[4]},
                         {'label': "Différence date", 'value': bar_cols[5]},
                         {'label': "Différence sortie", 'value': bar_cols[6]},
                         {'label': "Coefficient de match", 'value': bar_cols[13]},
                     ],
            optionHeight=35,
            value= bar_cols[13],               #dropdown value selected automatically when page loads
            multi=False,                        #allow multiple dropdown values to be selected
            style={'width':"50%"},                #use dictionary to define CSS styles of your dropdown
            ),
    ]),

    # Barplot
    html.Div([
        dcc.Graph(id='barplot')], style = {"width" : '100%'}),

            dbc.Row([
                dbc.Col([
                    # Pie Select Col Div
                    html.Div([

                        html.Label(['Choisissez une colonne :'],
                                   style={'font-weight': 'bold', "text-align": "center"}),

                        dcc.Dropdown(id='select_pie_col',
                                     options=[
                                         {'label': "Sincérité partenaire", 'value': bar_cols[0]},
                                         {'label': "Attirance partenaire", 'value': bar_cols[1]},
                                         {'label': "Fun partenaire", 'value': bar_cols[2]},
                                         {'label': "Intelligence partenaire", 'value': bar_cols[3]},
                                         {'label': "Différence d'âge", 'value': bar_cols[4]},
                                         {'label': "Différence date", 'value': bar_cols[5]},
                                         {'label': "Différence sortie", 'value': bar_cols[6]},
                                     ],
                                     optionHeight=35,
                                     value=bar_cols[0],  # dropdown value selected automatically when page loads
                                     multi=False,  # allow multiple dropdown values to be selected
                                     style={'width': "50%"},  # use dictionary to define CSS styles of your dropdown
                                     ),
                    ]),
                    # Pie div
                    html.Div([
                        dcc.Graph(id='pie'),
                    ], style={"width": '100%'}),

                ], width=6),

                    dbc.Col([

                        # Graph du radar
                        dcc.Graph(id='radar', className="radar",
                                  style={'float': 'left', 'margin': 'auto'}),
                        # Radar
                        # Checklist du radar
                        html.Div([

                            dcc.Dropdown(id="checklist", className="radar",
                                         options=radar_cols,
                                         value=radar_cols,
                                         multi=True,
                                         style={'width': "100%"},
                                         # use dictionary to define CSS styles of your dropdown
                                         ),
                        ]),

                    ], width=6),

            ]),

        # Close Page 1
        ]),
        # Start Page 2
        dcc.Tab(label='Analyses du Modèle', children=[
            html.Div([
                dbc.Row([

                    dbc.Col([

                    dcc.Graph(id='conf_matrix',figure = dashF.conf_matrix(), style = {"width": '100%'}),

                ], width=6),

                dbc.Col([

                    html.H5(children = "Prédiction sur les données train et test"),
                    html.Img(src=dashF.b64_image(validation),  style = {"width": '100%'}),

                ], width=6),

                ]),
            ])
        # Close Page 2
        ])
    # Close Tabs
    ])
])

# Dbc Container
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
    fig = px.bar(df, x=column_chosen, y="Taux de match", color_discrete_sequence= ["#E0115F"], title="Exploration des données explicatives")

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

# Pie Callback
@app.callback(
    Output(component_id='pie', component_property='figure'),
    Input(component_id='select_pie_col', component_property='value')
    )

# Pie reactive function
def build_pie(column_chosen):
    df = dashF.interactive_pie(column_chosen)
    fig = px.pie(df, values='Taux de match', names=column_chosen, title = "Différence de match par variable")
    return fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)