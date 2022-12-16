#===================================
#Libraries
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
                    page_icon='📈',
                    layout='wide',
                    menu_items={
                    'Get Help': 'https://www.linkedin.com/in/pablocssousa/',
                    'Report a bug': "https://www.linkedin.com/in/pablocssousa/",
                    'About': "Dash Board criado a partir de dados públicos para desenvolvimento de projeto de análise de dados com Python. Para dúvidas e sugestões entre em contato através do LinkedIn : https://www.linkedin.com/in/pablocssousa/"
    }
                   )




#=============================================================
#Funções
#=============================================================

#Dicionários para conversão de dados
COUNTRIES = {
            1: "India",
            14: "Australia",
            30: "Brazil",
            37: "Canada",
            94: "Indonesia",
            148: "New Zeland",
            162: "Philippines",
            166: "Qatar",
            184: "Singapure",
            189: "South Africa",
            191: "Sri Lanka",
            208: "Turkey",
            214: "United Arab Emirates",
            215: "England",
            216: "United States of America",
            }

COLORS = {
            "3F7E00": "darkgreen",
            "5BA829": "green",
            "9ACD32": "lightgreen",
            "CDD614": "orange",
            "FFBA00": "red",
            "CBCBC8": "darkred",
            "FF7800": "darkred",
         }

booking_deliver = {
                    1: 'Sim',
                    0: 'Não'
                  }

#-----------------------------------------
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def country_name(country_id):
    return COUNTRIES[country_id]

def yes_no(yes_no_id):
    return booking_deliver[yes_no_id]

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

def color_name(color_code):
    return COLORS[color_code]

def data_clean( df ):
    ''' Esta função faz o tratamento e a limpeza do dataframe.
    
        Ações:
            -Elimina as linhas com células vazias ('NaN');
            -Renomeia as colunas;
            -Elimina linhas duplicadas;
            -Categoriza nome dos países;
            -Categoriza range de preços;
            -Categoriza cor das avaliações;
            -Categoriza tipo de culinária;
            -Reseta os indices do dataframe.

            Input: Dataframe
            Output: Dataframe '''
    
    #Renomando as colunas do dataframe
    df = rename_columns(df)

    #Eliminando linhas com dados vazios NaN
    df = df.dropna()

    #Eliminando linhas duplicadas
    df = df.drop_duplicates(keep='first')

    #Categorizando variável country_code
    for i in COUNTRIES.keys():
        df['country_code'] = df['country_code'].replace(i, country_name(i) )
    
    #Categorizando variável has table bookin
    df['has_table_booking_cat'] = df['has_table_booking']
    for i in booking_deliver.keys():
        df['has_table_booking_cat'] = df['has_table_booking_cat'].replace(i, yes_no(i) )

    #Categorizando variável has_online_delivery_cat
    df['has_online_delivery_cat'] = df['has_online_delivery']
    for i in booking_deliver.keys():
        df['has_online_delivery_cat'] = df['has_online_delivery_cat'].replace(i, yes_no(i) )

    #Categorizando variável has_online_delivery_cat
    df['is_delivering_now_cat'] = df['is_delivering_now']
    for i in booking_deliver.keys():
        df['is_delivering_now_cat'] = df['is_delivering_now_cat'].replace(i, yes_no(i) )


    #Categorizando variável price_range
    for i in range(1,5):
        df['price_range'] = df['price_range'].replace(i, create_price_tye(i) )

    #Categorizando coluna rating_color
    for i in COLORS.keys():
        df['rating_color'] = df['rating_color'].replace(i, color_name(i) )

    #Categorizando tipo de culinária por sua especialidade, considerada como sendo a da primeira posição
    df['cuisines'] = df.loc[:, 'cuisines'].apply(lambda x: x.split(', ')[0])

    #Resetando indices das linhas
    df = df.reset_index(drop = True)
    
    return df


def bar_graph(df, cols, group, x, y, operation, qtd = None, asc = False, title = ''):

    df_aux = ( df.loc[ : , cols]
                 .groupby(group)
                 .agg({cols[0] : operation}).sort_values(cols[0], ascending = asc) )
    
    df_aux = df_aux.round(2).reset_index()
    df_aux.columns = [ x , y ]
    
    if qtd != None:
        df_aux = df_aux.head(qtd)

    colors = ['#fe9666'] * 15
    colors[0] = '#fe5000'

    fig = go.Figure(data=[go.Bar(
        x=df_aux.loc[ : , x],
        y=df_aux.loc[ : , y],
        text = df_aux.loc[ : , y],
        textposition='auto',
        marker_color=colors
    )])
    fig.update_layout(title_text= title)
    return fig

def filtro(df, tipo, col, var ):
    '''
        Esta funçao tema  responsabilidade de realizar o filtro a ser aplicado.
        
        Input:
            -df: data frame que será filtrado.
            -tipo: informa o tipo de filtro a ser aplicado (slider or multiselect)
            -col : coluna do dataframe que será filtrada
            -var:  variável que contem o parâmetro do filtro
            
        Output: dataframe filtrado.
    '''
    if tipo == 'slider':
        df_filtrado = df[col] <= var
        df =  df.loc[df_filtrado , : ]
        
    elif tipo == 'multiselect':
        if var == 'Sim':
            var = 1
            df_filtrado = df[col].isin(var)
            df = df.loc[df_filtrado , : ]
        elif var == 'Não':
            var = 0
            df_filtrado = df[col].isin(var)
            df = df.loc[df_filtrado , : ]
        else:
            df_filtrado = df[col].isin(var)
            df = df.loc[df_filtrado , : ]
    
    return df


