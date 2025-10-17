import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="🥔 DCA Papa - Fertilización", layout="wide", page_icon="🥔", initial_sidebar_state="expanded")

# CSS personalizado - Diseño TIPO DASHBOARD
st.markdown("""
<style>
    /* Fondo principal */
    .main {
        background: #f5f5f5;
    }
    
    /* Cards con sombra */
    .card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Botones personalizados */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #4caf50, #8bc34a);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(76, 175, 80, 0.3);
    }
    
    /* Métricas */
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        color: #2e7d32;
    }
    
    /* Tabs personalizados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #e8f5e9;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #66bb6a;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# HEADER TIPO BANNER
st.markdown("""
<div style='background: linear-gradient(90deg, #2e7d32 0%, #4caf50 50%, #66bb6a 100%);
            padding: 10px 30px;
            color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h1 style='margin: 0; font-size: 28px;'>🥔 Sistema de Análisis Estadístico - Fertilización Papa</h1>
            <p style='margin: 5px 0 0 0; opacity: 0.9;'>Diseño Completamente al Azar (DCA)</p>
        </div>
        <div style='text-align: right; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 8px;'>
            <p style='margin: 0; font-size: 14px;'>👨‍🎓 Sergio Ronald Quispe Calsin</p>
            <p style='margin: 0; font-size: 16px; font-weight: bold;'>📋 Código: 221235</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# SIDEBAR CON DISEÑO DE MENÚ LATERAL
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(180deg, #4caf50, #66bb6a); 
                border-radius: 12px; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0; font-size: 48px;'>🥔</h1>
        <h3 style='color: white; margin: 10px 0 0 0;'>Panel de Control</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Navegación Principal")
    pagina = st.radio(
        "Seleccione:",
        ["🏠 Dashboard", "📊 Análisis por Modelo", "📈 Comparativa Global", "ℹ️ Información"],
        label_visibility="collapsed"
    )
    
    if pagina == "📊 Análisis por Modelo":
        st.markdown("---")
        st.markdown("#### Seleccione Modelo:")
        modelo = st.selectbox(
            "Modelo:",
            ["M1: Balanceado (60)", "M2: No Balanceado (68)", 
             "M3: Bal-Bal Submuestreo", "M4: Bal-NoBal Submuestreo",
             "M5: NoBal-Bal Submuestreo", "M6: Completamente Desbal."],
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    st.markdown("""
    <div style='background: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50;'>
        <p style='margin: 0; font-size: 12px; color: #2e7d32;'>
            <b>💡 Tip:</b> Navega por las diferentes secciones para explorar los análisis completos
        </p>
    </div>
    """, unsafe_allow_html=True)

# Funciones de generación de datos (mismas)
def generar_datos_modelo(semilla, medias, desv, n_dict=None):
    np.random.seed(semilla)
    datos = []
    
    if n_dict is None:
        n_dict = {t: 15 for t in medias.keys()}
    
    for trat in medias.keys():
        for i in range(n_dict[trat]):
            rendimiento = np.random.normal(medias[trat], desv[trat])
            datos.append({
                "ID": f"{trat}-{i+1:03d}",
                "Tratamiento": trat,
                "Rendimiento_kg_ha": round(rendimiento, 1)
            })
    return pd.DataFrame(datos)

def obtener_datos_modelo(numero):
    configs = {
        1: (100, {"T1": 32000, "T2": 28000, "T3": 35000, "T4": 30000}, 
            {"T1": 2500, "T2": 2800, "T3": 2200, "T4": 2600}, None),
        2: (200, {"T1": 31500, "T2": 29000, "T3": 36000, "T4": 31000},
            {"T1": 3000, "T2": 2900, "T3": 2400, "T4": 2700},
            {"T1": 14, "T2": 18, "T3": 16, "T4": 20}),
        3: (300, {"T1": 32500, "T2": 28500, "T3": 35500, "T4": 30500},
            {"T1": 2000, "T2": 2200, "T3": 1800, "T4": 2100}, None),
        4: (400, {"T1": 31800, "T2": 29500, "T3": 36500, "T4": 31500},
            {"T1": 2100, "T2": 2300, "T3": 1900, "T4": 2200}, None),
        5: (500, {"T1": 32200, "T2": 28800, "T3": 35800, "T4": 30800},
            {"T1": 2050, "T2": 2250, "T3": 1850, "T4": 2150}, None),
        6: (600, {"T1": 31000, "T2": 30000, "T3": 37000, "T4": 32000},
            {"T1": 2300, "T2": 2500, "T3": 2000, "T4": 2400}, None)
    }
    return generar_datos_modelo(*configs[numero])

def calcular_anova_simple(df):
    grupos = [df[df['Tratamiento'] == t]['Rendimiento_kg_ha'].values 
              for t in df['Tratamiento'].unique()]
    f_stat, p_value = stats.f_oneway(*grupos)
    
    n_total = len(df)
    k = len(df['Tratamiento'].unique())
    grand_mean = df['Rendimiento_kg_ha'].mean()
    
    ss_total = ((df['Rendimiento_kg_ha'] - grand_mean) ** 2).sum()
    ss_between = sum([len(df[df['Tratamiento'] == t]) * 
                      (df[df['Tratamiento'] == t]['Rendimiento_kg_ha'].mean() - grand_mean) ** 2 
                      for t in df['Tratamiento'].unique()])
    ss_within = ss_total - ss_between
    
    df_between = k - 1
    df_within = n_total - k
    
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    
    return {
        'F': f_stat, 'P': p_value, 'SS_B': ss_between, 'SS_W': ss_within,
        'SS_T': ss_total, 'DF_B': df_between, 'DF_W': df_within,
        'MS_B': ms_between, 'MS_W': ms_within
    }

# ==================== DASHBOARD PRINCIPAL ====================
if pagina == "🏠 Dashboard":
    
    # CARDS DE INFORMACIÓN
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #66bb6a, #81c784); padding: 20px; border-radius: 12px; text-align: center;'>
            <h3 style='color: white; margin: 0;'>🧪</h3>
            <h2 style='color: white; margin: 10px 0;'>4</h2>
            <p style='color: white; margin: 0; opacity: 0.9;'>Tratamientos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4caf50, #66bb6a); padding: 20px; border-radius: 12px; text-align: center;'>
            <h3 style='color: white; margin: 0;'>📊</h3>
            <h2 style='color: white; margin: 10px 0;'>6</h2>
            <p style='color: white; margin: 0; opacity: 0.9;'>Modelos DCA</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #388e3c, #4caf50); padding: 20px; border-radius: 12px; text-align: center;'>
            <h3 style='color: white; margin: 0;'>📈</h3>
            <h2 style='color: white; margin: 10px 0;'>kg/ha</h2>
            <p style='color: white; margin: 0; opacity: 0.9;'>Variable</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #2e7d32, #388e3c); padding: 20px; border-radius: 12px; text-align: center;'>
            <h3 style='color: white; margin: 0;'>🎯</h3>
            <h2 style='color: white; margin: 10px 0;'>ANOVA</h2>
            <p style='color: white; margin: 0; opacity: 0.9;'>Análisis</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # SECCIÓN DE TRATAMIENTOS
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h3 style='color: #2e7d32; margin-top: 0; border-bottom: 3px solid #4caf50; padding-bottom: 10px;'>
                🌱 Tratamientos Experimentales
            </h3>
        """, unsafe_allow_html=True)
        
        tratamientos = [
            {"icon": "🧪", "codigo": "T1", "nombre": "NPK Químico", "desc": "120-80-100 kg/ha"},
            {"icon": "🌿", "codigo": "T2", "nombre": "Orgánico", "desc": "Compost + Humus"},
            {"icon": "⚖️", "codigo": "T3", "nombre": "Mixto", "desc": "50% Químico + 50% Orgánico"},
            {"icon": "🦠", "codigo": "T4", "nombre": "Biofertilizante", "desc": "Microorganismos eficientes"}
        ]
        
        for t in tratamientos:
            st.markdown(f"""
            <div style='background: #f1f8e9; padding: 15px; margin: 10px 0; border-radius: 8px; 
                        border-left: 5px solid #4caf50;'>
                <div style='display: flex; align-items: center;'>
                    <span style='font-size: 32px; margin-right: 15px;'>{t['icon']}</span>
                    <div style='flex: 1;'>
                        <h4 style='margin: 0; color: #2e7d32;'>{t['codigo']}: {t['nombre']}</h4>
                        <p style='margin: 5px 0 0 0; color: #558b2f; font-size: 14px;'>{t['desc']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h3 style='color: #2e7d32; margin-top: 0;'>📋 Objetivo</h3>
            <p style='color: #555; line-height: 1.6;'>
                Determinar el <b style='color: #2e7d32;'>fertilizante más efectivo</b> 
                para maximizar el rendimiento del cultivo de papa.
            </p>
            <hr style='border: 1px solid #e0e0e0;'>
            <h4 style='color: #2e7d32;'>📊 Variable</h4>
            <p style='color: #555;'>Rendimiento (kg/ha)</p>
            <hr style='border: 1px solid #e0e0e0;'>
            <h4 style='color: #2e7d32;'>🔬 Diseño</h4>
            <p style='color: #555;'>Completamente al Azar</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # VISTA RÁPIDA DE MODELOS
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <h3 style='color: #2e7d32; margin-top: 0;'>📊 Modelos Disponibles</h3>
    """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    modelos_info = [
        ("M1", "Balanceado", "60 parcelas (15×4)", "#66bb6a"),
        ("M2", "No Balanceado", "68 parcelas", "#4caf50"),
        ("M3", "Bal-Bal Sub", "20 lotes, 4 parc/lote", "#388e3c"),
        ("M4", "Bal-NoBal Sub", "20 lotes, var parc", "#2e7d32"),
        ("M5", "NoBal-Bal Sub", "Lotes var, 4 parc", "#1b5e20"),
        ("M6", "Desbalanceado", "Estructura variable", "#33691e")
    ]
    
    for i, (cod, nombre, desc, color) in enumerate(modelos_info):
        with cols[i % 3]:
            st.markdown(f"""
            <div style='background: {color}; padding: 15px; border-radius: 8px; margin-bottom: 15px; text-align: center;'>
                <h3 style='color: white; margin: 0;'>{cod}</h3>
                <p style='color: white; margin: 8px 0; font-size: 16px; font-weight: bold;'>{nombre}</p>
                <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 13px;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== ANÁLISIS POR MODELO ====================
elif pagina == "📊 Análisis por Modelo":
    
    num_modelo = int(modelo.split(":")[0][1])
    df = obtener_datos_modelo(num_modelo)
    anova = calcular_anova_simple(df)
    
    # HEADER DEL MODELO
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #4caf50, #66bb6a); 
                padding: 20px 30px; border-radius: 12px; margin-bottom: 25px;'>
        <h2 style='color: white; margin: 0;'>{modelo}</h2>
        <p style='color: white; margin: 5px 0 0 0; opacity: 0.9;'>
            📊 {len(df)} observaciones | 🧪 {df['Tratamiento'].nunique()} tratamientos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # PESTAÑAS CON DISEÑO LIMPIO
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Datos", "🧮 ANOVA", "📊 Visualización", "💾 Exportar"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📊 Tabla de Datos")
            st.dataframe(df, use_container_width=True, height=400)
        
        with col2:
            st.markdown("#### 📈 Estadísticas")
            stats_df = df.groupby('Tratamiento')['Rendimiento_kg_ha'].agg(['count', 'mean', 'std']).round(1)
            stats_df.columns = ['n', 'Media', 'DE']
            st.dataframe(stats_df, use_container_width=True)
            
            st.markdown("#### 🎯 Resumen")
            mejor = df.groupby('Tratamiento')['Rendimiento_kg_ha'].mean().idxmax()
            mejor_val = df.groupby('Tratamiento')['Rendimiento_kg_ha'].mean().max()
            st.success(f"**Mejor:** {mejor}")
            st.metric("Rendimiento", f"{mejor_val:.0f} kg/ha")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Tabla ANOVA")
            anova_table = pd.DataFrame({
                'Fuente': ['Tratamientos', 'Error', 'Total'],
                'SC': [f"{anova['SS_B']:.1f}", f"{anova['SS_W']:.1f}", f"{anova['SS_T']:.1f}"],
                'GL': [anova['DF_B'], anova['DF_W'], anova['DF_B'] + anova['DF_W']],
                'CM': [f"{anova['MS_B']:.1f}", f"{anova['MS_W']:.1f}", '-'],
                'F': [f"{anova['F']:.3f}", '-', '-'],
                'P-valor': [f"{anova['P']:.4f}", '-', '-']
            })
            st.dataframe(anova_table, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### 🎯 Resultado")
            if anova['P'] < 0.05:
                st.success("✅ **SIGNIFICATIVO**")
                st.write(f"p-valor = {anova['P']:.4f} < 0.05")
                st.write("Existen diferencias entre tratamientos")
            else:
                st.warning("⚠️ **NO SIGNIFICATIVO**")
                st.write(f"p-valor = {anova['P']:.4f} ≥ 0.05")
            
            st.markdown("#### 📊 Estadístico F")
            st.metric("Valor F", f"{anova['F']:.3f}")
    
    with tab3:
        # Gráfico de cajas horizontal
        fig1 = px.box(df, y='Tratamiento', x='Rendimiento_kg_ha', 
                      orientation='h',
                      title='Distribución por Tratamiento',
                      color='Tratamiento',
                      color_discrete_sequence=['#66bb6a', '#4caf50', '#388e3c', '#2e7d32'])
        fig1.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico de promedios
        medias = df.groupby('Tratamiento')['Rendimiento_kg_ha'].mean().reset_index()
        fig2 = go.Figure(data=[
            go.Bar(x=medias['Tratamiento'], y=medias['Rendimiento_kg_ha'],
                   marker_color=['#66bb6a', '#4caf50', '#388e3c', '#2e7d32'])
        ])
        fig2.update_layout(title='Rendimiento Promedio', height=400,
                          yaxis_title='Rendimiento (kg/ha)')
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab4:
        st.markdown("#### 💾 Descargar Resultados")
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Datos', index=False)
            anova_table.to_excel(writer, sheet_name='ANOVA', index=False)
        
        st.download_button(
            "📥 Descargar Excel",
            data=output.getvalue(),
            file_name=f"modelo_{num_modelo}_resultados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ==================== COMPARATIVA GLOBAL ====================
elif pagina == "📈 Comparativa Global":
    
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <h2 style='color: #2e7d32; margin-top: 0;'>📈 Comparación entre Todos los Modelos</h2>
    """, unsafe_allow_html=True)
    
    comparacion = []
    for i in range(1, 7):
        df = obtener_datos_modelo(i)
        anova = calcular_anova_simple(df)
        mejor = df.groupby('Tratamiento')['Rendimiento_kg_ha'].mean().idxmax()
        
        comparacion.append({
            'Modelo': f'M{i}',
            'n': len(df),
            'F-stat': round(anova['F'], 3),
            'P-valor': round(anova['P'], 4),
            'Significativo': '✅' if anova['P'] < 0.05 else '❌',
            'Mejor Trat.': mejor
        })
    
    comp_df = pd.DataFrame(comparacion)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)
    
    # Gráfico comparativo
    fig = px.bar(comp_df, x='Modelo', y='F-stat', 
                 color='Significativo',
                 color_discrete_map={'✅': '#4caf50', '❌': '#e57373'},
                 title='Estadísticos F por Modelo')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== INFORMACIÓN ====================
elif pagina == "ℹ️ Información":
    
    st.markdown("""
    <div style='background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <h2 style='color: #2e7d32;'>ℹ️ Acerca del Sistema</h2>
        <p style='color: #555; font-size: 16px; line-height: 1.8;'>
            Sistema desarrollado para el análisis estadístico de diseños experimentales 
            completamente al azar (DCA) en estudios de fertilización de papa.
        </p>
        
        <h3 style='color: #2e7d32; margin-top: 30px;'>🎓 Autor</h3>
        <p style='color: #555;'><b>Sergio Ronald Quispe Calsin</b><br>Código: 221235</p>
        
        <h3 style='color: #2e7d32; margin-top: 30px;'>🛠️ Tecnologías</h3>
        <ul style='color: #555;'>
            <li>Python + Streamlit</li>
            <li>Pandas & NumPy</li>
            <li>SciPy (Análisis estadístico)</li>
            <li>Plotly (Visualización)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer minimalista
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #999; padding: 20px; border-top: 1px solid #e0e0e0;'>
    <p style='margin: 0;'>🥔 Sistema DCA Papa © 2025 | Sergio Ronald Quispe Calsin</p>
</div>
""", unsafe_allow_html=True)
