---
marp: true
theme: bsg
size: 16:9
paginate: true
footer: 'Python para Ingeniería de Datos · Capítulo 4: Manejo de datos y despliegue local · BSG Institute'
---

---

<!-- _class: title -->
# Capítulo 4: Manejo de datos y despliegue local
## Formatos de archivos y storage

---

<!-- _class: section -->
# Sección 7: Formatos de archivos y storage
## En esta sección construiremos la capa de formatos de archivos y storage del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de formatos de archivos y storage en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 4.7.1: CSV vs Parquet
- Bloque 4.7.2: Organización local de datos
- Bloque 4.7.3: Cloud storage (demo)
- Bloque 4.7.4: Integración con pipeline

---

<!-- ============================================================ -->
<!-- BLOQUE 4.7.1 — CSV vs Parquet                               -->
<!-- Scripts: scripts/cap4/4_7_1_Script.py                    -->
<!-- Notebook: notebooks/cap4/4_7_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 4.7.1
## CSV vs Parquet

> El pipeline guarda datos; ahora estudiamos cómo elegir el formato correcto para cada caso.

**Al terminar este bloque podrás:**
- Comparar CSV y Parquet en tamaño, velocidad de lectura y compatibilidad
- Leer y escribir Parquet con Pandas y pyarrow
- Elegir el formato adecuado según el caso de uso (interoperabilidad vs eficiencia)

---

# Capítulo 4: Manejo de datos y despliegue local, Sesión 7: Almacenamiento y Cloud, Bloque 1: Formatos de almacenamiento

## La importancia del almacenamiento en la Ingeniería de Datos

El almacenamiento no es solo "guardar datos", es una decisión de diseño crítica en cualquier pipeline. La forma en que persistes la información impacta directamente en:

* **Costos:** Almacenar terabytes de datos de forma ineficiente multiplica los costos de infraestructura.
* **Velocidad de lectura/escritura (I/O):** El cuello de botella más común en procesamiento de datos no es la CPU, sino el tiempo que toma leer o escribir en disco.
* **Interoperabilidad:** Los datos almacenados por tu pipeline probablemente serán consumidos por otras herramientas (APIs, motores SQL, dashboards). El formato elegido debe ser compatible con estos consumidores.

En ingeniería de datos, optimizar el almacenamiento es el primer paso para construir sistemas robustos y eficientes.

---

# Capítulo 4: Manejo de datos y despliegue local, Sesión 7: Almacenamiento y Cloud, Bloque 1: Formatos de almacenamiento

## Tipos de archivos comunes: CSV y Parquet

En el ecosistema de datos, interactuamos con múltiples formatos, pero dos de los más predominantes son **CSV** (Comma-Separated Values) y **Parquet**.

### Características de CSV
* **Legibilidad:** Es un formato de texto plano. Puede ser abierto y leído por un ser humano, Excel, o cualquier editor de texto.
* **Simplicidad:** Altamente estandarizado y soportado por prácticamente cualquier lenguaje de programación o sistema heredado.
* **Desventajas:** No infiere tipos de datos de forma nativa (todo se lee como texto inicialmente), ocupa mucho espacio y no está optimizado para consultas complejas.

### Características de Parquet
* **Eficiencia:** Es un formato binario. No puede ser leído directamente por un humano, pero es extremadamente rápido para las máquinas.
* **Tipado estricto:** Guarda la metadata del esquema (schema) y los tipos de datos en el mismo archivo.
* **Compresión:** Diseñado nativamente para comprimir datos de manera muy eficiente, reduciendo drásticamente el peso del archivo.

---

# Capítulo 4: Manejo de datos y despliegue local, Sesión 7: Almacenamiento y Cloud, Bloque 1: Formatos de almacenamiento

## Formatos Row-based vs Columnar

Para entender por qué Parquet es más eficiente que CSV en analítica, debemos entender cómo guardan la información.

### Almacenamiento basado en filas (Row-based)
Formatos como **CSV** o JSON guardan los datos registro por registro. 
* Si tienes una tabla con 100 columnas y solo quieres sumar los valores de la columna "ingresos", el sistema tiene que leer toda la fila (las 100 columnas) registro por registro para extraer solo ese dato.
* **Ideal para:** Escrituras transaccionales (agregar un nuevo cliente con todos sus datos).

### Almacenamiento basado en columnas (Columnar)
Formatos como **Parquet** guardan los datos agrupados por columnas.
* Todos los valores de la columna "ingresos" se almacenan juntos en el disco.
* Si necesitas sumar los "ingresos", el sistema va directo a ese bloque de memoria, ignorando las otras 99 columnas.
* **Ideal para:** Analítica, cálculos de métricas y lectura masiva de datos específicos.

---

# Capítulo 4: Manejo de datos y despliegue local, Sesión 7: Almacenamiento y Cloud, Bloque 1: Formatos de almacenamiento

## Compresión, Eficiencia e Impacto en la Performance

La arquitectura columnar de Parquet permite un nivel de compresión que un formato basado en filas rara vez alcanza. 

* **Codificación y Compresión:** Al tener datos del mismo tipo juntos (por ejemplo, una columna de puros números enteros o fechas repetidas), los algoritmos de compresión (como Snappy o Gzip) funcionan de manera óptima.
* **Impacto en el pipeline:** 
  * Un archivo CSV de 1 GB puede reducirse a 150 MB en Parquet.
  * Menos tamaño significa menos datos viajando por la red (menor latencia).
  * Menos datos en disco significa lecturas más rápidas (menor I/O).

**Comparación de Performance (Estimación Conceptual):**
| Métrica | CSV | Parquet |
| :--- | :--- | :--- |
| Tamaño en disco | Alto | Bajo |
| Velocidad de escritura | Rápida | Moderada (requiere estructurar) |
| Velocidad de lectura analítica| Lenta | Muy rápida |
| Preservación de tipos | No (texto plano) | Sí (metadata incluida) |

---

# Capítulo 4: Manejo de datos y despliegue local, Sesión 7: Almacenamiento y Cloud, Bloque 1: Formatos de almacenamiento

## Selección de formato y preparación para la escalabilidad

La elección del formato dependerá de la etapa del pipeline y del caso de uso.

### Casos de uso recomendados
* **Usa CSV cuando:** 
  * Estás ingiriendo datos de sistemas legacy que solo exportan en texto.
  * Necesitas hacer una inspección visual rápida de una muestra de datos.
  * El volumen de datos es pequeño (unos pocos miles de registros).
* **Usa Parquet cuando:**
  * Estás guardando datos limpios y transformados (Capa "Processed" o "Silver/Gold").
  * Los datos van a ser consultados frecuentemente para dashboards o machine learning.
  * Manejas millones de registros y necesitas optimizar costos de nube y tiempos de respuesta.

### Preparación para pipelines escalables
Adoptar formatos como Parquet desde el inicio te prepara para escalar. A medida que tu pipeline crezca de procesar megabytes a terabytes, un almacenamiento columnar evitará que tu infraestructura colapse, asegurando un flujo de datos >> rápido, seguro y económico.

---

<!-- _class: code -->
## Practica: Comparar CSV vs Parquet con el dataset de transacciones

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar csv vs parquet con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap4/4_7_1_Script.py
"""
Capítulo 4: Manejo de datos y despliegue local
Sección 7: Almacenamiento local y en la nube
Bloque 1: Importancia del almacenamiento y comparación de formatos (CSV vs Parquet)

Descripción: Este script demuestra empíricamente las diferencias entre los formatos
CSV (row-based, texto plano) y Parquet (columnar, comprimido) en términos de 
tamaño en disco, tiempos de escritura y tiempos de lectura. 
Entender estas diferencias es clave para preparar pipelines escalables.
"""

import pandas as pd
import numpy as np
import time
import os

# Establecer semilla para garantizar la reproducibilidad de los datos
np.random.seed(987654)

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap4/4_7_1_Script.ipynb)

---

## Errores comunes en el Bloque 4.7.1

- **Usar CSV para datos de más de 1M filas**
  → rendimiento muy bajo en lecturas

- **No especificar el schema al leer Parquet**
  → tipos inferidos incorrectamente

- **Confundir compresión snappy con gzip**
  → diferencias en velocidad vs tamaño

---

## Resumen: Bloque 4.7.1

**Lo que aprendiste:**
- Comparar CSV y Parquet en tamaño, velocidad de lectura y compatibilidad
- Leer y escribir Parquet con Pandas y pyarrow
- Elegir el formato adecuado según el caso de uso (interoperabilidad vs eficiencia)

