```python
# -*- coding: utf-8 -*-
# Capítulo 3: Exposición y consumo de datos
# Sección 6: Visualización con Streamlit
# Bloque 4: Métricas y visualizaciones

# Importar las librerías necesarias
import streamlit as st
import pandas as pd
import numpy as np

# Configurar la página del dashboard
st.set_page_config(page_title="Dashboard de Transacciones", layout="wide")

# ST10: Conexión con lógica de negocio
# ST11: Dashboard como herramienta de decisión
st.title("Dashboard Ejecutivo de Ventas")
st.markdown("""
Esta herramienta permite analizar los datos procesados por nuestro pipeline. 
Utilice los filtros laterales para explorar las métricas clave y tomar decisiones basadas en datos.
""")

# Generar datos simulados consistentes con el pipeline
# Se utiliza el caché de Streamlit para no recalcular en cada interacción
@st.cache_data
def cargar_datos():
    # Establecer semilla para reproducibilidad
    np.random.seed(987654)
    
    # Crear un rango de fechas
    fechas = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    
    # Construir un DataFrame simulando los datos limpios de nuestro ETL
    datos = {
        "fecha": np.random.choice(fechas, 1000),
        "cliente": np.random.choice(["Cliente A", "Cliente B", "Cliente C", "Cliente D"], 1000),
        "categoria": np.random.choice(["Electrónica", "Ropa", "Hogar", "Servicios"], 1000),
        "monto": np.random.uniform(50, 5000, 1000).round(2)
    }
    df = pd.DataFrame(datos)
    df.sort_values("fecha", inplace=True)
    return df

# Cargar los datos
df_transacciones = cargar_datos()

# ==============================================================================
# ST4: Filtros interactivos (fecha, cliente)
# ST5: Segmentación de datos
# ==============================================================================
st.sidebar.header("Filtros Interactivos")
st.sidebar.markdown("Use estos controles para segmentar la información.")

# Definir límites de fechas
fecha_min = df_transacciones['fecha'].min().date()
fecha_max = df_transacciones['fecha'].max().date()

# Control para filtrar por rango de fechas
rango_fechas = st.sidebar.date_input(
    "Seleccionar Rango de Fechas",
    value=[fecha_min, fecha_max],
    min_value=fecha_min,
    max_value=fecha_max
)

# Control para filtrar por cliente
clientes_disponibles = df_transacciones['cliente'].unique()
clientes_seleccionados = st.sidebar.multiselect(
    "Filtrar por Cliente",
    options=clientes_disponibles,
    default=clientes_disponibles
)

# Control para filtrar por categoría
categorias_disponibles = df_transacciones['categoria'].unique()
categorias_seleccionadas = st.sidebar.multiselect(
    "Filtrar por Categoría",
    options=categorias_disponibles,
    default=categorias_disponibles
)

# Validar que el rango de fechas tenga inicio y fin
if len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas
    
    # Aplicar todos los filtros al DataFrame
    mask = (
        (df_transacciones['fecha'].dt.date >= fecha_inicio) &
        (df_transacciones['fecha'].dt.date <= fecha_fin) &
        (df_transacciones['cliente'].isin(clientes_seleccionados)) &
        (df_transacciones['categoria'].isin(categorias_seleccionadas))
    )
    df_filtrado = df_transacciones[mask]
else:
    # Estado por defecto si no se seleccionan dos fechas
    df_filtrado = df_transacciones.copy()

# ==============================================================================
# ST1: Creación de métricas clave (KPIs)
# ST2: Cálculo de agregados (sum, avg, count)
# ST8: Validación de métricas
# ==============================================================================
st.subheader("Métricas Principales (KPIs)")

# Calcular agregaciones
ingresos_totales = df_filtrado['monto'].sum()
numero_transacciones = df_filtrado['monto'].count()
ticket_promedio = df_filtrado['monto'].mean() if numero_transacciones > 0 else 0

# Crear columnas para mostrar KPIs organizados
col1, col2, col3 = st.columns(3)

# ST9: Comunicación efectiva de datos (formatos claros)
with col1:
    st.metric(label="Ingresos Totales", value=f"${ingresos_totales:,.2f}")
with col2:
    st.metric(label="Total de Transacciones", value=f"{numero_transacciones:,}")
with col3:
    st.metric(label="Ticket Promedio", value=f"${ticket_promedio:,.2f}")

st.markdown("---")

# ==============================================================================
# ST3: Uso de gráficos (barras, líneas)
# ST6: Interpretación de visualizaciones
# ==============================================================================
st.subheader("Análisis Visual")

col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.markdown("**Tendencia de Ingresos a lo Largo del Tiempo**")
    # Preparar datos para gráfico de líneas (Agrupación por semana)
    df_temporal = df_filtrado.set_index('fecha').resample('W')['monto'].sum().reset_index()
    
    # Generar gráfico de líneas nativo
    st.line_chart(data=df_temporal, x='fecha', y='monto')
    st.caption("Interpretación: Evolución semanal de los ingresos. Ayuda a identificar estacionalidad.")

with col_grafico2:
    st.markdown("**Distribución de Ingresos por Categoría**")
    # Preparar datos para gráfico de barras
    df_categoria = df_filtrado.groupby('categoria')['monto'].sum().reset_index()
    df_categoria = df_categoria.set_index('categoria')
    
    # Generar gráfico de barras nativo
    st.bar_chart(df_categoria)
    st.caption("Interpretación: Comparativa del volumen de ventas por tipo de producto.")

st.markdown("---")

# ==============================================================================
# ST7: Errores comunes en dashboards
# Evitar mostrar tablas de datos crudos inmensas sin contexto o paginación.
# Se muestra sólo un resumen y los datos más recientes.
# ==============================================================================
st.subheader("Detalle de Transacciones Recientes")
st.markdown("Se exponen los últimos 10 registros para una auditoría rápida sin sobrecargar la interfaz.")

# Mostrar los datos ordenados descendentemente por fecha limitando a 10
st.dataframe(
    df_filtrado.sort_values("fecha", ascending=False).head(10),
    use_container_width=True
)
```