import streamlit as st

def display_doc():
    # Título da documentação
    st.title("Previsão de Casos de Arboviroses")

    # Descrição geral do projeto
    st.write("""
    A escolha do projeto de Previsão de Casos de Arboviroses é fundamentada na
relevância crescente desse tema para a saúde pública. Doenças como dengue, zika e
chikungunya afetam milhões de pessoas anualmente, representando um desafio
significativo, especialmente em regiões onde o aumento das temperaturas e chuvas
intensas favorece a proliferação do mosquito Aedes aegypti. 
A previsão de surtos é, portanto, essencial para antecipar respostas rápidas e eficazes, 
reduzindo a letalidade e o impacto sobre os sistemas de saúde.
             
Além disso, o projeto desempenha um papel importante na conscientização da
população sobre medidas preventivas, promovendo o engajamento comunitário e a
educação em saúde. A integração entre diferentes setores também fortalece a
coordenação no combate às arboviroses, possibilitando uma gestão mais eficiente de
recursos financeiros e humanos. Essas ações, direcionadas às áreas mais
vulneráveis, são fundamentais para proteger a saúde da população e melhorar a
qualidade de vida nas comunidades afetadas.
             
Outro aspecto relevante é o impacto dessas doenças na economia e no
bem-estar social. Surtos de dengue, zika e chikungunya sobrecarregam os sistemas
de saúde, aumentam os custos com internações e medicamentos e afetam a
produtividade da população economicamente ativa. Portanto, prever e mitigar esses
eventos não apenas protege a saúde pública, mas também contribui para a
sustentabilidade econômica e social das comunidades, reforçando a importância do
projeto no cenário atual.
    """)

  
    st.header("Partes da aplicação")
    st.write("""
    O projeto se divide em 3 partes:
    - **Dados Arboviroses**: Exibe os dados sobre Arboviroses do municipio selecionado com filtro de ano e tipo do vírus.
    - **Previsão de casos**: Faz previsão de casos através a partir de dados fornecidos via API utilisando modelos de Machine Learning .
    - **Documentação**: Documentação de todo codigo.
    """)


    st.header("Arquivos do projeto")
    st.subheader("main.py")

    st.write("""
As funcionalidades do arquivo main.py são:
             
- **Importação de Bibliotecas**: Utiliza Streamlit para a interface e locale para definir a localidade em português do Brasil.
             
- **Configuração da Página**: Define o layout como amplo e adiciona um título centralizado.
             
- **Sidebar**: Exibe uma imagem relacionada a arboviroses e inclui links para um repositório do GitHub e para o site Info Dengue.
             
**Abas**: Cria três abas:
             
- **Dados Arboviroses**: Chama uma função para exibir um mapa.
- **Previsão de Casos**: Chama uma função para mostrar previsões.
- **Documentação**: Chama uma função para exibir informações/documentação do projeto.
            
    """)


    st.code("""
import streamlit as st
import locale

# Tenta definir a localidade para português do Brasil
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'C')  # Usa uma localidade padrão se falhar

from dados import display_map  # Supondo que você tenha um módulo chamado dados
from doc import display_doc     # Supondo que você tenha um módulo chamado doc
from previsao import display_forecast  # Importa a função do arquivo previsao.py

# Configuração da página para layout amplo
st.set_page_config(layout='wide')

# Adicionando título "Imersão Profissional" acima das abas
st.markdown("<h4 style='text-align: center;'>Trabalho de Imersão Profissional: Aplicação de Métodos de Aprendizagem de Máquina</h4>", unsafe_allow_html=True)

# Exibir imagem com legenda
st.sidebar.markdown(
    "<div style='text-align: center;'>"
    "<img src='https://cpplimeira.com.br/wp-content/uploads/2016/01/mosquito_vadimmmus.png' width='180'>"
    "<p style='font-size: 20px;'>Dados Arboviroses</p>"
    "</div>",
    unsafe_allow_html=True
)

# Criando abas para Dados arboviroses, Previsão de casos e Documentação no topo da página
tab1, tab2, tab3 = st.tabs(["Dados arboviroses", "Previsão de casos", "Documentação"])

with tab1:
    st.markdown("<h1 style='font-size: 30px;'></h1>", unsafe_allow_html=True)
    display_map()  # Chama a função que exibe o mapa

with tab2:
    # Chama a função que exibe a previsão apenas quando a aba é acessada
    display_forecast()  

with tab3:
    st.markdown("<h1 style='font-size: 30px;'>Documentação</h1>", unsafe_allow_html=True)
    display_doc()

# Adicionando logo do GitHub e link na parte inferior do sidebar
st.sidebar.markdown(
    "<div style='display: flex; align-items: center;'>"
    "<a href='https://github.com/W-DataScientist/arbovirose' target='_blank'>"
    "<img src='https://banner2.cleanpng.com/20180920/aey/kisspng-scalable-vector-graphics-github-computer-icons-log-github-brand-octacat-social-svg-png-icon-free-down-5ba35d7db54fe5.6273953815374329577427.jpg' width='25' style='margin-right: 8px;'>"
    "</a>"
    "<a href='https://github.com/W-DataScientist/arbovirose'>Arbovirose</a>"
    "</div>",
    unsafe_allow_html=True
)

# Adicionando link da Info Dengue no sidebar
st.sidebar.markdown(
    "<div style='display: flex; align-items: center; margin-top: 10px;'>"
    "<a href='https://info.dengue.mat.br/' target='_blank'>"
    "<img src='https://info.dengue.mat.br/static/img/info-dengue-logo-multicidades.png' width='25' style='margin-right: 8px;'>"
    "</a>"
    "<a href='https://info.dengue.mat.br/'>Info Dengue</a>"
    "</div>",
    unsafe_allow_html=True
)
    """, language='python')



   
    st.subheader("dados.py")

    

    st.write("""
Visualiza dados epidemiológicos de arboviroses (Dengue, Zika e Chikungunya) em municípios brasileiros. 
Aqui estão os principais pontos:
             
- **Importação de Bibliotecas**: Utiliza Streamlit para a interface, Pydeck para mapas, e Plotly para gráficos interativos.
             
- **Configuração da Página**: Define o layout como amplo para melhor visualização.
             
**Funções Principais**:
             
fetch_data(): Carrega dados de um arquivo JSON local.
fetch_epidemiological_data(): Obtém dados de uma API com base em geocódigo, doença e ano.
display_map(): Exibe um mapa e gráficos interativos:
             
Permite selecionar município e ano.
Exibe gráficos dos casos ao longo das semanas epidemiológicas.
Mostra a população do município selecionado.
             
**Interatividade**: Usuários podem escolher quais doenças visualizar e interagir com gráficos e mapas para analisar os dados de forma clara e acessível.
            
    """)

    st.code("""
    import streamlit as st
import pydeck as pdk
import json
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página para layout amplo
st.set_page_config(layout='wide')

# Função para buscar dados do JSON localmente
def fetch_data():
    try:
        with open('allmun.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Arquivo allmun.json não encontrado.")
        return None

# Função para buscar dados da API
def fetch_epidemiological_data(geocode, disease, year):
    url = f"https://info.dengue.mat.br/api/alertcity?geocode={geocode}&disease={disease}&format=json&ew_start=1&ew_end=52&ey_start={year}&ey_end={year}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao buscar dados da API.")
        return None

def display_map():
    data = fetch_data()
    if data:
        # Extraindo nomes de municípios para a sidebar
        municipios = {feature['properties']['_id']: feature for feature in data['features']}
        municipio_names = list(municipios.keys())

        # Verificando se "São Paulo - SP" está na lista de municípios
        default_municipio = "São Paulo - SP"
        
        # Se não estiver, use o primeiro município disponível
        if default_municipio not in municipio_names:
            default_municipio = municipio_names[0]

        # Sidebar para seleção do município com "São Paulo - SP" como padrão
        selected_municipio = st.sidebar.selectbox("Município:", municipio_names, index=municipio_names.index(default_municipio))

        # Obtendo as coordenadas e a população do município selecionado
        coordinates = municipios[selected_municipio]['geometry']['coordinates']
        populacao = municipios[selected_municipio]['properties']['populacao']  # Extraindo a população

        # Adicionando um calendário para selecionar o ano, com 2024 como padrão
        current_year = datetime.now().year
        years = list(range(2014, current_year + 1))
        selected_year = st.sidebar.selectbox("Ano:", years, index=years.index(2024))

        # Adicionando checkboxes para Dengue, Zika e Chikungunya marcados por padrão.
        dengue_checked = st.sidebar.checkbox("Dengue", value=True)
        chikungunya_checked = st.sidebar.checkbox("Chikungunya", value=False)
        zika_checked = st.sidebar.checkbox("Zika", value=False)

        # Obtendo o cod_mun do município selecionado para usar como geocode na API
        geocode = municipios[selected_municipio]['properties']['cod_mun']

        # Dicionário para armazenar os dados das doenças selecionadas
        disease_map = {
            "Dengue": dengue_checked,
            "Chikungunya": chikungunya_checked,
            "Zika": zika_checked,
        }

        # Inicializando a figura do gráfico e o dicionário total_cases
        fig = go.Figure()
        total_cases = {disease: 0 for disease in disease_map if disease_map[disease]}

        # Cores para cada doença
        colors = {
            "Dengue": 'black',
            "Zika": 'orange',
            "Chikungunya": 'red'
        }

        # Coletando dados de cada doença selecionada e adicionando ao gráfico
        for disease, is_checked in disease_map.items():
            if is_checked:
                epidemiological_data = fetch_epidemiological_data(geocode, disease.lower(), selected_year)
                if epidemiological_data:
                    df = pd.DataFrame(epidemiological_data)

                    # Extraindo a semana do formato SE (ex: 202350)
                    df['Semana'] = df['SE'].astype(str).str[-2:].astype(int)

                    weeks = df['Semana'].tolist()
                    casos = df['casos'].tolist()  # Usando casos para Dengue, Zika e Chikungunya
                    
                    fig.add_trace(go.Scatter(x=weeks, y=casos,
                                             mode='lines+markers',
                                             name=disease,
                                             line=dict(color=colors[disease])))  # Usando linhas para doenças

                    # Somando os casos totais para cada doença selecionada (apenas doenças com linha)
                    total_cases[disease] += sum(casos)

        # Criar um título que inclui o total de casos para cada doença e o nome do município
        title_cases = ', '.join([f"{disease}: {total_cases[disease]}" for disease in total_cases if total_cases[disease] > 0])
        
        fig.update_layout(title=f'Casos em {selected_municipio} - {selected_year} - {title_cases}',
                          xaxis_title='Semana Epidemiológica',
                          yaxis_title='Casos',
                          legend_title='Arboviroses')

        # Definindo os rótulos das semanas no formato "01 - Jan"
        month_mapping = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 
                         5: 'Mai', 6: 'Jun', 7: 'Jul', 
                         8: 'Ago', 9: 'Set', 
                         10: 'Out', 11: 'Nov', 12: 'Dez'}
        
        week_labels = []
        
        for week in range(1, 53):
            if week <= 4:
                month_number = 1  # Janeiro
            elif week <= 8:
                month_number = 2  # Fevereiro
            elif week <= 13:
                month_number = 3  # Março
            elif week <= 17:
                month_number = 4  # Abril
            elif week <= 22:
                month_number = 5  # Maio
            elif week <= 26:
                month_number = 6  # Junho
            elif week <= 30:
                month_number = 7  # Julho
            elif week <= 35:
                month_number = 8  # Agosto
            elif week <= 39:
                month_number = 9  # Setembro
            elif week <= 43:
                month_number = 10 # Outubro
            elif week <= 48:
                month_number = 11 # Novembro
            else:
                month_number = 12 # Dezembro

            week_labels.append(f'{week:02} - {month_mapping[month_number]}')

        # Atualizando o eixo x com ticks e labels corretos.
        fig.update_xaxes(tickvals=list(range(1, 53)), ticktext=week_labels)

        # Exibindo o gráfico no Streamlit acima do mapa
        st.plotly_chart(fig)

        # Exibindo a população abaixo do gráfico.
        st.markdown(f"##### População de {selected_municipio}: {populacao}")

        # Criando a camada do polígono com pydeck
        polygon_layer = pdk.Layer(
            "GeoJsonLayer",
            data={"type": "FeatureCollection", "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": coordinates
                }
            }]},
            get_fill_color=[255, 0, 0],   # Cor do preenchimento (vermelho)
            get_line_color=[0, 0, 0],     # Cor da linha (preto)
            line_width_min_pixels=2,
            opacity=0.5,
            pickable=True,
        )

        # Definindo a visualização para abranger todo o Brasil
        view_state = pdk.ViewState(
            latitude=-14.2350,
            longitude=-51.9253,
            zoom=3.1,
            pitch=0,
        )

        # Criando o deck e exibindo no Streamlit com estilo light
        deck = pdk.Deck(
            layers=[polygon_layer],
            initial_view_state=view_state,
            map_style='mapbox://styles/mapbox/light-v11',
        )

        st.pydeck_chart(deck)

# Chama a função principal para exibir o mapa e gráficos na aplicação Streamlit.
display_map()

    """, language='python')




    st.subheader("previsao.py")

    st.write("""
    Prevê casos de arboviroses (Dengue, Zika e Chikungunya) em municípios brasileiros. Aqui estão os principais pontos:
             
Importação de Bibliotecas: Utiliza Streamlit para a interface, Pydeck para mapas, Plotly para gráficos, e Scikit-learn para modelos de aprendizado de máquina.
Configuração da Página: Define o layout como amplo para melhor visualização.
             
Funções Principais:
             
Carregar Dados: Lê dados de um arquivo JSON local e busca dados epidemiológicos de uma API.
Simulação de Dados Futuros: Gera dados simulados para temperatura, umidade e taxa de reprodução (Rt).
Previsão: Permite ao usuário selecionar município e doença, treina um modelo (Random Forest ou Regressão Linear) com dados históricos, e faz previsões para o futuro.
Visualização Interativa: Exibe gráficos que comparam dados históricos com previsões futuras, permitindo que os usuários analisem diferentes cenários.
            
    """)

    st.code("""
    import streamlit as st
import pydeck as pdk
import json
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Configuração da página para layout amplo
st.set_page_config(layout='wide')

# Função para carregar dados do JSON
def fetch_municipios_data():
    try:
        with open('allmun.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Arquivo 'allmun.json' não encontrado. Certifique-se de que ele está na mesma pasta.")
        return None

# Função para buscar dados da API
def fetch_epidemiological_data(geocode, disease):
    url = f"https://info.dengue.mat.br/api/alertcity?geocode={geocode}&disease={disease}&format=json&ew_start=1&ew_end=52&ey_start=2014&ey_end=2024"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro ao buscar dados da API: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Erro ao conectar na API: {e}")
        return []

# Função para simular dados futuros
def simulate_future_data(weeks, historical_population):
    return pd.DataFrame({
        'Semana': weeks,
        'Temp Média': np.random.uniform(20, 30, size=len(weeks)),
        'Umidade Média': np.random.uniform(60, 90, size=len(weeks)),
        'Rt': np.random.uniform(0.8, 1.2, size=len(weeks)),
        'População': [historical_population] * len(weeks)
    })

# Função principal
def display_forecast():
    # Carregar dados dos municípios
    municipios_data = fetch_municipios_data()
    if not municipios_data:
        return

    # Extraindo nomes e dados dos municípios
    municipios = {feature['properties']['_id']: feature for feature in municipios_data['features']}
    municipio_names = list(municipios.keys())

    # Configuração da barra lateral
    st.sidebar.title("Configurações para previsão")
    selected_municipio = st.sidebar.selectbox("Município:", municipio_names, index=0)
    selected_disease = st.sidebar.selectbox("Arbovirose:", ["Dengue", "Zika", "Chikungunya"])
    
    # Obter informações do município selecionado
    municipio_info = municipios.get(selected_municipio)
    if not municipio_info:
        st.error("Erro ao obter informações do município selecionado.")
        return

    geocode = municipio_info['properties'].get('cod_mun')
    population = municipio_info['properties'].get('populacao', 0)

    # Buscar dados epidemiológicos
    historical_data = fetch_epidemiological_data(geocode, selected_disease)
    if not historical_data:
        st.warning("Nenhum dado epidemiológico disponível para este município.")
        return

    # Processar os dados históricos
    all_weeks_data = []
    years_used = set()
    for week_data in historical_data:
        year = int(str(week_data['SE'])[:4])  # Extraindo o ano do formato SE
        years_used.add(year)
        all_weeks_data.append({
            'Semana': int(str(week_data['SE'])[-2:]),
            'Casos': week_data['casos'],
            'Ano': year,
            'Temp Média': week_data['tempmed'],
            'Umidade Média': week_data['umidmed'],
            'Rt': week_data['Rt'],
            'População': week_data['pop']
        })

    historical_df = pd.DataFrame(all_weeks_data)
    if historical_df.empty:
        st.warning("Os dados retornados estão vazios.")
        return

    # Agrupar dados por semana
    historical_weekly_cases = historical_df.groupby(['Ano', 'Semana']).mean().reset_index()

    # Ligar/desligar anos de treinamento
    st.sidebar.subheader("Selecione o ano")
    years_to_display = []
    for year in sorted(years_used):
        if st.sidebar.checkbox(str(year), value=True):
            years_to_display.append(year)

    # Filtrar os dados históricos pelos anos selecionados
    filtered_data = historical_weekly_cases[historical_weekly_cases['Ano'].isin(years_to_display)]

    # Treinamento do modelo
    try:
        X = filtered_data[['Semana', 'Temp Média', 'Umidade Média', 'Rt', 'População']]
        y = filtered_data['Casos']

        # Remover valores nulos (se houver)
        X = X.dropna()
        y = y[X.index]

        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Porcentagem de dados usados no treinamento
        train_percentage = (len(X_train) / len(X)) * 100 if len(X) > 0 else 0

        # Configuração do modelo
        model_option = st.sidebar.selectbox("Modelo de Regressão:", ["Random Forest", "Regressão Linear"])
        if model_option == "Random Forest":
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        elif model_option == "Regressão Linear":
            model = LinearRegression()

        # Treinar modelo
        model.fit(X_train, y_train)

        # Previsões no conjunto de teste
        y_pred = model.predict(X_test)

        # Cálculo das métricas de erro
        model_accuracy = max(0, min(r2_score(y_test, y_pred) * 100, 100)) if len(y_test) > 0 else 0
        mse = mean_squared_error(y_test, y_pred) if len(y_test) > 0 else 0
        mae = mean_absolute_error(y_test, y_pred) if len(y_test) > 0 else 0

    except Exception as e:
        st.error(f"Erro no treinamento do modelo: {e}")
        return

    # Simular dados futuros
    future_data = simulate_future_data(np.arange(1, 53), population)
    predicted_cases = model.predict(future_data)
    predicted_cases = np.maximum(predicted_cases, 0)

    # Criar gráfico interativo
    fig = go.Figure()

    # Adicionando dados históricos por ano selecionado
    for year in years_to_display:
        year_data = historical_weekly_cases[historical_weekly_cases['Ano'] == year]
        fig.add_trace(go.Scatter(
            x=year_data['Semana'],
            y=year_data['Casos'],
            mode='lines+markers',
            name=f"Ano {year}",
            line=dict(dash='dash'),
        ))

    # Adicionando dados de previsão
    fig.add_trace(go.Scatter(
        x=future_data['Semana'],
        y=predicted_cases,
        mode='lines+markers',
        name='Previsão 2025',
        line=dict(color='red', width=2),
    ))

    # Configurações do layout sem "Anos utilizados"
    fig.update_layout(
        title=(f"Linha Temporal - Dados de Treinamento vs Previsão<br>"
               f"Treinamento: {train_percentage:.1f}% dos dados | Precisão (R²): {model_accuracy:.2f}%<br>"
               f"Erro Médio Absoluto (MAE): {mae:.2f} | Erro Quadrático Médio (MSE): {mse:.2f}"),
        xaxis_title="Semana Epidemiológica",
        yaxis_title="Número de Casos",
        legend_title="Anos",
        template="plotly_white",
        height=600,
    )

    # Certifique-se de que o eixo X tenha marcas de 1 a 52
    fig.update_xaxes(tickvals=np.arange(1, 53), ticktext=[str(i) for i in range(1, 53)])

    st.plotly_chart(fig)

# Chama a função principal
display_forecast()

    """, language='python')




    st.subheader("doc.py")

    st.write("""

            Descreve toda documentação de codigo da aplicação
    """)

    st.code("""
    
...

    """, language='python')
