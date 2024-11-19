import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import json

# Função para buscar dados da API
def fetch_epidemiological_data(geocode, disease):
    url = f"https://info.dengue.mat.br/api/alertcity?geocode={geocode}&disease={disease}&format=json&ew_start=1&ew_end=52&ey_start=2014&ey_end=2024"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao buscar dados da API.")
        return None

# Função para carregar municípios e códigos do IBGE
def load_municipalities():
    with open('allmun.json', 'r') as f:
        data = json.load(f)
    municipalities = {feature['properties']['_id']: feature['properties']['cod_mun'] for feature in data['features']}
    return municipalities

# Função principal para exibir o gráfico
def display_previsao():
    # Carregar municípios e códigos do IBGE
    municipalities = load_municipalities()

    # Adicionando um filtro na página para selecionar o código do IBGE
    selected_city = st.selectbox(
        "Selecione o município para previsão de casos de Dengue em 2025:",
        list(municipalities.keys()),
        index=list(municipalities.keys()).index("São Paulo - SP")  # Pre-select São Paulo
    )
    geocode = municipalities[selected_city]

    # Coletando dados históricos (2014-2024) para Dengue
    data = fetch_epidemiological_data(geocode, "dengue")
    all_weeks_data = []

    if data:
        for week_data in data:
            week_info = {
                'Semana': int(str(week_data['SE'])[-2:]),  # Extraindo a semana do formato SE
                'Casos': week_data['casos'],
                'Temp Média': week_data['tempmed'],
                'Umidade Média': week_data['umidmed'],
                'Rt': week_data['Rt'],
                'População': week_data['pop']  # Adicionando a população dos dados coletados
            }
            all_weeks_data.append(week_info)

    # Criar um DataFrame com os dados coletados
    historical_df = pd.DataFrame(all_weeks_data)

    # Agrupar por semana e calcular a média dos casos
    historical_weekly_cases = historical_df.groupby('Semana').mean().reset_index()

    # Criar variáveis independentes e dependentes
    X = historical_weekly_cases[['Semana', 'Temp Média', 'Umidade Média', 'Rt', 'População']]
    y = historical_weekly_cases['Casos']

    # Dividir os dados em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo Random Forest sem validação cruzada
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Prever casos para 2025 (52 semanas)
    future_weeks = np.arange(1, 53).reshape(-1, 1)  # Semanas de 1 a 52 para 2025

    # Simular valores futuros para temperatura média, umidade e Rt
    future_temp_med = np.random.uniform(low=20, high=30, size=52)  # Temperatura média simulada
    future_umid_med = np.random.uniform(low=60, high=90, size=52)  # Umidade média simulada
    future_rt = np.random.uniform(low=0.8, high=1.2, size=52)      # Rt simulado

    future_data = pd.DataFrame({
        'Semana': future_weeks.flatten(),
        'Temp Média': future_temp_med,
        'Umidade Média': future_umid_med,
        'Rt': future_rt,
        'População': [np.mean(historical_weekly_cases['População'])] * 52  # Usando média da população histórica nas previsões futuras
    })

    predicted_cases = model.predict(future_data)

    # Garantir que os casos previstos não sejam negativos
    predicted_cases = np.maximum(predicted_cases, 0)

    # Criar um DataFrame para armazenar as previsões
    forecast_df = pd.DataFrame({
        'Semana': future_weeks.flatten(),
        'Casos Previsto': predicted_cases
    })

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=forecast_df['Semana'],
        y=forecast_df['Casos Previsto'],
        name='Casos Previsto',
        marker_color='red',
        text=forecast_df['Casos Previsto'],
        textposition='auto'
    ))

    fig.update_layout(
        xaxis_title='Semana Epidemiológica',
        yaxis_title='Número de Casos',
        xaxis=dict(tickmode='linear', tickvals=list(range(1, 53))),
        yaxis_tickprefix='Casos: ',
        showlegend=False,
        height=450,
        width=1000,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

# Chame a função display_previsao() quando a aba correspondente for selecionada.
display_previsao()
