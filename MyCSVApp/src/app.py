# importação daos módulos e bibliotecas
import pathlib # esta biblioteca foi importada para manipulação do arquivo csv, conforme https://www.youtube.com/watch?v=Gv910_b5ID0&t=784s
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

PATH = pathlib.Path(__file__).parent #uso do pathlib para leitura do arquivo csv
DATA_PATH = PATH.joinpath("data").resolve()
df = pd.read_csv(DATA_PATH.joinpath("vacina_atibaia.csv"), sep=';', low_memory=False)

df = df.rename_axis('doses').reset_index()# define o indice original como uma coluna chamada doses e cria um novo indice
doses = df['doses'].iloc[-1]# le o utlimo valor da coluna doses

app = Dash(__name__)#cria a aplicação com o dash
app.title = "Vacinação Atibaia"
server = app.server

# DADOS POR DATA
data = df.vacina_dataAplicacao.value_counts().to_frame()
data = data.rename_axis('Data').reset_index()
data.rename(columns={'vacina_dataAplicacao': 'Doses aplicadas'}, inplace=True)
data.Data = pd.to_datetime(data.Data, format="%Y-%m-%d")  # converte os dados para o formato de data
data = data.sort_values("Data")  # ordena por ordem de data
final = data['Data'].iloc[-1]
final = ("{}/{}/{}".format(final.day, final.month, final.year))

fig3 = px.line(data, x="Data", y="Doses aplicadas", color_discrete_sequence=["green"],
               title="Quantidade de doses aplicadas por dia no município de Atibaia-SP")
fig3.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig3.update_layout(font_color="white", title_font_color="white", font=dict(family='Andale Mono, monospace'))

# DADOS POR SEXO
sexo = df.paciente_enumSexoBiologico.value_counts(normalize=True).to_frame()  # converte os dados da coluna sexo para o df sexo como porcentagem
sexo = sexo.rename_axis('Sexo').reset_index()  # define o indice original como uma coluna e cria um novo indice
sexo.rename(columns={'paciente_enumSexoBiologico': 'Porcentagem'}, inplace=True)
sexo.loc[sexo['Sexo'] == 'F', 'Sexo'] = 'Mulheres'  # altera o item F da coluna sexo
sexo.loc[sexo['Sexo'] == 'M', 'Sexo'] = 'Homens'  # altera o item M da coluna sexo

fig1 = px.pie(sexo, values="Porcentagem", names="Sexo",
              title="Porcentagem de vacinados por sexo no município de Atibaia-SP",
              color="Sexo", color_discrete_map={'Homens': 'steelblue', 'Mulheres': 'indianred'}, hole=.5)
fig1.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig1.update_layout(font_color="white", title_font_color="white", font=dict(family='Andale Mono, monospace'))

# DADOS POR NOME DA VACINA
vacina = df.vacina_nome.value_counts().to_frame()
vacina = vacina.rename_axis('Vacina/Fabricante').reset_index()
vacina.rename(columns={'vacina_nome': 'Quantidade'}, inplace=True)

fig2 = px.pie(vacina, values="Quantidade", names="Vacina/Fabricante",
              title="Porcentagem de doses aplicadas por fabricante no município de Atibaia-SP", hole=.3)
fig2.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig2.update_layout(font_color="white", title_font_color="white", font=dict(family='Andale Mono, monospace'))

# DADOS POR UBS
posto = df.estalecimento_noFantasia.value_counts().to_frame()
posto = posto.rename_axis('Posto').reset_index()
posto.rename(columns={'estalecimento_noFantasia': 'Doses'}, inplace=True)

fig4 = px.bar(posto, y='Posto', x='Doses', color_discrete_sequence=["darkslategray"],
              title="Quantidade de doses aplicadas por UBS no município de Atibaia-SP")
fig4.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig4.update_layout(font_color="white", title_font_color="white", font=dict(family='Andale Mono, monospace'))

app.layout = html.Div([ # layout da página html do dash

    html.Div(
        className="header-container",
        children=[
            html.Div(
                className="app-header",
                children=[html.Div('Vacinação Covid-19', className="app-header-title"),
                          html.Div('Atibaia-SP', className="app-header-title")
                          ]
            )
        ]
    ),

    html.Div(
        className="header-container",
        children=[
            html.Div(
                className="app-box",
                children=[html.Div('Total de doses aplicadas:', className="app-box-text"),
                          html.Div(doses, className="app-box-text"),

                          html.Div('Última atualização em:', className="app-box-text"),
                          html.Div(final, className="app-box-text"),

                          html.Div('Fonte dos dados:', className="app-box-text"),
                          html.A(href="https://opendatasus.saude.gov.br/dataset/covid-19-vacinacao",
                                 children=[
                                     html.Img(alt="Datasus", src="/assets/OpenDatasus.png",
                                              style={'width': "100px", 'height': "30px", 'margin-left': "-3px"})
                                 ]
                                 ),

                          ]
            )
        ]
    ),

    html.Div(
        dcc.Graph(  # Gráfico 1
            id="sexo",
            figure=fig3
        )
    ),

    html.Div(
        dcc.Graph(  # Gráfico 2
            id="fabricante",
            figure=fig2
        )
    ),

    html.Div(
        dcc.Graph(  # Gráfico 3
            id="data",
            figure=fig4
        )
    ),

    html.Div(
        dcc.Graph(  # Gráfico 4
            id="ubs",
            figure=fig1
        )
    ),

    html.Footer(
        html.Div(
            children=[
                html.A("Desenvolvido por Reginaldo G. Santos - 2022"),
                html.A(href="https://github.com/reginaldogalli",
                       children=[
                           html.Img(alt="Github", src="/assets/github.png")
                       ]
                       ),
                html.A(href="https://www.linkedin.com/in/reginaldogalli/",
                       children=[
                           html.Img(alt="Linkedin", src="/assets/linkedin.png")
                       ]
                       )
            ]
        )
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)
