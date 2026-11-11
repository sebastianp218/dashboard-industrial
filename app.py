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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "🏭 Resumen general",
        "📦 Producción y calidad",
        "📈 Variables operativas",
        "⚠️ Fallas",
        "💡 Hallazgos",
        "📋 Datos"
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

    st.header("📦 Producción y calidad")

    # ==================================================
    # PRODUCCIÓN POR LÍNEA
    # ==================================================

    st.subheader("Producción acumulada por línea")

    produccion_linea = (
        df_filtrado
        .groupby("linea", as_index=False)["produccion"]
        .sum()
    )

    fig_prod_linea = px.bar(
        produccion_linea,
        x="linea",
        y="produccion",
        title="Producción total por línea",
        labels={
            "linea": "Línea de producción",
            "produccion": "Producción acumulada"
        },
        text_auto=True
    )

    st.plotly_chart(
        fig_prod_linea,
        use_container_width=True
    )


    # ==================================================
    # PRODUCCIÓN EN EL TIEMPO
    # ==================================================

    st.subheader("Evolución temporal de la producción")

    produccion_tiempo = (
        df_filtrado
        .set_index("timestamp")
        .resample("1D")["produccion"]
        .sum()
        .reset_index()
    )

    fig_prod_tiempo = px.line(
        produccion_tiempo,
        x="timestamp",
        y="produccion",
        markers=True,
        title="Producción diaria",
        labels={
            "timestamp": "Fecha",
            "produccion": "Producción"
        }
    )

    st.plotly_chart(
        fig_prod_tiempo,
        use_container_width=True
    )


    # ==================================================
    # PRODUCCIÓN POR TURNO
    # ==================================================

    st.subheader("Producción por turno")

    produccion_turno = (
        df_filtrado
        .groupby("turno", as_index=False)["produccion"]
        .sum()
    )

    fig_prod_turno = px.bar(
        produccion_turno,
        x="turno",
        y="produccion",
        title="Producción acumulada por turno",
        labels={
            "turno": "Turno",
            "produccion": "Producción acumulada"
        },
        text_auto=True
    )

    st.plotly_chart(
        fig_prod_turno,
        use_container_width=True
    )


    st.markdown("---")

    st.header("🔍 Análisis de calidad")


    # ==================================================
    # DEFECTOS POR LÍNEA
    # ==================================================

    st.subheader("Defectos por línea")

    defectos_linea = (
        df_filtrado
        .groupby("linea", as_index=False)["defectos"]
        .sum()
    )

    fig_def_linea = px.bar(
        defectos_linea,
        x="linea",
        y="defectos",
        title="Defectos acumulados por línea",
        labels={
            "linea": "Línea de producción",
            "defectos": "Defectos"
        },
        text_auto=True
    )

    st.plotly_chart(
        fig_def_linea,
        use_container_width=True
    )


    # ==================================================
    # PORCENTAJE DE DEFECTOS POR LÍNEA
    # ==================================================

    st.subheader("Porcentaje de defectos por línea")

    calidad_linea = (
        df_filtrado
        .groupby("linea")
        .agg(
            produccion_total=("produccion", "sum"),
            defectos_totales=("defectos", "sum")
        )
        .reset_index()
    )

    calidad_linea["porcentaje_defectos"] = (
        calidad_linea["defectos_totales"]
        / calidad_linea["produccion_total"]
        * 100
    )

    fig_porcentaje_def = px.bar(
        calidad_linea,
        x="linea",
        y="porcentaje_defectos",
        title="Porcentaje de defectos por línea",
        labels={
            "linea": "Línea de producción",
            "porcentaje_defectos": "Defectos (%)"
        },
        text_auto=".2f"
    )

    st.plotly_chart(
        fig_porcentaje_def,
        use_container_width=True
    )


    # ==================================================
    # DEFECTOS POR TURNO
    # ==================================================

    st.subheader("Defectos por turno")

    defectos_turno = (
        df_filtrado
        .groupby("turno", as_index=False)["defectos"]
        .sum()
    )

    fig_def_turno = px.bar(
        defectos_turno,
        x="turno",
        y="defectos",
        title="Defectos acumulados por turno",
        labels={
            "turno": "Turno",
            "defectos": "Defectos"
        },
        text_auto=True
    )

    st.plotly_chart(
        fig_def_turno,
        use_container_width=True
    )
