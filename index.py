import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps import app1, app2
from app import app

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

layout = html.Div(
    style={"textAlign":"justify"},
    children=[
    dcc.Markdown('''
        # Analyse des données

        ## Contexte

        ihoih iuoh iuojio joijiu gtuy hio jop kopjoygiu hjpotdrdrtyfj

    ''')
    ], className='container')


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return layout

if __name__ == '__main__':
    app.run_server(debug=True)
