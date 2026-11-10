import streamlit as st
import pandas as pd
import plotly.express as px


# ======================================================
# CONFIGURACIÓN DE LA PÁGINA
# ======================================================

st.set_page_config(
    page_title="Dashboard Industrial",
    page_icon="🏭",
    layout="wide"
)


# ======================================================
# TÍTULO
# ======================================================

st.title("🏭 Dashboard Industrial")

st.markdown(
    """
    Aplicación interactiva para analizar el desempeño de una planta
    industrial compuesta por tres líneas de producción.

    El dashboard permite analizar producción, calidad, variables
    operativas y registros de falla.
    """
)


# ======================================================
# CARGA DE DATOS
# ======================================================

@st.cache_data
def cargar_datos():

    df = pd.read_csv(
        "data/dataset_planta_bigdata.csv"
    )

    # Convertir timestamp a fecha/hora
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # Eliminar registros con fecha inválida
    df = df.dropna(
        subset=["timestamp"]
    )

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Ordenar cronológicamente
    df = df.sort_values(
        "timestamp"
    )

    return df


df = cargar_datos()


# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("🔎 Filtros")


# ------------------------------------------------------
# FILTRO POR LÍNEA
# ------------------------------------------------------

lineas_disponibles = sorted(
    df["linea"]
    .dropna()
    .unique()
)

lineas_seleccionadas = st.sidebar.multiselect(
    "Línea de producción",
    options=lineas_disponibles,
    default=lineas_disponibles
)


# ------------------------------------------------------
# FILTRO POR TURNO
# ------------------------------------------------------

turnos_disponibles = sorted(
    df["turno"]
    .dropna()
    .unique()
)

turnos_seleccionados = st.sidebar.multiselect(
    "Turno",
    options=turnos_disponibles,
    default=turnos_disponibles
)


# ------------------------------------------------------
# FILTRO POR FECHA
# ------------------------------------------------------

fecha_min = df["timestamp"].min().date()
fecha_max = df["timestamp"].max().date()

rango_fechas = st.sidebar.date_input(
    "Rango de fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)


# ======================================================
# APLICAR FILTROS
# ======================================================

df_filtrado = df.copy()


# Línea
df_filtrado = df_filtrado[
    df_filtrado["linea"]
    .isin(lineas_seleccionadas)
]


# Turno
df_filtrado = df_filtrado[
    df_filtrado["turno"]
    .isin(turnos_seleccionados)
]


# Fecha
if len(rango_fechas) == 2:

    fecha_inicio = pd.to_datetime(
        rango_fechas[0]
    )

    fecha_fin = (
        pd.to_datetime(rango_fechas[1])
        + pd.Timedelta(days=1)
    )

    df_filtrado = df_filtrado[
        (
            df_filtrado["timestamp"]
            >= fecha_inicio
        )
        &
        (
            df_filtrado["timestamp"]
            < fecha_fin
        )
    ]


# ======================================================
# VALIDAR FILTROS
# ======================================================

if df_filtrado.empty:

    st.warning(
        "No existen registros para la combinación de filtros seleccionada."
    )

    st.stop()


# ======================================================
# INFORMACIÓN DE FILTROS
# ======================================================

st.sidebar.markdown("---")

st.sidebar.metric(
    "Registros seleccionados",
    f"{len(df_filtrado):,}"
)


# ======================================================
# PESTAÑAS DEL DASHBOARD
# ======================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🏭 Resumen general",
        "📦 Producción y calidad",
        "📈 Variables operativas",
        "⚠️ Fallas",
        "💡 Hallazgos"
    ]
)


# ======================================================
# TAB 1 — RESUMEN GENERAL
# ======================================================

with tab1:

    st.header(
        "Resumen general de la planta"
    )


    # --------------------------------------------------
    # KPI
    # --------------------------------------------------

    produccion_total = (
        df_filtrado["produccion"]
        .sum()
    )

    produccion_promedio = (
        df_filtrado["produccion"]
        .mean()
    )

    defectos_totales = (
        df_filtrado["defectos"]
        .sum()
    )


    if produccion_total > 0:

        porcentaje_defectos = (
            defectos_totales
            / produccion_total
            * 100
        )

    else:

        porcentaje_defectos = 0


    registros_falla = (
        df_filtrado["falla"]
        .sum()
    )


    porcentaje_falla = (
        registros_falla
        / len(df_filtrado)
        * 100
    )


    # --------------------------------------------------
    # MOSTRAR KPI
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Producción total",
        f"{produccion_total:,.0f}"
    )

    col2.metric(
        "Producción promedio",
        f"{produccion_promedio:,.2f}"
    )

    col3.metric(
        "Defectos totales",
        f"{defectos_totales:,.0f}"
    )


    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Porcentaje de defectos",
        f"{porcentaje_defectos:.2f} %"
    )

    col5.metric(
        "Registros con falla",
        f"{registros_falla:,.0f}"
    )

    col6.metric(
        "Registros con falla (%)",
        f"{porcentaje_falla:.2f} %"
    )


    st.markdown("---")


    st.info(
        """
        Los indicadores se actualizan automáticamente
        de acuerdo con los filtros seleccionados.
        """
    )


# ======================================================
# TAB 2 — PRODUCCIÓN Y CALIDAD
# ======================================================

with tab2:

    st.header(
        "📦 Producción y calidad"
    )

    st.info(
        "En el siguiente paso incorporaremos aquí las gráficas de producción y calidad."
    )


# ======================================================
# TAB 3 — VARIABLES OPERATIVAS
# ======================================================

with tab3:

    st.header(
        "📈 Variables operativas"
    )

    st.info(
        "Aquí incorporaremos temperatura, vibración y presión."
    )


# ======================================================
# TAB 4 — FALLAS
# ======================================================

with tab4:

    st.header(
        "⚠️ Análisis de fallas"
    )

    st.info(
        "Aquí incorporaremos el análisis de fallas desarrollado anteriormente."
    )


# ======================================================
# TAB 5 — HALLAZGOS
# ======================================================

with tab5:

    st.header(
        "💡 Hallazgos y recomendaciones"
    )

    st.info(
        "Esta sección se completará después de analizar los resultados finales."
    )
