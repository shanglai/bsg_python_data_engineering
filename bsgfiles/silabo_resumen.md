# Curso: Python para Ingeniería de Datos
## Resumen del Sílabo

---

## Estructura del curso

| # | Capítulo | Secciones | Bloques |
|---|----------|-----------|---------|
| 1 | Fundamentos de Python aplicado a datos | Sección 1: Python para procesamiento · Sección 2: Pandas y mini ETL | 8 bloques |
| 2 | Almacenamiento y consultas de datos | Sección 3: SQL y MySQL · Sección 4: Pipeline v1 | 8 bloques |
| 3 | Exposición y consumo de datos | Sección 5: APIs con FastAPI · Sección 6: Visualización con Streamlit | 8 bloques |
| 4 | Manejo de datos y despliegue local | Sección 7: Formatos y storage · Sección 8: Docker | 8 bloques |
| 5 | Automatización y orquestación | Sección 9: Automatización · Sección 10: Orquestación e infra | 8 bloques |
| 6 | Integración, despliegue y proyecto final | Sección 11: CI/CD y monitoreo · Sección 12: Proyecto e IA | 7 bloques |

**Total: 6 capítulos · 12 secciones · 47 bloques**

---

## Capítulo 1 — Fundamentos de Python aplicado a datos

### Sección 1: Python para procesamiento de datos

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 1.1.1 | Introducción al curso y caso del pipeline | Data Engineering, pipeline, dataset de transacciones, filosofía del curso |
| 1.1.2 | Variables, tipos y estructuras básicas | int/float/str/bool, listas, diccionarios, loops, nulos |
| 1.1.3 | Lectura de archivos CSV y primeros scripts | módulo csv, parsing, encoding, scripts reproducibles |
| 1.1.4 | Funciones aplicadas a limpieza de datos | encapsulación, try/except, list comprehensions, modularidad |

### Sección 2: Pandas y mini ETL

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 1.2.1 | Introducción a Pandas y DataFrames | Series/DataFrame, read_csv, head/shape/info |
| 1.2.2 | Limpieza de datos (nulos, tipos, columnas) | isnull, fillna/dropna, astype, normalización |
| 1.2.3 | Transformaciones y generación de variables | filtrado, columnas derivadas, apply, groupby |
| 1.2.4 | Guardado de datos (CSV y Parquet) | ETL completo, persistencia, CSV vs Parquet |

---

## Capítulo 2 — Almacenamiento y consultas de datos

### Sección 3: SQL y MySQL

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 2.3.1 | Fundamentos SQL (SELECT, WHERE) | tablas, claves, sintaxis, Python vs SQL |
| 2.3.2 | JOINs y agregaciones | INNER/LEFT JOIN, SUM/COUNT/AVG, GROUP BY |
| 2.3.3 | Conexión Python → MySQL | mysql-connector, SQLAlchemy, queries desde Python |
| 2.3.4 | Inserción y consulta del pipeline | INSERT, validación post-carga, ETL completo |

### Sección 4: Pipeline de datos v1

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 2.4.1 | Integración CSV/API → transformación | ingesta, múltiples fuentes, pipeline continuo |
| 2.4.2 | Persistencia en MySQL y archivos | dual storage, append vs overwrite |
| 2.4.3 | Modularización del pipeline | separación responsabilidades, estructura de carpetas |
| 2.4.4 | Ejecución completa del pipeline | end-to-end, sanity checks, pipeline reproducible |

---

## Capítulo 3 — Exposición y consumo de datos

### Sección 5: APIs con FastAPI

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 3.5.1 | Introducción a APIs y FastAPI | HTTP, GET/POST, endpoints, JSON, contrato |
| 3.5.2 | Endpoints básicos | rutas, path operations, Swagger UI, datos estáticos |
| 3.5.3 | Conexión API → base de datos | queries dinámicas, capa de acceso a datos |
| 3.5.4 | Filtros y validaciones | query params, Pydantic, códigos HTTP, seguridad básica |

