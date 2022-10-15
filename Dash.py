# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from Chart_data import m_ad
app = Dash(__name__)

#rearrangement du dataframe pour le plot

df = m_ad

#Creation du Barplot
fig = px.bar(df, x="diff_age", y="Taux_match", color="diff_age", barmode="relative")
fig.update_layout(showlegend=False)

#Mise en place du html
app.layout = html.Div(children=[
    html.H1(children='EasyDate Dashboard'),

    html.Div(children='''
        Number of matches by age difference
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    dcc.Graph(
        id='example-graph2',
        figure=fig
    )
], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'middle'})

if __name__ == '__main__':
    app.run_server(debug=True)