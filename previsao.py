import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
import plotly.graph_objects as go

# Função para buscar dados da API
def fetch_epidemiological_data(geocode, disease):
    url = f"https://info.dengue.mat.br/api/alertcity?geocode={geocode}&disease={disease}&format=json&ew_start=1&ew_end=52&ey_start=2014&ey_end=2024"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao buscar dados da API.")
        return None

# Função principal para exibir o gráfico
def display_previsao():
    geocode = "3550308"  # Código do município

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

    # Sidebar para seleção de modelo e estratégia (sem filtro de ano)
    st.sidebar.title("Configurações do Modelo")
    
    model_option = st.sidebar.selectbox(
        "Escolha o modelo:",
        ("Random Forest", "Regressão Linear")
    )
    
    cross_val_option = st.sidebar.checkbox("Usar Validação Cruzada")

    # Treinar o modelo com base na seleção do usuário
    if model_option == "Random Forest":
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        if cross_val_option:
            scores = cross_val_score(model, X, y, cv=5)
            st.write(f"Scores da validação cruzada: {scores}")

    elif model_option == "Regressão Linear":
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        if cross_val_option:
            scores = cross_val_score(model, X, y, cv=5)
            st.write(f"Scores da validação cruzada: {scores}")

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

    # Definindo os nomes dos meses correspondentes às semanas (considerando que as semanas são de 1 a 52)
    month_labels = [
        "Jan", "Jan", "Jan", "Jan", "Fev", "Fev", "Fev", "Fev",
        "Mar", "Mar", "Mar", "Mar", "Abr", "Abr", "Abr", "Abr",
        "Mai", "Mai", "Mai", "Mai", "Jun", "Jun", "Jun", "Jun",
        "Jul", "Jul", "Jul", "Jul", "Ago", "Ago", "Ago", "Ago",
        "Set", "Set", "Set", "Set", "Out", "Out", "Out", "Out",
        "Nov", "Nov", "Nov", "Nov", "Dez", "Dez", "Dez", "Dez"
    ]

    ticktext_labels = [f"{week}<br>{month}" for week, month in zip(range(1, 53), month_labels)]

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
        xaxis=dict(tickmode='linear', tickvals=list(range(1, 53)), ticktext=ticktext_labels),
        yaxis_tickprefix='Casos: ',
        showlegend=False,
        height=450,  # Altura ajustada pela metade
        width=1000,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

# Chame a função display_previsao() quando a aba correspondente for selecionada.
display_previsao()
