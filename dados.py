import streamlit as st
import pydeck as pdk
import json
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Função para buscar dados do JSON localmente ou via URL
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

        # Exibindo o gráfico no Streamlit acima do mapa.
        st.plotly_chart(fig)

        # Exibindo a população abaixo do gráfico.
        st.markdown(f"##### População de {selected_municipio}: {populacao}")

        # Criando a camada do polígono com pydeck.
        polygon_layer = pdk.Layer(
            "GeoJsonLayer",
            data={"type": "FeatureCollection", "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": coordinates,
                }
            }]},
            get_fill_color=[255,0,0],   # Cor do preenchimento (vermelho)
            get_line_color=[0,0,0],     # Cor da linha (preto)
            line_width_min_pixels=2,
            opacity=0.5,
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=-14.2350,
            longitude=-51.9253,
            zoom=3.1,
            pitch=0,
        )

        deck = pdk.Deck(
            layers=[polygon_layer],
            initial_view_state=view_state,
            map_style='mapbox://styles/mapbox/light-v11',
        )

        st.pydeck_chart(deck)

# Chama a função principal para exibir o mapa e gráficos na aplicação Streamlit.
display_map()
