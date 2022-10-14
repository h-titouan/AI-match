# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

#rearrangement du dataframe pour le plot

df = pd.read_csv("data.csv")
df.diff_age = round(df.diff_age)
df = df.loc[df["match"]==1.0,["diff_age","match"]]
df['Counts'] = df.groupby(['diff_age'])['match'].transform('count')
df= df.drop_duplicates()
df = df.reset_index(drop=True)
del df["match"]
df.columns = ['diff_age','match']

print("Hello world !")
print("LOl")

#Creation du Barplot
fig = px.bar(df, x="diff_age", y="match", color="diff_age", barmode="group")

#Mise en place du html
app.layout = html.Div(children=[
    html.H1(children='EasyDate Dashboard'),

    html.Div(children='''
        Number of matches by age difference
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)