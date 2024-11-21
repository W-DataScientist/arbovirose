import streamlit as st
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