**Lo que construiste:**
El script `4_7_1_Script.py` que comparar csv vs parquet con el dataset de transacciones usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 4.7.2: Organización local de datos

---

<!-- ============================================================ -->
<!-- BLOQUE 4.7.2 — Organización local de datos                  -->
<!-- Scripts: scripts/cap4/4_7_2_Script.py                    -->
<!-- Notebook: notebooks/cap4/4_7_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 4.7.2
## Organización local de datos

> Con los formatos dominados, organizamos el almacenamiento local de forma profesional.

**Al terminar este bloque podrás:**
- Diseñar una estructura de carpetas para un data lake local (raw/processed/output)
- Implementar particionado por fecha en los archivos Parquet
- Crear funciones de utilidad para gestionar rutas de forma dinámica

---

## Concepto de almacenamiento local

El almacenamiento local se refiere a la persistencia de datos directamente en los discos de la máquina o servidor donde se ejecuta nuestro pipeline de ingeniería de datos. 

En etapas tempranas de desarrollo o en flujos de datos a pequeña escala, el disco local actúa como nuestro primer "Data Lake". Aunque está limitado por la capacidad del hardware específico y no cuenta con la disponibilidad de la nube, ofrece ventajas operativas:

* **Baja latencia:** La lectura y escritura es inmediata, acelerando la fase de desarrollo y pruebas.
* **Simplicidad:** No requiere autenticación de red, configuración de credenciales complejas ni gestión de permisos de servicios externos.
* **Aislamiento:** Permite probar transformaciones de forma segura sin afectar bases de datos de producción.

Comprender cómo gestionar datos localmente es el paso previo y fundamental antes de migrar a soluciones en la nube como Amazon S3 o Google Cloud Storage.

---

## Organización de carpetas y estructura de datos

Un proyecto de ingeniería de datos sin una estructura de carpetas definida rápidamente se vuelve inmanejable. La separación lógica de los datos según su nivel de procesamiento garantiza orden y claridad.

La convención estándar en la industria divide los datos en tres niveles principales:

1. **Raw (Datos crudos):**
   * Es el punto de entrada. Aquí se guardan los datos tal como provienen de la fuente original (APIs, bases de datos, CSVs externos).
   * **Regla de oro:** Los datos en la carpeta `raw` son inmutables. Nunca se sobrescriben ni se modifican manualmente.

2. **Processed (Datos procesados o intermedios):**
   * Contiene datos que ya pasaron por una limpieza inicial (manejo de nulos, corrección de tipos).
   * Se utilizan como pasos intermedios si el pipeline falla y necesita reanudarse sin volver a procesar desde cero.

3. **Output / Curated (Datos finales):**
   * Datos completamente transformados, enriquecidos y listos para ser consumidos por reportes, dashboards o modelos de Machine Learning.

---

## Estructura de directorio de un proyecto

Una vista clásica de un proyecto de datos bien organizado se vería de la siguiente manera:

```text
mi_pipeline_datos/
|-- data/
|   |-- raw/
|   |   |-- transacciones_202310.csv
|   |-- processed/
|   |   |-- transacciones_limpias_202310.parquet
|   |-- output/
|   |   |-- reporte_mensual_202310.csv
|-- src/
|   |-- ingesta.py
|   |-- transformacion.py
|-- requirements.txt
```

Esta separación física refleja las etapas lógicas del pipeline (Extract >> Transform >> Load).

---

## Convenciones de nombres (Naming Conventions)

Nombrar los archivos de manera estructurada es vital para que tanto humanos como scripts puedan identificar el contenido sin necesidad de abrirlos. 

**Buenas prácticas para nombrar archivos:**
* **Ser descriptivo:** Indicar qué contiene el archivo (`ventas`, `clientes`, `logs`).
* **Usar minúsculas y guiones bajos:** Evitar espacios y caracteres especiales (`ventas_mensuales.csv` en lugar de `Ventas Mensuales Final!.csv`).
* **Incluir marcas de tiempo:** Utilizar el formato ISO estándar para fechas, preferiblemente `YYYYMMDD` o `YYYYMMDD_HHMMSS`. Esto permite que los archivos se ordenen alfanuméricamente de manera natural en el explorador de archivos.
* **Indicar versiones:** Si un archivo se reprocesa, es útil manejar sufijos como `_v1`, `_v2`.

**Ejemplo de evolución de un archivo:**
* `data/raw/users_20231101.csv`
* `data/processed/users_cleaned_20231101.parquet`

---

## Manejo de rutas en Python

En ingeniería de datos, el código debe funcionar en cualquier máquina, independientemente de si el sistema operativo es Windows, macOS o Linux. El principal error al manejar archivos locales es usar rutas absolutas (ej. `C:/Usuarios/Juan/proyecto/data`).