# ======================================================
# TAB 3 — VARIABLES OPERATIVAS
# ======================================================

with tab3:

    st.header("📈 Variables operativas")

    st.markdown(
        """
        Las gráficas presentan promedios horarios para facilitar
        la identificación de tendencias y variaciones operativas.
        """
    )


    # ==================================================
    # AGREGACIÓN TEMPORAL
    # ==================================================

    operativas = (
        df_filtrado
        .set_index("timestamp")
        [["temperatura", "vibracion", "presion"]]
        .resample("1h")
        .mean()
        .reset_index()
    )


    # ==================================================
    # TEMPERATURA
    # ==================================================

    st.subheader("🌡️ Temperatura")

    fig_temp = px.line(
        operativas,
        x="timestamp",
        y="temperatura",
        title="Evolución temporal de la temperatura",
        labels={
            "timestamp": "Fecha y hora",
            "temperatura": "Temperatura"
        }
    )

    st.plotly_chart(
        fig_temp,
        use_container_width=True
    )


    # ==================================================
    # VIBRACIÓN
    # ==================================================

    st.subheader("〰️ Vibración")

    fig_vib = px.line(
        operativas,
        x="timestamp",
        y="vibracion",
        title="Evolución temporal de la vibración",
        labels={
            "timestamp": "Fecha y hora",
            "vibracion": "Vibración"
        }
    )

    st.plotly_chart(
        fig_vib,
        use_container_width=True
    )


    # ==================================================
    # PRESIÓN
    # ==================================================

    st.subheader("🔵 Presión")

    fig_pres = px.line(
        operativas,
        x="timestamp",
        y="presion",
        title="Evolución temporal de la presión",
        labels={
            "timestamp": "Fecha y hora",
            "presion": "Presión"
        }
    )

    st.plotly_chart(
        fig_pres,
        use_container_width=True
    )
# ======================================================
# TAB 4 — FALLAS
# ======================================================