def world_map( df ):
    df_aux = ( df.loc[ : , ['country_code','city','latitude','longitude']]
                  .groupby( ['country_code','city'] )
                  .median()
                  .reset_index() )
        
    mapa = folium.Map()


    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['latitude'] , 
                          location_info['longitude']]).add_to(mapa)

        
    return mapa

#=============================================================
#Import dataset
#=============================================================

df_raw = pd.read_csv('dataset/zomato.csv')

df = data_clean( df_raw )




#===================================
# Sidebar no Streamlit
#===================================


image2 = Image.open( 'logo_fome_zero_2.png' )
st.sidebar.image( image2, width=800,use_column_width='auto')
st.sidebar.write('<h2 style=\'text-align: center; color: #fe9666;\'>O melhor Marketplace, os melhores Restaurantes', unsafe_allow_html=True)

st.sidebar.markdown( """___""" )

st.sidebar.markdown( '## **Filtros:**' )

#st.sidebar.markdown( """___""" )
#qtd_slider = st.sidebar.slider(
#                '**Data:**',
#                value = pd.datetime(2022, 4 , 13),
#                min_value = pd.datetime(2022, 2, 11),
#                max_value = pd.datetime(2022, 4, 6),
#                format = 'DD-MM-YYYY'
#                )

#st.sidebar.markdown( """___""" )

country_options = st.sidebar.multiselect(
                '**Países:**',
                ['Australia', 'Brazil','Canada', 'England', 'India', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'United States of America'],
                default = ['Australia', 'Brazil','Canada', 'England', 'India', 'Indonesia', 'New Zeland', 'Philippines', 'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates', 'United States of America']
                        )


#st.sidebar.markdown( """___""" )

price_options = st.sidebar.multiselect(
                'Faixa de preço:',
                ['cheap', 'expensive', 'gourmet', 'normal'],
                default = ['cheap', 'expensive', 'gourmet', 'normal']
                        )

table_booking = st.sidebar.multiselect(
                'Restaurantes que fazem reserva:',
                ['Sim' , 'Não'],
                default = ['Sim' , 'Não']
                        )

online_deliver = st.sidebar.multiselect(
                'Restaurantes que aceitam pedidos online:',
                ['Sim' , 'Não'],
                default = ['Sim' , 'Não']
                        )

is_delivering = st.sidebar.multiselect(
                'Restaurantes que fazem entrega:',
                ['Sim' , 'Não'],
                default = ['Sim' , 'Não']
                        )


st.sidebar.markdown( """___""" )
st.sidebar.markdown( '### Powered by Pablo Carvalho' )

#Filtro de data
#filtro(df, tipo, col, var )
#df = filtro( df, 'slider', 'Order_Date', date_slider )

#Filtro de Países

df = filtro( df, 'multiselect', 'country_code', country_options )

#Filtro de Faixa de Preço

df = filtro( df, 'multiselect', 'price_range', price_options )

#Filtro de Reserva

df = filtro( df, 'multiselect', 'has_table_booking_cat', table_booking )

#Filtro de Pedido online

df = filtro( df, 'multiselect', 'has_online_delivery_cat', online_deliver )

#Filtro de faz entrega

df = filtro( df, 'multiselect', 'is_delivering_now_cat', is_delivering )



#===================================
# Layout no Streamlit
#===================================


image = Image.open( 'cover_fome_zero_2.png' )
st.image( image, width=600,use_column_width='None')
st.write('<h1 style=\'text-align: left; color: #101820;\'>📈 Visão Geral', unsafe_allow_html=True)


st.markdown('<h1 style=\'text-align: center; color: #fe5000;\'>Nossos números falam por si mesmo:', unsafe_allow_html=True)

with st.container():
    col1, col2, col3, col4, col5 = st.columns( 5 )
    with col1:
        qtd_paises = df['country_code'].nunique()
        st.write('<h6 style=\'text-align: center; color: #fe9666;\'>Quantidade de países em que estamos presente', unsafe_allow_html=True)
        st.write(f'<h2 style=\'text-align: center; color: #101820;\'>{qtd_paises}', unsafe_allow_html=True)
    with col2:
        qtd_city = df['city'].nunique()
        st.write('<h6 style=\'text-align: center; color: #fe9666;\'>Quantidade de cidades em que estamos presente', unsafe_allow_html=True)
        st.write(f'<h2 style=\'text-align: center; color: #101820;\'>{qtd_city}', unsafe_allow_html=True)
    with col3:
        qtd_restaurantes = df['restaurant_id'].nunique()
        st.write('<h6 style=\'text-align: center; color: #fe9666;\'>Total de restaurantes parceiros', unsafe_allow_html=True)
        st.write(f'<h2 style=\'text-align: center; color: #101820;\'>{qtd_restaurantes}', unsafe_allow_html=True)
    with col4:
        total_cuisines = df['cuisines'].nunique()
        st.write('<h6 style=\'text-align: center; color: #fe9666;\'>Quantidade de culinária diferentes que servimos', unsafe_allow_html=True)
        st.write(f'<h2 style=\'text-align: center; color: #101820;\'>{total_cuisines}', unsafe_allow_html=True)
    with col5:
        total_ratings = df['votes'].sum()
        st.write('<h6 style=\'text-align: center; color: #fe9666;\'>Total de avaliações enviadas', unsafe_allow_html=True)
        st.write(f'<h2 style=\'text-align: center; color: #101820;\'>{total_ratings}', unsafe_allow_html=True)
        
with st.container():
    st.markdown('''---''')
    st.markdown('<h2 style=\'text-align: left; color: #fe5000;\'>A FOME ZERO no mundo', unsafe_allow_html=True)
    st.write(f'<h4 style=\'text-align: right; color: #101820;\'>Nossos parceiros estão em todos os lugares', unsafe_allow_html=True)
    mapa = world_map( df )
    folium_static( mapa, width =1024 , height =800)