**El uso de la librería `pathlib`:**
Python ofrece el módulo `pathlib`, que maneja las rutas de forma orientada a objetos y resuelve automáticamente los conflictos de separadores de directorios (los `\` de Windows frente a los `/` de sistemas UNIX).

```python
from pathlib import Path

# Definir la ruta base del proyecto (el directorio actual)
BASE_DIR = Path(__file__).resolve().parent.parent

# Construir rutas de manera dinámica
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "output"

# Asegurar que el directorio exista
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

El uso de rutas relativas asegura la portabilidad del pipeline.

---

## Estrategias de escritura: Sobrescritura vs Append

Cuando el pipeline llega a la fase de almacenamiento, debemos decidir cómo registrar los nuevos datos. Existen dos estrategias principales:

**1. Sobrescritura (Overwrite / Full Load):**
* Consiste en borrar el archivo anterior y escribir uno nuevo completo cada vez que corre el pipeline.
* **Uso ideal:** Tablas de dimensiones o catálogos pequeños (ej. un catálogo de productos que se actualiza diariamente), o cuando calcular incrementos es más costoso que procesar todo de nuevo.

**2. Inserción incremental (Append):**
* Consiste en agregar los registros nuevos al final del archivo existente (o crear particiones nuevas).
* **Uso ideal:** Tablas de hechos o registros transaccionales (ej. ventas diarias, logs de usuarios). 
* **Ventaja:** Mayor eficiencia, ya que solo se procesa la diferencia (el delta).

---

## Versionado básico y Manejo de datos históricos

El almacenamiento local requiere estrategias de versionado para proteger la historia de la información. 

**Manejo de datos históricos:**
En un esquema incremental o particionado, en lugar de mantener un único archivo gigante, se recomienda crear archivos separados por rangos de tiempo (por ejemplo, un archivo diario o mensual). 

* `ventas_20231001.parquet`
* `ventas_20231002.parquet`

**Versionado de datos procesados:**
Si la lógica de transformación cambia (por ejemplo, se descubre un error en el cálculo de impuestos), contar con los archivos `raw` intactos nos permite regenerar los datos históricos. Guardar las nuevas salidas con un identificador de versión (`_v2`) nos permite comparar el impacto del nuevo pipeline frente al anterior.

---

## Evitar pérdida de datos y Reproducibilidad

La pérdida de datos es uno de los mayores riesgos en la ejecución de pipelines. 

**Medidas de prevención:**
1. **Inmutabilidad del Raw:** Como se mencionó, bloquear lógicamente las modificaciones al directorio de origen.
2. **Validación antes de sobrescribir:** Si se usa la estrategia de "Overwrite", el script debe verificar que el nuevo dataset no está vacío o corrupto antes de eliminar la versión anterior.
3. **Escritura atómica:** Escribir los resultados en un archivo temporal (`temp_output.csv`) y renombrarlo solo cuando la escritura haya finalizado exitosamente. Esto evita archivos incompletos si el proceso se interrumpe a la mitad.

**Reproducibilidad del pipeline:**
Un pipeline es reproducible si, al alimentarlo con los mismos datos crudos (`raw`), genera exactamente la misma salida (`output`). Mantener una gestión estricta de rutas relativas, un entorno cerrado y un historial inmutable de datos de entrada garantiza que el código sea predecible y seguro.

---

<!-- _class: code -->
## Practica: Implementar estructura de carpetas de data lake local

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar organización local de datos con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap4/4_7_2_Script.py
"""
Capítulo 4: Manejo de datos y despliegue local
Sección 7: Storage local y nube
Bloque 2: Concepto de almacenamiento local

Descripción:
Este script aborda los fundamentos de la persistencia de datos a nivel local.
Cubre la creación de la estructura de directorios típica de un proyecto de datos (raw, processed, output),
el manejo robusto de rutas, convenciones de nombres, estrategias de guardado (append vs overwrite) y 
el versionado de archivos para garantizar la reproducibilidad y evitar la pérdida de datos históricos.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap4/4_7_2_Script.ipynb)

---

## Errores comunes en el Bloque 4.7.2

- **Guardar todos los archivos en la misma carpeta**
  → imposible encontrar datos históricos

- **No incluir la fecha en el nombre del archivo**
  → sobreescritura accidental

- **Usar rutas absolutas hardcodeadas**
  → el pipeline falla en otro entorno

---

## Resumen: Bloque 4.7.2

**Lo que aprendiste:**
- Diseñar una estructura de carpetas para un data lake local (raw/processed/output)
- Implementar particionado por fecha en los archivos Parquet
- Crear funciones de utilidad para gestionar rutas de forma dinámica

**Lo que construiste:**
El script `4_7_2_Script.py` que implementar estructura de carpetas de data lake local usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 4.7.3: Cloud storage (demo)

---

<!-- ============================================================ -->
<!-- BLOQUE 4.7.3 — Cloud storage (demo)                         -->
<!-- Scripts: scripts/cap4/4_7_3_Script.py                    -->
<!-- Notebook: notebooks/cap4/4_7_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 4.7.3
## Cloud storage (demo)

> El almacenamiento local tiene límites; vemos cómo escalar a la nube (demo del instructor).

**Al terminar este bloque podrás:**
- Entender los conceptos de Object Storage (S3, GCS, Azure Blob)
- Ver cómo se estructura un bucket y cómo se nombran los objetos
- Comparar el costo y latencia de cloud storage vs almacenamiento local

---

# Capítulo 4: Manejo de datos y despliegue local, Sección 7: Almacenamiento, Bloque 3: Cloud storage (demo)

## Introducción al Almacenamiento en la Nube
* **Limitaciones del entorno local:** Hasta este punto del curso, nuestro pipeline ha dependido del almacenamiento en el disco duro de nuestra computadora. Esto presenta límites estrictos de capacidad, vulnerabilidad ante fallos físicos y aislamiento frente a otros miembros del equipo.
* **El almacenamiento en la Nube:** Permite externalizar la persistencia de datos hacia servidores remotos y altamente optimizados administrados por proveedores tecnológicos, accesibles a través de internet.
* **Transición de local a cloud:** El cambio arquitectónico es sutil pero poderoso. En lugar de leer `C:/datos/transacciones.csv`, leeremos desde un identificador remoto. La lógica de transformación en Python o Pandas permanece exactamente igual.

## El Concepto de Object Storage
* A diferencia de un disco duro tradicional (almacenamiento por bloques) o una estructura clásica de carpetas, la nube en ingeniería de datos utiliza **Object Storage** (Almacenamiento de Objetos).
* **Componentes fundamentales:**
  * **Bucket (Contenedor o Cubeta):** Es el espacio de almacenamiento de nivel superior. Funciona como el directorio raíz de tus datos y su nombre debe ser único a nivel global.
  * **Objeto:** Es el archivo en sí mismo junto con toda su información. Un CSV o un archivo Parquet es un objeto.
  * **Llave (Key):** Es el identificador único del objeto dentro del bucket. Para nosotros simula una ruta de carpetas (por ejemplo: `datos_crudos/2026/transacciones.csv`), pero estructuralmente es un sistema plano.
  * **Metadatos:** Información adicional ligada al objeto (tamaño, tipo de formato, fecha de modificación).

## Servicios Comunes y sus Ventajas
* Existen múltiples proveedores, pero en la industria de datos hay estándares claros que ofrecen servicios de Object Storage:
  * **Amazon S3 (Simple Storage Service):** El estándar de la industria, perteneciente a AWS.
  * **Google Cloud Storage (GCS):** La alternativa robusta de Google Cloud Platform.
* **Ventajas clave para el Data Engineering:**
  * **Escalabilidad:** El almacenamiento es virtualmente infinito. Puedes comenzar con unos cuantos megabytes y escalar automáticamente a petabytes sin configurar hardware nuevo.
  * **Disponibilidad y Durabilidad:** Los archivos se replican en múltiples ubicaciones físicas. La probabilidad de que un archivo se pierda o corrompa es prácticamente nula.

## Seguridad Básica y Uso Colaborativo
* **Seguridad conceptual:** En la nube la seguridad es primordial. Por defecto, todos los buckets deben ser **privados**.
  * El acceso desde nuestro pipeline en Python requiere autenticación mediante credenciales (Access Keys o cuentas de servicio).
  * Siempre se aplica el principio de menor privilegio: si un script solo necesita limpiar datos, se le otorga permiso de lectura y no de borrado definitivo.
* **Uso colaborativo:**
  * Al centralizar los archivos en la nube, se crea una única fuente de verdad (Single Source of Truth).
  * Varios ingenieros de datos, analistas y modelos de inteligencia artificial pueden consultar o procesar la misma base de datos cruda sin transferirse archivos localmente.

## Integración del Almacenamiento con Pipelines
* El Cloud Storage es el núcleo de los Data Lakes (Lagos de Datos) modernos. Funciona como el puente entre diferentes sistemas.
* **Fases dentro del pipeline:**
  * **Ingesta:** Los datos desde una API externa o base de datos de origen se extraen y se depositan como archivos crudos en el bucket.
  * **Transformación:** Nuestro script de limpieza se conecta al bucket, descarga el CSV a memoria, realiza las operaciones en Pandas y sube el archivo resultante (como Parquet) a una nueva ruta procesada.
  * **Consumo:** Herramientas externas pueden leer directamente esos resultados intermedios o finales listos para análisis.

## Interacción con la Nube (Demo Conceptual)
* Para automatizar la interacción desde Python, utilizamos las librerías oficiales de los proveedores (conocidas como SDKs), como `boto3` para AWS o `google-cloud-storage` para GCP.
* **Operaciones centrales a ejecutar:**
  * **Listado de archivos:** Explorar el bucket para identificar qué nuevos archivos de datos han llegado y necesitan ser procesados.
  * **Descarga de archivos:** `Bucket en nube >> Memoria RAM del script`. Extraer el objeto para su transformación.
  * **Subida de archivos:** `Script local >> Bucket en nube`. Enviar el nuevo dataset transformado de vuelta a un almacenamiento seguro y duradero para concluir el pipeline.

---

## Cloud storage (demo)

> **Bloque de demostración** — el instructor ejecuta en vivo.
> No hay script para correr en este bloque.

---

## Errores comunes en el Bloque 4.7.3

- **No configurar permisos IAM correctamente**
  → acceso denegado en producción

- **Subir datos sensibles sin cifrado**
  → riesgo de exposición

- **No establecer una política de retención**
  → costos de almacenamiento crecientes

---

## Resumen: Bloque 4.7.3

**Lo que aprendiste:**
- Entender los conceptos de Object Storage (S3, GCS, Azure Blob)
- Ver cómo se estructura un bucket y cómo se nombran los objetos
- Comparar el costo y latencia de cloud storage vs almacenamiento local

**Lo que construiste:**
Comprendiste los conceptos de cloud storage (demo) a través de la demostración.

**Siguiente paso →** Bloque 4.7.4: Integración con pipeline

---

<!-- ============================================================ -->
<!-- BLOQUE 4.7.4 — Integración con pipeline                     -->
<!-- Scripts: scripts/cap4/4_7_4_Script.py                    -->
<!-- Notebook: notebooks/cap4/4_7_4_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 4.7.4
## Integración con pipeline

> Conectamos el storage con el pipeline: los datos fluyen de la extracción al almacenamiento.

**Al terminar este bloque podrás:**
- Modificar el pipeline para guardar en la estructura de carpetas del data lake
- Leer desde el data lake en el siguiente paso del pipeline
- Verificar la integridad de los archivos guardados con checksums

---

## Integración de Almacenamiento en el Pipeline

* El almacenamiento de datos no es una tarea aislada, sino el componente que vertebra todas las fases de un pipeline.
* Consiste en diseñar estratégicamente dónde y cómo interactúan nuestros scripts de Python con el disco duro local o los buckets en la nube.
* En un flujo real, los datos pasan de ser variables temporales en la memoria RAM (como un DataFrame de Pandas) a convertirse en activos persistentes.
* Un pipeline bien diseñado conoce de manera programática la ruta exacta de donde debe extraer los datos crudos y dónde debe depositar los datos limpios o agregados, permitiendo una ejecución continua y sin intervención humana.

---

## Manejo y Escritura de Resultados Intermedios

* Durante transformaciones complejas, los procesos pueden fallar debido a límites de memoria, desconexiones o errores de lógica.
* Guardar **resultados intermedios** (staging data) es una práctica fundamental que permite:
  * **Recuperación:** Retomar el procesamiento desde el último punto de control sin tener que volver a extraer o limpiar los datos desde cero.
  * **Auditoría:** Rastrear cómo se veía el dato exactamente antes de una agregación o unión compleja.
  * **Reutilización:** Otros equipos (por ejemplo, Ciencia de Datos) pueden necesitar acceder a los datos limpios antes de que sean agrupados para métricas de negocio.
* Patrón arquitectónico común: `Ingesta` >> `Capa Raw` >> `Limpieza` >> `Capa Intermedia` >> `Transformación Final` >> `Capa Final`.

---

## Persistencia y Lectura de Resultados Finales

* El resultado final es el "producto de datos" definitivo, aquel que aportará valor directo al negocio a través de analistas, dashboards o sistemas de toma de decisiones.
* **Persistencia:** Implica escribir el conjunto de datos final en una ubicación definitiva y segura, utilizando convenciones de nomenclatura claras.
* **Lectura:** Los sistemas aguas abajo (downstream) dependerán de esta estructura. Deben poder leer los datos de manera predecible y estandarizada.
* Una vez persistidos, los datos de una ejecución deben tratarse como inmutables. Si se detecta un error, la mejor práctica no es editar el archivo manualmente, sino corregir el código y reprocesar el pipeline para generar un archivo nuevo.

---

## Uso de Múltiples Formatos en el Pipeline

* No existe un único formato de archivo perfecto; un pipeline maduro aprovecha las fortalezas de distintos formatos según la etapa del procesamiento:
  * **Fase de Ingesta (Raw):** Se suelen mantener los formatos de origen, frecuentemente legibles por humanos o estándar de intercambio web, como CSV o JSON.
  * **Fase Intermedia (Staged):** Se adoptan formatos eficientes y tipados, como Parquet. Esto acelera drásticamente los pasos de lectura posteriores en Python y preserva los tipos de datos (evitando que una fecha se lea de nuevo como texto).
  * **Fase Final (Output):** Se consolida en Parquet para análisis masivos en herramientas de Big Data, o se inserta directamente en una base de datos SQL para consumo transaccional.

---

## Validación de Datos Almacenados

* El simple hecho de que un script ejecute una instrucción de guardado sin arrojar errores no garantiza la integridad de los datos.
* Es imperativo implementar **Sanity Checks** (pruebas de cordura) tras la escritura de archivos:
  * **Tamaño del archivo:** Un archivo generado con un tamaño de 0 bytes o significativamente menor al histórico habitual es una alerta roja.
  * **Conteo de registros:** Comparar la longitud del DataFrame en memoria contra los registros efectivamente persistidos o insertados en la base de datos.
  * **Prueba de re-lectura:** Cargar una pequeña muestra del archivo recién guardado para confirmar que no hubo pérdida de formato, desajustes de delimitadores o problemas de codificación (ej. caracteres UTF-8 corruptos).

---

## Introducción al Particionamiento de Datos (Conceptual)

* A medida que el volumen de información crece, leer y procesar un único archivo gigante se vuelve técnica y económicamente ineficiente.
* El **particionamiento** consiste en dividir lógicamente los datos físicos en múltiples directorios estructurados, basándose en el valor de una o más columnas clave (generalmente fechas o categorías geográficas).
* Estructura típica particionada:
  * `/datos/procesados/year=2026/month=04/day=28/transacciones.parquet`
* **Beneficio analítico:** Si una consulta requiere analizar únicamente las ventas del día de hoy, el motor de consulta descartará de inmediato los años y meses anteriores, reduciendo el tiempo y el costo computacional.

---

## Flujo Completo con Almacenamiento

* La integración total de los conceptos de almacenamiento resulta en el siguiente flujo end-to-end:
  1. **Extracción:** Se consumen datos desde una API hacia la memoria del entorno Python.
  2. **Landing (Raw):** Se descarga el payload tal cual en un directorio de crudos (ej. `raw_data_20260428.json`).
  3. **Procesamiento:** Se lee el archivo raw, se aplican conversiones de tipos y manejo de valores nulos.
  4. **Staging:** Se guarda el resultado en un directorio intermedio (ej. `cleaned_data_20260428.parquet`).
  5. **Agregación:** Se carga el archivo intermedio, se aplican agrupaciones (Group By) para calcular KPIs.
  6. **Producción:** Se persisten las métricas finales en una base de datos MySQL y en un almacenamiento estructurado (`final_metrics_20260428.parquet`) para consumo dual.

---

## Preparación para Automatización y Consumo por APIs

* Un almacenamiento estructurado de forma predecible es el requisito previo fundamental para escalar el proyecto a niveles productivos.
* **De cara a la automatización:** Los scripts deben dejar de usar nombres de archivo estáticos (ej. `datos.csv`). Se implementan rutas dinámicas basadas en la fecha de ejecución del sistema. Esto permite que herramientas como Cron o Airflow ejecuten el flujo diariamente, generando un archivo nuevo cada día sin sobrescribir el historial.
* **De cara al consumo (APIs):** Una vez que la estructura de salida es estable, podemos construir una API con FastAPI que sepa exactamente a qué tabla de base de datos o a qué ruta de partición consultar para proveer los datos más actualizados a un dashboard interactivo.

---

<!-- _class: code -->
## Practica: Integrar el data lake local en el pipeline ETL

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar integración con pipeline con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap4/4_7_4_Script.py
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Configurar semilla para reproducibilidad según lineamientos
np.random.seed(987654)

# 1. Configurar estructura de directorios para el almacenamiento
def configurar_directorios():
    """
    Crear la estructura de carpetas para datos crudos, intermedios y finales.
    Garantizar una organizacion estructurada de los archivos del pipeline.
    """
    directorios = [
        "data/raw",
        "data/intermediate",
        "data/final"

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap4/4_7_4_Script.ipynb)

---

## Errores comunes en el Bloque 4.7.4

- **No validar que el archivo se escribió correctamente antes de avanzar al siguiente paso**

- **Leer el archivo con pandas sin especificar el schema**
  → tipos incorrectos

- **Mezclar datos crudos y procesados en la misma carpeta**
  → confusión en el equipo

---

## Resumen: Bloque 4.7.4

**Lo que aprendiste:**
- Modificar el pipeline para guardar en la estructura de carpetas del data lake
- Leer desde el data lake en el siguiente paso del pipeline
- Verificar la integridad de los archivos guardados con checksums

**Lo que construiste:**
El script `4_7_4_Script.py` que integrar el data lake local en el pipeline etl usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 4.8.1: Introducción a Docker

---

<!-- _class: section -->
# Sección 8: Docker y entorno reproducible
## En esta sección construiremos la capa de docker y entorno reproducible del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de docker y entorno reproducible en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 4.8.1: Introducción a Docker
- Bloque 4.8.2: Creación de Dockerfile
- Bloque 4.8.3: requirements.txt y dependencias
- Bloque 4.8.4: docker-compose y servicios

---

<!-- ============================================================ -->
<!-- BLOQUE 4.8.1 — Introducción a Docker                        -->
<!-- Scripts: scripts/cap4/4_8_1_Script.py                    -->
<!-- Notebook: notebooks/cap4/4_8_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 4.8.1
## Introducción a Docker

> Nuestro pipeline funciona en nuestra máquina; Docker lo hace reproducible en cualquier entorno.

**Al terminar este bloque podrás:**
- Entender qué es un contenedor Docker y por qué resuelve el problema 'en mi máquina funciona'
- Instalar Docker y verificar la instalación con docker run hello-world
- Distinguir imagen, contenedor, registry y volumen

---

# Capítulo 4: Manejo de datos y despliegue local, Sesión 8: Docker y entorno reproducible, Bloque 1: Introducción a Docker

## El problema de los entornos no reproducibles

En el desarrollo de software y la ingeniería de datos, es muy común construir un script o un pipeline que funciona perfectamente en nuestra computadora, pero que falla estrepitosamente al enviarlo a producción o al compartirlo con un colega. 

A este fenómeno se le conoce universalmente como el problema de "En mi máquina funciona" (Works on my machine).

Las causas principales de este problema incluyen:
* Diferentes versiones del sistema operativo (Windows vs. Linux vs. macOS).
* Diferentes versiones de Python (ej. Python 3.9 vs Python 3.11).
* Dependencias y librerías faltantes o en versiones incompatibles.
* Variables de entorno y configuraciones de red distintas.

---

## Introducción a Docker

Para resolver el problema de los entornos inconsistentes, surge Docker. Docker es una plataforma de software que permite empaquetar, distribuir y ejecutar aplicaciones dentro de entornos aislados. 

En lugar de instalar Python, las librerías y configurar el sistema operativo paso a paso en cada servidor nuevo, Docker nos permite crear un paquete estándar que contiene todo lo necesario para que nuestro código se ejecute.

Si funciona en el entorno de desarrollo local dentro de Docker, funcionará exactamente igual en el servidor de producción, en la nube o en la computadora de otro desarrollador.

---

## Concepto de Imagen en Docker

Una **Imagen** de Docker es una plantilla de solo lectura que contiene las instrucciones para crear un entorno ejecutable. 

Podemos pensar en una imagen como la receta de un pastel o el plano arquitectónico de un edificio. Contiene de manera estática:
* Una versión específica del sistema operativo (por ejemplo, Ubuntu o Alpine Linux).
* El lenguaje de programación (ej. Python 3.10).
* El código fuente de nuestro pipeline de datos.
* Todas las dependencias (Pandas, FastAPI, SQLAlchemy, etc.).

Las imágenes se construyen una vez y se pueden compartir a través de registros (como Docker Hub).

---

## Concepto de Contenedor

Mientras que la imagen es la receta, un **Contenedor** es el pastel ya horneado. Es una instancia viva y en ejecución de una imagen.

Características de un contenedor:
* **Aislado:** Se ejecuta de forma independiente de otros contenedores y del sistema operativo anfitrión (host).
* **Efímero:** Está diseñado para ser creado, ejecutado y destruido sin afectar al sistema base.
* **Interactivo:** Puede recibir peticiones, conectarse a bases de datos y procesar información, tal como lo haría un servidor tradicional.

En nuestro contexto, un contenedor será el entorno exacto donde se ejecutará nuestro script de extracción y transformación de datos.

---

## Diferencia entre Máquina Virtual (VM) y Contenedor

Es fundamental no confundir Docker con las Máquinas Virtuales tradicionales.

**Máquina Virtual (VM):**
* Virtualiza el hardware (CPU, memoria, disco).
* Incluye un sistema operativo invitado (Guest OS) completo, lo que la hace pesada (pesa Gigabytes).
* Tarda minutos en arrancar.

**Contenedor (Docker):**
* Virtualiza únicamente el sistema operativo.
* Comparte el núcleo (Kernel) del sistema operativo anfitrión.
* Es sumamente ligero (pesa Megabytes) y arranca en fracciones de segundo.

---

## Uso de Docker en Ingeniería de Datos

En la ingeniería de datos moderna, Docker no es una opción, es un estándar de la industria. Sus aplicaciones directas incluyen:

* **Aislamiento de pipelines:** Ejecutar procesos ETL heredados en Python 2.7 y nuevos procesos en Python 3.10 en el mismo servidor sin conflictos.
* **Bases de datos locales:** Levantar un servidor MySQL, PostgreSQL o MongoDB en segundos para pruebas locales sin instalar el motor en nuestra máquina.
* **Orquestación:** Herramientas como Apache Airflow utilizan contenedores para ejecutar tareas aisladas y escalables.
* **Despliegue de APIs:** Exponer nuestros datos limpios mediante una API (FastAPI) empaquetada, lista para subirse a la nube.

---

## Instalación y Ejecución Básica

Para utilizar Docker en entornos de desarrollo, habitualmente instalamos **Docker Desktop** (disponible para Windows, Mac y Linux). 

Una vez instalado, interactuamos con Docker a través de la terminal o línea de comandos. El comando más clásico para verificar la instalación es:

`docker run hello-world`

Lo que sucede internamente con este comando es:
1. Docker busca la imagen "hello-world" localmente.
2. Si no la encuentra, la descarga (pull) desde Docker Hub.
3. Crea un contenedor a partir de esa imagen.
4. Ejecuta el contenedor, el cual imprime un mensaje de éxito en la consola y luego se detiene.

---

## Ciclo de vida de los contenedores

Los contenedores tienen un ciclo de vida bien definido, que controlamos mediante comandos específicos de Docker:

* **Creación y Ejecución (Running):** `docker run [nombre_imagen]` crea e inicia un contenedor.
* **Pausa (Paused):** El proceso se congela en memoria, sin consumir CPU.
* **Detención (Stopped):** `docker stop [id_contenedor]` detiene la ejecución del contenedor de forma segura, pero sus datos y estado persisten en el disco.
* **Reinicio:** Un contenedor detenido puede volver a iniciarse con `docker start [id_contenedor]`.
* **Eliminación (Deleted):** `docker rm [id_contenedor]` destruye permanentemente el contenedor. (Nota: esto no elimina la imagen base).

---

## Beneficios clave: Portabilidad y Consistencia

Adoptar Docker en nuestros proyectos de datos nos otorga dos superpoderes:

**Portabilidad:** El principio de "Construye una vez, ejecuta en cualquier lugar". Una imagen de Docker puede ejecutarse en el laptop de un desarrollador, en un servidor on-premise de la empresa o en servicios gestionados de la nube (AWS, Google Cloud, Azure) sin requerir modificaciones en el código.

**Consistencia:** Garantiza que los entornos de Desarrollo, Pruebas (Testing) y Producción sean clones exactos. Esto elimina por completo las sorpresas de último minuto durante los despliegues causadas por diferencias de configuración.

---

## Docker en pipelines reales (Caso del curso)

En nuestro proyecto, pasaremos de tener scripts dispersos a un sistema estructurado utilizando contenedores. El flujo de trabajo con Docker se verá así:

1. **Base de Datos:** Levantaremos un contenedor preconfigurado con MySQL.
2. **Transformación:** Nuestro pipeline de ingesta y limpieza (Pandas) se ejecutará dentro de un contenedor, escribiendo datos en el contenedor de MySQL.
3. **Consumo:** Empaquetaremos nuestra aplicación FastAPI en una imagen Docker, la cual se conectará a la base de datos para exponer la información.

Con esto, dejaremos de depender de las instalaciones locales de nuestra máquina y nuestro pipeline será 100% reproducible por cualquier persona con un solo comando.

---

<!-- _class: code -->
## Practica: Ejecutar el primer contenedor Docker

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar introducción a docker con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap4/4_8_1_Script.py
"""
Capítulo 4: Manejo de datos y despliegue local
Sección 8: Docker y entorno reproducible
Bloque 1: Introducción a Docker

Descripción:
Este script sirve como base teórica y práctica para introducir los conceptos
de Docker en el contexto de la ingeniería de datos. El código a continuación
representa un mini-pipeline que ejemplifica el problema "en mi máquina funciona",
preparando el terreno para su posterior contenedorización.

Subtemas abordados en la documentación del script:
ST1: Problema de entornos no reproducibles.
ST2: "Works on my machine" problem.
ST3: Introducción a Docker.
ST4: Concepto de imagen.
ST5: Concepto de contenedor.
ST6: Diferencia entre VM y contenedor.

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap4/4_8_1_Script.py`

---

## Errores comunes en el Bloque 4.8.1

- **Confundir imagen (plantilla) con contenedor (instancia en ejecución)**

- **No añadir el usuario actual al grupo docker**
  → necesitar sudo en cada comando

- **Detener un contenedor con Ctrl+C sin limpiarlo**
  → contenedores zombie acumulados

---

## Resumen: Bloque 4.8.1

**Lo que aprendiste:**
- Entender qué es un contenedor Docker y por qué resuelve el problema 'en mi máquina funciona'
- Instalar Docker y verificar la instalación con docker run hello-world
- Distinguir imagen, contenedor, registry y volumen

**Lo que construiste:**
El script `4_8_1_Script.py` que ejecutar el primer contenedor docker usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 4.8.2: Creación de Dockerfile

---

<!-- ============================================================ -->
<!-- BLOQUE 4.8.2 — Creación de Dockerfile                       -->
<!-- Scripts: scripts/cap4/4_8_2_Script.py                    -->
<!-- Notebook: notebooks/cap4/4_8_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 4.8.2
## Creación de Dockerfile

> Con Docker instalado, empaquetamos nuestro script de pipeline en una imagen propia.

**Al terminar este bloque podrás:**
- Escribir un Dockerfile válido para una aplicación Python
- Construir una imagen con docker build y etiquetarla correctamente
- Ejecutar el contenedor y verificar que el script del pipeline corre correctamente

---

# Capítulo 4: Manejo de datos y despliegue local, Sesión 8: Docker y entorno reproducible, Bloque 2: Creación de Dockerfile

## ¿Qué es un Dockerfile?

Un Dockerfile es un documento de texto sin formato que contiene todas las instrucciones y comandos necesarios para ensamblar una imagen de Docker. En el contexto de la ingeniería de datos, es la "receta" exacta que garantiza que nuestro pipeline o nuestra API tengan exactamente el mismo entorno, independientemente de la máquina donde se ejecuten.

Al construir una imagen a partir de un Dockerfile, Docker lee las instrucciones de arriba hacia abajo y ejecuta cada paso secuencialmente. El resultado final es una plantilla empaquetada (imagen) lista para ser instanciada como un contenedor.

---

## Instrucciones básicas de un Dockerfile

Para construir cualquier entorno en Docker, utilizamos una serie de palabras clave reservadas. Las cuatro más fundamentales son:

*   **FROM**: Define la imagen base desde la cual comenzaremos a construir. Todo Dockerfile debe comenzar con esta instrucción (por ejemplo, una instalación limpia de Python).
*   **COPY**: Permite transferir archivos o directorios desde nuestra máquina local (el host) hacia el sistema de archivos del contenedor.
*   **RUN**: Ejecuta comandos en la terminal del contenedor durante el proceso de construcción de la imagen. Es ideal para instalar dependencias de sistema operativo o paquetes de Python.
*   **CMD**: Especifica el comando por defecto que se ejecutará cuando un contenedor se inicie a partir de la imagen construida. A diferencia de RUN, no se ejecuta durante la construcción.

---

## El sistema de capas en Docker

Cada instrucción en un Dockerfile (como RUN, COPY o ADD) crea una nueva "capa" (layer) de solo lectura en la imagen resultante. Docker utiliza un sistema de almacenamiento en caché para estas capas.

Si modificamos una línea en nuestro Dockerfile, Docker solo reconstruirá esa capa y todas las capas subsecuentes. Las capas anteriores se reutilizarán desde la caché, lo que acelera enormemente los tiempos de construcción. 

Este comportamiento hace que la estructura de nuestro archivo no solo sea una cuestión de orden lógico, sino también de rendimiento.

---

## Orden de instrucciones

Debido al sistema de caché por capas, el orden en el que escribimos las instrucciones es crítico. La regla de oro es colocar los elementos que cambian con menor frecuencia en la parte superior del archivo y los que cambian con mayor frecuencia en la parte inferior.

1.  **Imágenes base y dependencias del sistema**: Rara vez cambian.
2.  **Instalación de librerías (requirements.txt)**: Cambian ocasionalmente.
3.  **Código fuente del pipeline o API**: Cambia constantemente con cada nuevo desarrollo.

Si colocamos el código fuente antes de instalar las dependencias, cualquier cambio en el código invalidará la caché de la instalación, forzando a descargar todas las librerías nuevamente en cada construcción.

---

## Optimización básica de imágenes

En ingeniería de datos, queremos imágenes ligeras para que los despliegues sean rápidos y consuman menos almacenamiento. Algunas estrategias de optimización incluyen:

*   **Uso de imágenes base ligeras**: En lugar de usar la imagen estándar de Python (que puede pesar cerca de 1 GB), se prefiere usar versiones reducidas como `python:3.9-slim` o Alpine, las cuales solo contienen lo mínimo necesario.
*   **Agrupación de comandos RUN**: Encadenar comandos con `&&` y limpiar la caché de los gestores de paquetes en la misma instrucción (por ejemplo, `apt-get clean`) evita que se generen capas intermedias con archivos temporales innecesarios.
*   **Instalar solo lo necesario**: Evitar librerías de desarrollo en la imagen final de producción.

---

## Configuración del entorno e Inclusión del código

Para empaquetar nuestro pipeline, debemos preparar el entorno de trabajo dentro del contenedor utilizando la instrucción **WORKDIR**. Esto define el directorio activo para cualquier instrucción RUN, CMD, o COPY que siga.

Una vez configurado el directorio, procedemos a incluir nuestro código. El flujo recomendado es:

1. Establecer el directorio de trabajo (`WORKDIR /app`).
2. Copiar el archivo de dependencias (`COPY requirements.txt .`).
3. Ejecutar la instalación (`RUN pip install -r requirements.txt`).
4. Copiar los scripts del pipeline (`COPY . .`).

Adicionalmente, se puede usar la instrucción **ENV** para definir variables de entorno necesarias para la ejecución (como rutas por defecto o configuraciones de zona horaria).

---

## Construcción de la imagen

Una vez que el Dockerfile está redactado, el siguiente paso es compilarlo para generar la imagen. Esto se realiza desde la terminal con el comando `docker build`.

La sintaxis básica es:
`docker build -t nombre_de_la_imagen:etiqueta .`

*   `-t`: Permite asignar un nombre y opcionalmente una etiqueta (tag) a la imagen, como `pipeline_ventas:v1`.
*   `.` (punto): Indica el "build context", es decir, el directorio actual donde Docker buscará el Dockerfile y los archivos a copiar. Todo el contenido de este directorio se envía al motor de Docker.

---

## Ejecución del contenedor

Con la imagen construida, podemos instanciarla y poner a correr nuestro pipeline utilizando el comando `docker run`.

Para ejecutar un script que hace un procesamiento batch y termina:
`docker run nombre_de_la_imagen:etiqueta`

Para ejecutar una API (como FastAPI) que necesita exponer un puerto hacia nuestra máquina local, utilizamos el flag de publicación de puertos:
`docker run -p 8000:8000 nombre_de_la_imagen:etiqueta`

Si el pipeline necesita leer o escribir archivos en nuestra máquina local en lugar del sistema aislado del contenedor, podemos montar volúmenes usando el flag `-v ruta_local:ruta_contenedor`.

---

## Debugging básico

Es común que la construcción de la imagen o la ejecución del contenedor fallen en los primeros intentos. Existen formas de diagnosticar el problema:

*   **Durante el build**: Si un paso `RUN` falla, Docker mostrará la salida del error en la terminal. Se debe revisar la instrucción exacta que causó la falla.
*   **Si el contenedor falla al iniciar**: Utilizar `docker logs id_del_contenedor` para ver qué imprimió la aplicación antes de detenerse.
*   **Exploración interactiva**: Si necesitamos inspeccionar los archivos dentro de la imagen para ver si se copiaron correctamente, podemos abrir una terminal interactiva sobre la imagen omitiendo el CMD por defecto:
    `docker run -it nombre_de_la_imagen:etiqueta /bin/bash`

---

## Buenas prácticas en Dockerfile

Para consolidar la creación de contenedores robustos en ingeniería de datos, se deben adoptar las siguientes buenas prácticas:

*   **Usar archivo .dockerignore**: Funciona igual que .gitignore. Previene que archivos innecesarios (como entornos virtuales, datos locales pesados o archivos de caché) se envíen al contexto de construcción, ahorrando tiempo y espacio.
*   **Fijar versiones**: Nunca utilizar la etiqueta `latest` para imágenes base en producción. Definir una versión específica (ej. `python:3.9.7-slim`) garantiza que las actualizaciones futuras de la imagen base no rompan el pipeline inesperadamente.
*   **Un proceso por contenedor**: Un contenedor debe tener un solo propósito. Si el proyecto requiere una API y una Base de Datos, deben ser dos contenedores distintos que se comuniquen entre sí, no ambos instalados en el mismo Dockerfile.

---

<!-- _class: code -->
## Practica: Construir una imagen Docker para el pipeline

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar creación de dockerfile con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap4/4_8_2_Script.py
import os

def generar_script_pipeline():
    """
    Generar un script de pipeline básico en Python.
    Este script será el que empaquetaremos dentro del contenedor Docker.
    (Cubre ST7: Inclusión del código del pipeline).
    """
    contenido_pipeline = """# -*- coding: utf-8 -*-
import pandas as pd
import os

def ejecutar_pipeline():
    print("Iniciando ejecución del pipeline dentro del contenedor...")
    
    # Crear datos simulados para el ejemplo
    datos = {
        'id_transaccion': [1, 2, 3],

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap4/4_8_2_Script.py`

---

## Errores comunes en el Bloque 4.8.2

- **Olvidar COPY el archivo requirements.txt antes de RUN pip install**
  → cache invalidado en cada build

- **No especificar WORKDIR**
  → los archivos se crean en / y el contenedor queda desordenado

- **Usar una imagen base demasiado grande (python:3.11) en lugar de python:3.11-slim**
  → builds lentos

---

## Resumen: Bloque 4.8.2

**Lo que aprendiste:**
- Escribir un Dockerfile válido para una aplicación Python
- Construir una imagen con docker build y etiquetarla correctamente
- Ejecutar el contenedor y verificar que el script del pipeline corre correctamente

**Lo que construiste:**
El script `4_8_2_Script.py` que construir una imagen docker para el pipeline usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 4.8.3: requirements.txt y dependencias

---

<!-- ============================================================ -->
<!-- BLOQUE 4.8.3 — requirements.txt y dependencias              -->
<!-- Scripts: scripts/cap4/4_8_3_Script.py                    -->
<!-- Notebook: notebooks/cap4/4_8_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 4.8.3
## requirements.txt y dependencias

> Una buena imagen Docker gestiona sus dependencias de forma explícita y reproducible.

**Al terminar este bloque podrás:**
- Crear un requirements.txt completo y con versiones pinneadas
- Usar pip freeze vs pip list para generar el archivo de dependencias
- Entender el impacto de las versiones en la reproducibilidad del entorno

---

## Gestión de dependencias en Python

En el desarrollo de pipelines de datos, rara vez escribimos todo el código desde cero. Utilizamos paquetes creados por terceros para facilitar tareas complejas.

* **¿Qué es una dependencia?** Es cualquier librería o paquete de código externo que nuestro proyecto necesita para funcionar correctamente.
* **El ecosistema Python:** Python incluye una "librería estándar" (herramientas nativas), pero para ingeniería de datos dependemos fuertemente de paquetes externos como Pandas, SQLAlchemy o FastAPI.
* **El problema de la gestión:** Si enviamos nuestro script a otro servidor sin indicar qué librerías necesita, el script fallará al intentar importar módulos inexistentes. Gestionar dependencias es llevar un registro exacto de lo que nuestro código requiere.

---

## Uso de requirements.txt

En la comunidad de Python, existe un estándar de facto para declarar las dependencias de un proyecto: un archivo de texto simple llamado `requirements.txt`.

* **Propósito:** Actúa como un "manifiesto" o lista de compras para el entorno de Python.
* **Estructura:** Es un archivo de texto plano donde cada línea representa un paquete que debe ser instalado.
* **Legibilidad:** Al ser texto plano, es fácil de leer por humanos, fácil de rastrear en sistemas de control de versiones (como Git) y fácil de interpretar por gestores de paquetes como `pip`.

---

## Generación de dependencias (pip freeze)

No es necesario escribir el archivo `requirements.txt` a mano cada vez que instalamos una nueva librería. Python nos provee herramientas para automatizar esto.

* **El comando pip freeze:** Este comando escanea el entorno actual de Python e imprime una lista de todas las librerías instaladas junto con sus versiones exactas.
* **Generación del archivo:** Utilizando la redirección de consola, podemos volcar esta salida directamente al archivo.

```bash
pip freeze > requirements.txt
```

* **Nota importante:** Es fundamental hacer esto dentro de un entorno virtual limpio para evitar incluir librerías globales del sistema que nuestro proyecto realmente no utiliza.

---

## Fijación de versiones

Un archivo `requirements.txt` no solo lista los nombres de las librerías, sino que también establece las versiones a utilizar. A esto se le conoce como "pinning" o fijación.

* **Sintaxis de fijación:**
  * `pandas==2.0.3` (Instala exactamente esta versión, es la práctica más segura para despliegues).
  * `pandas>=1.5.0` (Instala cualquier versión igual o superior, útil para desarrollo pero riesgoso en producción).
* **¿Por qué fijar versiones?** Las librerías de software se actualizan constantemente. Una actualización mayor puede eliminar una función que tu pipeline de datos estaba utilizando, rompiendo el proceso. Fijar la versión garantiza estabilidad.

---

## Problemas de compatibilidad

A medida que los pipelines crecen y requieren más librerías, es común enfrentarse a conflictos de dependencias, un fenómeno conocido coloquialmente como "Dependency Hell".

* **Dependencias transitivas:** Cuando instalas el Paquete A, este a su vez puede instalar el Paquete B. Tu proyecto hereda todas esas dependencias subyacentes.
* **El conflicto:** Puede ocurrir que la librería X requiera la versión 1.0 de una herramienta, mientras que la librería Y requiera la versión 2.0 de esa misma herramienta. 
* **Prevención:** Mantener un archivo `requirements.txt` lo más específico y limpio posible, e integrar herramientas de manejo de entornos virtuales o contenedores, ayuda a aislar el proyecto y evitar choques con otras aplicaciones.

---

## Integración con Dockerfile

Una vez que tenemos nuestro `requirements.txt`, el siguiente paso es decirle a Docker que instale estas herramientas dentro de nuestro contenedor.

El proceso en un `Dockerfile` debe ser ordenado y lógico:

```dockerfile
# 1. Definir la imagen base
FROM python:3.9-slim

# 2. Establecer el directorio de trabajo
WORKDIR /app

# 3. Copiar el archivo de dependencias al contenedor
COPY requirements.txt /app/

# 4. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt
```

Al copiar primero solo el archivo de requerimientos, le permitimos a Docker optimizar el proceso de construcción de la imagen.

---

## Instalación de dependencias en contenedor

El comando `RUN pip install -r requirements.txt` es el corazón de la preparación de nuestro entorno dentro de Docker.

* **Caché de capas en Docker:** Docker construye imágenes por capas. Si tu `requirements.txt` no ha cambiado, Docker reutilizará la capa donde ya se instalaron las librerías, ahorrando mucho tiempo en compilaciones futuras.
* **Uso de --no-cache-dir:** En el ejemplo anterior usamos esta bandera de `pip`. Esto evita que Python guarde los archivos temporales de descarga de los paquetes. En un contenedor, esto es ideal porque reduce el tamaño final de la imagen, haciéndola más ligera y rápida de mover.

---

## Reproducibilidad del entorno

La combinación de Docker y un archivo `requirements.txt` bien definido nos otorga el "Santo Grial" de la ingeniería de software y datos: la reproducibilidad total.

* **Mismo sistema operativo:** Docker garantiza que el sistema subyacente (ej. Ubuntu, Alpine) sea el mismo en tu computadora y en el servidor de producción.
* **Mismas librerías:** El `requirements.txt` con versiones fijadas garantiza que el motor de procesamiento de datos sea matemáticamente idéntico en cualquier lugar.
* **Resultado:** Si tu script para limpiar datos nulos funciona en tu computadora local, funcionará exactamente igual en la nube. Adiós al "en mi máquina sí funciona".

---

## Manejo de librerías externas vs internas

Es importante distinguir qué va en el `requirements.txt` y qué no.

* **Librerías estándar (Internas):** Paquetes como `os`, `sys`, `csv`, `json`, `datetime` o `math` vienen incluidos con la instalación base de Python. NO deben agregarse al `requirements.txt`.
* **Librerías externas:** Paquetes que tuviste que instalar con `pip install ...` como `pandas`, `sqlalchemy`, `fastapi`, `uvicorn`, o `requests`. Estos son obligatorios en tu `requirements.txt`.
* **Regla de oro:** Si el código usa un `import` de algo que no construiste tú y no viene preinstalado en Python, debe estar documentado como dependencia.

---

## Buenas prácticas de dependencias

Para mantener un pipeline de datos sano a largo plazo, adopta estas prácticas:

1. **Aislamiento local:** Nunca uses el entorno global de tu sistema operativo para desarrollar. Usa siempre entornos virtuales (`venv`, `conda`) por cada proyecto.
2. **Dependencias mínimas:** No instales paquetes "por si acaso". Cada librería añade peso a la imagen de Docker, tiempo de descarga y posibles vulnerabilidades de seguridad.
3. **Revisión periódica:** Actualiza las librerías de forma controlada. Revisa los registros de cambios (changelogs) antes de subir la versión en tu `requirements.txt`.
4. **Limpieza antes del freeze:** Asegúrate de desinstalar paquetes que probaste pero que finalmente no usaste en tu código antes de ejecutar `pip freeze`.

---

## Preparación para despliegue

Con las dependencias controladas e integradas en un Dockerfile, hemos superado una de las barreras más grandes para llevar un proyecto a producción.

* El pipeline de datos ahora es un **artefacto autocontenido**.
* Tiene el código (scripts de transformación).
* Tiene el motor (versión exacta de Python).
* Tiene sus herramientas (librerías fijadas).

Este encapsulamiento nos deja listos para el siguiente nivel de la ingeniería de datos: orquestar este contenedor junto con bases de datos y APIs utilizando herramientas como Docker Compose.

---

<!-- _class: code -->
## Practica: Crear y optimizar el requirements.txt del pipeline

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar requirements.txt y dependencias con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap4/4_8_3_Script.py
"""
Capítulo 4: Manejo de datos y despliegue local
Sección 8: Docker y entorno reproducible
Bloque 3: requirements.txt y dependencias

Este script demuestra cómo gestionar las dependencias de un proyecto en Python,
la generación de un archivo requirements.txt, la fijación de versiones y la
validación de librerías externas, conceptos clave para preparar el entorno
para un contenedor Docker.
"""

import os
import subprocess
import sys
import random

# Establecer semilla aleatoria por convención del curso
random.seed(987654)

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap4/4_8_3_Script.py`

---

## Errores comunes en el Bloque 4.8.3

- **No pinnear versiones en requirements.txt**
  → builds no reproducibles

- **Incluir dependencias de desarrollo en requirements.txt de producción**
  → imagen innecesariamente grande

- **Olvidar una dependencia transitiva**
  → ImportError en el contenedor aunque funciona localmente

---

## Resumen: Bloque 4.8.3

**Lo que aprendiste:**
- Crear un requirements.txt completo y con versiones pinneadas
- Usar pip freeze vs pip list para generar el archivo de dependencias
- Entender el impacto de las versiones en la reproducibilidad del entorno

**Lo que construiste:**
El script `4_8_3_Script.py` que crear y optimizar el requirements.txt del pipeline usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 4.8.4: docker-compose y servicios

---

<!-- ============================================================ -->
<!-- BLOQUE 4.8.4 — docker-compose y servicios                   -->
<!-- Scripts: scripts/cap4/4_8_4_Script.py                    -->
<!-- Notebook: notebooks/cap4/4_8_4_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 4.8.4
## docker-compose y servicios

> El pipeline necesita varios servicios (app + BD); docker-compose los orquesta juntos.

**Al terminar este bloque podrás:**
- Escribir un docker-compose.yml que levante el pipeline y MySQL juntos
- Usar variables de entorno (.env) para configurar los servicios
- Gestionar la red interna entre contenedores y los volúmenes de datos

---

## Introducción a docker-compose y Múltiples Servicios

En escenarios reales de ingeniería de datos, un sistema rara vez consiste en un solo componente. Por lo general, tenemos una base de datos, una API para consumo y scripts de procesamiento, todos interactuando entre sí.

**¿Qué es docker-compose?**
Es una herramienta de Docker que permite definir y ejecutar aplicaciones compuestas por múltiples contenedores.

**Concepto de múltiples servicios**
En lugar de levantar manualmente cada contenedor, vinculándolos uno por uno mediante comandos extensos, organizamos nuestra arquitectura en "servicios". Cada servicio representa un componente funcional del pipeline (ej. servicio de base de datos, servicio de ingesta, servicio de API), permitiendo que todos se gestionen de manera unificada.

---

## Definición de Servicios y el Archivo compose.yaml

La configuración de nuestra arquitectura multicontenedor se realiza de forma declarativa mediante un archivo en formato YAML, usualmente llamado `compose.yaml` o `docker-compose.yml`.

**Estructura básica de compose.yaml**
El archivo define la versión de la sintaxis y una lista de `services`. Cada servicio detalla qué imagen usar (o cómo construirla desde un Dockerfile) y sus configuraciones específicas.

```yaml
version: '3.8'
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
  api:
    build: ./api
    depends_on:
      - db
```
Con este archivo, definimos la infraestructura local completa en código, haciéndola versionable y reproducible por cualquier miembro del equipo.

---

## Configuración de Puertos y Redes entre Contenedores

Para que los contenedores sean útiles, deben poder comunicarse con el exterior y entre ellos.

**Configuración de Puertos**
La instrucción `ports` mapea un puerto de la máquina host (tu computadora) a un puerto dentro del contenedor. Formato: `HOST:CONTENEDOR`.
Ejemplo: `8000:80` expone el puerto 80 del contenedor en el puerto 8000 de tu máquina.

**Redes Internas (Networking)**
Por defecto, docker-compose crea una red interna virtual para todos los servicios definidos en el archivo.
* **Resolución de nombres:** Dentro de esta red, los contenedores pueden comunicarse usando el nombre del servicio como hostname. 
* Si la API necesita conectarse a la base de datos, la cadena de conexión apuntará a `host=db` en lugar de `localhost` o una IP estática.

---

## Levantamiento de Servicios

Una de las mayores ventajas de docker-compose es la simplicidad operativa. Reemplaza múltiples comandos complejos de Docker con instrucciones sencillas de orquestación local.

**Comandos principales:**
* `docker-compose up`: Construye (si es necesario), crea e inicia todos los contenedores descritos en el archivo. Bloquea la terminal mostrando los logs en tiempo real.
* `docker-compose up -d`: Ejecuta los servicios en modo "detached" (segundo plano), liberando la terminal.
* `docker-compose down`: Detiene y elimina los contenedores, redes y volúmenes creados por el `up`.

Esta simplicidad garantiza que el ambiente de desarrollo sea idéntico para todos: un solo comando levanta toda la infraestructura.

---

## Integración API y Base de Datos (Orquestación Local)

Al orquestar localmente, controlamos cómo y cuándo interactúan los servicios, manejando las dependencias del sistema.

**Manejo de Dependencias**
El parámetro `depends_on` indica el orden de inicio. Si la API requiere consultar información, debe esperar a que el servicio `db` inicie primero.

**Paso de Variables de Entorno**
Para conectar la API con la base de datos de manera segura y dinámica, pasamos las credenciales mediante la instrucción `environment` en el `compose.yaml`.

```yaml
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASS=root
```
Esto separa la configuración del código fuente, una excelente práctica en ingeniería de software y datos.

---

## Debugging de Servicios

Cuando se manejan múltiples contenedores interactuando en red, identificar el origen de un error es crucial. docker-compose incluye herramientas integradas para el monitoreo y solución de problemas.

**Inspección del entorno:**
* `docker-compose ps`: Muestra el estado actual de los servicios (Running, Exited, etc.) y los puertos expuestos.
* `docker-compose logs`: Consolida la salida estándar de todos los servicios.
* `docker-compose logs [nombre_servicio]`: Aísla los logs de un servicio específico (ej. verificar por qué la API retornó un error 500).

Si un servicio falla al iniciar, el primer paso es revisar sus logs para confirmar si se debe a un error de código, una variable de entorno faltante o un problema de conexión de red.

---

## Sistema Completo en Contenedores

La meta de empaquetar todo con docker-compose es lograr un pipeline funcional e integrado, operando como una unidad independiente del entorno local del desarrollador.

**Flujo Integrado**
1. **Almacenamiento:** Un contenedor con MySQL activo y escuchando conexiones.
2. **Procesamiento:** Un script en Python (o contenedor temporal) que extrae, transforma y carga (ETL) los datos en la base de datos.
3. **Consumo:** Un contenedor con FastAPI que lee la base de datos y expone endpoints.

Al consolidar estas tres piezas en un único archivo `compose.yaml`, logramos un sistema de datos encapsulado. Cualquier persona puede clonar el repositorio, ejecutar un comando y tener un pipeline end-to-end funcionando en minutos.

---

<!-- _class: code -->
## Practica: Levantar el pipeline + MySQL con docker-compose

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar docker-compose y servicios con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap4/4_8_4_Script.py
import os
import random

# Definir semilla para procesos aleatorios
random.seed(987654)

def generar_requirements():
    """
    Generar el archivo requirements.txt con las dependencias del proyecto.
    """
    contenido = """pandas==2.1.1
sqlalchemy==2.0.21
pymysql==1.1.0
fastapi==0.103.2
uvicorn==0.23.2
"""
    with open("requirements.txt", "w", encoding="utf-8") as file:
        file.write(contenido)

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap4/4_8_4_Script.py`

---

## Errores comunes en el Bloque 4.8.4

- **No esperar a que MySQL esté listo antes de conectar el pipeline**
  → connection refused

- **Exponer puertos de BD al exterior**
  → riesgo de seguridad

- **No usar volúmenes persistentes para MySQL**
  → pérdida de datos al reiniciar el contenedor

---

## Resumen: Bloque 4.8.4

**Lo que aprendiste:**
- Escribir un docker-compose.yml que levante el pipeline y MySQL juntos
- Usar variables de entorno (.env) para configurar los servicios
- Gestionar la red interna entre contenedores y los volúmenes de datos

**Lo que construiste:**
El script `4_8_4_Script.py` que levantar el pipeline + mysql con docker-compose usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 5.9.1: Scripts automatizados