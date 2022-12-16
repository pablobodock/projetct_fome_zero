#===================================

import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import inflection
import folium
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


#--------------------------------------------

st.set_page_config(
                    page_title='Visão Geral',
                    page_icon='🏡',
                    layout='wide',
                    menu_items={
                    'Get Help': 'https://www.linkedin.com/in/pablocssousa/',
                    'Report a bug': "https://www.linkedin.com/in/pablocssousa/",
                    'About': "Dash Board criado a partir de dados públicos para desenvolvimento de projeto de análise de dados com Python. Para dúvidas e sugestões entre em contato através do LinkedIn : https://www.linkedin.com/in/pablocssousa/"
    }
                   )

#===================================
# Sidebar no Streamlit
#===================================

#image_path = 'images\\'
image2 = Image.open( 'logo_fome_zero_2.png' )
st.sidebar.image( image2, width=800,use_column_width='auto')
st.sidebar.write('<h2 style=\'text-align: center; color: #fe9666;\'>O melhor Marketplace, os melhores Restaurantes', unsafe_allow_html=True)

st.sidebar.markdown( """___""" )

st.sidebar.write('  ')





st.sidebar.markdown( '### Powered by Pablo Carvalho' )

#===================================
# Layout no Streamlit
#===================================

#image_path = 'images\\'
image = Image.open( 'cover_fome_zero_2.png' )
st.image( image, width=600,use_column_width='None')
st.write('<h1 style=\'text-align: right; color: #101820;\'>FOME ZERO Marks Dashboard 📈', unsafe_allow_html=True)

st.markdown(
    """
    Marks Dashboard foi construído para acompanhar as métricas de crescimento e desempenho  dos Restaurantes.
    ### Como utilizar esse Marks Dashboard?
    - Visão Geral:
        - Apresenta as marcas atuais da empresa com relação a números absolutos de parceiros, avaliações e atuação geográfica.
    - Visão Países:
        - Acompanhamento dos números de restaurantes, cidades, tipos de culinárias e avaliações por país.
    - Visão Cidades:
        - Apresenta os quantitativos de restaurantes cadastrados na base de dados em relação a suas notas de avaliação, tipos distintos de culinária e modelo de negócio.
    - Visão Restaurantes:
        -Apresenta as marcas de avaliação dos principais tipos de culinária oferecidos pelos restaurantes da plataforma.
        -Traz comparativos do modelo de negócio com métricas de avaliação, tipos de culinária e preço médio do prato para o casal.
        
    ### Ask for Help
    - Time de Data Science no Discord
        - Pablo Carvalho#3156
""" )