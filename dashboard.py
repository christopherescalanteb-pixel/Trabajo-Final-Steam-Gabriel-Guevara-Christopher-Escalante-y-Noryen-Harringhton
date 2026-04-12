import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Análisis de Datos de Steam", layout="wide")

# 2. Título principal con imagen relacionada
#st.image("http://googleusercontent.com/image_collection/image_retrieval/681894429186253607_0", use_container_width=True)
st.title("🕹️ Dashboard de Análisis de Steam")
st.write("Gabriel Guevara, Christopher Escalante y Noryen Harringhton") 
st.markdown("---")

#3. Carga de datos
@st.cache_data
def load_data():
     return pd.read_csv('steam_cleaned_full.csv') 
df = pd.read_csv('steam_cleaned_full.csv')
df['production_scale'] = pd.Categorical(df['production_scale'], categories=['Indie', 'AAA/AA'], ordered=True)


# 4. Creación de las 9 pestañas

nombres_pestañas = [
    "📊 Distribución de Positividad", 
    "🌍 Usuarios Totales Acumulados", 
    "💻 Cuota de Mercado F2P vs Premium ",
    "💰 Precio vs Tiempo",
    "🏷️  Retención por Géneros",
    "📈 Evolución de Ventas Mensuales por Año" ,
    "🔍 Accesibilidad",
    "📅  Estacionalidad de Lanzamientos"
    
]

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8,= st.tabs(nombres_pestañas)

# 4. Organización del contenido por pestaña

with tab1:
    st.subheader(nombres_pestañas[0])
    
    st.info("Contenido del gráfico 1...")

with tab2:
    st.subheader(nombres_pestañas[1])
    
    st.info("Contenido del gráfico 2...")

with tab3:
    st.subheader(nombres_pestañas[2])
   
    st.info("Contenido del gráfico 3...")

with tab4:
    st.subheader(nombres_pestañas[3])
    st.info("Contenido del gráfico 4...")

with tab5:
    st.subheader(nombres_pestañas[4])
    st.info("Contenido del gráfico 5...")

with tab6:
    st.subheader(nombres_pestañas[5])
    st.info("Contenido del gráfico 6...")

with tab7:
    st.subheader(nombres_pestañas[6])
    st.info("Contenido del gráfico 7...")

with tab8:
    st.subheader(nombres_pestañas[7])
    st.info("Contenido del gráfico 8...")

    

            
