import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps import app1, app2, arbres
from app import app

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout = html.Div(
    style={"textAlign":"justify"},
    children=[
        html.Div([
            html.P("Blog")
        ], style={'textAlign': 'center', 'margin':'auto','fontSize':'90px','marginTop':'10%'}),
        html.Div([
            html.P("Analyse de données")
        ], style={'textAlign': 'center', 'margin':'auto','fontSize':'100px'}),
        html.Br(),
        html.Div([
            html.P("Derniers billets :")
        ], style={'textAlign': 'center', 'margin':'auto','fontSize':'30px'}),
        html.Div([
            dcc.Link('Arbres urbains parisiens', href='/arbres')
        ], style={'textAlign': 'center', 'margin':'auto','fontSize':'30px'})
    ], className='container')


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/arbres':
        return arbres.layout
    else:
        return layout

if __name__ == '__main__':
    app.run_server(debug=True)
