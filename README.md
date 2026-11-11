# Dashboard Industrial – Proyecto Integrador

Proyecto final de la asignatura **Digitalización de Plantas Productivas**.

## Descripción

Este proyecto desarrolla una aplicación web interactiva en **Streamlit** para analizar el desempeño de una planta industrial compuesta por tres líneas de producción.

El dashboard utiliza un conjunto de datos históricos de planta y permite analizar indicadores de producción, calidad, variables operativas y registros de falla mediante filtros interactivos.

## Objetivo

Desarrollar una herramienta de visualización y análisis que facilite la supervisión del comportamiento de la planta y permita identificar tendencias, diferencias entre líneas de producción, condiciones operativas y posibles oportunidades de mejora.

## Herramientas utilizadas

- Python
- Pandas
- Plotly
- Streamlit
- GitHub
- Streamlit Community Cloud
- Inteligencia Artificial (ChatGPT)

## Dataset

La aplicación utiliza el archivo:

`data/dataset_planta_bigdata.csv`

El conjunto de datos contiene información histórica de tres líneas de producción e incluye variables relacionadas con:

- Línea de producción
- Turno
- Operario
- Temperatura
- Vibración
- Presión
- Producción
- Defectos
- Registros de falla

## Funcionalidades del dashboard

El dashboard permite:

- Consultar seis indicadores clave de desempeño (KPI).
- Analizar la producción por línea, turno y periodo.
- Analizar defectos y porcentajes de defectos.
- Monitorear temperatura, vibración y presión.
- Analizar registros y porcentajes de falla.
- Explorar la relación entre vibración y fallas.
- Filtrar la información por línea, turno y rango de fechas.
- Consultar una tabla interactiva con los datos filtrados.
- Descargar los registros filtrados en formato CSV.
- Consultar hallazgos y recomendaciones generados a partir de los datos.

## Estructura del proyecto

```text
dashboard-industrial/
│
├── app.py
├── requirements.txt
├── README.md
│
└── data/
    └── dataset_planta_bigdata.csv
```

## Ejecución local

Para ejecutar el proyecto localmente:

```bash
pip install -r requirements.txt
```

Posteriormente ejecutar:

```bash
streamlit run app.py
```

## Integrantes

- Sebastián Pantoja
- Juliana Castañeda
- Gabriela Álvares

## Aplicación publicada

Dashboard disponible en Streamlit Community Cloud:

https://dashboard-industrial-b8rw7pxrjsuykrxjk89mp4.streamlit.app/

## Repositorio

El código fuente, los datos y las dependencias necesarias para ejecutar el proyecto se encuentran en este repositorio público de GitHub.
