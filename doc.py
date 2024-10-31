import streamlit as st

def display_doc():
    st.header("Documentação do Código - dados.py")

    st.write("""
    Este documento descreve o código contido no arquivo `dados.py`, que é responsável por buscar dados de um JSON e exibir um mapa utilizando a biblioteca Pydeck.
    Além disso, ele permite a visualização de casos epidemiológicos de arboviroses em diferentes municípios.
    """)

    st.subheader("1. Importação de Bibliotecas")
    st.write("""
    O código começa com a importação das bibliotecas necessárias:
    - **streamlit**: Usada para criar a interface do usuário.
    - **pydeck**: Usada para visualização de dados geoespaciais em mapas.
    - **requests**: Usada para fazer requisições HTTP e obter dados JSON.
    - **pandas**: Usada para manipulação e análise de dados.
    """)

    st.code("""
import streamlit as st
import pydeck as pdk
import requests
import pandas as pd
""", language='python')

    st.subheader("2. Função fetch_data()")
    st.write("""
    Esta função é responsável por buscar os dados do JSON a partir de uma URL. 
    Se a requisição for bem-sucedida (código de status 200), os dados são retornados; 
    caso contrário, uma mensagem de erro é exibida.
    """)

    st.code("""
def fetch_data():
    url = "https://storage.googleapis.com/maps_js/allmun.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao buscar dados.")
        return None
""", language='python')

    st.subheader("3. Função display_map(selected_municipio)")
    st.write("""
    Esta função exibe o mapa para o município selecionado. Ela realiza as seguintes etapas:
    
    1. **Busca os Dados**: Chama a função `fetch_data()` para obter os dados JSON.
    
    2. **Extração de Municípios**: Extrai os nomes dos municípios e suas coordenadas.
    
    3. **Criação da Camada do Mapa**: Utiliza Pydeck para criar uma camada do polígono correspondente ao município selecionado.
    
    4. **Configuração da Visualização**: Define a posição inicial do mapa e cria o deck que será exibido na interface.
    
    5. **Exibição do Mapa**: Renderiza o mapa na aplicação Streamlit.

   O parâmetro `selected_municipio` deve ser o nome do município que você deseja visualizar no mapa.
   """)

    st.code("""
def display_map(selected_municipio):
    data = fetch_data()
    if data:
        municipios = {feature['properties']['municipioNome']: feature for feature in data['features']}
        coordinates = municipios[selected_municipio]['geometry']['coordinates']
        
        polygon_layer = pdk.Layer(
            "GeoJsonLayer",
            data={"type": "FeatureCollection", "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": coordinates
                }
            }]},
            get_fill_color=[255, 0, 0],
            get_line_color=[0, 0, 0],
            line_width_min_pixels=2,
            opacity=0.5,
            pickable=True,
        )

        initial_latitude = coordinates[0][0][0][1]
        initial_longitude = coordinates[0][0][0][0]

        view_state = pdk.ViewState(
            latitude=initial_latitude,
            longitude=initial_longitude,
            zoom=8,
            pitch=0,
        )

        deck = pdk.Deck(
            layers=[polygon_layer],
            initial_view_state=view_state,
            map_style='mapbox://styles/mapbox/satellite-v9',
        )

        st.pydeck_chart(deck)
        st.markdown(f"### Município Selecionado: **{selected_municipio}**")
""", language='python')

    st.subheader("4. Conclusão")
    st.write("""
    O arquivo `dados.py` é fundamental para a visualização de dados geoespaciais em um aplicativo Streamlit, permitindo que os usuários interajam com informações sobre diferentes municípios através de um mapa interativo.
    
    Para que o aplicativo funcione corretamente, certifique-se de ter todas as dependências instaladas e que os dados estejam acessíveis.
    """)