with tab4:

    st.header("⚠️ Análisis de fallas")


    # ==================================================
    # FALLAS POR LÍNEA
    # ==================================================

    st.subheader("Registros con falla por línea")

    fallas_linea = (
        df_filtrado
        .groupby("linea", as_index=False)["falla"]
        .sum()
        .rename(
            columns={
                "falla": "registros_con_falla"
            }
        )
    )

    fig_fallas_linea = px.bar(
        fallas_linea,
        x="linea",
        y="registros_con_falla",
        title="Cantidad de registros con falla por línea",
        labels={
            "linea": "Línea de producción",
            "registros_con_falla": "Registros con falla"
        },
        text_auto=True
    )

    st.plotly_chart(
        fig_fallas_linea,
        use_container_width=True
    )


    # ==================================================
    # EVOLUCIÓN TEMPORAL DE LAS FALLAS
    # ==================================================

    st.subheader("Evolución temporal de las fallas")

    fallas_tiempo = (
        df_filtrado
        .set_index("timestamp")
        .resample("1D")["falla"]
        .sum()
        .reset_index()
    )

    fig_fallas_tiempo = px.line(
        fallas_tiempo,
        x="timestamp",
        y="falla",
        markers=True,
        title="Registros con falla por día",
        labels={
            "timestamp": "Fecha",
            "falla": "Registros con falla"
        }
    )

    st.plotly_chart(
        fig_fallas_tiempo,
        use_container_width=True
    )


    # ==================================================
    # PORCENTAJE DE FALLA POR LÍNEA
    # ==================================================

    st.subheader(
        "Porcentaje de registros con falla por línea"
    )

    porcentaje_fallas_linea = (
        df_filtrado
        .groupby("linea")
        .agg(
            registros_totales=("falla", "count"),
            registros_con_falla=("falla", "sum")
        )
        .reset_index()
    )

    porcentaje_fallas_linea["porcentaje_falla"] = (
        porcentaje_fallas_linea["registros_con_falla"]
        / porcentaje_fallas_linea["registros_totales"]
        * 100
    )

    fig_porcentaje_fallas = px.bar(
        porcentaje_fallas_linea,
        x="linea",
        y="porcentaje_falla",
        title="Porcentaje de registros con falla por línea",
        labels={
            "linea": "Línea de producción",
            "porcentaje_falla": "Registros con falla (%)"
        },
        text_auto=".2f"
    )

    st.plotly_chart(
        fig_porcentaje_fallas,
        use_container_width=True
    )


    # ==================================================
    # RELACIÓN ENTRE VIBRACIÓN Y FALLAS
    # ==================================================

    st.subheader(
        "Relación entre vibración y registros de falla"
    )

    df_fallas = df_filtrado.copy()

    df_fallas["estado_falla"] = (
        df_fallas["falla"]
        .map({
            0: "Sin falla",
            1: "Con falla"
        })
    )

    fig_vibracion_falla = px.box(
        df_fallas,
        x="estado_falla",
        y="vibracion",
        points="outliers",
        title="Distribución de vibración según el estado de falla",
        labels={
            "estado_falla": "Estado",
            "vibracion": "Vibración"
        }
    )

    st.plotly_chart(
        fig_vibracion_falla,
        use_container_width=True
    )


    st.caption(
        """
        La gráfica permite explorar asociaciones entre los
        niveles de vibración y los registros de falla.
        Una asociación visual no implica necesariamente causalidad.
        """
    )
# ======================================================
# TAB 5 — HALLAZGOS
# ======================================================

