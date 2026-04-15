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

with tab5:
    st.header("Impacto del Soporte Multiplataforma en el Rendimiento")

    agrupacion = df_filtrado.groupby('multiplataforma').agg(
        owners_avg_mean=('owners_avg', 'mean'),
        ratio_pos_mean=('ratio_positivo', 'mean')
    ).reset_index()

    if not agrupacion.empty:
        colores_t5 = {'Multiplataforma': '#4CAF50', 'Solo Windows': '#E53935'}
        fig5 = make_subplots(rows=1, cols=2, subplot_titles=("Ventas estimadas", "Críticas positivas"))

        for plataforma in agrupacion['multiplataforma']:
            df_sub = agrupacion[agrupacion['multiplataforma'] == plataforma]
            
            fig5.add_trace(
                go.Bar(
                    x=df_sub['multiplataforma'],
                    y=df_sub['owners_avg_mean'],
                    text=df_sub['owners_avg_mean'],
                    texttemplate='%{text:,.0f}',
                    textposition='outside',
                    marker_color=colores_t5[plataforma],
                    showlegend=False
                ),
                row=1, col=1
            )
            
            fig5.add_trace(
                go.Bar(
                    x=df_sub['multiplataforma'],
                    y=df_sub['ratio_pos_mean'],
                    text=df_sub['ratio_pos_mean'],
                    texttemplate='%{text:.1%}',
                    textposition='outside',
                    marker_color=colores_t5[plataforma],
                    showlegend=False
                ),
                row=1, col=2
            )

        fig5.update_layout(**layout_estandar)
        fig5.update_yaxes(title_text="Promedio de propietarios", showgrid=True, gridcolor="#333333", row=1, col=1)
        fig5.update_yaxes(title_text="Ratio de reseñas", tickformat=".0%", showgrid=True, gridcolor="#333333", row=1, col=2)
        
        st.plotly_chart(fig5, use_container_width=True)

        try:
            val_ventas_multi = agrupacion.loc[agrupacion['multiplataforma'] == 'Multiplataforma', 'owners_avg_mean'].values[0]
            val_ventas_win = agrupacion.loc[agrupacion['multiplataforma'] == 'Solo Windows', 'owners_avg_mean'].values[0]
            incremento_ventas = (val_ventas_multi - val_ventas_win) / val_ventas_win
            
            st.markdown(f"""
            *Interpretación:*
            Los resultados demuestran que los títulos multiplataforma superan significativamente a los exclusivos de Windows en ambas métricas. 
            Específicamente, presentan un incremento del *{incremento_ventas:.1%}* en el promedio de propietarios estimados y una mayor aceptación crítica, 
            lo que sugiere que la accesibilidad técnica es un factor determinante para el alcance masivo y la satisfacción del usuario.
            """)
        except IndexError:
            st.info("Filtre ambos estados de plataforma para visualizar la comparativa de incremento.") 


with tab6:
    st.header("Identificación de Nichos de Oportunidad")

    combo = df_filtrado.groupby(['genre_main', 'tipo_juego']).agg(
        n_juegos=('tipo_juego', 'count'),
        ratio_prom=('ratio_positivo', 'mean')
    ).reset_index()

    combo['indice_oportunidad'] = combo['ratio_prom'] / np.log(combo['n_juegos'] + 1)

    combo['combo_label'] = combo['genre_main'].astype(str) + " - " + combo['tipo_juego'].astype(str)
    
    combo_top15 = combo.nlargest(15, 'indice_oportunidad').sort_values(by='indice_oportunidad', ascending=True)

    if not combo_top15.empty:
        fig6 = px.bar(
            combo_top15,
            x="indice_oportunidad",
            y="combo_label",
            color="tipo_juego",
            orientation='h',
            color_discrete_map={"Indie": "#4CAF50", "AAA": "#E53935", "AA": "#F1F106"}
        )

        fig6.update_layout(
            **layout_estandar,
            xaxis_title="Índice de oportunidad",
            yaxis_title="Combinación Género - Categoría",
            legend_title_text="Categoría",
            height=700
        )
        
        st.plotly_chart(fig6, use_container_width=True)

        st.markdown("""
        *Interpretación:*
        El Índice de Oportunidad destaca segmentos donde existe una alta satisfacción del usuario con una competencia relativamente baja. 
        Las primeras posiciones representan nichos con alto potencial estratégico, ya que la demanda no está saturada por una oferta excesiva de títulos.
        """)           