### Sección 6: Visualización con Streamlit

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 3.6.1 | Introducción a Streamlit | app web en Python, componentes básicos, prototipado |
| 3.6.2 | Dashboard básico | tablas, métricas, gráficos simples, storytelling |
| 3.6.3 | Conexión a API o datos procesados | consumo de endpoints, lectura directa, arquitectura |
| 3.6.4 | Métricas y visualizaciones | KPIs, barras/líneas, filtros interactivos |

---

## Capítulo 4 — Manejo de datos y despliegue local

### Sección 7: Formatos de archivos y storage

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 4.7.1 | CSV vs Parquet | columnar vs row-based, compresión, performance |
| 4.7.2 | Organización local de datos | raw/processed/output, naming, versionado |
| 4.7.3 | Cloud storage (demo) | GCS/S3, object storage, escalabilidad |
| 4.7.4 | Integración con pipeline | resultados intermedios, particionamiento (intro) |

### Sección 8: Docker y entorno reproducible

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 4.8.1 | Introducción a Docker | imagen, contenedor, VM vs Docker, portabilidad |
| 4.8.2 | Creación de Dockerfile | FROM/COPY/RUN/CMD, capas, optimización |
| 4.8.3 | requirements.txt y dependencias | pip freeze, fijación de versiones, reproducibilidad |
| 4.8.4 | docker-compose y servicios | compose.yaml, API + DB, redes entre contenedores |

---

## Capítulo 5 — Automatización y orquestación

### Sección 9: Automatización de procesos

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 5.9.1 | Scripts automatizados | batch, parametrización, pipelines ejecutables |
| 5.9.2 | Cronjobs | sintaxis cron, tareas recurrentes, paths/permisos |
| 5.9.3 | Logs y ejecución programada | logging, INFO/WARNING/ERROR, trazabilidad |
| 5.9.4 | Integración con pipeline | ejecución periódica, retry (intro), pipeline operativo |

### Sección 10: Orquestación e infraestructura

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 5.10.1 | Introducción a Airflow | DAG, dependencias, cron vs Airflow |
| 5.10.2 | DAG simple | tareas, dependencias, UI Airflow, buenas prácticas |
| 5.10.3 | Infraestructura como código (Terraform demo) | IaC, declarativo, init→plan→apply, bucket demo |
| 5.10.4 | Definición del proyecto final | rutas (pipeline/API/dashboard), criterios, entregables |

---

## Capítulo 6 — Integración, despliegue y proyecto final

### Sección 11: CI/CD y monitoreo

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 6.11.1 | Introducción a GitHub y repositorios | control de versiones, commits, flujo add/commit/push |
| 6.11.2 | CI/CD con GitHub Actions | integración continua, workflows, push/PR triggers |
| 6.11.3 | Monitoreo (logs, health checks) | observabilidad, /health endpoint, Prometheus (intro) |
| 6.11.4 | Seguimiento del proyecto | revisión de arquitectura, validación end-to-end |

### Sección 12: Presentación de proyecto e IA aplicada

| Bloque | Tema | Subtemas clave |
|--------|------|----------------|
| 6.12.1 | Presentación de proyectos (parte 1) | arquitectura, demo funcional, decisiones técnicas |
| 6.12.2 | Presentación de proyectos (parte 2) | retroalimentación entre pares, comparación de enfoques |
| 6.12.3 | IA como acelerador de ingeniería | LLMs en DE, prompting, limitaciones, validación humana |

---

## Hilo conductor del curso

El curso gira en torno a un **dataset de transacciones** que evoluciona a lo largo de los 6 capítulos:

```
CSV crudo → Python → Pandas → MySQL → FastAPI → Streamlit
                                ↓
                           Docker → Airflow → GitHub CI/CD
```

Cada bloque agrega una capa al sistema, de modo que al final el alumno tiene un **pipeline de datos completo y desplegable**.

---

## Notas para generación de contenido

- **Profundidad**: introductoria-intermedia. No asume experiencia previa en DE.
- **Enfoque**: aplicado (no teórico). Cada bloque tiene un script o componente concreto.
- **Caso práctico único**: el dataset de transacciones corre de principio a fin.
- **Entregable final**: pipeline, API REST o dashboard (el alumno elige su ruta).
- **Último bloque**: IA como copiloto (generación de Dockerfiles, SQL, funciones de limpieza con prompts).