with tab5:

    st.header("💡 Hallazgos y recomendaciones")

    st.markdown(
        """
        Los siguientes hallazgos se calculan a partir de los
        datos correspondientes a los filtros seleccionados.
        """
    )

    # ==================================================
    # 1. HALLAZGO DE PRODUCCIÓN
    # ==================================================

    produccion_por_linea = (
        df_filtrado
        .groupby("linea")["produccion"]
        .sum()
        .sort_values(ascending=False)
    )

    linea_mayor_produccion = produccion_por_linea.index[0]
    mayor_produccion = produccion_por_linea.iloc[0]

    produccion_total_h = produccion_por_linea.sum()

    participacion_produccion = (
        mayor_produccion
        / produccion_total_h
        * 100
    )


    # ==================================================
    # 2. HALLAZGO DE CALIDAD
    # ==================================================

    calidad = (
        df_filtrado
        .groupby("linea")
        .agg(
            produccion=("produccion", "sum"),
            defectos=("defectos", "sum")
        )
    )

    calidad["porcentaje_defectos"] = (
        calidad["defectos"]
        / calidad["produccion"]
        * 100
    )

    linea_mayor_defectos = (
        calidad["porcentaje_defectos"]
        .idxmax()
    )

    mayor_porcentaje_defectos = (
        calidad
        .loc[
            linea_mayor_defectos,
            "porcentaje_defectos"
        ]
    )


    # ==================================================
    # 3. HALLAZGO DE FALLAS
    # ==================================================

    fallas = (
        df_filtrado
        .groupby("linea")
        .agg(
            registros=("falla", "count"),
            fallas=("falla", "sum")
        )
    )

    fallas["porcentaje_falla"] = (
        fallas["fallas"]
        / fallas["registros"]
        * 100
    )

    linea_mayor_falla = (
        fallas["porcentaje_falla"]
        .idxmax()
    )

    mayor_porcentaje_falla = (
        fallas
        .loc[
            linea_mayor_falla,
            "porcentaje_falla"
        ]
    )
    # ==================================================
    # RELACIÓN VIBRACIÓN - FALLA
    # ==================================================

    vibracion_falla = (
        df_filtrado
        .groupby("falla")["vibracion"]
        .median()
    )

    if 0 in vibracion_falla.index and 1 in vibracion_falla.index:

        vibracion_sin_falla = vibracion_falla.loc[0]
        vibracion_con_falla = vibracion_falla.loc[1]

        diferencia_vibracion = (
            vibracion_con_falla
            - vibracion_sin_falla
        )


    # ==================================================
    # MOSTRAR HALLAZGOS
    # ==================================================

    st.subheader("🔎 Principales hallazgos")

    st.success(
        f"""
        **Hallazgo 1 — Producción:**  
        La {linea_mayor_produccion} presenta la mayor producción
        acumulada en el periodo seleccionado, con
        {mayor_produccion:,.0f} unidades, equivalentes al
        {participacion_produccion:.2f}% de la producción analizada.
        """
    )

    st.warning(
        f"""
        **Hallazgo 2 — Calidad:**  
        La {linea_mayor_defectos} presenta el mayor porcentaje de
        defectos, con una tasa de
        {mayor_porcentaje_defectos:.2f}% respecto a su producción.
        """
    )

    st.error(
        f"""
        **Hallazgo 3 — Fallas:**  
        La {linea_mayor_falla} presenta el mayor porcentaje de
        registros con falla, con
        {mayor_porcentaje_falla:.2f}% de sus registros asociados
        a una falla.
        """
    )


    # ==================================================
    # ANÁLISIS COMPLEMENTARIO
    # ==================================================

    if 0 in vibracion_falla.index and 1 in vibracion_falla.index:

        st.info(
            f"""
            **Análisis complementario:**  
            La mediana de vibración en registros sin falla es
            {vibracion_sin_falla:.2f}, mientras que en los registros
            con falla es {vibracion_con_falla:.2f}.
            La diferencia observada es de
            {diferencia_vibracion:.2f}.
            """
        )
    # ==================================================
    # RECOMENDACIONES
    # ==================================================

    st.subheader("🛠️ Recomendaciones")

    st.markdown(
        f"""
        **1. Analizar las prácticas de la {linea_mayor_produccion}.**  
        Evaluar los factores operativos asociados con su mayor nivel
        de producción y determinar cuáles prácticas podrían utilizarse
        como referencia para las demás líneas, verificando previamente
        que no impliquen deterioro en calidad o confiabilidad.

        **2. Priorizar acciones de mejora de calidad en la
        {linea_mayor_defectos}.**  
        Analizar las causas asociadas con su mayor porcentaje de
        defectos, considerando variables operativas, turno y condiciones
        del proceso para identificar oportunidades de reducción de
        reprocesos y desperdicios.

        **3. Reforzar el seguimiento de la {linea_mayor_falla}.**  
        Debido a que presenta el mayor porcentaje de registros con
        falla, se recomienda fortalecer el monitoreo de variables como
        vibración, temperatura y presión y evaluar acciones de
        mantenimiento preventivo o predictivo.
        """
    )
# ======================================================
# TAB 6 — DATOS
# ======================================================

with tab6:

    st.header("📋 Datos de la planta")

    st.markdown(
        """
        En esta sección se muestran los registros correspondientes
        a los filtros seleccionados en el panel lateral.
        """
    )

    # Cantidad de registros filtrados
    st.metric(
        "Registros mostrados",
        f"{len(df_filtrado):,}"
    )

    # Tabla interactiva
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True
    )

    # ==================================================
    # DESCARGA CSV
    # ==================================================

    csv = df_filtrado.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 Descargar datos filtrados en CSV",
        data=csv,
        file_name="datos_planta_filtrados.csv",
        mime="text/csv"
    )
