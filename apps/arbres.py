import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import pandas as pd
import re
import plotly.express as px
import plotly.graph_objects as go
pd.options.display.max_rows = 300

df = pd.read_csv("apps/arbres/les-arbres.csv",sep=";")
df['longitude'] = df.geo_point_2d.apply(lambda x: str(x).split(",")[1])
df['latitude'] = df.geo_point_2d.apply(lambda x: str(x).split(",")[0])
df.latitude = df.latitude.astype(float)
df.longitude = df.longitude.astype(float)
df = df[df['ARRONDISSEMENT'].str.contains('PARIS')]
df_rem = pd.read_excel('apps/arbres/base-cc-filosofi-2015.xls',header=4,dtype=str)
df_rem = df_rem[df_rem['Code géographique'].str[:2] == '75']
df_rem = df_rem[['Code géographique','Libellé géographique','Médiane du niveau vie (€)']]
df_rem = df_rem.rename(columns={'Code géographique':'INSEE','Médiane du niveau vie (€)': 'NIVEAU_DE_VIE'})
df_rem['ARRONDISSEMENT'] = df_rem['Libellé géographique'].apply(lambda x: re.sub("\D", "", x))
df_rem['ARRONDISSEMENT'] = df_rem['ARRONDISSEMENT'].apply(lambda x: 'PARIS '+x+'E ARRDT')
df_rem['ARRONDISSEMENT'] = df_rem['ARRONDISSEMENT'].apply(lambda x: x.replace(' 1E ARRDT',' 1ER ARRDT'))
df_rem = df_rem[['INSEE','ARRONDISSEMENT','NIVEAU_DE_VIE']]
df_pop = pd.read_csv('apps/arbres/Communes.csv',sep=";")
df_pop = df_pop[df_pop['DEPCOM'].str[:2] == '75']
df_pop = df_pop[['COM','PMUN']]
df_pop['ARRONDISSEMENT'] = df_pop['COM'].apply(lambda x: re.sub("\D", "", x))
df_pop['ARRONDISSEMENT'] = df_pop['ARRONDISSEMENT'].apply(lambda x: 'PARIS '+x+'E ARRDT')
df_pop['ARRONDISSEMENT'] = df_pop['ARRONDISSEMENT'].apply(lambda x: x.replace(' 1E ARRDT',' 1ER ARRDT'))
df_pop = df_pop[['ARRONDISSEMENT','PMUN']]
df_sup = pd.read_csv("apps/arbres/correspondance-code-insee-code-postal.csv",sep=";")
df_sup = df_sup[df_sup['Code INSEE'].str[:2] == '75']
df_sup = df_sup[['Commune','Superficie']]
df_sup['ARRONDISSEMENT'] = df_sup['Commune'].apply(lambda x: re.sub("\D", "", x))
df_sup['ARRONDISSEMENT'] = df_sup['ARRONDISSEMENT'].apply(lambda x: 'PARIS '+x+'E ARRDT')
df_sup['ARRONDISSEMENT'] = df_sup['ARRONDISSEMENT'].apply(lambda x: x.replace(' 1E ARRDT',' 1ER ARRDT'))
df_sup['ARRONDISSEMENT'] = df_sup['ARRONDISSEMENT'].apply(lambda x: x.replace(' 751',' 1ER ARRDT'))
df_sup = df_sup[['ARRONDISSEMENT','Superficie']]
df_arr = df.groupby(['ARRONDISSEMENT'],as_index=False)[['IDBASE']].count()
df_arr = pd.merge(df_arr,df_sup,on='ARRONDISSEMENT',how='left')
df_arr = pd.merge(df_arr,df_pop,on='ARRONDISSEMENT',how='left')
df_arr = pd.merge(df_arr,df_rem,on='ARRONDISSEMENT',how='left')
df_arr['ARRONDISSEMENT'] = df_arr['INSEE'] + ' - ' + df_arr['ARRONDISSEMENT']
df_arr['ARBRE_PAR_HA'] = df_arr['IDBASE'] / df_arr['Superficie']
df_arr = df_arr.sort_values(by=['ARRONDISSEMENT']).reset_index()

fig1 = px.pie(df, values='IDBASE', names='DOMANIALITE')

from app import app

layout = html.Div(
    children=[
    html.Div([
        html.P("Les arbres parisiens")
    ], style={'textAlign': 'center', 'margin':'auto','fontSize':'60px'}),
    html.Br(),
    dcc.Markdown('''

        ### Présentation du jeu de données

        Le jeu de données que j'ai décidé d'explorer aujourd'hui est un jeu de données mis à disposition par la Ville de Paris sur la plateforme [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/les-arbres-paris/). Il s'agit de la liste des arbres parisiens. Pour chacun d'entre eux, un certain nombre de propriétés y sont associés (emplacement dans la ville, dimensions, arbres remarquables...). Les arbres sont également localisés géographiquement. 

        Alors, premier réflexe, on va simplement afficher les données. Le jeu de données est disponible au format csv, on peut donc le visualiser assez facilement sans traitement :

    '''),

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.head(20).to_dict('records'),
        style_table={
            'overflowY': 'scroll',
            'overflowX': 'scroll',
        }
    ),

    dcc.Markdown('''

        ### Généralités

        On peut d'abord se demander combien d'arbres au total sont plantés à Paris, avec le Jeu de données fournis, c'est assez facile de le déterminer : 

    '''),

    html.Div([
        html.P(str(df.shape[0])+" arbres")
    ], style={'textAlign': 'center', 'margin':'auto','fontSize':'60px'}),

    dcc.Graph(figure=fig1)

], style={'position':'relative','width':'100%','max-width':'600px','margin':'0 auto','padding':'0 20px','fontFamily':'Helvetica Neue,Helvetica,Arial,sans-serif','textAlign':'justify'})
