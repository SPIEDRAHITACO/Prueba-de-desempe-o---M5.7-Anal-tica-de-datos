<!-- General index of project files and folders, written as a simple reference map. -->

# Guía general de archivos del proyecto

Este documento describe, en términos generales, para qué sirve cada archivo y carpeta importante del repositorio. No entra línea por línea; resume el propósito funcional de cada componente.

## 1. Archivos principales del proyecto

### `README.md`
Documento principal del proyecto. Explica el objetivo general, la arquitectura, cómo ejecutar el pipeline, qué salidas genera y cómo se conecta todo con Power BI.

### `.env.example`
Plantilla de variables de entorno. Sirve como base para configurar la conexión a PostgreSQL y otros parámetros del pipeline sin exponer credenciales reales.

### `.gitignore`
Lista de archivos y carpetas que no deben subirse al control de versiones, como el entorno virtual, la caché de Python, archivos `.env` y salidas generadas.

### `requirements.txt`
Lista de dependencias Python necesarias para ejecutar el proyecto.

## 2. Carpeta `docs/`

### `docs/sales_data_sample.csv`
Fuente principal de ventas. Contiene el dataset transaccional que se limpia, analiza e integra con las dimensiones generadas por API y por transformación local.

### `docs/PHASE_1_DOCUMENTATION.md`
Documento técnico de Fase 1. Resume el alcance, el modelo final, la calidad de datos, la estrategia de asignación de clientes y la evidencia de validación.

### `docs/solution_justification.md`
Explica por qué se tomó el enfoque actual: uso de scripts modulares, modelo estrella, PostgreSQL como núcleo de integración, normalización de países y vistas analíticas.

### `docs/powerbi_build_guide.md`
Guía práctica para construir el reporte en Power BI. Describe opciones de conexión, páginas sugeridas y mapeo de preguntas de negocio a visualizaciones.

### `docs/FILE_GUIDE_ES.md`
Este mismo documento. Sirve como índice general del repositorio para entender rápidamente la función de cada archivo.

## 3. Carpeta `sql/`

### `sql/schema.sql`
Define la estructura de la base de datos en PostgreSQL. Crea el modelo estrella con dimensiones de fecha, geografía, productos y clientes, más la tabla de hechos de ventas.

### `sql/analytics_views.sql`
Crea las vistas analíticas que responden las preguntas del negocio. Estas vistas están pensadas para Power BI y para consultas directas sobre PostgreSQL.

## 4. Carpeta `src/`

### `src/common.py`
Centraliza utilidades compartidas: rutas del proyecto, carga de configuración desde `.env` y normalización de nombres de países.

### `src/00_create_database.py`
Automatiza la creación de la base de datos destino en PostgreSQL si todavía no existe.

### `src/01_ingest_and_profile.py`
Lee el CSV de ventas, limpia tipos, normaliza columnas y genera el reporte de calidad de datos.

### `src/02_build_customers_api.py`
Consume la API de RandomUser para construir la dimensión de clientes sintéticos.

### `src/03_build_regions_api.py`
Consume la API de RestCountries para construir la dimensión geográfica con información de países y regiones.

### `src/04_build_products.py`
Construye la dimensión de productos a partir de los códigos únicos del dataset de ventas y genera el archivo de ventas enriquecido con `producto_id`.

### `src/05_integrate_and_load_pg.py`
Es el núcleo del ETL. Une ventas, clientes, productos, fecha y geografía; crea las tablas dimensionales; carga todo en PostgreSQL; y deja listas las vistas analíticas.

### `src/06_export_powerbi_views.py`
Exporta las vistas analíticas desde PostgreSQL a CSV para que puedan consumirse en Power BI de manera rápida.

### `src/run_pipeline.py`
Orquesta todo el flujo de principio a fin en un solo comando. Ejecuta la creación de base, ingestión, construcción de dimensiones, carga e ինտégración, y exportación final.

### `src/__init__.py`
Marca la carpeta `src` como paquete Python. No agrega lógica de negocio; solo ayuda a la estructura del proyecto.

## 5. Carpeta `outputs/`

Esta carpeta contiene salidas generadas automáticamente por el pipeline. No son archivos de código; son evidencias del proceso y datos listos para análisis.

### `outputs/processed/`
Contiene los datasets ya procesados y listos para uso analítico o para Power BI.

Archivos principales:

- `sales_cleaned.csv`: ventas limpias y tipificadas.
- `customers.csv`: clientes generados desde API.
- `regions.csv`: países y metadata geográfica.
- `products.csv`: dimensión de productos.
- `sales_with_product_id.csv`: ventas enriquecidas con `producto_id`.
- `integration_report.csv`: resumen de carga e integración de la Fase 1.
- `powerbi_sales_trend_monthly.csv`: export de la vista de tendencia mensual.
- `powerbi_sales_by_region.csv`: export de ventas por región.
- `powerbi_product_performance.csv`: export de desempeño de productos.
- `powerbi_low_performance_regions.csv`: export de regiones con bajo rendimiento.
- `powerbi_customer_value.csv`: export de valor de clientes.
- `powerbi_geo_behavior.csv`: export de comportamiento geográfico.

### `outputs/reports/`
Contiene los reportes de calidad de datos.

Archivos principales:

- `data_quality_report.json`: versión estructurada del diagnóstico de calidad.
- `data_quality_report.md`: versión legible para revisión humana.

## 6. Carpetas de soporte

### `notebooks/`
Carpeta reservada para notebooks de exploración o pruebas. En este momento está vacía.

### `.venv/`
Entorno virtual local de Python. No forma parte del código fuente; solo permite ejecutar el proyecto con las dependencias correctas.

### `.git/`
Metadatos del repositorio Git. No se modifica manualmente.

## 7. Resumen funcional por flujo

Si se mira el proyecto por etapas, la función de cada grupo es esta:

1. Entrada y limpieza: `docs/sales_data_sample.csv`, `src/01_ingest_and_profile.py`.
2. Enriquecimiento externo: `src/02_build_customers_api.py`, `src/03_build_regions_api.py`.
3. Dimensión de producto: `src/04_build_products.py`.
4. Integración y carga: `src/00_create_database.py`, `src/05_integrate_and_load_pg.py`, `sql/schema.sql`.
5. Análisis: `sql/analytics_views.sql`, `src/06_export_powerbi_views.py`.
6. Orquestación: `src/run_pipeline.py`.
7. Documentación: `README.md` y los archivos en `docs/`.

## 8. Qué está listo para usar

El proyecto ya tiene cubierto lo necesario para la entrega funcional:

- Pipeline ejecutable de punta a punta.
- Modelo estrella en PostgreSQL.
- Reporte de calidad de datos.
- Vistas analíticas para Power BI.
- Documentación técnica y de apoyo.

## 9. Nota final

Los archivos dentro de `outputs/` se regeneran con cada ejecución del pipeline. Si cambian los datos fuente o las respuestas de las APIs, los CSV pueden variar ligeramente, pero la estructura general del proyecto se mantiene.
