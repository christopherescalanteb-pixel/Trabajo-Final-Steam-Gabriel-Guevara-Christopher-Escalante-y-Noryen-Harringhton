import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Análisis de Datos de Steam", layout="wide")

st.title("🕹️ Análisis de Juegos de Steam: ¿Cuáles son los mejores juegos?")
st.write("Gabriel Guevara, Christopher Escalante y Noryen Harringhton") 
st.markdown("---")

@st.cache_data
def load_data():
     return pd.read_csv('steam_limpio_corregido.csv') 
steam_data = pd.read_csv("steam_limpio_corregido.csv")
steam_data['tipo_juego'] = pd.Categorical(steam_data['tipo_juego'], categories=['Indie', 'AAA'], ordered=True)

nombres_pestañas = [
    "📊 Indie vs AAA: Comparativa del Ratio de Reseñas Positivas", 
    "🌍 Retención Real: Free to Play vs Premium", 
    "🏷️  Impacto del Precio en la Valoración del Usuario",
    "📈 Concentración de Propietarios y Tiempo de Juego",
    "💻 Cuota de Mercado F2P vs Premium ",
     "💰 Precio vs Tiempo",
    "🔍 Accesibilidad",
    "📅  Estacionalidad de Lanzamientos"
    
]

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8,= st.tabs(nombres_pestañas)


with tab1:
    st.subheader("📊 Indie vs AAA: Comparativa del Ratio de Reseñas Positivas")
    
    
    df_filtrado_violin = steam_data[steam_data['tipo_juego'].isin(["Indie", "AAA"])]

    fig1 = px.violin(
        df_filtrado_violin,
        x="tipo_juego",
        y="ratio_positivo",
        color="tipo_juego",
        box=True,
        color_discrete_map={"Indie": "#2ca02c", "AAA": "#d62728"}
    )

    fig1.update_layout(
        title="¿Los Indie superan a los AAA en valoración?",
        xaxis_title="Tipo de juego",
        yaxis_title="Ratio de reseñas positivas",
        yaxis_tickformat=".0%"
    )

    st.plotly_chart(fig1, use_container_width=True)
    
    with st.expander("Ver detalles del gráfico"):
        st.markdown("Los juegos Indie muestran una mayor variabilidad en su ratio de reseñas positivas, con valores que van desde muy bajos hasta muy altos. Los AAA son más consistentes, con distribuciones más estrechas y generalmente altas. No se observa que los Indie superen claramente a los AAA, pero sí que algunos Indie alcanzan niveles de valoración tan altos como los mejores AAA.")


with tab2:
    st.subheader(nombres_pestañas[1])
    
    
    df_filtrado_dispersion = steam_data[
        (steam_data['owners_min'] > 0) & 
        (steam_data['average_playtime'] < 50000) & 
        (steam_data['modelo_negocio'].notna())
    ].copy()

    df_filtrado_dispersion['horas_juego'] = df_filtrado_dispersion['average_playtime'] / 60

    fig2 = px.scatter(
        df_filtrado_dispersion,
        x="owners_min",
        y="horas_juego",
        color="modelo_negocio",
        log_x=True,
        trendline="lowess",
        opacity=0.4,
        color_discrete_map={"Free to Play": "#4CAF50", "Premium": "#E53935"}
    )

    fig2.update_layout(
        template="plotly_dark",
        title="<b>Relación entre popularidad y retención</b>",
        xaxis_title="<b>Propietarios estimados (escala log)</b>",
        yaxis_title="<b>Tiempo promedio de juego (horas)</b>"
    )

    st.plotly_chart(fig2, use_container_width=True)
    with st.expander("Ver detalles del gráfico"):
        st.markdown("Los juegos Free to Play (F2P) muestran una retención mucho más alta a medida que crecen en popularidad, mientras que los Premium también retienen más cuando son exitosos, pero con una pendiente más suave. Esto sugiere que los gigantes F2P sí generan ecosistemas de altísima retención, típicos de juegos como servicio, pero no son los únicos: los Premium más exitosos también logran retención elevada, aunque con un patrón distinto.")


