import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análisis de Datos de Steam", layout="wide")

st.title("🕹️ Análisis de Juegos de Steam: ¿Cuáles son los mejores juegos?")
st.write("Gabriel Guevara, Christopher Escalante y Noryen Harringhton") 
st.markdown("---")

@st.cache_data
def load_data():
     return pd.read_csv('steam_cleaned_full.csv') 
df = pd.read_csv('steam_cleaned_full.csv')
df['production_scale'] = pd.Categorical(df['production_scale'], categories=['Indie', 'AAA/AA'], ordered=True)

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


with tab1:
    st.subheader("📊 Distribución de Positividad")
    
    fig1 = px.violin(df, x='production_scale', y='positivity_ratio', color='production_scale',
                     box=True, points=False, template="plotly_dark",
                     color_discrete_map={'Indie': '#00CC96', 'AAA/AA': '#EF553B'},
                     title="Distribución de Positividad: Indie vs AAA/AA",
                     labels={'production_scale': 'Escala de Producción', 'positivity_ratio': 'Ratio de Positividad'})
    
    fig1.update_layout(title_font_size=20, margin=dict(t=60, b=40, l=40, r=40))
    
    st.plotly_chart(fig1, use_container_width=True)
    
    with st.expander("Ver detalles del gráfico"):
        st.markdown("""
        **GRÁFICO 1: Distribución de Positividad (Violín Estático)**
        - **Qué es:** Gráfico de densidad probabilística de la métrica de satisfacción.
        - **Qué se ve:** Concentración de calidad percibida por escala de producción corregida.
        - **Elementos:** Eje X (Escala), Eje Y (Positividad).
        """)

with tab2:
    st.subheader(nombres_pestañas[1])
    
    users_scale = df.groupby('production_scale', as_index=False)['owners_numeric'].sum()
    
    fig2 = px.bar(users_scale, x='production_scale', y='owners_numeric', color='production_scale',
                  template="plotly_dark", text_auto='.2s',
                  color_discrete_map={'Indie': '#00CC96', 'AAA/AA': '#EF553B'},
                  title="Usuarios Totales Acumulados: Indie vs AAA/AA",
                  labels={'production_scale': 'Escala de Producción', 'owners_numeric': 'Usuarios Totales'})
    
    fig2.update_traces(textposition='outside', textfont_size=14)
    fig2.update_layout(title_font_size=20, showlegend=False)
    

    st.plotly_chart(fig2, use_container_width=True)
    

    with st.expander("Ver detalles del gráfico"):
        st.markdown("""
        **GRÁFICO 2: Usuarios Totales Acumulados (Barras)**
        - **Qué es:** Volumen de mercado estático por escala.
        - **Qué se ve:** Distribución total de adopción.
        - **Elementos:** Eje X (Escala), Eje Y (Millones de usuarios).
        """)

with tab3:
    st.subheader(nombres_pestañas[2])
   
    fig3 = px.pie(df, names='type', values='owners_numeric', hole=0.6,
                  color='type', template="plotly_dark", 
                  color_discrete_sequence=["#00CC96", '#EF553B'],
                  title="Cuota de Mercado: F2P vs Premium (Total Usuarios)")
    fig3.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=16,
                       marker=dict(line=dict(color='#111111', width=2)))
    fig3.update_layout(title_font_size=20, annotations=[dict(text='Mercado', x=0.5, y=0.5, font_size=20, showarrow=False)])
    
    st.plotly_chart(fig3, use_container_width=True)
    
    with st.expander("Ver detalles del gráfico"):
        st.markdown("""
        **GRÁFICO 3: Cuota de Mercado F2P vs Premium (Dona)**
        - **Qué es:** Proporción de mercado estática.
        - **Qué se ve:** Distribución del volumen total de jugadores según modelo de monetización.
        """)

with tab4:
    st.subheader(nombres_pestañas[3])

    df_played = df[df['median_playtime_hours'] > 0].copy()
    df_played['primary_genre'] = df_played['genres'].apply(
        lambda x: str(x).replace(',', ';').split(';')[0].strip()
    )

    all_genres = df_played.groupby('primary_genre', as_index=False).agg(
        median_playtime=('median_playtime_hours', 'median')
    ).sort_values('median_playtime', ascending=False)

    custom_gradient = ['#EF553B', '#00CC96'] 

    fig5 = px.bar(
        all_genres, 
        x='primary_genre', 
        y='median_playtime', 
        color='median_playtime',
        color_continuous_scale=custom_gradient, # Aplicación del degradado
        template="plotly_dark", 
        text_auto='.1f',
        title="Retención de Jugadores: Todos los Géneros (Excluyendo inactivos)",
        labels={'primary_genre': 'Género Principal', 'median_playtime': 'Horas Medianas'}
    )

    fig5.update_traces(textposition='outside')
    fig5.update_layout(
        title_font_size=20, 
        xaxis_tickangle=-90, 
        coloraxis_showscale=False, 
        height=700,
        margin=dict(t=80, b=150)
    )

    st.plotly_chart(fig5, use_container_width=True)

    with st.expander("Ver detalles del gráfico"):
        st.markdown("""
        **GRÁFICO 5: Retención por Géneros (Barras)**
        - **Qué es:** Medición de retención basada en el tiempo de juego mediano.
        - **Qué se ve:** Qué géneros logran mantener a los usuarios jugando por más tiempo.
        - **Colores:** El degradado indica la intensidad de la retención (Verde = Mayor retención).
        """)

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

    

            
