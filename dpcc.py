import streamlit as st 
import pandas as pd



import seaborn as sns
import numpy as np
import datetime as datetime
from dateutil.relativedelta import relativedelta # to add days or years

from matplotlib import pyplot as plt
import plotly.express as px

import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

st.write("""
# Dinámica Inmobiliaria en King County 
## Propuesto por
#### Edison Fabián Rubio Torres
""")

st.write('Este dashboard tiene por objevito presentar rápida y fácilmente la información derivada del estudio de la dinámica inmobiliaria en King Count, WA (USA). Los datos están disponibles [aquí](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction) ')

#data = pd.read_csv( 'data/kc_house_data.csv' )
@st.cache
def get_data():
     url = 'https://raw.githubusercontent.com/Fnz19/Entregable_Diplomado_ciencia_de_Datos/master/data/kc_house_data.csv'
     return pd.read_csv(url)

data = get_data()
#st.dataframe(data)



st.title('Filtros')
##forma de seleccionarlos los datos para el filtro







OptFiltro = st.multiselect(
     'Variables a incluir en los filtros:',
     ['Habitaciones', 'Precio', 'Baños', 'Área construida (pies cuadrados)','Pisos','Vista al agua','Evaluación de la propiedad','Condición'],
     ['Precio'])

if 'Precio' in OptFiltro: 
     if data['price'].min() < data['price'].max():
          min_price, max_price = st.sidebar.select_slider(
          'Rango de precio',
          options=list(sorted(set(data['price']))),
          value=(data['price'].min(),data['price'].max()))
          data = data[(data['price']>= min_price)&(data['price']<= max_price)]
    

if 'Habitaciones' in OptFiltro: 
     if data['bedrooms'].min() < data['bedrooms'].max():
          max_habs = st.select_slider(
          'Número de Habitaciones',
          options=list(sorted(set(data['bedrooms']))),
          value=(data['bedrooms'].max()))
          data = data[(data['bedrooms']>= max_habs)]
    
     
if 'Baños' in OptFiltro: 
     if data['bathrooms'].min() < data['bathrooms'].max():
          min_banhos, max_banhos = st.select_slider(
          'Número de baños ',
          options=list(sorted(set(data['bathrooms']))),
          value=(data['bathrooms'].min(), data['bathrooms'].max()))
          data = data[(data['bathrooms']>= min_banhos)&(data['bathrooms']<= max_banhos)]
    
    

if 'Pisos' in OptFiltro: 
     if data['floors'].min() < data['floors'].max():
          min_pisos, max_pisos = st.select_slider(
          'Número de Pisos',
          options=list(sorted(set(data['floors']))),
          value=(data['floors'].min(),data['floors'].max()))
          data = data[(data['floors']>= min_pisos)&(data['floors']<= max_pisos)]
     

if 'Vista al agua' in OptFiltro: 
     if data['view'].min() < data['view'].max():
          min_vista, max_vista = st.select_slider(
          'Puntaje de vista al agua',
          options=list(sorted(set(data['view']))),
          value=(data['view'].min(),data['view'].max()))
          data = data[(data['view']>= min_vista)&(data['view']<= max_vista)]
     
if 'Evaluación de la propiedad' in OptFiltro:
     if data['grade'].min() < data['grade'].max():
          min_cond, max_cond = st.select_slider(
          'Índice de evaluación de la propiedad',
          options=list(sorted(set(data['grade']))),
          value=(data['grade'].min(),data['grade'].max()))
          data = data[(data['grade']>= min_cond)&(data['grade']<= max_cond)]
     

if 'Condición' in OptFiltro:
     if data['condition'].min() < data['condition'].max():
          min_condi, max_condi = st.select_slider(
          'Condición de la propiedad',
          options=list(sorted(set(data['condition']))),
          value=(data['condition'].min(),data['condition'].max()))
          data = data[(data['condition']>= min_condi)&(data['condition']<= max_condi)]
     





mapa = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=9)
markercluster = MarkerCluster().add_to(mapa)
for nombre, fila in data.iterrows():
    folium.Marker([fila['lat'],fila['long']],
                popup = 'Precio: ${}, \n Fecha: {} \n {} habitaciones \n {} baños \n constuida en {} \n Precio por pie cuadrado: {}'.format(
                  fila['price'],
                  fila['date'],
                  fila['bedrooms'],
                  fila['bathrooms'],
                  fila['yr_built'], 
                  fila['sqft_living'])
    ).add_to(markercluster)
folium_static(mapa)


# Estadística Descriptiva 
att_num = data.select_dtypes(include = ['int64','float64'])
media = pd.DataFrame(att_num.apply(np.mean))
mediana = pd.DataFrame(att_num.apply(np.median))
std = pd.DataFrame(att_num.apply(np.std))
maximo = pd.DataFrame(att_num.apply(np.max))
minimo = pd.DataFrame(att_num.apply(np.min))
df_EDA = pd.concat([minimo,media,mediana,maximo,std], axis = 1)
df_EDA.columns = ['Mínimo','Media','Mediana','Máximo','std']
st.header('Datos descriptivos')
df_EDA = df_EDA.drop(index =['id', 'lat', 'long','yr_built','yr_renovated'], axis = 0 )

df_EDA.index =['Precio','No. Cuartos', 'No. Baños', 'Área construida (pies cuadrados)', 
                    'Área del terreno (pies cuadrados)', 'No. pisos', 'Vista agua (dummy)',
                    'Puntaje de la vista', 'Condición','Evaluación propiedad (1-13)',
                    'Área sobre tierra', 'Área sótano', 'Área construída 15 casas más próximas', 
                    'Área del terreno 15 casas más próximas', 'Precio por pie cuadrado']
col1, col2 = st.columns(2)
col1.metric("No. Casas", data.shape[0],str(100*round(data.shape[0]/data_ref.shape[0],4))+'% de las casas disponibles',delta_color="off")
#col2.metric("No. Casas Nuevas (Construida después de 1990)",data[data['house_age'] == 'new_house'].shape[0],str(100*round(data[data['house_age'] == 'new_house'].shape[0]/data_ref.shape[0],4))+'% de las casas disponibles',delta_color="off")
st.dataframe(df_EDA)  