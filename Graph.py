from pyexpat import model
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
from Chart_data import m_ad, dataG
from Nettoyage_donnees import model_ready
app = Dash(__name__)


df = m_ad
dataG = dataG

fig3 = px.pie(df, values='Taux_match', names='diff_age')
fig3.update_layout(showlegend=False)

categories = ["int_corr", "diff_age", "diff_date", "diff_go_out", "sinc_o", "attr_o", "fun_o", 
           "diff_intel", "diff_sinc", "diff_shar", "diff_amb", "diff_attr", "diff_fun", "intel_o"]

fig5 = go.Figure()
fig5.add_trace(go.Scatterpolar(
      r=[0.315267,3.178344,1.661765,0.902752,0.847308,0.726390,0.555163,6.794465,6.658629,6.802592,6.946236,13.346743,6.391057,0.667255],
      theta=categories,
      name='Match'
))
fig5.add_trace(go.Scatterpolar(
      r=[0.299630,3.799305,1.601048,1.120491,0.650555,0.404404,0.246688,6.774984,7.107700,6.642148,7.043938,12.326343,6.217810,0.452023],
      theta=categories,
      name='No Match'
))
#

fig5.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      )),
  showlegend=False
)
