## Thiago França 22300013
## Lucas Miralha 22300040
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

url_theme1 = dbc.themes.VAPOR ## cor do plano de fundo
url_theme2 = dbc.themes.FLATLY ## cor do plano de fundo

template_theme1 = 'vapor'
template_theme2 = 'flatly'

df = pd.read_csv('Seguranca_informacao.csv') ## Abre o arquivo
state_options = [{'label': x, 'value': x} for x in df['Ano'].unique()]
labels=[{'DOS','Web','Worm','Scan','Invasao'} for x in df['Ano'].unique()]
total_anos = df.copy(deep = True)
total_anos = total_anos.groupby(['Ano']).sum()
tipos = ['Worm','DOS','Invasao','Web','Scan','Fraude','Outros']

##LAYOUT PRINCIPAL DO DASHBOARD "Html"
app.layout = dbc.Container([
   
    ##Grafico de Linha
    dbc.Row([
        dbc.Col([
            ThemeSwitchAIO(aio_id = 'theme', themes = [url_theme2,url_theme1]),##cor do fundo
            html.H3('Mes x DOS'),
            dcc.Dropdown(
                id = 'Ano',
                value = [state['label'] for state in state_options[:10]],
                multi = True,
                options = state_options
            ),
            dcc.Dropdown(
                id = 'Tipo',
                value = 'DOS',
                multi = True,
                options = tipos
            )
        ])
    ]),
     dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'line_graph')
        ])
    ]),
    
    ##Grafico de Pizza
    dbc.Row([ 
        dbc.Col([ 
            dbc.Row([ 
                html.H3('Percentual de ataques'),
                dcc.Dropdown(
                    id = 'pizza',
                    options = state_options,
                    value = 2019,
                    multi = False,
                    clearable = False 
                ),
                dcc.Graph(id='pizza_pie'), 
            ]) 
        ]) 
    ]), 

    ##Graficos de Caixa
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                    id = 'Web',
                    value = state_options[0]['label'],
                    options = state_options
                    ), 
                
                dcc.Graph(id = 'box1')
                ]),
            ]),
        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                    id = 'DOS',
                    value = state_options[0]['label'],
                    options = state_options
                    ),
                dcc.Graph(id = 'box2')
                ])
            ]),
        ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                    id = 'Scan',
                    value = state_options[0]['label'],
                    options = state_options
                    ), 
                
                dcc.Graph(id = 'box3')
                ])
            ]),
        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                    id = 'Fraude',
                    value = state_options[0]['label'],
                    options = state_options
                    ),
                dcc.Graph(id = 'box4')
                ])
            ])
        ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                    id = 'Invasao',
                    value = state_options[0]['label'],
                    options = state_options
                    ), 
                
                dcc.Graph(id = 'box5')
                ])
            ]),
        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                    id = 'Worm',
                    value = state_options[0]['label'],
                    options = state_options
                    ),
                dcc.Graph(id = 'box6')
                ])
            ])
        ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                    id = 'Outros',
                    value = state_options[0]['label'],
                    options = state_options
                    ), 
                
                dcc.Graph(id = 'box7')
                ])
            ])
    ])
])

##Callbacks para a interacao e atualizacoo dos graficos

@app.callback(
    Output('line_graph', 'figure'),
    Input('Ano', 'value'),
    Input('Tipo', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def line(Ano, Tipo, toggle):
    templates = template_theme2 if toggle else template_theme1

    df_data = df.copy(deep = True)
    mask = df_data['Ano'].isin(Ano)

    fig = px.line(df_data[mask], x = 'Mes', y = Tipo, color = 'Ano', template=templates) #mexe em nos eixos do grafico principal

    return fig

@app.callback( 
    [Output('pizza_pie', 'figure')], 
    [Input('pizza', 'value')],
    [Input(ThemeSwitchAIO.ids.switch('theme'), 'value')]  
) 
def update_graphs(Anos, toggle): 
    templates = template_theme2 if toggle else template_theme1
    tipos = ['Worm','DOS','Invasao','Web','Scan','Fraude','Outros']
    ddff = total_anos.loc[:,tipos]
    dff = ddff.transpose()

    pie_fig = px.pie(dff, values=Anos, names=tipos) 
    pie_fig.update_layout(template=templates) 

    return [pie_fig]

@app.callback(
    Output('box1', 'figure'),
    Input('Web', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box1(Web, toggle):
    templates = template_theme2 if toggle else template_theme1

    df_data = df.copy(deep = True)
    data_jogador = df_data[df_data['Ano'].isin([Web])]

    fig = px.box(data_jogador, x = 'Web', template = templates, points='all', title=Web)

    return fig

@app.callback(
    Output('box2', 'figure'),
    Input('DOS', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box2(DOS, toggle):
    templates = template_theme2 if toggle else template_theme1

    df_data = df.copy(deep = True)
    data_DOS = df_data[df_data['Ano'].isin([DOS])]

    fig = px.box(data_DOS, x = 'DOS', template = templates, points='all', title=DOS)

    return fig

@app.callback(
    Output('box3', 'figure'),
    Input('Scan', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box3(Scan, toggle):
    templates = template_theme2 if toggle else template_theme1

    df_data = df.copy(deep = True)
    data_jogador = df_data[df_data['Ano'].isin([Scan])]

    fig = px.box(data_jogador, x = 'Scan', template = templates, points='all', title=Scan)

    return fig

@app.callback(
    Output('box4', 'figure'),
    Input('Fraude', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box4(Fraude, toggle):
    templates = template_theme2 if toggle else template_theme1

    df_data = df.copy(deep = True)
    data_jogador = df_data[df_data['Ano'].isin([Fraude])]

    fig = px.box(data_jogador, x = 'Fraude', template = templates, points='all', title=Fraude)

    return fig

@app.callback(
    Output('box5', 'figure'),
    Input('Invasao', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box5(Invasao, toggle):
    templates = template_theme2 if toggle else template_theme1

    df_data = df.copy(deep = True)
    data_jogador = df_data[df_data['Ano'].isin([Invasao])]

    fig = px.box(data_jogador, x = 'Invasao', template = templates, points='all', title=Invasao)

    return fig

@app.callback(
    Output('box6', 'figure'),
    Input('Worm', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box6(Worm, toggle):
    templates = template_theme2 if toggle else template_theme1

    df_data = df.copy(deep = True)
    data_jogador = df_data[df_data['Ano'].isin([Worm])]

    fig = px.box(data_jogador, x = 'Worm', template = templates, points='all', title=Worm)

    return fig

@app.callback(
    Output('box7', 'figure'),
    Input('Outros', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def box7(Outros, toggle):
    templates = template_theme2 if toggle else template_theme1

    df_data = df.copy(deep = True)
    data_jogador = df_data[df_data['Ano'].isin([Outros])]

    fig = px.box(data_jogador, x = 'Outros', template = templates, points='all', title=Outros)

    return fig

if __name__ == '__main__':
    app.run_server(debug = True, port='8051')