with tab3:
    st.subheader(nombres_pestañas[2])
    

    df_filtrado_box = steam_data[(steam_data['price'] > 0) & (steam_data['price'] <= 500)].copy()
    
    bins = [0, 5, 10, 20, 40, 60, 100, 500]
    etiquetas = ["0-5", "5-10", "10-20", "20-40", "40-60", "60-100", "100-500"]
    df_filtrado_box['price_bin'] = pd.cut(df_filtrado_box['price'], bins=bins, labels=etiquetas)

    fig3 = px.box(
        df_filtrado_box,
        x="price_bin",
        y="ratio_positivo",
        color="price_bin",
        
        color_discrete_sequence=["#B71C1C", "#E62424", "#E53935", "#FF5252", "#81C784", "#4CAF50", "#2E7D32"]
    )

    fig3.update_layout(
        template="plotly_dark",
        paper_bgcolor="#121212",
        plot_bgcolor="#1E1E1E",
        title={
            'text': "<b>Valoración según rangos de precio</b>",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, color="#E0E0E0")
        },
        xaxis_title="<b>Rango de precio (USD)</b>",
        yaxis_title="<b>Ratio de reseñas positivas</b>",
        yaxis=dict(
            tickformat=".0%",
            showgrid=True,
            gridcolor="#333333",
            zeroline=False
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        font=dict(
            family="Helvetica, Arial, sans-serif",
            size=12,
            color="#B0B0B0"
        ),
        showlegend=False,
        margin=dict(l=60, r=40, t=80, b=60)
    )

    
    st.plotly_chart(fig3, use_container_width=True)
    with st.expander("Ver detalles del gráfico"):
        st.markdown("El precio no determina la valoración. Los juegos baratos, medianos y caros tienen medianas muy parecidas. No se observa que los usuarios sean más críticos con los juegos caros, ni que los juegos de mayor precio reciban mejores reseñas.")

with tab4:
    st.subheader("📈 Concentración de Propietarios y Tiempo de Juego")
    

    col_izquierda, col_derecha = st.columns(2)
    
    
    with col_izquierda:
        
        top_propietarios = steam_data.nlargest(10, 'owners_avg').sort_values(by='owners_avg', ascending=False)

        fig_top = px.bar(
            top_propietarios,
            x="name",
            y="owners_avg",
            color="name",
            color_discrete_sequence=["#2E7D32", "#388E3C", "#4CAF50", "#66BB6A", "#81C784", "#E57373", "#EF5350", "#E53935", "#C62828", "#B71C1C"]
        )

        fig_top.update_layout(
            height=500, 
            template="plotly_dark",
            paper_bgcolor="#121212",
            plot_bgcolor="#1E1E1E",
            title={'text': "<b>Top 10 Juegos por Propietarios</b>", 'x': 0.5, 'xanchor': 'center'},
            xaxis_title="<b>Juego</b>",
            yaxis_title="<b>Propietarios (Promedio)</b>",
            showlegend=False,
            margin=dict(t=80, b=100, l=40, r=40)
        )

        
        st.plotly_chart(fig_top, use_container_width=True)
        
        
        st.markdown("El gráfico muestra una alta concentración de popularidad: pocos títulos acumulan la mayoría de propietarios. Esto describe el tamaño del mercado, pero no permite inferir compromiso ni tiempo de juego. Es un gráfico contextual, no explicativo.")
        

    
    with col_derecha:
        
        medianas = steam_data.groupby('owners_group', as_index=False)['median_playtime'].median()
        medianas.rename(columns={'median_playtime': 'mediana'}, inplace=True)
        orden_grupos = ["Menos de 1M", "1M - 5M", "5M - 10M", "10M - 20M", "20M+"]

        fig_median = px.bar(
            medianas,
            x="owners_group",
            y="mediana",
            color="owners_group",
            category_orders={"owners_group": orden_grupos},
            color_discrete_sequence=["#B71C1C", "#E53935", "#FF5252", "#81C784", "#2E7D32"]
        )

        fig_median.update_layout(
            height=500,
            template="plotly_dark",
            paper_bgcolor="#121212",
            plot_bgcolor="#1E1E1E",
            title={'text': "<b>Retención por Tamaño de Audiencia</b>", 'x': 0.5, 'xanchor': 'center'},
            xaxis_title="<b>Grupo de Propietarios</b>",
            yaxis_title="<b>Tiempo Mediano (minutos)</b>",
            showlegend=False,
            margin=dict(t=80, b=40, l=40, r=40)
        )
        
        fig_median.update_traces(texttemplate='%{y:,.0f}', textposition='outside')

        
        st.plotly_chart(fig_median, use_container_width=True)
        
        
        st.markdown("La mediana del tiempo de juego es similar en casi todos los grupos (200–350 min). Esto indica que el comportamiento típico del jugador no cambia significativamente según la popularidad del juego. El grupo 20M+ presenta una mediana mayor, pero esto se debe a títulos excepcionales, no a una tendencia general.")
        
        


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

    

            
