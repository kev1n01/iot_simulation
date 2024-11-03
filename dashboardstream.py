import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import numpy as np
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Sistema Acuapónico",
    page_icon="🌱",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
        .stMetric {
            background-color: #000000;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ffffff;
        }
        .stMetric:hover {
            background-color: #333333;
            cursor: pointer;
        }
        .metric-title {
            font-size: 0.8em;
            color: #000000;
        }
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Función para generar datos simulados en tiempo real
def generate_real_time_data(base_values, noise_level=0.1):
    return {
        key: value + np.random.normal(0, noise_level * abs(value))
        for key, value in base_values.items()
    }

# Configuración de la barra lateral para selección de página
with st.sidebar:
    st.title("🌱 Sistema Acuapónico")
    page = st.radio("Navegación:", ["📊 Monitoreo en Tiempo Real", "📈 Producción Histórica"])

# Página 1: Monitoreo en Tiempo Real
if page == "📊 Monitoreo en Tiempo Real":
    st.title("Dashboard en Tiempo Real - Sistema Acuapónico")
    
    # Placeholder para datos en tiempo real
    if 'historical_data' not in st.session_state:
        st.session_state.historical_data = []
    
    # Valores base para simulación
    base_values = {
        "nivel_de_ph": 7.0,
        "nivel_de_oxigeno_agua_mg_L": 6.5,
        "temperatura_agua_C": 25.0,
        "temperatura_ambiente_C": 22.0,
        "humedad_ambiente_%": 65.0,
        "cantidad_alimento_g": 100.0,
        "nivel_de_agua_cm": 50.0
    }
    
    # Generar nuevos datos
    new_data = generate_real_time_data(base_values)
    st.session_state.historical_data.append({**new_data, 'timestamp': datetime.now()})
    
    # Mantener solo los últimos 100 puntos de datos
    if len(st.session_state.historical_data) > 100:
        st.session_state.historical_data = st.session_state.historical_data[-100:]
    
    # Convertir a DataFrame
    data = pd.DataFrame(st.session_state.historical_data)
    
    # Crear métricas en tiempo real
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_ph = new_data["nivel_de_ph"]
        previous_ph = st.session_state.historical_data[-2]["nivel_de_ph"] if len(st.session_state.historical_data) > 1 else current_ph
        st.metric(
            label="Nivel de pH",
            value=f"{current_ph:.2f}",
            delta=f"{current_ph - previous_ph:.2f}"
        )

        current_oxigen = new_data["nivel_de_oxigeno_agua_mg_L"]
        previous_oxigen = st.session_state.historical_data[-2]["nivel_de_oxigeno_agua_mg_L"] if len(st.session_state.historical_data) > 1 else current_oxigen
        st.metric(
            label="Oxígeno (mg/L)",
            value=f"{current_oxigen:.2f}",
            delta=f"{current_oxigen - previous_oxigen:.2f}"
        )

    with col2:
        current_temp_amb = new_data["temperatura_ambiente_C"]
        previous_temp_amb = st.session_state.historical_data[-2]["temperatura_ambiente_C"] if len(st.session_state.historical_data) > 1 else current_temp_amb
        st.metric(
            label="Temperatura Ambiente (°C)",
            value=f"{current_temp_amb:.2f}",
            delta=f"{current_temp_amb - previous_temp_amb:.2f}"
        )

        current_humidity = new_data["humedad_ambiente_%"]
        previous_humidity = st.session_state.historical_data[-2]["humedad_ambiente_%"] if len(st.session_state.historical_data) > 1 else current_humidity
        st.metric(
            label="Humedad (%)",
            value=f"{current_humidity:.1f}",
            delta=f"{current_humidity - previous_humidity:.1f}"
        )
        
    with col3:
        current_temp = new_data["temperatura_agua_C"]
        previous_temp = st.session_state.historical_data[-2]["temperatura_agua_C"] if len(st.session_state.historical_data) > 1 else current_temp
        st.metric(
            label="Temperatura Agua (°C)",
            value=f"{current_temp:.1f}",
            delta=f"{current_temp - previous_temp:.1f}"
        )

        current_eat = new_data["cantidad_alimento_g"]
        previous_eat = st.session_state.historical_data[-2]["cantidad_alimento_g"] if len(st.session_state.historical_data) > 1 else current_eat
        st.metric(
            label="Cantidad de Alimento (g)",
            value=f"{current_eat:.1f}",
            delta=f"{current_eat - previous_eat:.1f}"
        )

    # Crear gráficos con diferentes estilos
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=(
            "Oxígeno Disuelto", "Temperaturas", 
             "Nivel de Agua", "Humedad",
            "Alimentación"
        )
    )

    # 1. Area chart para oxígeno
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["nivel_de_oxigeno_agua_mg_L"],
            fill='tozeroy',
            name="Oxígeno",
            line_color='rgba(0,100,255,0.8)'
        ),
        row=1, col=1
    )

    # 2. Line chart para temperaturas
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["temperatura_agua_C"],
            name="Temp. Agua",
            line=dict(color='blue', width=2)
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["temperatura_ambiente_C"],
            name="Temp. Ambiente",
            line=dict(color='red', width=2)
        ),
        row=1, col=2
    )

    # 3. Bar chart para humedad
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["humedad_ambiente_%"],
            name="Humedad",
            marker_color='rgba(0,255,100,0.6)'
        ),
        row=2, col=1

    )

    # 4. Scatter plot para nivel de agua
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["nivel_de_agua_cm"],
            mode='markers',
            marker=dict(
                size=10,
                color=data["nivel_de_agua_cm"],
                colorscale='Viridis',
            ),
            name="Nivel Agua"
        ),
        row=1, col=3
    )

    # 5. Combined line and bar para alimentación
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["cantidad_alimento_g"],
            name="Alimento (línea)",
            line=dict(color='orange', width=2)
        ),
        row=2, col=2
    )
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["cantidad_alimento_g"],
            name="Alimento (barra)",
            marker_color='rgba(255,165,0,0.3)'
        ),
        row=2, col=2
    )

    fig.update_layout(
        height=800,
        showlegend=False,
        title_text="Monitoreo en Tiempo Real del Sistema Acuapónico"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Actualizar cada 3 segundos
    time.sleep(3)
    st.rerun()

elif page == "📈 Producción Histórica":
    st.title("Dashboard de Producción - Vista Histórica")
    
    try:
        # Cargar datos
        produccion_data = pd.read_excel('proceso_de_produccion.xlsx')
        
        # Asegurar que las columnas numéricas sean del tipo correcto
        numeric_columns = ['cantidad_cosecha', 'venta_kg', 'costo_produccion', 
                         'ganancia', 'ingreso_produccion', 'mortalidad_produccion', 
                         'Peso_produccion', 'cantidad_produccion']
        
        for col in numeric_columns:
            produccion_data[col] = pd.to_numeric(produccion_data[col], errors='coerce')
        
        # Filtros en la barra lateral
        with st.sidebar:
            st.header("Filtros")
            col1, col2 = st.columns(2)
            
            with col1:
                selected_year = st.selectbox(
                    "Año",
                    options=sorted(produccion_data["fecha_año"].unique()),
                    index=len(produccion_data["fecha_año"].unique()) - 1
                )
                
            with col2:
                selected_month = st.selectbox(
                    "Mes",
                    options=sorted(produccion_data["fecha_mes"].unique())
                )
            
            tipo_produccion = st.multiselect(
                "Tipo de Producción",
                options=produccion_data["tipo"].unique(),
                default=produccion_data["tipo"].unique()
            )

        # Filtrar datos
        filtered_data = produccion_data[
            (produccion_data["fecha_año"] == selected_year) &
            (produccion_data["fecha_mes"] == selected_month) &
            (produccion_data["tipo"].isin(tipo_produccion))
        ]

        # Métricas generales - Primera fila
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_produccion = filtered_data["cantidad_produccion"].sum()
            st.metric("Producción Total", f"{total_produccion:.2f} kg")
        
        with col2:
            total_ingresos = filtered_data["ingreso_produccion"].sum()
            st.metric("Ingresos Totales", f"S/. {total_ingresos:,.2f}")
        
        with col3:
            total_ganancia = filtered_data["ganancia"].sum()
            st.metric("Ganancia Total", f"S/.{total_ganancia:,.2f}")

        # Métricas generales - Segunda fila
        col1, col2, col3 = st.columns(3)
        
        with col1:
            promedio_peso = filtered_data["Peso_produccion"].mean()
            st.metric("Peso Promedio", f"{promedio_peso:.2f} kg")
        
        with col2:
            mortalidad = filtered_data["mortalidad_produccion"].mean()
            st.metric("Mortalidad Promedio", f"{mortalidad:.2f}%")
        
        with col3:
            venta_kg = filtered_data["venta_kg"].sum()
            st.metric("Venta Total", f"{venta_kg:.2f} kg")

        # Preparar datos para los gráficos
        chart_data_production = pd.melt(
            filtered_data,
            id_vars=['tipo'],
            value_vars=['cantidad_cosecha', 'venta_kg'],
            var_name='Métrica',
            value_name='Valor'
        )

        chart_data_financials = pd.melt(
            filtered_data,
            id_vars=['tipo'],
            value_vars=['costo_produccion', 'ganancia'],
            var_name='Métrica',
            value_name='Valor'
        )

        # Gráficos de producción y costos
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de barras comparativo
            chart_comparison = alt.Chart(chart_data_production).mark_bar().encode(
                x=alt.X('tipo:N', title='Tipo'),
                y=alt.Y('Valor:Q', title='Cantidad (kg)'),
                color=alt.Color('Métrica:N', title='Métrica'),
                tooltip=['tipo', 'Métrica', 'Valor']
            ).properties(
                title="Comparación Cosecha vs Venta",
                width=400,
                height=300
            )
            st.altair_chart(chart_comparison, use_container_width=True)

        with col2:
            # Gráfico de línea de costos y ganancias
            chart_financials = alt.Chart(chart_data_financials).mark_line(point=True).encode(
                x=alt.X('tipo:N', title='Tipo'),
                y=alt.Y('Valor:Q', title='Valor ($)'),
                color=alt.Color('Métrica:N', title='Métrica'),
                tooltip=['tipo', 'Métrica', 'Valor']
            ).properties(
                title="Tendencia de Costos y Ganancias",
                width=400,
                height=300
            )
            st.altair_chart(chart_financials, use_container_width=True)

        # Tabla de datos detallada
        st.subheader("Detalles de Producción")
        columns_to_show = [
            'fecha_mes', 'tipo', 'cantidad_cosecha', 'venta_kg',
            'costo_produccion', 'ingreso_produccion', 'ganancia',
            'mortalidad_produccion', 'Peso_produccion'
        ]
        st.dataframe(
            filtered_data[columns_to_show].sort_values('fecha_mes', ascending=False),
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Error al cargar los datos de producción: {str(e)}")