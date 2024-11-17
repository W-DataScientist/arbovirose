import streamlit as st
import locale

# Tenta definir a localidade para português do Brasil
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'C')  # Usa uma localidade padrão se falhar

from dados import display_map
from doc import display_doc
from previsao import display_previsao

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
    st.markdown("<h1 style='font-size: 30px;'>Previsão de Casos</h1>", unsafe_allow_html=True)
    display_previsao()

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
