from pdb import run
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Dashboard Analítico de Steam",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp {
        animation: fadeIn 1s ease-in-out;
    }
    div[role="tablist"] {
        animation: slideDown 0.5s ease-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    @keyframes slideDown {
        0% { transform: translateY(-20px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
<<<<<<< HEAD
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
    
=======
    df = pd.read_csv("steam_limpio_corregido.csv")
    df['tipo_juego'] = pd.Categorical(df['tipo_juego'], categories=['Indie', 'AA', 'AAA'], ordered=True)
    return df

try:
    steam_data = load_data()
except FileNotFoundError:
    st.error("Error crítico: Archivo 'steam_limpio_corregido.csv' no localizado.")
    st.stop()

st.sidebar.header("Filtros Globales")

generos = st.sidebar.multiselect(
    "Seleccionar Géneros",
    options=sorted(steam_data["genre_main"].unique()),
    default=sorted(steam_data["genre_main"].unique())
)

modelos = st.sidebar.multiselect(
    "Modelo de Negocio",
    options=steam_data["modelo_negocio"].unique(),
    default=steam_data["modelo_negocio"].unique()
)

df_filtrado = steam_data[
    (steam_data["genre_main"].isin(generos)) &
    (steam_data["modelo_negocio"].isin(modelos))
>>>>>>> 1d14ff1 (dashboard modificado, añadida side bar con filtros por genero y modelo de negocio, organizacion de los datasets en carpetas separadas, columnas de metricas dinamicas)
]

def formato_corto(n):
    if n >= 1e9:
        return f"{n / 1e9:.1f}B"
    elif n >= 1e6:
        return f"{n / 1e6:.1f}M"
    elif n >= 1e3:
        return f"{n / 1e3:.1f}K"
    return f"{n:.0f}"

st.title("Dashboard del Análisis de Mercado: Videojuegos en la Plataforma Steam")
st.markdown("""
**Autores:** Christopher Escalante, Gabriel Guevara, Noryen Harringhton | **Asignatura:** Computación I  
**Institución:** Universidad Central de Venezuela, Facultad de Ciencias Económicas y Sociales
""")
st.divider()

st.markdown("### KPI'S Clave del Mercado de Videojuegos en Steam")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_owners = df_filtrado["owners_avg"].sum()
    st.metric("Alcance Total", formato_corto(total_owners))

with col2:
    avg_ratio = df_filtrado["ratio_positivo"].mean()
    st.metric("Satisfacción Media", f"{avg_ratio:.1%}")

with col3:
    avg_playtime = df_filtrado["median_playtime"].mean()
    st.metric("Retención Promedio", f"{avg_playtime:,.0f} min")

with col4:
    avg_price = df_filtrado["price"].mean()
    st.metric("Precio Promedio", f"${avg_price:.2f}")

with col5:
    total_games = len(df_filtrado)
    st.metric("Títulos", formato_corto(total_games))

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. Indie vs AAA", 
    "2. F2P vs Premium", 
    "3. Precio vs Valoración", 
    "4. Propietarios", 
    "5. Multiplataforma", 
    "6. Nichos"
])

layout_estandar = dict(
    template="plotly_dark", 
    paper_bgcolor="rgba(0,0,0,0)", 
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Helvetica, Arial, sans-serif", size=14, color="#E0E0E0"),
    margin=dict(t=40, b=40, l=40, r=40)
)

with tab1:
<<<<<<< HEAD
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

=======
    st.header("¿Los Indie superan a los AAA en valoración?")
    
    df_filtrado_violin = df_filtrado[df_filtrado['tipo_juego'].isin(["Indie", "AAA"])]

    if not df_filtrado_violin.empty:
        fig1 = px.violin(
            df_filtrado_violin,
            x="tipo_juego",
            y="ratio_positivo",
            color="tipo_juego",
            box=True,
            color_discrete_map={"Indie": "#2ca02c", "AAA": "#d62728"}
        )

        fig1.update_layout(
            **layout_estandar,
            xaxis_title="Tipo de juego",
            yaxis_title="Ratio de reseñas positivas",
            yaxis_tickformat=".0%"
        )
        
        st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    **Interpretación:**
    Los juegos Indie muestran una mayor variabilidad en su ratio de reseñas positivas, con valores que van desde muy bajos hasta muy altos. 
    Los AAA son más consistentes, con distribuciones más estrechas y generalmente altas. 
    No se observa que los Indie superen claramente a los AAA, pero sí que algunos Indie alcanzan niveles de valoración tan altos como los mejores AAA.
    """)

with tab2:
    st.header("Relación entre popularidad y retención")

    df_t2 = df_filtrado[
        (df_filtrado['owners_min'] > 0) & 
        (df_filtrado['average_playtime'] < 50000) & 
        (df_filtrado['modelo_negocio'].notna())
    ].copy()

    df_t2['horas_juego'] = df_t2['average_playtime'] / 60

    if not df_t2.empty:
        fig2 = px.scatter(
            df_t2,
            x="owners_min",
            y="horas_juego",
            color="modelo_negocio",
            log_x=True,
            trendline="lowess",
            opacity=0.4,
            color_discrete_map={"Free to Play": "#4CAF50", "Premium": "#E53935"}
        )

        fig2.update_layout(
            **layout_estandar,
            xaxis_title="Propietarios estimados (escala log)",
            yaxis_title="Tiempo promedio de juego (horas)",
            yaxis=dict(range=[0, 800], showgrid=True, gridcolor="#333333"),
            xaxis=dict(showgrid=True, gridcolor="#333333"),
            legend_title_text="Modelo de negocio"
        )

        fig2.update_traces(
            selector=dict(mode='markers'),
            marker=dict(size=4)
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **Interpretación:**
    Los juegos Free to Play (F2P) muestran una retención mucho más alta a medida que crecen en popularidad, mientras que los Premium también retienen más cuando son exitosos, pero con una pendiente más suave. Esto sugiere que los gigantes F2P sí generan ecosistemas de altísima retención, típicos de juegos como servicio, pero no son los únicos: los Premium más exitosos también logran retención elevada, aunque con un patrón distinto.
    """)

with tab3:
    st.header("Valoración según rangos de precio")

    df_t3 = df_filtrado[(df_filtrado['price'] > 0) & (df_filtrado['price'] <= 500)].copy()
    
    bins = [0, 5, 10, 20, 40, 60, 100, 500]
    etiquetas = ["0-5", "5-10", "10-20", "20-40", "40-60", "60-100", "100-500"]
    df_t3['price_bin'] = pd.cut(df_t3['price'], bins=bins, labels=etiquetas)

    if not df_t3.empty:
        fig3 = px.box(
            df_t3,
            x="price_bin",
            y="ratio_positivo",
            color="price_bin",
            color_discrete_sequence=["#B71C1C", "#E62424", "#E53935", "#FF5252", "#81C784", "#4CAF50", "#2E7D32"]
        )

        fig3.update_layout(
            **layout_estandar,
            xaxis_title="Rango de precio (USD)",
            yaxis_title="Ratio de reseñas positivas",
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
            showlegend=False
        )

        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    **Interpretación:**
    El precio no determina la valoración. Los juegos baratos, medianos y caros tienen medianas muy parecidas. 
    No se observa que los usuarios sean más críticos con los juegos caros, ni que los juegos de mayor precio reciban mejores reseñas. 
    La satisfacción se mantiene constante independientemente del desembolso económico del usuario.
    """)

with tab4:
    st.header("Análisis de Volumen y Retención por Segmento")
>>>>>>> 1d14ff1 (dashboard modificado, añadida side bar con filtros por genero y modelo de negocio, organizacion de los datasets en carpetas separadas, columnas de metricas dinamicas)
    
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Top 10: Volumen de Mercado")
        
        top_propietarios = df_filtrado.nlargest(10, 'owners_avg').sort_values(by='owners_avg', ascending=False)
        
        if not top_propietarios.empty:
            fig4_a = px.bar(
                top_propietarios,
                x="name",
                y="owners_avg",
                color="name",
                color_discrete_sequence=["#2E7D32", "#388E3C", "#4CAF50", "#66BB6A", "#81C784", 
                                          "#E57373", "#EF5350", "#E53935", "#C62828", "#B71C1C"]
            )

            fig4_a.update_layout(
                **layout_estandar,
                xaxis_title="Juego",
                yaxis_title="Propietarios estimados",
                yaxis=dict(tickformat=","),
                xaxis=dict(tickangle=-45),
                showlegend=False,
                height=500 
            )
            
            st.plotly_chart(fig4_a, use_container_width=True)
            
            st.markdown("""
            **Interpretación:**
            Este gráfico identifica los "titanes" del segmento seleccionado. Existe una alta concentración de usuarios en pocos títulos; sin embargo, un gran volumen de propietarios no siempre garantiza una alta retención individual.
            """)

    with col_b:
        st.subheader("Profundidad de Consumo")
        
        medianas = df_filtrado.groupby('owners_group', as_index=False)['median_playtime'].median()
        medianas.rename(columns={'median_playtime': 'mediana'}, inplace=True)

        orden_grupos = ["Menos de 1M", "1M - 5M", "5M - 10M", "10M - 20M", "20M+"]

        if not medianas.empty:
            fig4_b = px.bar(
                medianas,
                x="owners_group",
                y="mediana",
                color="owners_group",
                category_orders={"owners_group": orden_grupos},
                color_discrete_sequence=["#B71C1C", "#E53935", "#FF5252", "#81C784", "#2E7D32"]
            )

            fig4_b.update_layout(
                **layout_estandar,
                xaxis_title="Grupo de propietarios",
                yaxis_title="Tiempo mediano (minutos)",
                yaxis=dict(tickformat=","),
                showlegend=False,
                height=500
            )

            fig4_b.update_traces(
                texttemplate='%{y:,.0f}',
                textposition='outside'
            )
            
            st.plotly_chart(fig4_b, use_container_width=True)
            
            st.markdown("""
            **Interpretación:**
            Existe una correlación positiva clara: a mayor número de propietarios, mayor es el tiempo mediano de juego. Esto valida que los juegos con comunidades masivas logran ciclos de vida más largos y mayor compromiso.
            """)