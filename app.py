import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Análisis DCA - Fertilización Papa", layout="wide", page_icon="🥔")

# CSS personalizado para colores verdes pasteles
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
    }
    .stButton>button {
        background: linear-gradient(135deg, #81c784 0%, #66bb6a 100%);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    div[data-testid="stMetricValue"] {
        color: #2e7d32;
        font-size: 28px;
        font-weight: bold;
    }
    .css-1d391kg {
        background-color: #c8e6c9;
    }
</style>
""", unsafe_allow_html=True)

# ENCABEZADO PERSONALIZADO con gradiente verde pastel
st.markdown("""
<div style='background: linear-gradient(135deg, #a5d6a7 0%, #c8e6c9 50%, #e8f5e9 100%); 
            padding: 30px; 
            border-radius: 20px; 
            margin-bottom: 30px;
            box-shadow: 0 8px 16px rgba(46, 125, 50, 0.2);
            border: 3px solid #81c784;'>
    <h1 style='text-align: center; 
               color: #1b5e20; 
               font-size: 42px;
               text-shadow: 2px 2px 4px rgba(255,255,255,0.5);
               margin-bottom: 10px;'>
        🥔 Análisis Estadístico de Diseños Experimentales 🌱
    </h1>
    <h2 style='text-align: center; 
               color: #2e7d32; 
               font-size: 28px;
               margin-bottom: 15px;'>
        Diseño Completamente al Azar (DCA) - Fertilización en Papa
    </h2>
    <div style='background-color: rgba(255,255,255,0.9); 
                padding: 15px; 
                border-radius: 15px;
                border-left: 5px solid #43a047;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
        <p style='text-align: center; 
                  font-size: 22px; 
                  color: #1b5e20;
                  margin: 0;
                  font-weight: bold;'>
            👨‍🎓 <span style='color: #2e7d32;'>Sergio Ronald Quispe Calsin</span> | 
            📋 Código: <span style='color: #43a047;'>221235</span>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar con estilo verde pastel
st.sidebar.markdown("""
<div style='background: linear-gradient(180deg, #a5d6a7 0%, #c8e6c9 100%); 
            padding: 20px; 
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(46, 125, 50, 0.2);'>
    <h2 style='color: #1b5e20; text-align: center; margin: 0;'>
        📋 Navegación
    </h2>
</div>
""", unsafe_allow_html=True)

seccion = st.sidebar.radio(
    "Seleccione una sección:",
    ["🏠 Inicio", "📚 Teoría", "📊 Modelos Experimentales", "📈 Comparación de Modelos"],
    label_visibility="collapsed"
)

# Si selecciona Modelos, mostrar submenu
modelo_seleccionado = None
if seccion == "📊 Modelos Experimentales":
    st.sidebar.markdown("""
    <div style='background-color: #e8f5e9; 
                padding: 15px; 
                border-radius: 10px;
                border-left: 4px solid #66bb6a;
                margin-top: 10px;'>
        <h3 style='color: #2e7d32; margin-top: 0;'>🔬 Seleccione el Modelo:</h3>
    </div>
    """, unsafe_allow_html=True)
    
    modelo_seleccionado = st.sidebar.selectbox(
        "Modelo:",
        ["Modelo 1: Balanceado", "Modelo 2: No Balanceado", 
         "Modelo 3: Bal-Bal (Sub)", "Modelo 4: Bal-NoBal (Sub)",
         "Modelo 5: NoBal-Bal (Sub)", "Modelo 6: NoBal-NoBal (Sub)"],
        label_visibility="collapsed"
    )

# Funciones para generar datos (mismas que antes)
def generar_datos_modelo1():
    np.random.seed(100)
    datos = []
    medias = {"T1": 32000, "T2": 28000, "T3": 35000, "T4": 30000}
    desv = {"T1": 2500, "T2": 2800, "T3": 2200, "T4": 2600}
    
    for trat in ["T1", "T2", "T3", "T4"]:
        for i in range(15):
            rendimiento = np.random.normal(medias[trat], desv[trat])
            datos.append({
                "Parcela": i+1,
                "Tratamiento": trat,
                "Rendimiento_kg_ha": round(rendimiento, 1)
            })
    return pd.DataFrame(datos)

def generar_datos_modelo2():
    np.random.seed(200)
    datos = []
    medias = {"T1": 31500, "T2": 29000, "T3": 36000, "T4": 31000}
    desv = {"T1": 3000, "T2": 2900, "T3": 2400, "T4": 2700}
    n_parcelas = {"T1": 14, "T2": 18, "T3": 16, "T4": 20}
    
    for trat in ["T1", "T2", "T3", "T4"]:
        for i in range(n_parcelas[trat]):
            rendimiento = np.random.normal(medias[trat], desv[trat])
            datos.append({
                "Parcela": i+1,
                "Tratamiento": trat,
                "Rendimiento_kg_ha": round(rendimiento, 1)
            })
    return pd.DataFrame(datos)

def generar_datos_modelo3():
    np.random.seed(300)
    datos = []
    medias = {"T1": 32500, "T2": 28500, "T3": 35500, "T4": 30500}
    desv_lote = {"T1": 2000, "T2": 2200, "T3": 1800, "T4": 2100}
    desv_parcela = 1200
    
    for trat in ["T1", "T2", "T3", "T4"]:
        for lote in range(1, 6):
            media_lote = np.random.normal(medias[trat], desv_lote[trat])
            for parcela in range(1, 5):
                rendimiento = np.random.normal(media_lote, desv_parcela)
                datos.append({
                    "Lote": f"{trat}-L{lote}",
                    "Parcela": parcela,
                    "Tratamiento": trat,
                    "Rendimiento_kg_ha": round(rendimiento, 1)
                })
    return pd.DataFrame(datos)

def generar_datos_modelo4():
    np.random.seed(400)
    datos = []
    medias = {"T1": 31800, "T2": 29500, "T3": 36500, "T4": 31500}
    desv_lote = {"T1": 2100, "T2": 2300, "T3": 1900, "T4": 2200}
    desv_parcela = 1100
    n_parcelas_lote = {"T1": 3, "T2": 4, "T3": 5, "T4": 3}
    
    for trat in ["T1", "T2", "T3", "T4"]:
        for lote in range(1, 6):
            media_lote = np.random.normal(medias[trat], desv_lote[trat])
            for parcela in range(1, n_parcelas_lote[trat] + 1):
                rendimiento = np.random.normal(media_lote, desv_parcela)
                datos.append({
                    "Lote": f"{trat}-L{lote}",
                    "Parcela": parcela,
                    "Tratamiento": trat,
                    "Rendimiento_kg_ha": round(rendimiento, 1)
                })
    return pd.DataFrame(datos)

def generar_datos_modelo5():
    np.random.seed(500)
    datos = []
    medias = {"T1": 32200, "T2": 28800, "T3": 35800, "T4": 30800}
    desv_lote = {"T1": 2050, "T2": 2250, "T3": 1850, "T4": 2150}
    desv_parcela = 1150
    n_lotes = {"T1": 4, "T2": 6, "T3": 5, "T4": 7}
    
    for trat in ["T1", "T2", "T3", "T4"]:
        for lote in range(1, n_lotes[trat] + 1):
            media_lote = np.random.normal(medias[trat], desv_lote[trat])
            for parcela in range(1, 5):
                rendimiento = np.random.normal(media_lote, desv_parcela)
                datos.append({
                    "Lote": f"{trat}-L{lote}",
                    "Parcela": parcela,
                    "Tratamiento": trat,
                    "Rendimiento_kg_ha": round(rendimiento, 1)
                })
    return pd.DataFrame(datos)

def generar_datos_modelo6():
    np.random.seed(600)
    datos = []
    medias = {"T1": 31000, "T2": 30000, "T3": 37000, "T4": 32000}
    desv_lote = {"T1": 2300, "T2": 2500, "T3": 2000, "T4": 2400}
    desv_parcela = 1300
    n_lotes = {"T1": 4, "T2": 6, "T3": 5, "T4": 7}
    parcelas_por_lote = {
        "T1": [3, 4, 5, 4],
        "T2": [5, 4, 6, 4, 5, 4],
        "T3": [4, 5, 3, 6, 4],
        "T4": [6, 4, 5, 4, 6, 5, 4]
    }
    
    for trat in ["T1", "T2", "T3", "T4"]:
        for lote in range(n_lotes[trat]):
            media_lote = np.random.normal(medias[trat], desv_lote[trat])
            n_parcelas = parcelas_por_lote[trat][lote]
            for parcela in range(1, n_parcelas + 1):
                rendimiento = np.random.normal(media_lote, desv_parcela)
                datos.append({
                    "Lote": f"{trat}-L{lote+1}",
                    "Parcela": parcela,
                    "Tratamiento": trat,
                    "Rendimiento_kg_ha": round(rendimiento, 1)
                })
    return pd.DataFrame(datos)

def calcular_anova_unifactorial_pasos(df):
    st.markdown("""
    <div style='background: linear-gradient(135deg, #c8e6c9 0%, #e8f5e9 100%); 
                padding: 20px; 
                border-radius: 15px;
                border-left: 5px solid #66bb6a;
                margin-bottom: 20px;'>
        <h3 style='color: #1b5e20; margin: 0;'>📐 Cálculos Paso a Paso - ANOVA Unifactorial</h3>
    </div>
    """, unsafe_allow_html=True)
    
    n_total = len(df)
    tratamientos = sorted(df['Tratamiento'].unique())
    k = len(tratamientos)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🔢 N total", n_total)
    col2.metric("🧪 Tratamientos", k)
    col3.metric("📊 Grupos", k)
    
    st.markdown("#### Paso 2: Cálculo de medias por tratamiento")
    medias_df = df.groupby('Tratamiento').agg({
        'Rendimiento_kg_ha': ['count', 'mean', 'sum']
    }).round(2)
    medias_df.columns = ['n', 'Media', 'Suma']
    st.dataframe(medias_df, use_container_width=True)
    
    grand_mean = df['Rendimiento_kg_ha'].mean()
    st.success(f"**🎯 Media General (Ȳ..):** {grand_mean:.2f} kg/ha")
    
    st.markdown("#### Paso 3: Cálculo de Sumas de Cuadrados")
    
    ss_total = ((df['Rendimiento_kg_ha'] - grand_mean) ** 2).sum()
    st.info(f"**SCT = {ss_total:.2f}**")
    
    ss_between = 0
    for trat in tratamientos:
        n_i = len(df[df['Tratamiento'] == trat])
        mean_i = df[df['Tratamiento'] == trat]['Rendimiento_kg_ha'].mean()
        ss_i = n_i * (mean_i - grand_mean) ** 2
        ss_between += ss_i
    
    st.info(f"**SC Tratamientos = {ss_between:.2f}**")
    
    ss_within = ss_total - ss_between
    st.info(f"**SC Error = {ss_within:.2f}**")
    
    df_between = k - 1
    df_within = n_total - k
    df_total = n_total - 1
    
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    
    f_calc = ms_between / ms_within
    p_value = 1 - stats.f.cdf(f_calc, df_between, df_within)
    
    if p_value < 0.05:
        st.markdown("""
        <div style='background-color: #c8e6c9; padding: 15px; border-radius: 10px; border-left: 5px solid #66bb6a;'>
            <p style='color: #1b5e20; font-size: 18px; margin: 0;'>
                ✅ <b>Como p-valor < 0.05, rechazamos H₀</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Como p-valor ≥ 0.05, no rechazamos H₀")
    
    return {
        'SS_Between': ss_between, 'SS_Within': ss_within, 'SS_Total': ss_total,
        'DF_Between': df_between, 'DF_Within': df_within, 'DF_Total': df_total,
        'MS_Between': ms_between, 'MS_Within': ms_within,
        'F_Statistic': f_calc, 'P_Value': p_value
    }

def calcular_anova_bifactorial_pasos(df):
    st.markdown("""
    <div style='background: linear-gradient(135deg, #c8e6c9 0%, #e8f5e9 100%); 
                padding: 20px; 
                border-radius: 15px;
                border-left: 5px solid #66bb6a;'>
        <h3 style='color: #1b5e20; margin: 0;'>📐 ANOVA Bifactorial</h3>
    </div>
    """, unsafe_allow_html=True)
    
    df_bif = df.copy()
    df_bif['Factor_A'] = df_bif['Tratamiento']
    
    zonas = []
    for trat in sorted(df_bif['Tratamiento'].unique()):
        subset = df_bif[df_bif['Tratamiento'] == trat]
        n_trat = len(subset)
        n_alta = n_trat // 3
        n_baja = n_trat // 3
        n_media = n_trat - n_alta - n_baja
        zonas_trat = ['Alta'] * n_alta + ['Media'] * n_media + ['Baja'] * n_baja
        zonas.extend(zonas_trat)
    
    df_bif['Factor_B'] = zonas
    
    factor_a = sorted(df_bif['Factor_A'].unique())
    factor_b = sorted(df_bif['Factor_B'].unique())
    a = len(factor_a)
    b = len(factor_b)
    n_total = len(df_bif)
    
    grand_mean = df_bif['Rendimiento_kg_ha'].mean()
    medias_a = df_bif.groupby('Factor_A')['Rendimiento_kg_ha'].mean()
    medias_b = df_bif.groupby('Factor_B')['Rendimiento_kg_ha'].mean()
    
    ss_total = ((df_bif['Rendimiento_kg_ha'] - grand_mean) ** 2).sum()
    
    ss_a = sum([len(df_bif[df_bif['Factor_A'] == nivel]) * (medias_a[nivel] - grand_mean) ** 2 
                for nivel in factor_a])
    
    ss_b = sum([len(df_bif[df_bif['Factor_B'] == nivel]) * (medias_b[nivel] - grand_mean) ** 2 
                for nivel in factor_b])
    
    ss_ab = 0
    for nivel_a in factor_a:
        for nivel_b in factor_b:
            subset = df_bif[(df_bif['Factor_A'] == nivel_a) & (df_bif['Factor_B'] == nivel_b)]
            if len(subset) > 0:
                n_cell = len(subset)
                mean_cell = subset['Rendimiento_kg_ha'].mean()
                ss_ab += n_cell * (mean_cell - medias_a[nivel_a] - medias_b[nivel_b] + grand_mean) ** 2
    
    ss_error = ss_total - ss_a - ss_b - ss_ab
    
    df_a = a - 1
    df_b = b - 1
    df_ab = (a - 1) * (b - 1)
    df_error = n_total - (a * b)
    
    cm_a = ss_a / df_a if df_a > 0 else 0
    cm_b = ss_b / df_b if df_b > 0 else 0
    cm_ab = ss_ab / df_ab if df_ab > 0 else 0
    cm_error = ss_error / df_error if df_error > 0 else 1
    
    f_a = cm_a / cm_error if cm_error > 0 else 0
    f_b = cm_b / cm_error if cm_error > 0 else 0
    f_ab = cm_ab / cm_error if cm_error > 0 else 0
    
    p_a = 1 - stats.f.cdf(f_a, df_a, df_error) if f_a > 0 else 1
    p_b = 1 - stats.f.cdf(f_b, df_b, df_error) if f_b > 0 else 1
    p_ab = 1 - stats.f.cdf(f_ab, df_ab, df_error) if f_ab > 0 else 1
    
    return {
        'SS_A': ss_a, 'SS_B': ss_b, 'SS_AB': ss_ab, 'SS_Error': ss_error, 'SS_Total': ss_total,
        'DF_A': df_a, 'DF_B': df_b, 'DF_AB': df_ab, 'DF_Error': df_error, 'DF_Total': n_total - 1,
        'MS_A': cm_a, 'MS_B': cm_b, 'MS_AB': cm_ab, 'MS_Error': cm_error,
        'F_A': f_a, 'F_B': f_b, 'F_AB': f_ab,
        'P_A': p_a, 'P_B': p_b, 'P_AB': p_ab
    }

def tukey_hsd(df):
    from scipy.stats import studentized_range
    medias = df.groupby('Tratamiento')['Rendimiento_kg_ha'].mean().sort_values(ascending=False)
    n = df.groupby('Tratamiento')['Rendimiento_kg_ha'].count()
    
    grupos = [df[df['Tratamiento'] == t]['Rendimiento_kg_ha'].values for t in df['Tratamiento'].unique()]
    n_total = len(df)
    k = len(df['Tratamiento'].unique())
    
    ss_within = sum([(df[df['Tratamiento'] == t]['Rendimiento_kg_ha'] - 
                      df[df['Tratamiento'] == t]['Rendimiento_kg_ha'].mean()).pow(2).sum() 
                     for t in df['Tratamiento'].unique()])
    df_within = n_total - k
    mse = ss_within / df_within
    
    comparaciones = []
    tratamientos = list(medias.index)
    
    for i in range(len(tratamientos)):
        for j in range(i+1, len(tratamientos)):
            t1, t2 = tratamientos[i], tratamientos[j]
            diff = abs(medias[t1] - medias[t2])
            n_harmonic = 2 / (1/n[t1] + 1/n[t2])
            se = np.sqrt(mse / n_harmonic)
            q_crit = studentized_range.ppf(0.95, len(tratamientos), df_within)
            hsd = q_crit * se
            
            comparaciones.append({
                'Comparación': f"{t1} vs {t2}",
                'Diferencia (kg/ha)': round(diff, 2),
                'HSD': round(hsd, 2),
                'Significativo': 'Sí ✅' if diff > hsd else 'No ❌'
            })
    
    return pd.DataFrame(comparaciones), medias

def crear_graficos(df, result_uni):
    st.markdown("""
    <div style='background: linear-gradient(135deg, #a5d6a7 0%, #c8e6c9 100%); 
                padding: 20px; 
                border-radius: 15px;
                margin-bottom: 20px;'>
        <h2 style='color: #1b5e20; margin: 0;'>📊 Visualización de Resultados</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Boxplot con colores verdes
    colores_verdes = ['#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9']
    
    fig_box = px.box(df, x='Tratamiento', y='Rendimiento_kg_ha',
                     title='🌱 Distribución de Rendimiento por Tratamiento',
                     labels={'Rendimiento_kg_ha': 'Rendimiento (kg/ha)'},
                     color='Tratamiento',
                     color_discrete_sequence=colores_verdes)
    fig_box.update_layout(
        plot_bgcolor='rgba(232, 245, 233, 0.3)',
        paper_bgcolor='white',
        font=dict(color='#1b5e20', size=14),
        title_font=dict(size=20, color='#2e7d32')
    )
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Violin plot
    fig_violin = px.violin(df, x='Tratamiento', y='Rendimiento_kg_ha',
                          title='🎻 Densidad de Distribución del Rendimiento',
                          color='Tratamiento', box=True,
                          color_discrete_sequence=colores_verdes)
    fig_violin.update_layout(
        plot_bgcolor='rgba(232, 245, 233, 0.3)',
        paper_bgcolor='white',
        font=dict(color='#1b5e20', size=14),
        title_font=dict(size=20, color='#2e7d32')
    )
    st.plotly_chart(fig_violin, use_container_width=True)

def mostrar_interpretaciones(df, result_uni):
    st.markdown("""
    <div style='background: linear-gradient(135deg, #81c784 0%, #a5d6a7 100%); 
                padding: 25px; 
                border-radius: 15px;
                box-shadow: 0 6px 12px rgba(46, 125, 50, 0.2);
                margin: 20px 0;'>
        <h2 style='color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
            💡 Interpretaciones y Conclusiones
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    medias = df.groupby('Tratamiento')['Rendimiento_kg_ha'].mean().sort_values(ascending=False)
    mejor_trat = medias.index[0]
    mejor_media = medias.iloc[0]
    
    descripciones = {
        'T1': 'Fertilizante químico NPK 120-80-100',
        'T2': 'Fertilizante orgánico (compost + humus)',
        'T3': 'Fertilizante mixto (50% químico + 50% orgánico)',
        'T4': 'Biofertilizante con microorganismos eficientes'
    }
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #c8e6c9 0%, #e8f5e9 100%); 
                padding: 25px; 
                border-radius: 15px;
                border: 3px solid #66bb6a;
                box-shadow: 0 6px 12px rgba(0,0,0,0.1);'>
        <h3 style='color: #1b5e20; margin-top: 0;'>🏆 Mejor Tratamiento</h3>
        <div style='background-color: white; 
                    padding: 20px; 
                    border-radius: 10px;
                    border-left: 5px solid #43a047;'>
            <h2 style='color: #2e7d32; margin: 0 0 10px 0;'>{mejor_trat}</h2>
            <p style='color: #1b5e20; font-size: 18px; margin: 5px 0;'>
                <b>{descripciones[mejor_trat]}</b>
            </p>
            <p style='color: #43a047; font-size: 24px; font-weight: bold; margin: 10px 0 0 0;'>
                📊 Rendimiento: {mejor_media:.1f} kg/ha ({mejor_media/1000:.1f} ton/ha)
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if result_uni['P_Value'] < 0.05:
        st.markdown("""
        <div style='background-color: #c8e6c9; 
                    padding: 15px; 
                    border-radius: 10px;
                    margin-top: 15px;
                    border-left: 5px solid #66bb6a;'>
            <p style='color: #1b5e20; font-size: 18px; margin: 0;'>
                ✅ <b>Diferencias estadísticamente significativas detectadas</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

def exportar_excel(df, anova_uni, anova_bif, tukey_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Datos', index=False)
        
        anova_uni_df = pd.DataFrame({
            'Fuente': ['Entre Tratamientos', 'Error', 'Total'],
            'SC': [anova_uni['SS_Between'], anova_uni['SS_Within'], anova_uni['SS_Total']],
            'GL': [anova_uni['DF_Between'], anova_uni['DF_Within'], anova_uni['DF_Total']],
            'CM': [anova_uni['MS_Between'], anova_uni['MS_Within'], ''],
            'F': [anova_uni['F_Statistic'], '', ''],
            'P-valor': [anova_uni['P_Value'], '', '']
        })
        anova_uni_df.to_excel(writer, sheet_name='ANOVA Unifactorial', index=False)
        
        if not tukey_df.empty:
            tukey_df.to_excel(writer, sheet_name='Tukey HSD', index=False)
    
    return output.getvalue()

# ==================== SECCIÓN INICIO ====================
if seccion == "🏠 Inicio":
    st.markdown("---")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%); 
                padding: 25px; 
                border-radius: 15px;
                border: 3px solid #81c784;
                box-shadow: 0 6px 12px rgba(46, 125, 50, 0.15);
                margin-bottom: 30px;'>
        <h2 style='color: #1b5e20; margin-top: 0;'>📄 Contexto del Caso</h2>
        <p style='font-size: 18px; line-height: 1.8; color: #2e7d32;'>
            Este estudio tiene como objetivo <b style='color: #1b5e20;'>determinar el mejor fertilizante</b> 
            para maximizar el rendimiento del cultivo de papa (<i>Solanum tuberosum</i>) hasta alcanzar 
            un rendimiento comercial óptimo.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='background-color: #c8e6c9; 
                    padding: 20px; 
                    border-radius: 12px;
                    border-left: 5px solid #66bb6a;
                    margin-bottom: 20px;'>
            <h3 style='color: #1b5e20; margin-top: 0;'>🌱 Factor Experimental</h3>
            <p style='color: #2e7d32; font-size: 16px; margin: 0;'>
                <b>Tipo de fertilizante</b> para cultivo de papa
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 Tratamientos Evaluados")
        tratamientos_df = pd.DataFrame({
            'Código': ['T1', 'T2', 'T3', 'T4'],
            'Descripción': [
                '🧪 Fertilizante químico NPK 120-80-100',
                '🌿 Fertilizante orgánico (compost + humus)',
                '⚖️ Fertilizante mixto (50% químico + 50% orgánico)',
                '🦠 Biofertilizante con microorganismos eficientes'
            ]
        })
        st.dataframe(tratamientos_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        <div style='background-color: #a5d6a7; 
                    padding: 20px; 
                    border-radius: 12px;
                    margin-top: 20px;'>
            <h3 style='color: #1b5e20; margin-top: 0;'>📈 Variable Respuesta</h3>
            <p style='color: white; font-size: 18px; font-weight: bold; margin: 0;'>
                Rendimiento en kilogramos por hectárea (kg/ha)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #81c784 0%, #a5d6a7 100%); 
                    padding: 20px; 
                    border-radius: 15px;
                    box-shadow: 0 6px 12px rgba(46, 125, 50, 0.2);'>
            <h3 style='color: white; text-align: center; margin-top: 0;'>📚 Modelos Disponibles</h3>
            <div style='background-color: rgba(255,255,255,0.9); 
                        padding: 15px; 
                        border-radius: 10px;'>
                <p style='margin: 8px 0; color: #1b5e20;'><b>1️⃣</b> Balanceado</p>
                <p style='margin: 8px 0; color: #1b5e20;'><b>2️⃣</b> No Balanceado</p>
                <p style='margin: 8px 0; color: #1b5e20;'><b>3️⃣</b> Bal-Bal (Sub)</p>
                <p style='margin: 8px 0; color: #1b5e20;'><b>4️⃣</b> Bal-NoBal (Sub)</p>
                <p style='margin: 8px 0; color: #1b5e20;'><b>5️⃣</b> NoBal-Bal (Sub)</p>
                <p style='margin: 8px 0; color: #1b5e20;'><b>6️⃣</b> NoBal-NoBal (Sub)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== SECCIÓN TEORÍA ====================
elif seccion == "📚 Teoría":
    st.header("📚 Marco Teórico")
    st.markdown("### Diseño Completamente al Azar (DCA)")
    st.latex(r"Y_{ij} = \mu + \tau_i + \varepsilon_{ij}")

# ==================== SECCIÓN MODELOS ====================
elif seccion == "📊 Modelos Experimentales":
    
    def mostrar_analisis_completo(df, titulo, descripcion):
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #66bb6a 0%, #81c784 100%); 
                    padding: 20px; 
                    border-radius: 15px;
                    margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0;'>{titulo}</h2>
            <p style='color: white; font-size: 16px; margin: 10px 0 0 0;'>{descripcion}</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📊 Datos", "🔢 ANOVA Unifactorial", "🔢 ANOVA Bifactorial", 
             "📈 Gráficos", "📥 Exportar"]
        )
        
        with tab1:
            st.subheader("Datos Experimentales")
            st.dataframe(df, use_container_width=True, height=400)
            
            summary = df.groupby('Tratamiento')['Rendimiento_kg_ha'].agg([
                ('N', 'count'), ('Media', 'mean'), ('Desv.Est.', 'std'),
                ('Mín', 'min'), ('Máx', 'max')
            ]).round(2)
            st.dataframe(summary, use_container_width=True)
        
        with tab2:
            result_uni = calcular_anova_unifactorial_pasos(df)
            
            if result_uni['P_Value'] < 0.05:
                st.markdown("### 🔍 Prueba de Tukey HSD")
                tukey_df, medias = tukey_hsd(df)
                st.dataframe(tukey_df, use_container_width=True, hide_index=True)
        
        with tab3:
            result_bif = calcular_anova_bifactorial_pasos(df)
        
        with tab4:
            crear_graficos(df, result_uni)
            mostrar_interpretaciones(df, result_uni)
        
        with tab5:
            tukey_df, _ = tukey_hsd(df) if result_uni['P_Value'] < 0.05 else (pd.DataFrame(), None)
            excel_data = exportar_excel(df, result_uni, result_bif, tukey_df)
            st.download_button("📥 Descargar Excel Completo", excel_data, 
                             f"{titulo.lower().replace(' ', '_')}.xlsx",
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    if modelo_seleccionado == "Modelo 1: Balanceado":
        df = generar_datos_modelo1()
        mostrar_analisis_completo(df, "🌱 Modelo 1: DCA Balanceado", 
                                 "60 parcelas experimentales (15 por tratamiento)")
    elif modelo_seleccionado == "Modelo 2: No Balanceado":
        df = generar_datos_modelo2()
        mostrar_analisis_completo(df, "🌱 Modelo 2: No Balanceado", 
                                 "68 parcelas con distribución desigual")
    elif modelo_seleccionado == "Modelo 3: Bal-Bal (Sub)":
        df = generar_datos_modelo3()
        mostrar_analisis_completo(df, "🌱 Modelo 3: Bal-Bal", 
                                 "20 lotes, 4 parcelas por lote")
    elif modelo_seleccionado == "Modelo 4: Bal-NoBal (Sub)":
        df = generar_datos_modelo4()
        mostrar_analisis_completo(df, "🌱 Modelo 4: Bal-NoBal", 
                                 "20 lotes, parcelas variables por lote")
    elif modelo_seleccionado == "Modelo 5: NoBal-Bal (Sub)":
        df = generar_datos_modelo5()
        mostrar_analisis_completo(df, "🌱 Modelo 5: NoBal-Bal", 
                                 "Lotes desiguales, 4 parcelas por lote")
    elif modelo_seleccionado == "Modelo 6: NoBal-NoBal (Sub)":
        df = generar_datos_modelo6()
        mostrar_analisis_completo(df, "🌱 Modelo 6: Completamente Desbalanceado", 
                                 "Estructura completamente variable")

# ==================== COMPARACIÓN ====================
elif seccion == "📈 Comparación de Modelos":
    st.markdown("""
    <div style='background: linear-gradient(135deg, #81c784 0%, #a5d6a7 100%); 
                padding: 25px; 
                border-radius: 15px;
                margin-bottom: 25px;'>
        <h2 style='color: white; margin: 0;'>📈 Comparación entre Modelos Experimentales</h2>
    </div>
    """, unsafe_allow_html=True)
    
    modelos_data = {
        "Modelo 1": generar_datos_modelo1(),
        "Modelo 2": generar_datos_modelo2(),
        "Modelo 3": generar_datos_modelo3(),
        "Modelo 4": generar_datos_modelo4(),
        "Modelo 5": generar_datos_modelo5(),
        "Modelo 6": generar_datos_modelo6()
    }
    
    comparacion = []
    for nombre, df in modelos_data.items():
        grupos = [df[df['Tratamiento'] == t]['Rendimiento_kg_ha'].values 
                 for t in df['Tratamiento'].unique()]
        f_stat, p_value = stats.f_oneway(*grupos)
        media_general = df['Rendimiento_kg_ha'].mean()
        
        comparacion.append({
            'Modelo': nombre,
            'n Total': len(df),
            'Media General (kg/ha)': round(media_general, 1),
            'F-statistic': round(f_stat, 4),
            'P-valor': round(p_value, 6),
            'Significativo': 'Sí ✅' if p_value < 0.05 else 'No ❌'
        })
    
    comp_df = pd.DataFrame(comparacion)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

# Footer con estilo verde
st.markdown("---")
st.markdown("""
<div style='background: linear-gradient(135deg, #a5d6a7 0%, #c8e6c9 100%); 
            padding: 20px; 
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(46, 125, 50, 0.2);'>
    <p style='color: #1b5e20; font-size: 16px; margin: 0;'>
        <b>🌱 Desarrollado para análisis estadístico de diseños experimentales en agricultura 🥔</b>
    </p>
    <p style='color: #2e7d32; font-size: 18px; font-weight: bold; margin: 10px 0 0 0;'>
        Sergio Ronald Quispe Calsin | Código: 221235
    </p>
</div>
""", unsafe_allow_html=True)