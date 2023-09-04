from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO





url_theme1 = dbc.themes.VAPOR ## cor do pljogador de fundo
url_theme2 = dbc.themes.FLATLY ## cor do pljogador de fundo

template_theme1 = 'vapor'
template_theme2 = 'flatly'

df = pd.read_csv('Seguranca_informacao.csv') ## Abre o arquivo
state_options = [{'label': x, 'value': x} for x in df['Ano'].unique()] ## Escolhe uma coluna para comparacao
labels=[{'DOS','Web','Worm','Scan','Invasao'} for x in df['Ano'].unique()]
##LAYOUT PRINCIPAL DO DASHBOARD "Html"
app.layout = dbc.Container([
   
   
    dbc.Row([
        dbc.Col([
            ThemeSwitchAIO(aio_id = 'theme', themes = [url_theme2,url_theme1]),##cor do fundo
            html.H3('Mes x DOS'),
            dcc.Dropdown(
                id = 'Ano',
                value = [state['label'] for state in state_options[:3]],
                multi = True,
                options = state_options
            ),
        ])
    ]),
    
     dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'line_graph')
        ])
    ]),
    
    ##Pizza
    dbc.Row([ 
        dbc.Col([ 
            dbc.Row([ 
                dcc.Dropdown( 
                    id='pizza', 
                    options=[state['value'] for state in state_options[:3]], 
                    value= state_options, 
                ), 
                dcc.Graph(id='pizza_pie'), 
            ]) 
        ]), 
    ]), 



    dbc.Row([
        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                    id = 'Web',
                    value = state_options[0]['label'],
                    options = state_options
                    ), # pode usar o sm e o md aqui também
                
                dcc.Graph(id = 'box1')
                ]),
            ]),
        dbc.Col([
            dbc.Row([
                dcc.Dropdown(
                    id = 'DOS',
                    value = state_options[1]['label'],
                    options = state_options
                    ),
                dcc.Graph(id = 'box2')
                ])
            ])
    ])
])


@app.callback(
    Output('line_graph', 'figure'),
    Input('Ano', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value') 
)
def line(Ano, toggle):
    templates = template_theme2 if toggle else template_theme1

    df_data = df.copy(deep = True) # isso é muito pesado mano, bora tentar melhorar isso
    mask = df_data['Ano'].isin(Ano)

    fig = px.line(df_data[mask], x = 'Mes', y = 'DOS', color = 'Ano', template=templates) #mexe em nos eixos do grafico principal

    return fig

@app.callback( 
    [Output('pizza_pie', 'figure')], 
    Input('Ano', 'value'), 
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')  
) 
def update_graphs(values, toggle): 
    templates = template_theme2 if toggle else template_theme1
   # Selecione as colunas relevantes
    colunas = ['Web', 'DOS', 'Worm', 'Invasao', 'Scan']

    # Calcule a soma das ocorrências para cada coluna
    soma_por_coluna = df[colunas].sum()

    values = soma_por_coluna.values 

    pie_fig = px.pie(values=values, names=colunas) 
    pie_fig.update_traces(textinfo='percent+label', pull=[0.1] + [0] * (len(values) - 1)) 

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

if __name__ == '__main__':
    app.run_server(debug = True, port='8051')