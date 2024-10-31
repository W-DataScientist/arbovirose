import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime, timedelta

# Função para obter dados da API com base no geocode e tipo de arbovirose.
def fetch_data(geocode, arbovirose):
    url = f"https://info.dengue.mat.br/api/alertcity?geocode={geocode}&disease={arbovirose}&format=json&ew_start=1&ew_end=52&ey_start=2024&ey_end=2024"
    response = requests.get(url)
    data = response.json()
    return data

# Função para calcular o primeiro dia da semana epidemiológica.
def get_first_day_of_epi_week(year, week):
    first_day_of_year = datetime(year, 1, 1)
    if first_day_of_year.weekday() <= 3:
        first_week_start = first_day_of_year - timedelta(days=first_day_of_year.weekday())
    else:
        first_week_start = first_day_of_year + timedelta(days=(7 - first_day_of_year.weekday()))
    
    epi_week_start = first_week_start + timedelta(weeks=week - 1)
    return epi_week_start

# Função para processar os dados.
def process_data(data):
    if isinstance(data, list):
        records = []
        
        for item in data:
            data_inicio = datetime.fromtimestamp(item['data_iniSE'] / 1000)
            records.append({
                'mes': data_inicio.strftime('%B'),
                'mes_abreviado': data_inicio.strftime('%b').capitalize(),
                'mes_num': data_inicio.month,
                'ano': data_inicio.year,
                'semana_epidemiologica': item.get('SE', None),
                'casos': item.get('casos', None),
                'nivel': item.get('nivel', None),
                'pop': item.get('pop', None),
                'tempmin': item.get('tempmin', None),
                'umidmax': item.get('umidmax', None),
                'umidmed': item.get('umidmed', None),
                'umidmin': item.get('umidmin', None),
                'tempmed': item.get('tempmed', None),
                'tempmax': item.get('tempmax', None),
                'notif_accum_year': item.get('notif_accum_year', None)
            })
        return pd.DataFrame(records)
    else:
        st.error("Formato de dados inesperado: Esperado uma lista.")
        return pd.DataFrame()

def display_previsao():
    geocode = "2302503"  
    arbovirose = "dengue"  

    data = fetch_data(geocode, arbovirose)
    df = process_data(data)

    ano_atual = datetime.now().year  
    df_atual = df[df['ano'] == ano_atual]

    df_semanal = df_atual.groupby(['semana_epidemiologica']).agg({'casos': 'sum'}).reset_index()

    df_semanal['umidmed'] = df_atual.groupby(['semana_epidemiologica'])['umidmed'].mean().values 
    df_semanal['tempmed'] = df_atual.groupby(['semana_epidemiologica'])['tempmed'].mean().values 

    df_semanal['mes_abreviado'] = df_semanal['semana_epidemiologica'].apply(lambda se: get_first_day_of_epi_week(ano_atual, se).strftime('%b').capitalize())
    
    df_semanal['label'] = df_semanal.apply(lambda x: f'{x["semana_epidemiologica"]:02d} - {x["mes_abreviado"]}', axis=1)

    if not df_semanal.empty:
        fig_dengue = px.bar(df_semanal,
                            x='label',
                            y='casos',
                            title=f'Casos de Dengue em {ano_atual} (Por Semana Epidemiológica)',
                            labels={'label': 'Semana Epidemiológica - Mês', 'casos': 'Número de Casos'},
                            color='casos',
                            color_continuous_scale=px.colors.sequential.YlOrRd,
                            barmode='group')

        fig_dengue.update_layout(margin=dict(l=0, r=0, t=50, b=40), width=1500)
        st.plotly_chart(fig_dengue)

        for arbovirose in ["chikungunya", "zika"]:
            data = fetch_data(geocode, arbovirose) 
            df = process_data(data) 
            df_atual = df[df['ano'] == ano_atual] 
            df_semanal = df_atual.groupby(['semana_epidemiologica']).agg({'casos': 'sum'}).reset_index() 
            df_semanal['umidmed'] = df_atual.groupby(['semana_epidemiologica'])['umidmed'].mean().values 
            df_semanal['tempmed'] = df_atual.groupby(['semana_epidemiologica'])['tempmed'].mean().values 
            df_semanal['mes_abreviado'] = df_semanal['semana_epidemiologica'].apply(lambda se: get_first_day_of_epi_week(ano_atual, se).strftime('%b').capitalize()) 
            df_semanal['label'] = df_semanal.apply(lambda x: f'{x["semana_epidemiologica"]:02d} - {x["mes_abreviado"]}', axis=1)

            if not df_semanal.empty:
                fig_other = px.bar(df_semanal,
                                   x='label',
                                   y='casos',
                                   title=f'Casos de {arbovirose.capitalize()} em {ano_atual} (Por Semana Epidemiológica)',
                                   labels={'label': 'Semana Epidemiológica - Mês','casos':'Número de Casos'},
                                   color='casos',
                                   color_continuous_scale=px.colors.sequential.YlOrRd,
                                   barmode='group')

                fig_other.update_layout(margin=dict(l=0, r=0, t=50, b=40), width=1500)

                st.plotly_chart(fig_other)

    else:
        st.write("Nenhum dado disponível para o ano selecionado.")

if __name__ == "__main__":
    display_previsao()
