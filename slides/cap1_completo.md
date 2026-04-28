---
marp: true
theme: bsg
size: 16:9
paginate: true
footer: 'Python para Ingeniería de Datos · Capítulo 1: Fundamentos de Python aplicado a datos · BSG Institute'
---

---

<!-- _class: title -->
# Capítulo 1: Fundamentos de Python aplicado a datos
## Python para procesamiento de datos

---

<!-- _class: section -->
# Sección 1: Python para procesamiento de datos
## En esta sección construiremos la capa de python para procesamiento de datos del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de python para procesamiento de datos en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 1.1.1: Introducción al curso y caso del pipeline
- Bloque 1.1.2: Variables, tipos y estructuras básicas
- Bloque 1.1.3: Lectura de archivos CSV y primeros scripts
- Bloque 1.1.4: Funciones aplicadas a limpieza de datos

---

<!-- ============================================================ -->
<!-- BLOQUE 1.1.1 — Introducción al curso y caso del pipeline    -->
<!-- Scripts: scripts/cap1/1_1_1_Script.py                    -->
<!-- Notebook: notebooks/cap1/1_1_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 1.1.1
## Introducción al curso y caso del pipeline

> Comenzamos desde cero: aquí construiremos el dataset crudo que acompañará todo el curso.

**Al terminar este bloque podrás:**
- Entender qué es un pipeline de datos y por qué lo necesitamos
- Generar un archivo CSV con datos transaccionales reales (con errores incluidos)
- Leer un archivo CSV con Python nativo y explorar su contenido

---

## ¿Qué es Data Engineering?

La **Ingeniería de Datos (Data Engineering)** es la disciplina encargada de diseñar, construir y mantener la infraestructura y los sistemas que permiten recolectar, almacenar y procesar grandes volúmenes de datos.

Mientras otras áreas se enfocan en responder preguntas de negocio, la ingeniería de datos se asegura de que los datos existan de forma confiable, estén limpios y se encuentren accesibles para quien los necesite. 

**En resumen:** Es el trabajo de "plomería" y construcción de cimientos para que cualquier iniciativa basada en datos pueda funcionar.

---

## Data Engineering vs. Data Science vs. Data Analysis

Es común confundir los roles en el ecosistema de datos. Una forma sencilla de ver sus diferencias es mediante una analogía de construcción:

*   **Data Engineer (El Arquitecto/Constructor):** Construye las carreteras, tuberías y cimientos. Extrae los datos de múltiples fuentes, los limpia y los almacena. *Herramientas: Python, SQL, Docker, Airflow, Cloud.*
*   **Data Scientist (El Ingeniero Automotriz):** Diseña motores predictivos y algoritmos que corren sobre esas carreteras. Busca patrones complejos y crea modelos de Machine Learning. *Herramientas: Python, R, Scikit-learn, TensorFlow.*
*   **Data Analyst (El Navegante):** Conduce sobre la carretera para reportar el estado del tráfico. Toma los datos limpios, genera reportes, dashboards y responde a preguntas directas del negocio. *Herramientas: SQL, Excel, Tableau, PowerBI.*

---

## La importancia de la ingeniería de datos en las empresas modernas

Hoy en día, todas las empresas quieren ser *Data-Driven* (impulsadas por datos) e implementar Inteligencia Artificial. Sin embargo, no pueden hacerlo sin una base sólida.

*   **Escalabilidad:** Los datos crecen exponencialmente. Se necesitan sistemas que no colapsen.
*   **Accesibilidad:** Los analistas y científicos de datos pasan hasta el 80% de su tiempo buscando y limpiando datos si no hay un buen ingeniero de datos respaldándolos.
*   **Democratización:** Un buen sistema de datos permite que cualquier área de la empresa (Marketing, Ventas, Finanzas) pueda tomar decisiones basadas en información en tiempo real.

---

## Consecuencias de una mala práctica en Data Engineering

El principio fundamental del procesamiento de datos es **GIGO** (*Garbage In, Garbage Out* / Basura entra, basura sale). 

Si los cimientos fallan, todo el edificio colapsa. Las consecuencias de una mala gestión de datos incluyen:
*   **Decisiones de negocio erróneas:** Basadas en métricas mal calculadas o datos incompletos.
*   **Pérdida de confianza:** Si los usuarios notan que un dashboard muestra información incorrecta, dejarán de usar las herramientas de datos.
*   **Altos costos operativos:** Arreglar datos de forma manual y repetitiva consume tiempo y dinero.
*   **Fallas en producción:** Modelos de Machine Learning entrenados con datos inconsistentes generarán predicciones desastrosas.

---

## ¿Qué es un Pipeline de Datos?

Un **Pipeline (tubería) de datos** es un conjunto de procesos automatizados que mueven datos desde uno o múltiples sistemas de origen hacia un sistema de destino. 

En el camino, los datos generalmente sufren alteraciones para ser útiles. Imagina una planta potabilizadora de agua: 
1. Se extrae agua cruda (origen).
2. Pasa por filtros y procesos químicos (transformación).
3. Se almacena en tanques limpios (destino) lista para el consumo.

En software, un pipeline elimina la necesidad de mover o procesar datos manualmente (por ejemplo, descargando y limpiando un Excel cada lunes).

---

## Componentes principales de un pipeline

Todo pipeline de datos consta típicamente de 4 etapas fundamentales (conocidas en parte como flujo ETL/ELT):

1.  **Ingesta (Extract):** Conectarse a las fuentes de datos (bases de datos, APIs, archivos CSV de proveedores) y extraer la información en crudo.
2.  **Transformación (Transform):** Limpiar, filtrar, enriquecer y dar formato a los datos. Es aquí donde se aplica la lógica de negocio.
3.  **Almacenamiento (Load):** Guardar los datos ya procesados en un lugar seguro y estructurado (Bases de datos, Data Warehouses, Data Lakes).
4.  **Consumo:** La capa final donde herramientas de visualización, modelos de IA o aplicaciones externas leen los datos limpios.

---

## Arquitectura básica de datos: Visión General

Para que el pipeline funcione, necesitamos una arquitectura que lo soporte. Una arquitectura moderna simple se ve así:

*   **Fuentes (Sources):** Sistemas transaccionales (MySQL), CRMs (Salesforce), archivos planos (CSV, JSON), APIs públicas.
*   **Procesamiento:** Scripts en Python (Pandas) o frameworks distribuidos (Spark) que ejecutan la limpieza.
*   **Orquestación:** Herramientas (como Airflow o Cron) que dictan *cuándo* y *en qué orden* corren los scripts.
*   **Almacenamiento:** Sistemas como AWS S3, Google Cloud Storage, o bases de datos como PostgreSQL.
*   **Visualización:** Dashboards (Streamlit, PowerBI) consumiendo directamente el almacenamiento.

---

## El caso práctico del curso: Dataset de Transacciones

Para asimilar estos conceptos, no nos quedaremos solo en la teoría. A lo largo del curso construiremos un pipeline real de principio a fin.

**Nuestro escenario:**
Somos el equipo de datos de una plataforma de e-commerce o retail. Todos los días recibimos un **Dataset de Transacciones** (ventas, clientes, montos, fechas) proveniente de diferentes sucursales.

**El objetivo:**
Leer estos datos, procesarlos con Python, almacenarlos en una base de datos MySQL, exponerlos mediante una API web y finalmente crear un dashboard interactivo para la gerencia.

---

## Problemas reales en los datos (y en nuestro caso práctico)

El dataset que recibiremos no será perfecto. Nos enfrentaremos a los mismos problemas que un Data Engineer encuentra en su día a día:

*   **Valores Nulos (Missing data):** Transacciones sin el ID del cliente o sin monto registrado.
*   **Duplicados:** Sistemas de origen que enviaron la misma compra dos veces por un error de red.
*   **Inconsistencias de formato:** Fechas escritas como `DD-MM-YYYY` en unos registros y `YYYY/MM/DD` en otros. Tipos de datos incorrectos (números guardados como texto).
*   **Errores de negocio:** Transacciones con montos negativos donde no debería haberlos.

Nuestro pipeline deberá ser lo suficientemente robusto para manejar, alertar o limpiar estos errores automáticamente.

---

## Filosofía del curso: Aprendizaje basado en sistemas

En lugar de aprender funciones de Python aisladas o comandos de SQL de memoria, utilizaremos un enfoque de **pensamiento sistémico (Pipeline Thinking)**.

*   No aprenderemos "cómo hacer un for loop en Python", aprenderemos "cómo usar un for loop para iterar sobre miles de transacciones de ventas".
*   Cada herramienta (Python, Pandas, MySQL, Docker, FastAPI) será vista como **un engranaje dentro de un motor más grande**.
*   Al finalizar, no tendrás scripts sueltos, tendrás un **producto de datos funcional, automatizado y desplegable**, igual al que construirías en una empresa de tecnología real.

---

<!-- _class: code -->
## Practica: Generar el CSV de transacciones

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar introducción al curso y caso del pipeline con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap1/1_1_1_Script.py
import random
import csv
import os
from datetime import datetime, timedelta

# Establecer semilla aleatoria para reproducibilidad de los datos (Regla del curso)
random.seed(987654)

def generar_datos_transaccionales(num_registros=100):
    """
    Generar una lista de diccionarios simulando transacciones de una tienda.
    Se inyectan intencionalmente errores comunes en los datos (nulos, formatos, duplicados).
    """
    estados_posibles = ['COMPLETADA', 'PENDIENTE', 'FALLIDA', 'CANCELADA', '']
    tiendas = ['Tienda_Norte', 'Tienda_Sur', 'Tienda_Centro', 'Tienda_Este', None]
    
    datos = []
    fecha_base = datetime(2023, 1, 1)

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap1/1_1_1_Script.ipynb)

---

## Errores comunes en el Bloque 1.1.1

- **No usar random.seed()**
  → resultados distintos en cada ejecución

- **Abrir el CSV sin encoding correcto**
  → caracteres rotos

- **Confundir el modo 'w' (sobreescribe) con 'a' (acumula) al escribir archivos**

---

## Resumen: Bloque 1.1.1

**Lo que aprendiste:**
- Entender qué es un pipeline de datos y por qué lo necesitamos
- Generar un archivo CSV con datos transaccionales reales (con errores incluidos)
- Leer un archivo CSV con Python nativo y explorar su contenido

**Lo que construiste:**
El script `1_1_1_Script.py` que generar el csv de transacciones usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 1.1.2: Variables, tipos y estructuras básicas

---

<!-- ============================================================ -->
<!-- BLOQUE 1.1.2 — Variables, tipos y estructuras básicas       -->
<!-- Scripts: scripts/cap1/1_1_2_Script.py                    -->
<!-- Notebook: notebooks/cap1/1_1_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 1.1.2
## Variables, tipos y estructuras básicas

> Con el dataset ya creado, ahora aprendemos el lenguaje que nos permite manipularlo.

**Al terminar este bloque podrás:**
- Distinguir los tipos de datos principales de Python (str, int, float, bool, None)
- Usar listas, tuplas y diccionarios para representar una transacción
- Aplicar operaciones básicas de comparación y lógica sobre los datos

---

## Concepto de variable en procesamiento de datos

En el contexto de la ingeniería de datos, procesamos grandes volúmenes de información. Para poder manipular esta información en la memoria de la computadora, necesitamos **variables**.

* **¿Qué es una variable?** Es un espacio reservado en la memoria que almacena un valor y al que le asignamos un nombre simbólico.
* **En el contexto de datos:** Las variables actúan como contenedores temporales. Pueden almacenar desde el valor de una sola transacción hasta un dataset completo antes de ser enviado a una base de datos.
* **Asignación en Python:** Se utiliza el operador `=`.
  
```python
# Asignando el valor de una transacción a una variable
monto_transaccion = 1500.50
```

---

## Tipos de datos en Python

Python maneja distintos tipos de datos básicos. En un pipeline, identificar correctamente el tipo de dato es el primer paso para evitar errores. 

Basándonos en nuestro caso práctico de un dataset de transacciones:

* **Enteros (`int`):** Números sin decimales. Útiles para identificadores o conteos.
  * `id_transaccion = 1001`
* **Flotantes (`float`):** Números con decimales. Críticos para valores monetarios o métricas.
  * `monto = 250.75`
* **Cadenas de texto (`str`):** Secuencias de caracteres. Representan nombres, fechas (en formato crudo) o categorías.
  * `cliente = "Ana Pérez"`
* **Booleanos (`bool`):** Valores lógicos de Verdadero o Falso. Sirven para banderas lógicas o validaciones.
  * `transaccion_aprobada = True`

---

## Impacto de los tipos en el procesamiento de datos

Tratar los datos con el tipo incorrecto es uno de los errores más comunes y destructivos en la ingeniería de datos.

* **Operaciones permitidas:** No podemos realizar una suma matemática entre textos, ni operaciones de texto en números sin transformarlos antes.
* **Uso de memoria:** Diferentes tipos de datos consumen distintas cantidades de memoria.
* **Almacenamiento (Bases de datos):** Las bases de datos relacionales (como MySQL) son estrictas. Si intentamos insertar el texto `"150.5"` en una columna numérica, el pipeline fallará y los datos se perderán o bloquearán el flujo.

---

## Conversión de tipos (Casting)

La mayoría de los datos externos (como archivos CSV o respuestas de APIs) se leen inicialmente como texto (`str`). El **casting** es el proceso de transformar un dato de un tipo a otro.

* Es una de las tareas de **transformación** más básicas en un pipeline.
* Se utilizan las funciones nativas de Python: `int()`, `float()`, `str()`, `bool()`.

```python
# Dato recibido de un archivo CSV (siempre es texto)
monto_csv = "350.99"

# Casting a flotante para poder operar matemáticamente
monto_real = float(monto_csv)

# Ahora podemos aplicar lógica de negocio (ej. sumar impuestos)
monto_con_iva = monto_real * 1.16
```

---

## Listas como representación de colecciones de datos

Una variable simple almacena un solo valor, pero en la vida real procesamos miles de registros. Aquí entran las **estructuras de datos**.

Las **listas** en Python son colecciones ordenadas y mutables que pueden contener múltiples elementos. En procesamiento de datos, una lista suele representar una **columna** entera de datos o una secuencia continua de eventos.

```python
# Una lista representando múltiples montos de transacciones
montos_diarios = [120.5, 340.0, 15.99, 450.25]

# Accediendo al primer elemento (índice 0)
primer_monto = montos_diarios[0]
```

---

## Diccionarios como representación de registros

Si una lista nos sirve para agrupar múltiples valores sueltos, los **diccionarios** son ideales para representar **registros o filas** de un dataset. 

Un diccionario almacena información en pares de `clave: valor`.

* Cada **clave** equivale al nombre de una columna.
* Cada **valor** equivale al dato de esa fila para dicha columna.

```python
# Representación de una sola transacción (una fila de nuestro dataset)
transaccion = {
    "id": 1001,
    "cliente": "Juan López",
    "monto": 250.75,
    "aprobada": True
}

# Accediendo al nombre del cliente
nombre = transaccion["cliente"]
```

---

## Iteración con loops (for)

Para aplicar transformaciones a todos los datos de nuestra colección, utilizamos **ciclos de iteración** (`for`).

En la ingeniería de datos, iterar significa recorrer un conjunto de datos (ej. un millón de filas) registro por registro para aplicar reglas de limpieza o cálculo.

```python
dataset = [
    {"id": 1, "monto": 100.0},
    {"id": 2, "monto": 250.5},
    {"id": 3, "monto": 50.0}
]

# Recorremos cada diccionario dentro de la lista
for fila in dataset:
    monto_final = fila["monto"] * 1.16 # Cálculo de impuesto
    print(f"Transacción {fila['id']} procesada. Monto final: {monto_final}")
```

---

## Operaciones básicas (suma, concatenación)

Dependiendo del tipo de dato, los operadores matemáticos de Python se comportan de forma distinta, lo cual es fundamental para procesar información.

* **Suma Matemática (`+`):** Se aplica sobre `int` o `float`.
  * `total = 150.5 + 40.0` $\rightarrow 190.5$
* **Concatenación (`+`):** Se aplica sobre `str`. Une dos cadenas de texto.
  * `nombre_completo = "Ana" + " " + "Pérez"` $\rightarrow \text{"Ana Pérez"}$
* **Riesgo:** Si un número viene como texto y sumamos, Python concatenará en lugar de realizar matemática.
  * `"150" + "40"` $\rightarrow \text{"15040"}$ (¡Error crítico de datos!)

---

## Problemas comunes en datos (tipos incorrectos, nulos)

En el mundo real, los datos **nunca** vienen limpios. Los primeros obstáculos en un pipeline son:

1. **Tipos incorrectos:** Esperamos un `float` pero recibimos un `str` con letras (ej. `"150.50 USD"`). Intentar hacer un casting `float("150.50 USD")` romperá el script.
2. **Valores Nulos o Vacíos:** Campos que simplemente no vienen en el origen de datos.
   * Representados en Python usualmente por `None` o cadenas vacías `""`.
   * Operar matemáticamente con `None` genera errores fatales en el código.

*Manejar estas excepciones es el núcleo de la etapa de "Limpieza" (Cleaning) en un ETL.*

---

## Tipado dinámico en Python y riesgos asociados

Python es un lenguaje de **tipado dinámico**. Esto significa que no necesitas declarar el tipo de una variable al crearla, y una misma variable puede cambiar de tipo durante su ejecución.

```python
# Esto es válido en Python:
dato = 150.0       # float
dato = "Anulado"   # ahora es str
```

**Riesgos en Data Engineering:**
Si tu pipeline espera que `dato` sea un número para multiplicarlo, pero en una iteración cambia a texto por un error en la fuente, el pipeline fallará. Por esto, siempre debemos **validar y forzar** los tipos de datos en la entrada.

---

## Procesamiento manual de datos (Pipeline básico)

Juntemos todos los conceptos. A continuación, un primer acercamiento a la lógica de un pipeline: **Extraer** información cruda, **Transformarla** (limpiar, cast, operar) y prepararla para **Cargarla**.

```python
# 1. EXTRACT (Datos crudos, simulando lectura de CSV)
datos_crudos = [
    {"id": "1", "monto_str": "100.50"},
    {"id": "2", "monto_str": "200.00"},
    {"id": "3", "monto_str": "error_dato"} # Dato corrupto
]

datos_procesados = []

# 2. TRANSFORM
for fila in datos_crudos:
    # Manejo manual de errores simples
    if fila["monto_str"].replace('.', '', 1).isdigit():
        monto_limpio = float(fila["monto_str"]) # Casting
        
        # 3. LOAD (Guardado en memoria)
        datos_procesados.append({
            "id": int(fila["id"]),
            "monto_calculado": monto_limpio
        })
```

---

```python

print(datos_procesados)
# Resultado esperado de datos limpios y tipados correctamente.

```

---

<!-- _class: code -->
## Practica: Representar una transacción con tipos de Python

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar variables, tipos y estructuras básicas con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap1/1_1_2_Script.py
id_transaccion = 1001          # int: Identificador numérico único
monto_transaccion = 250.50     # float: Valor monetario (decimal)
cliente = "Juan Pérez"         # str: Cadena de texto
es_valida = True               # bool: Estado lógico (Verdadero/Falso)

# Mostrar los tipos de datos asignados en memoria
print("--- Tipos de Datos Básicos ---")
print("Valor:", id_transaccion, "| Tipo:", type(id_transaccion))
print("Valor:", monto_transaccion, "| Tipo:", type(monto_transaccion))
print("Valor:", cliente, "| Tipo:", type(cliente))
print("Valor:", es_valida, "| Tipo:", type(es_valida))
print()

# ------------------------------------------------------------------------------
# ST3, ST4 & ST10: Impacto de los tipos, Conversión (casting) y Tipado dinámico
# Convertir tipos de datos y observar el comportamiento del tipado dinámico
# ------------------------------------------------------------------------------
print("--- Conversión de Tipos (Casting) y Tipado Dinámico ---")

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap1/1_1_2_Script.ipynb)

---

## Errores comunes en el Bloque 1.1.2

- **Confundir int y float**
  → errores en sumas de montos

- **Usar '==' para asignar en lugar de '='**
  → SyntaxError

- **Comparar con None usando == en lugar de 'is None'**
  → comportamiento inesperado

---

## Resumen: Bloque 1.1.2

**Lo que aprendiste:**
- Distinguir los tipos de datos principales de Python (str, int, float, bool, None)
- Usar listas, tuplas y diccionarios para representar una transacción
- Aplicar operaciones básicas de comparación y lógica sobre los datos

**Lo que construiste:**
El script `1_1_2_Script.py` que representar una transacción con tipos de python usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 1.1.3: Lectura de archivos CSV y primeros scripts

---

<!-- ============================================================ -->
<!-- BLOQUE 1.1.3 — Lectura de archivos CSV y primeros scripts   -->
<!-- Scripts: scripts/cap1/1_1_3_Script.py                    -->
<!-- Notebook: notebooks/cap1/1_1_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 1.1.3
## Lectura de archivos CSV y primeros scripts

> Ya sabemos qué contiene el CSV; ahora aprendemos a leerlo de forma correcta y robusta.

**Al terminar este bloque podrás:**
- Leer archivos CSV con el módulo nativo csv de Python
- Iterar fila por fila e imprimir valores específicos
- Manejar el encoding del archivo para evitar caracteres rotos

---

## Importancia y Estructura del Formato CSV

En el mundo de los datos, no siempre trabajaremos con bases de datos complejas o APIs. Muy a menudo, la información llega en archivos planos. 

El formato **CSV** (*Comma-Separated Values* o Valores Separados por Comas) es el estándar de facto para el intercambio de datos debido a su simplicidad, ligereza y compatibilidad universal.

**¿Cómo se estructura un CSV?**
*   **Filas:** Cada línea del texto representa un registro o "fila" de datos.
*   **Columnas:** Dentro de cada línea, los valores se separan por un delimitador (tradicionalmente una coma `,`, aunque también se usan punto y coma `;` o tabuladores).
*   **Encabezado (Opcional pero recomendado):** La primera fila suele contener los nombres de las columnas.

**Ejemplo visual de nuestro dataset de transacciones:**
```text
id_transaccion,fecha,id_cliente,monto
1001,2023-10-01,C-501,250.50
1002,2023-10-01,C-502,15.00
1003,2023-10-02,C-501,120.00
```

---

## Lectura e Iteración de Archivos en Python

Python incluye un módulo nativo llamado `csv` que nos facilita la lectura de estos archivos sin necesidad de instalar librerías adicionales.

Para leer un archivo de forma segura, utilizamos el manejador de contexto `with open(...)`. Esto garantiza que el archivo se cierre automáticamente al terminar, liberando recursos en la memoria.

**Ejemplo de lectura básica:**
```python
import csv

# Abrimos el archivo en modo lectura ('r')
with open('transacciones.csv', mode='r', encoding='utf-8') as archivo:
    lector_csv = csv.reader(archivo)
    
    # Iteramos fila por fila
    for fila in lector_csv:
        print(fila)
```
*Nota:* Al usar `csv.reader`, cada `fila` que iteramos se devuelve como una lista de cadenas de texto (strings). Es decir, `['1001', '2023-10-01', 'C-501', '250.50']`.

---

## Parsing de Datos (Transformación de Tipos)

Un detalle crucial en la ingeniería de datos: **al leer un archivo de texto, todo es texto**. Si queremos realizar operaciones matemáticas con un monto, no podemos sumar el string `'250.50'`; necesitamos transformarlo a un tipo numérico (un `float`). 

A este proceso de interpretar y convertir datos de un formato a otro se le conoce como **parsing**.

```python
import csv

transacciones_procesadas = []

with open('transacciones.csv', mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo) # DictReader usa la primera fila como llaves
    
    for fila in lector:
        # Parsing: Convertimos el string 'monto' a un float numérico
        monto_str = fila['monto']
        monto_num = float(monto_str) 
        
        # Guardamos el dato ya tipado correctamente
        fila['monto'] = monto_num
        transacciones_procesadas.append(fila)
```

---

## Manejo de Errores en Lectura (try/except)

En el mundo real, los datos están sucios. ¿Qué pasa si una celda de monto está vacía (`''`) o tiene texto como `'N/A'`? Nuestro código `float('N/A')` fallará, interrumpiendo todo el programa.

Para construir procesos robustos, usamos bloques `try/except`. Esto nos permite "intentar" una operación y capturar el error si algo sale mal, permitiendo que el script continúe.

```python
        monto_str = fila['monto']
        try:
            monto_num = float(monto_str)
        except ValueError:
            # Si hay un error de conversión (ej. texto no numérico o vacío)
            # Asignamos un valor por defecto (fallback) o lo ignoramos
            monto_num = 0.0
            print(f"Advertencia: Monto inválido '{monto_str}' en transacción {fila['id_transaccion']}")
```
Esta práctica evita que un solo error en un archivo de un millón de líneas destruya horas de procesamiento.

---

## Problemas Comunes en Archivos de Datos

Al recibir archivos externos, te enfrentarás frecuentemente a estos dolores de cabeza:

1.  **Encoding (Codificación de caracteres):** 
    *   *El problema:* Leer caracteres extraños (ej. `MÃ©xico` en lugar de `México`).
    *   *La solución:* Siempre especificar `encoding='utf-8'` al abrir el archivo. Si falla, intenta con `encoding='latin-1'` o `windows-1252`.
2.  **Delimitadores Inconsistentes:**
    *   *El problema:* En Latinoamérica y Europa, la coma se usa para decimales (`250,50`), por lo que los CSV suelen usar punto y coma (`;`) como separador de columnas.
    *   *La solución:* Indicar el delimitador en el lector: `csv.reader(archivo, delimiter=';')`.
3.  **Encabezados Faltantes o Sucios:**
    *   *El problema:* Columnas sin nombre, o con espacios (`" id_cliente "`).
    *   *La solución:* Limpiar los nombres de las columnas antes de procesar los datos (lo abordaremos a fondo en la sección de Pandas).

---

## Procesamiento Básico: Acumulaciones y Métricas

Una vez que tenemos los datos en Python y convertidos a los tipos correctos, podemos empezar a generar valor computando métricas básicas. 

Imaginemos que necesitamos saber el ingreso total (suma de montos) y la cantidad de transacciones procesadas.

```python
ingreso_total = 0.0
total_transacciones = 0

for transaccion in transacciones_procesadas:
    # Acumulamos el monto sumando al total existente
    ingreso_total += transaccion['monto']
    
    # Contamos la transacción
    total_transacciones += 1

ticket_promedio = ingreso_total / total_transacciones if total_transacciones > 0 else 0

print(f"Ingreso Total: ${ingreso_total}")
print(f"Total de Transacciones: {total_transacciones}")
print(f"Ticket Promedio: ${ticket_promedio:.2f}")
```
Acabamos de construir nuestra primera transformación lógica usando operaciones de agregación elementales.

---

## Scripts Reproducibles vs Ejecución Manual

Hasta ahora, podrías hacer estos cálculos abriendo Excel y usando la fórmula de suma. Sin embargo, en Ingeniería de Datos, nuestro objetivo es la **automatización y la escala**.

*   **Ejecución Manual (Excel, cuadernos interactivos):** Es propensa a errores humanos. Si los datos cambian, debes repetir los clics y transformaciones manualmente. Difícil de auditar.
*   **Scripts Reproducibles (Archivos `.py`):** Un script es una receta guardada. No importa si el archivo tiene 10 o 10 millones de filas; ejecutas `python mi_script.py` y el resultado será consistente. 

Un código modular y estructurado nos asegura que los datos siempre sean tratados exactamente bajo las mismas reglas de negocio.

---

## Introducción a "Pipeline Thinking"

Felicidades, sin darte cuenta, acabas de implementar los conceptos base de un **Pipeline de Datos**. 

En lugar de ver la programación como líneas aisladas, en Ingeniería de Datos pensamos en forma de flujo de agua (pipeline):

1.  **Extraer (Extract):** Leímos el archivo CSV con `open()` y `csv.reader()`.
2.  **Transformar (Transform):** Limpiamos los textos, convertimos los strings a floats (parsing) y manejamos los errores (`try/except`). Calculamos métricas de negocio.
3.  **Cargar (Load):** *(Aún en memoria)* Guardamos los datos limpios en una lista (`transacciones_procesadas`) listos para ser usados.

Este flujo de transformación es el corazón de nuestro trabajo. A medida que el curso avance, cambiaremos los archivos locales por bases de datos o servicios en la nube, pero esta lógica fundamental (Extraer -> Transformar -> Cargar) siempre se mantendrá.

---

<!-- _class: code -->
## Practica: Leer y filtrar el CSV de transacciones

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar lectura de archivos csv y primeros scripts con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap1/1_1_3_Script.py
import csv
import random
import os

# Fijar semilla para reproducibilidad según lineamientos
random.seed(987654)

# Definir el nombre del archivo con el que vamos a trabajar
ARCHIVO_CSV = "transacciones_pipeline.csv"

# =============================================================================
# 1. Generar un archivo CSV de prueba (Preparación del entorno)
# =============================================================================
# Vamos a crear un archivo con datos simulados que incluye errores intencionales
# para demostrar problemas comunes en la lectura de datos (ST7, ST9).

def generar_datos_prueba():
    """Generar un archivo CSV con datos de transacciones simulados."""

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap1/1_1_3_Script.ipynb)

---

## Errores comunes en el Bloque 1.1.3

- **No cerrar el archivo (usar open sin 'with')**
  → file leak

- **Olvidar csv.DictReader y usar csv.reader**
  → pérdida de encabezados

- **No especificar encoding='utf-8'**
  → errores en nombres con acentos

---

## Resumen: Bloque 1.1.3

**Lo que aprendiste:**
- Leer archivos CSV con el módulo nativo csv de Python
- Iterar fila por fila e imprimir valores específicos
- Manejar el encoding del archivo para evitar caracteres rotos

**Lo que construiste:**
El script `1_1_3_Script.py` que leer y filtrar el csv de transacciones usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 1.1.4: Funciones aplicadas a limpieza de datos

---

<!-- ============================================================ -->
<!-- BLOQUE 1.1.4 — Funciones aplicadas a limpieza de datos      -->
<!-- Scripts: scripts/cap1/1_1_4_Script.py                    -->
<!-- Notebook: notebooks/cap1/1_1_4_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 1.1.4
## Funciones aplicadas a limpieza de datos

> Pasamos de leer datos a transformarlos: las funciones son la base del pipeline.

**Al terminar este bloque podrás:**
- Definir funciones que validan y limpian campos individuales
- Aplicar funciones a cada fila del CSV para producir datos normalizados
- Separar responsabilidades: una función por tarea de limpieza

---

## Definición y propósito de funciones

En la programación, una **función** es un bloque de código reutilizable diseñado para realizar una tarea específica. 

Imagina una función como una pequeña "fábrica" o "caja negra":
1. **Entradas (Argumentos/Parámetros):** Los datos crudos que le entregamos.
2. **Proceso:** Las operaciones internas que transforman o evalúan los datos.
3. **Salidas (Return):** El resultado procesado que nos devuelve.

En ingeniería de datos, las funciones son cruciales porque nos permiten dejar de escribir scripts monolíticos (largos y desordenados) y empezar a construir bloques lógicos y organizados.

```python
def calcular_impuesto(precio):
    return precio * 0.16
```

---

## Funciones aplicadas a limpieza de datos

Cuando leemos datos de un archivo, como un CSV, a menudo vienen "sucios": textos con espacios extra, números formateados como monedas (`"$1,200.50"`), o fechas inconsistentes.

Crear funciones específicas para limpiar datos nos permite aplicar la misma regla de limpieza de manera uniforme a miles de registros.

```python
def limpiar_precio(precio_str):
    """Convierte un string de precio a un valor flotante."""
    precio_limpio = precio_str.replace('$', '').replace(',', '')
    return float(precio_limpio)

# Prueba
print(limpiar_precio("$1,250.99")) # Salida: 1250.99
```

---

## Encapsulación de lógica

La **encapsulación** significa ocultar los detalles complejos de una operación detrás de un nombre de función claro y descriptivo.

Al hacer esto, el código principal (tu pipeline) se vuelve mucho más fácil de leer. Quien lea tu código no necesita saber *cómo* se limpia el dato paso a paso, solo necesita saber *qué* hace la función.

* **Sin encapsular:** El código principal se llena de `.replace()`, `.strip()`, `.lower()`, etc.
* **Encapsulado:** El código principal solo llama a `limpiar_registro(fila)`.

---

## Manejo de errores en funciones

Los datos reales son impredecibles. Si una función espera un número y recibe un texto vacío o un valor corrupto, el programa "crasheará" (se detendrá abruptamente). En un pipeline de datos, esto es inaceptable.

Utilizamos bloques `try/except` dentro de nuestras funciones para atrapar estos errores y manejarlos de forma segura, permitiendo que el pipeline continúe su ejecución.

```python
def limpiar_edad(edad_str):
    try:
        return int(edad_str)
    except ValueError:
        # Si ocurre un error de conversión, devolvemos un valor seguro
        return None
```

---

## Valores por defecto y fallback (alternativas seguras)

Cuando ocurre un error o falta un dato, es una buena práctica tener un **fallback** (un plan B). Esto se logra retornando un valor por defecto que nuestro sistema entienda como "dato faltante" o "dato inválido" (como `None`, `0` o `"Desconocido"`).

Además, podemos definir parámetros por defecto en la misma función para hacerla más flexible.

```python
def estandarizar_categoria(categoria, valor_defecto="Sin Categoría"):
    if not categoria or categoria.strip() == "":
        return valor_defecto
    return categoria.strip().capitalize()
```

---

## Aplicación masiva: Listas por comprensión

Una vez que tenemos una función de limpieza, necesitamos aplicarla a cientos o miles de registros. Las **listas por comprensión** (List Comprehensions) son una forma "Pythónica", elegante y rápida de aplicar una función a todos los elementos de una lista.

**Enfoque tradicional (Bucle for):**
```python
precios_limpios = []
for p in precios_crudos:
    precios_limpios.append(limpiar_precio(p))
```

**Lista por comprensión (Más rápido y legible):**
```python
precios_limpios = [limpiar_precio(p) for p in precios_crudos]
```

---

## Separación de responsabilidades

Un principio fundamental en la ingeniería de datos es la **separación de responsabilidades** (Separation of Concerns). 

Nunca debemos mezclar la lógica de **ingesta** (leer el archivo) con la lógica de **transformación** (limpiar los datos) en la misma función.

* **Función A (Ingesta):** Se encarga única y exclusivamente de abrir el CSV y extraer las filas.
* **Función B (Transformación):** Recibe las filas y aplica las reglas de limpieza.

Esto permite que si mañana cambiamos la fuente de datos (ej. de CSV a una API), la función de transformación siga funcionando intacta.

---

## Buenas prácticas: Modularidad, claridad y reutilización

Para que tus funciones sean de nivel profesional, debes seguir ciertas reglas:

1. **Modularidad:** Cada función debe hacer **una sola cosa** y hacerla bien. Si tu función se llama `limpiar_y_guardar_y_enviar_email()`, está haciendo demasiado.
2. **Claridad:** Usa nombres de funciones que sean verbos de acción (`limpiar_datos`, `extraer_fecha`, `validar_email`).
3. **Reutilización:** Escribe funciones de manera genérica para que puedan ser utilizadas en diferentes partes de tu proyecto o incluso en proyectos futuros.

---

## Evitar duplicación de código (Principio DRY)

**DRY** significa *Don't Repeat Yourself* (No te repitas). 

Si te encuentras escribiendo la misma lógica de limpieza de espacios o conversión de mayúsculas en tres partes diferentes de tu script, es una señal de alerta. Esa lógica debe extraerse y colocarse en una única función.

**Beneficios del DRY:**
* **Menos errores:** Si hay un bug en la lógica, solo lo corriges en un lugar.
* **Mantenibilidad:** Menos líneas de código significan que es más fácil de leer y actualizar.

---

## Preparación para pipelines estructurados

Todo lo que hemos visto en este bloque es el puente entre "scripts que hacen cosas con datos" y la **Ingeniería de Datos real**.

Al encapsular la limpieza en funciones, manejar los errores, aplicar transformaciones masivas de forma eficiente y separar responsabilidades, estamos construyendo los cimientos de nuestro **Pipeline ETL** (Extracción, Transformación y Carga). 

En las siguientes sesiones, estas funciones modulares serán las piezas de lego con las que construiremos flujos de datos automatizados, robustos y tolerantes a fallos.

---

<!-- _class: code -->
## Practica: Limpiar el dataset con funciones

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar funciones aplicadas a limpieza de datos con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap1/1_1_4_Script.py
"""
Capítulo 1: Fundamentos de Python aplicado a datos
Sección 1: Python para procesamiento de datos
Bloque 4: Funciones aplicadas a limpieza de datos

Este script demuestra cómo utilizar funciones en Python para encapsular lógica 
de limpieza de datos, manejar errores y estructurar un mini-pipeline modular.
"""

import random

# Establecer semilla aleatoria por requerimiento de buenas prácticas y reproducibilidad
random.seed(987654)


# =============================================================================
# ST1: Definición y propósito de funciones
# ST3: Encapsulación de lógica

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap1/1_1_4_Script.ipynb)

---

## Errores comunes en el Bloque 1.1.4

- **Función sin 'return'**
  → siempre devuelve None, rompe el pipeline

- **Modificar la lista original dentro del bucle**
  → resultados impredecibles

- **Mezclar lectura y lógica de negocio en la misma función**
  → difícil de depurar

---

## Resumen: Bloque 1.1.4

**Lo que aprendiste:**
- Definir funciones que validan y limpian campos individuales
- Aplicar funciones a cada fila del CSV para producir datos normalizados
- Separar responsabilidades: una función por tarea de limpieza

**Lo que construiste:**
El script `1_1_4_Script.py` que limpiar el dataset con funciones usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 1.2.1: Introducción a Pandas y DataFrames

---

<!-- _class: section -->
# Sección 2: Pandas y mini ETL
## En esta sección construiremos la capa de pandas y mini etl del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de pandas y mini etl en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 1.2.1: Introducción a Pandas y DataFrames
- Bloque 1.2.2: Limpieza de datos (nulos, tipos, columnas)
- Bloque 1.2.3: Transformaciones y generación de variables
- Bloque 1.2.4: Guardado de datos (CSV y Parquet)

---

<!-- ============================================================ -->
<!-- BLOQUE 1.2.1 — Introducción a Pandas y DataFrames           -->
<!-- Scripts: scripts/cap1/1_2_1_Script.py                    -->
<!-- Notebook: notebooks/cap1/1_2_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 1.2.1
## Introducción a Pandas y DataFrames

> Después de Python puro, damos el salto a Pandas: la herramienta profesional para datos tabulares.

**Al terminar este bloque podrás:**
- Crear DataFrames desde diccionarios y archivos CSV con pd.read_csv()
- Inspeccionar un DataFrame con head(), shape e info()
- Entender la diferencia entre Series y DataFrame

---

## Introducción a Pandas como herramienta de manipulación
### ¿Qué es Pandas?

Pandas es la librería principal y el estándar de la industria para la manipulación y análisis de datos estructurados en Python. 

Construida sobre **NumPy** (librería de cálculo numérico), Pandas ofrece estructuras de datos rápidas, flexibles y expresivas, diseñadas para trabajar con datos tabulares y heterogéneos, típicos en escenarios de bases de datos y hojas de cálculo.

**¿Por qué es vital en la Ingeniería de Datos?**
* Simplifica enormemente tareas de limpieza, unión y filtrado de datos.
* Ofrece operaciones optimizadas escritas en C bajo el capó.
* Es el puente perfecto entre la extracción de datos en bruto y su almacenamiento final.

---

## Limitaciones de listas y diccionarios vs DataFrames
### ¿Por qué no usar simplemente estructuras nativas?

En el bloque anterior vimos cómo procesar datos con listas y diccionarios. Sin embargo, para pipelines de datos reales, estas estructuras presentan limitaciones importantes:

* **Falta de operaciones vectorizadas:** Sumar dos columnas en una lista de diccionarios requiere un bucle `for` manual.
* **Sintaxis verbosa:** Filtrar datos nulos o agrupar categorías con estructuras nativas requiere múltiples líneas de código complejo.
* **Bajo rendimiento:** Iterar fila por fila en Python puro es ineficiente para cientos de miles de registros.

**La solución de Pandas:** Proporciona un entorno donde las operaciones matemáticas o lógicas se aplican de forma inmediata a columnas enteras sin necesidad de escribir bucles.

---

## Concepto de Series y DataFrame
### La anatomía de Pandas

Pandas introduce dos estructuras de datos fundamentales para manejar información:

1. **La Serie (Series):**
   * Es una estructura unidimensional, equivalente a una lista de Python, un array o una **sola columna** en una tabla.
   * Cuenta con un índice (etiquetas para cada fila) que facilita la alineación de los datos.

2. **El DataFrame:**
   * Es una estructura bidimensional, equivalente a una tabla SQL o una hoja de cálculo Excel.
   * Se puede entender como un diccionario o colección de *Series* (columnas) que comparten el mismo índice (filas).

---

## Creación de DataFrames desde estructuras nativas
### De Python puro a Pandas

Podemos inicializar un DataFrame fácilmente utilizando estructuras que ya conocemos, como los diccionarios. Esta es una práctica común cuando estamos simulando datos o creando pequeños catálogos dentro del código.

```python
import pandas as pd

# Diccionario donde cada clave es una columna y los valores son listas (filas)
datos_transacciones = {
    "id_transaccion": [101, 102, 103],
    "cliente": ["Ana", "Luis", "Carlos"],
    "monto": [250.50, 15.00, 340.20]
}

# Creación del DataFrame
df = pd.DataFrame(datos_transacciones)
```
Al convertir estos datos, Pandas alinea automáticamente las listas, asigna un índice numérico (`0, 1, 2...`) y nos brinda acceso a toda su gama de métodos analíticos.

---

## Lectura de datos con Pandas (`read_csv`)
### Ingesta de datos en una sola línea

Mientras que el módulo nativo `csv` requiere abrir el archivo, leerlo y estructurar los bucles, Pandas abstrae todo este proceso con la función `read_csv()`.

Esta función es el estándar de oro para la lectura de datos planos en pipelines iniciales:

* **Manejo automático de encabezados:** Reconoce la primera fila como nombres de columnas.
* **Inferencia de tipos:** Intenta deducir si una columna es numérica, de texto o booleana automáticamente.
* **Flexibilidad:** Permite definir separadores (`sep=';'`), saltar filas (`skiprows`), o manejar codificaciones (`encoding='utf-8'`).

---

## Inspección inicial (`head`, `shape`, `info`)
### Conociendo la forma de los datos

Una vez cargado el DataFrame, el primer paso de un ingeniero de datos es inspeccionar qué se acaba de leer. Pandas nos da tres herramientas clave:

* **`df.head(n)`:** Muestra las primeras `n` filas (por defecto 5). Útil para verificar que el parseo (columnas y separadores) fue correcto.
* **`df.shape`:** Retorna una tupla `(filas, columnas)`. Nos da la escala inmediata del dataset.
* **`df.info()`:** Proporciona un resumen técnico exhaustivo. Muestra el número de filas, nombres de columnas, cantidad de valores **No nulos** en cada una y el tipo de dato subyacente. Es la mejor forma de detectar datos faltantes rápidamente.

---

## Tipos de columnas en Pandas
### El ecosistema de *dtypes*

En Pandas, cada columna (Serie) tiene un tipo de dato específico, conocido como `dtype`. Comprenderlos es vital, ya que un tipo incorrecto puede romper un pipeline o causar cálculos erróneos.

* **`object` / `string`:** Usado para texto o mezcla de tipos.
* **`int64`:** Números enteros (ej. cantidad de productos).
* **`float64`:** Números con decimales (ej. montos de transacciones).
* **`datetime64`:** Formatos de fecha y hora, esenciales para series temporales.
* **`bool`:** Valores lógicos `True` / `False`.

*Nota:* Si Pandas lee una columna numérica pero encuentra un solo caracter de texto (como un espacio o un signo de dólar), convertirá toda la columna al tipo `object`.

---

## Exploración básica de datos
### Entendiendo el contenido numérico y categórico

Más allá de la estructura, necesitamos entender la distribución de la información para definir nuestras reglas de limpieza.

* **`df.describe()`:** Genera estadísticas descriptivas para todas las columnas numéricas. Retorna el conteo, media, desviación estándar, valores mínimos, máximos y cuartiles. Ayuda a detectar valores atípicos (outliers).
* **`df['columna'].value_counts()`:** Aplicado a una columna específica (generalmente texto o categórica), cuenta la frecuencia de cada valor único. Es ideal para analizar distribuciones de categorías (ej. cantidad de transacciones por estado: *'Completado'*, *'Fallido'*).

---

## Contexto de uso en pipelines
### ¿Dónde encaja Pandas en la Ingeniería de Datos?

En la arquitectura de un pipeline (Ingesta $\rightarrow$ Transformación $\rightarrow$ Almacenamiento $\rightarrow$ Consumo), Pandas brilla principalmente en la fase de **Transformación**.

1. **Ingesta:** Pandas facilita la lectura inicial, pero a menudo los datos provienen de APIs o bases de datos donde otras librerías hacen la extracción inicial.
2. **Transformación:** Aquí es el rey. Usamos Pandas para limpiar nulos, cambiar tipos de datos, cruzar tablas y crear nuevas métricas de negocio.
3. **Almacenamiento:** Pandas prepara el formato final y permite exportar directamente a CSV, Parquet o conectarse a motores SQL.

Pandas nos permite escribir estas transformaciones en scripts reproducibles.

---

## Escalabilidad conceptual: Pandas vs Big Data
### ¿Cuándo Pandas deja de ser suficiente?

A pesar de su potencia, Pandas tiene una limitación arquitectónica fundamental: **opera *in-memory*** (todo el dataset debe caber en la memoria RAM de la máquina).

* **Small Data (Megabytes a pocos Gigabytes):** Pandas es la herramienta perfecta. Es rápido y altamente expresivo.
* **Big Data (Decenas de Gigabytes a Terabytes):** Pandas fallará (arrojará un error de falta de memoria o *Out of Memory*). 

Para escenarios de Big Data, la ingeniería de datos recurre a:
1. **Motores distribuidos:** Apache Spark (PySpark) o Dask, que dividen el trabajo en múltiples servidores.
2. **Librerías optimizadas en un solo nodo:** Polars, que maneja la memoria y el paralelismo de forma más agresiva que Pandas.
3. **Push-down computing:** Realizar las transformaciones directamente en el motor de la base de datos mediante SQL.

---

<!-- _class: code -->
## Practica: Cargar el CSV con Pandas y explorar su estructura

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar introducción a pandas y dataframes con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap1/1_2_1_Script.py
"""
Capítulo 1: Fundamentos de Python aplicado a datos
Sección 2: Pandas y mini ETL
Bloque 1: Introducción a Pandas y DataFrames

Este script cubre los siguientes subtemas (ST):
ST1: Introducción a Pandas como herramienta de manipulación de datos.
ST2: Limitaciones de listas/diccionarios vs DataFrames.
ST3: Concepto de Series y DataFrame.
ST4: Creación de DataFrames desde estructuras nativas.
ST5: Lectura de datos con Pandas (read_csv).
ST6: Inspección inicial (head, shape, info).
ST7: Tipos de columnas en Pandas.
ST8: Exploración básica de datos.
ST9: Contexto de uso en pipelines.
ST10: Escalabilidad conceptual (limitaciones de Pandas vs Big Data).
"""

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap1/1_2_1_Script.ipynb)

---

## Errores comunes en el Bloque 1.2.1

- **No importar pandas como 'pd'**
  → NameError en todo el script

- **Confundir df['columna'] (devuelve Serie) con df[['columna']] (devuelve DataFrame)**

- **Ignorar el índice**
  → errores al fusionar DataFrames

---

## Resumen: Bloque 1.2.1

**Lo que aprendiste:**
- Crear DataFrames desde diccionarios y archivos CSV con pd.read_csv()
- Inspeccionar un DataFrame con head(), shape e info()
- Entender la diferencia entre Series y DataFrame

**Lo que construiste:**
El script `1_2_1_Script.py` que cargar el csv con pandas y explorar su estructura usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 1.2.2: Limpieza de datos (nulos, tipos, columnas)

---

<!-- ============================================================ -->
<!-- BLOQUE 1.2.2 — Limpieza de datos (nulos, tipos, columnas)   -->
<!-- Scripts: scripts/cap1/1_2_2_Script.py                    -->
<!-- Notebook: notebooks/cap1/1_2_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 1.2.2
## Limpieza de datos (nulos, tipos, columnas)

> Con el DataFrame cargado, ahora limpiamos los datos sucios que generamos en el bloque 1.

**Al terminar este bloque podrás:**
- Detectar y eliminar valores nulos con isnull() y dropna()/fillna()
- Corregir tipos de datos con astype() y pd.to_numeric()
- Eliminar columnas innecesarias y renombrar con rename()

---

## 1. La Importancia de la Limpieza de Datos en Pipelines

En el mundo de los datos existe una regla de oro: **"Garbage In, Garbage Out" (Basura entra, basura sale)**. 

Si construimos un pipeline de datos perfecto pero lo alimentamos con datos corruptos o incorrectos, el resultado final no tendrá ningún valor. La limpieza de datos es la etapa donde tomamos los datos crudos (Raw Data) y los preparamos para que sean confiables.

**¿Por qué es crítica esta etapa?**
* Previene caídas en el pipeline (errores de ejecución por tipos de datos inesperados).
* Garantiza la validez de las métricas de negocio.
* Suele consumir entre el **60% y el 80%** del tiempo de un ingeniero o científico de datos.

---

## 2. Identificación de Valores Nulos (isnull)

En un dataset, la ausencia de información se representa comúnmente con el valor `NaN` (Not a Number) o `None`. Pandas nos ofrece herramientas vectorizadas para encontrarlos rápidamente.

Para identificar nulos usamos el método `.isnull()` o su alias `.isna()`.

```python
import pandas as pd

# Supongamos que cargamos nuestro dataset de transacciones
df = pd.read_csv('transacciones.csv')

# Devuelve un DataFrame de booleanos (True si es nulo)
mascara_nulos = df.isnull()

# Para ver cuántos nulos hay por cada columna, sumamos los valores True (1)
conteo_nulos = df.isnull().sum()
print(conteo_nulos)
```

Saber dónde y cuántos nulos tenemos es el primer paso antes de decidir qué hacer con ellos.

---

## 3. Tratamiento de Nulos: Eliminar o Imputar (dropna, fillna)

Una vez identificados, tenemos dos caminos principales: **eliminar** la información incompleta o **rellenarla (imputar)** con un valor lógico.

### Eliminar Nulos (`dropna`)
Útil cuando la cantidad de nulos es mínima y descartar esos registros no afecta el análisis general.

```python
# Elimina cualquier fila que contenga al menos un valor nulo
df_limpio = df.dropna()

# Elimina la fila SOLO si la columna 'monto' es nula
df_limpio = df.dropna(subset=['monto'])
```

### Rellenar Nulos (`fillna`)
Útil cuando queremos conservar el registro y podemos asumir un valor por defecto (un cero, la media, o un texto como "Desconocido").

```python
# Rellenar valores nulos de 'monto' con 0
df['monto'] = df['monto'].fillna(0)

# Rellenar nulos de texto con "Sin Categoría"
df['categoria'] = df['categoria'].fillna('Sin Categoría')
```

---

## 4. Conversión de Tipos de Datos (astype)

Es muy común que al leer un archivo (como un CSV), Pandas asigne un tipo de dato incorrecto. Por ejemplo, leer un número entero como texto (string). Esto impide realizar operaciones matemáticas.

El método `.astype()` nos permite forzar la conversión de una columna a un tipo de dato específico (como `int`, `float`, `str`, `bool`).

```python
# Verificamos los tipos de datos actuales
print(df.dtypes)

# Convertir la columna 'cantidad' de texto (object) a número entero (int)
df['cantidad'] = df['cantidad'].astype(int)

# Convertir 'monto' a número decimal (float)
df['monto'] = df['monto'].astype(float)
```
*Nota: Si la columna contiene valores que no se pueden convertir (como una letra en una columna que queremos pasar a `int`), Pandas arrojará un error. Se requiere limpieza previa.*

---

## 5. Normalización de Nombres de Columnas

Los nombres de las columnas suelen venir de bases de datos antiguas, hojas de cálculo o APIs con formatos inconsistentes (espacios, mayúsculas, caracteres especiales). 

Para acceder a las columnas fácilmente en Python, debemos **normalizarlas**:
1. Convertir todo a minúsculas.
2. Reemplazar espacios por guiones bajos (`_`).
3. Eliminar caracteres especiales.

```python
# Ver nombres actuales
print(df.columns) 
# Salida de ejemplo: Index(['ID Cliente', 'Monto Transacción!', 'Fecha'], dtype='object')

# Normalización usando métodos de string
df.columns = (
    df.columns
    .str.lower()                  # Todo a minúscula
    .str.replace(' ', '_')        # Espacios por guiones bajos
    .str.replace('[^\w\s]', '', regex=True) # Eliminar puntuación
)

print(df.columns)
# Salida normalizada: Index(['id_cliente', 'monto_transaccion', 'fecha'], dtype='object')
```

---

## 6. Manejo de Strings en Columnas

Cuando procesamos columnas de texto categóricas (como nombres, ciudades, correos), es muy probable encontrar problemas de espacios extra o variaciones en mayúsculas/minúsculas.

El **accessor `.str`** en Pandas nos permite aplicar funciones de texto a toda la columna de manera vectorizada.

```python
# Eliminar espacios en blanco al inicio y al final de los textos
df['ciudad'] = df['ciudad'].str.strip()

# Convertir todo a mayúsculas para homologar
df['estado'] = df['estado'].str.upper()

# Extraer partes de un texto (ej: dominio de un email)
df['dominio_email'] = df['email'].str.split('@').str[1]
```

---

## 7. Detección y Tratamiento de Inconsistencias

Las inconsistencias ocurren cuando el mismo concepto lógico está escrito de diferentes formas. Esto arruina las agrupaciones y las métricas.

*Ejemplo:* En la columna `metodo_pago` encontramos: `"TDC"`, `"tarjeta de credito"`, `"Tarjeta Crédito"`.

Podemos usar el método `.replace()` o mapeos mediante diccionarios para estandarizar estos valores.

```python
# Ver los valores únicos y su frecuencia
print(df['metodo_pago'].value_counts())

# Crear un diccionario de mapeo para estandarizar
mapeo_pagos = {
    'TDC': 'Tarjeta de Crédito',
    'tarjeta de credito': 'Tarjeta de Crédito',
    'Tarjeta Crédito': 'Tarjeta de Crédito',
    'efectivo': 'Efectivo',
    'CASH': 'Efectivo'
}

# Aplicar el reemplazo
df['metodo_pago'] = df['metodo_pago'].replace(mapeo_pagos)
```

---

## 8. Manejo de Duplicados

Los registros duplicados pueden inflar artificialmente nuestras métricas de negocio (ej. contar dos veces el mismo ingreso). 

Pandas proporciona `.duplicated()` para detectar duplicados y `.drop_duplicates()` para eliminarlos.

```python
# Detectar cuántas filas son exactamente iguales a otra
cantidad_duplicados = df.duplicated().sum()
print(f"Filas duplicadas: {cantidad_duplicados}")

# Eliminar duplicados exactos (mantiene la primera aparición por defecto)
df = df.drop_duplicates()

# Eliminar duplicados basados solo en un subconjunto de columnas (ej. mismo ID de transacción)
df = df.drop_duplicates(subset=['id_transaccion'])
```

---

## 9. Formatos Incorrectos: Fechas y Números

### Cadenas Numéricas Sucias
A veces los números vienen como texto con símbolos de moneda o separadores de miles (`"$1,200.50"`). No podemos usar `.astype(float)` directamente.

```python
# Limpiar caracteres especiales antes de convertir a número
df['ingreso'] = df['ingreso'].str.replace('$', '').str.replace(',', '')
df['ingreso'] = df['ingreso'].astype(float)
```

### Conversión de Fechas
Las fechas suelen leerse como cadenas de texto (`object`). Para poder extraer el mes, día o hacer diferencias de tiempo, debemos convertirlas al tipo `datetime` de Pandas.

```python
# Forzar conversión a formato fecha
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce') 
# 'coerce' convierte los valores que no son fechas en NaT (Not a Time, equivalente a nulo para fechas)
```

---

## 10. El Impacto de Datos Sucios en el Análisis

Ignorar los pasos anteriores tiene consecuencias directas y graves en etapas posteriores:

1. **Métricas Sesgadas:** Un duplicado en una tabla de ventas reportará ingresos mayores a los reales, engañando a la dirección de la empresa.
2. **Caída de Algoritmos:** Si entrenamos un modelo de Machine Learning y una columna numérica tiene un string accidental (ej. `"N/A"`), el modelo fallará en producción.
3. **Pérdida de Confianza:** Si los usuarios de los datos (Analistas, Científicos de Datos, Stakeholders) detectan inconsistencias constantemente, dejarán de confiar en el pipeline de ingeniería de datos.

La limpieza de datos es un **seguro de calidad**.

---

## 11. Buenas Prácticas de Limpieza

Para cerrar, cuando diseñemos la fase de limpieza en un pipeline de datos con Python y Pandas, debemos seguir estos principios:

1. **Nunca modifiques la fuente original (Raw Data):** Lee los datos crudos, límpialos y guárdalos en un nuevo archivo/tabla (Processed Data).
2. **Encapsula en funciones:** No uses celdas de código sueltas. Crea funciones modulares como `limpiar_nombres_columnas(df)` o `estandarizar_fechas(df)`.
3. **Documenta las decisiones lógicas:** Si decides rellenar los nulos con `0` en lugar de la media, deja un comentario explicando el motivo de negocio.
4. **Verifica siempre después de transformar:** Usa `df.info()` o `df.isnull().sum()` antes y después de tu limpieza para asegurarte de que los cambios aplicaron correctamente.

---

<!-- _class: code -->
## Practica: Limpiar nulos y corregir tipos en el DataFrame

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar limpieza de datos (nulos, tipos, columnas) con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap1/1_2_2_Script.py
"""
Capítulo 1: Fundamentos de Python aplicado a datos
Sección 2: Pandas y mini ETL
Bloque 2: Limpieza de datos (nulos, tipos, columnas)

Descripción:
Script enfocado en la limpieza de datos como etapa crítica en ingeniería de datos.
Se abordan valores nulos, conversión de tipos, normalización de columnas, manejo
de strings, duplicados e inconsistencias.

Subtemas (ST):
ST1: Importancia de la limpieza de datos en pipelines
ST2: Identificación de valores nulos (isnull)
ST3: Tratamiento de nulos (fillna, dropna)
ST4: Conversión de tipos de datos (astype)
ST5: Normalización de nombres de columnas
ST6: Manejo de strings en columnas
ST7: Detección de inconsistencias

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap1/1_2_2_Script.ipynb)

---

## Errores comunes en el Bloque 1.2.2

- **Usar fillna(0) en columnas de texto**
  → introduce '0' como valor falso

- **Olvidar inplace=True o la reasignación**
  → la limpieza no persiste

- **Convertir a int una columna con NaN**
  → ValueError (usar Int64 o float primero)

---

## Resumen: Bloque 1.2.2

**Lo que aprendiste:**
- Detectar y eliminar valores nulos con isnull() y dropna()/fillna()
- Corregir tipos de datos con astype() y pd.to_numeric()
- Eliminar columnas innecesarias y renombrar con rename()

**Lo que construiste:**
El script `1_2_2_Script.py` que limpiar nulos y corregir tipos en el dataframe usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 1.2.3: Transformaciones y generación de variables

---

<!-- ============================================================ -->
<!-- BLOQUE 1.2.3 — Transformaciones y generación de variables   -->
<!-- Scripts: scripts/cap1/1_2_3_Script.py                    -->
<!-- Notebook: notebooks/cap1/1_2_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 1.2.3
## Transformaciones y generación de variables

> Con datos limpios, ahora los enriquecemos: transformar es la 'T' del ETL.

**Al terminar este bloque podrás:**
- Crear columnas derivadas con operaciones vectorizadas
- Categorizar transacciones con np.where() y condiciones
- Calcular resúmenes con groupby() y agg()

---

## Selección de Columnas (ST1)

En un pipeline de datos, rara vez necesitamos toda la información que extraemos de la fuente original. Trabajar con datos innecesarios consume memoria y tiempo de procesamiento. 

La **selección de columnas** nos permite quedarnos únicamente con las variables que aportan valor a nuestro análisis o etapa de transformación.

### ¿Cómo lo hacemos en Pandas?
Podemos seleccionar una sola columna (que nos devuelve una Serie) o múltiples columnas (que nos devuelve un nuevo DataFrame).

```python
import pandas as pd

# Supongamos que tenemos nuestro dataset de transacciones
# df = pd.read_csv('transacciones.csv')

# Seleccionar una sola columna (Serie)
montos = df['monto']

# Seleccionar múltiples columnas (DataFrame)
# Nota el uso de doble corchete [[ ]]
df_reducido = df[['id_transaccion', 'id_cliente', 'monto']]
```

---

## Filtrado de Registros (ST2)

Así como filtramos columnas, a menudo necesitamos quedarnos solo con un subconjunto de filas que cumplan con ciertas condiciones. Esto se conoce como **filtrado de registros** o *boolean indexing* (indexación booleana).

Consiste en crear una "máscara" de valores Verdadero/Falso y aplicarla al DataFrame.

### Ejemplos prácticos

```python
# 1. Crear la condición (devuelve una serie de True/False)
condicion_exitosas = df['estado'] == 'completada'

# 2. Aplicar el filtro al DataFrame
df_completadas = df[condicion_exitosas]

# Podemos hacerlo en una sola línea y con múltiples condiciones
# Usamos & para "Y" (AND) y | para "O" (OR). 
# ¡Importante usar paréntesis para cada condición!
df_filtro = df[(df['monto'] > 100) & (df['estado'] == 'completada')]
```

---

## Operaciones Vectorizadas (ST3)

Una de las grandes ventajas de Pandas es la **vectorización**. Esto significa que podemos aplicar operaciones matemáticas a columnas enteras de forma simultánea, sin necesidad de usar bucles (`for` o `while`). 

Esto no solo hace que el código sea más fácil de leer, sino que es computacionalmente **mucho más rápido** (ya que está optimizado en lenguaje C por debajo).

### Ejemplo matemático
Si queremos calcular el total de una venta, la fórmula sería:
$$Total = Precio \times Cantidad$$

En Pandas, lo expresamos directamente con las columnas:

```python
# Operación matemática sobre columnas enteras
df['total_venta'] = df['precio_unitario'] * df['cantidad']

# Aplicar descuentos
df['monto_con_descuento'] = df['monto'] * 0.90
```

---

## Creación de Columnas Derivadas (ST4)

Las **columnas derivadas** son variables nuevas que creamos a partir de los datos existentes en nuestro DataFrame. Son fundamentales en la fase de transformación (la "T" del ETL), ya que enriquecen nuestro dataset con información procesada.

Podemos crear columnas derivadas usando:
* Operaciones aritméticas (como vimos en la vectorización).
* Lógica condicional (asignar valores basados en otras columnas).
* Extracción de datos (por ejemplo, sacar el año de una fecha).

```python
# Crear una columna estática
df['moneda'] = 'USD'

# Crear una columna condicional usando numpy.where
import numpy as np
# Si el monto es mayor a 500, es 'Alto', sino 'Normal'
df['categoria_monto'] = np.where(df['monto'] > 500, 'Alto', 'Normal')
```

---

## Uso de la función `apply` (ST5)

Aunque las operaciones vectorizadas son la mejor opción por su velocidad, a veces necesitamos aplicar una lógica muy compleja o usar funciones personalizadas que no se pueden vectorizar fácilmente. Para esto utilizamos el método `.apply()`.

`apply()` toma una función y la ejecuta fila por fila (o columna por columna) en el DataFrame.

```python
# Definimos una función personalizada con reglas de negocio
def categorizar_cliente(fila):
    if fila['monto'] > 1000 and fila['antiguedad_meses'] > 12:
        return 'VIP'
    elif fila['monto'] > 500:
        return 'Frecuente'
    else:
        return 'Regular'

# Aplicamos la función a nivel de fila (axis=1)
df['tipo_cliente'] = df.apply(categorizar_cliente, axis=1)
```
*Nota: Úsalo con precaución en datasets gigantes, ya que es más lento que la vectorización al evaluar los datos fila por fila.*

---

## Cálculo de Métricas (ST6)

En el procesamiento de datos, a menudo necesitamos obtener resúmenes de nuestro dataset. Pandas nos provee funciones de agregación rápidas para calcular métricas simples como ingresos totales, conteos, promedios, entre otros.

Estas métricas sirven tanto para validar nuestros datos como para reportar KPIs (Key Performance Indicators).

```python
# Conteo de registros (número total de transacciones)
total_transacciones = df['id_transaccion'].count()
# Alternativamente: len(df)

# Suma total (Ingresos brutos)
ingresos_totales = df['monto'].sum()

# Promedio (Ticket promedio)
ticket_promedio = df['monto'].mean()

print(f"Ingresos Totales: ${ingresos_totales}")
print(f"Ticket Promedio: ${ticket_promedio}")
```

---

## Agrupaciones Simples: Concepto de GroupBy (ST7)

Calcular el ingreso total es útil, pero en la realidad necesitamos métricas segmentadas: *¿Cuánto se vendió por cada cliente?* *¿Cuántas transacciones hubo por país?*

Aquí entra el concepto de **Split-Apply-Combine** (Dividir-Aplicar-Combinar) mediante la función `.groupby()`:
1. **Split**: Divide los datos en grupos según una clave (ej. `id_cliente`).
2. **Apply**: Aplica una función a cada grupo (ej. `sum()`).
3. **Combine**: Une los resultados en una nueva estructura de datos.

```python
# Calcular ingresos totales por cliente
ingresos_por_cliente = df.groupby('id_cliente')['monto'].sum()

# Calcular el número de transacciones por estado
transacciones_por_estado = df.groupby('estado')['id_transaccion'].count()
```

---

## Transformaciones basadas en Lógica de Negocio y su Valor (ST8, ST11)

Las transformaciones no son solo ejercicios matemáticos; son la traducción de la **lógica de negocio** a código. Un ingeniero de datos convierte las reglas operativas de una empresa en variables concretas que los analistas y modelos pueden usar.

### El valor de negocio
Si el departamento de marketing necesita hacer una campaña para "clientes en riesgo de abandono", el equipo de datos debe transformar las tablas transaccionales en una métrica como `dias_desde_ultima_compra`. 

**La transformación es el puente entre los datos crudos (raw data) y la toma de decisiones empresariales.** No transformamos por transformar, transformamos para generar valor.

---

## Feature Engineering Básico (ST9)

El *Feature Engineering* (Ingeniería de Características) es el proceso de usar el conocimiento del dominio para crear variables que hagan que los algoritmos de machine learning (o el análisis de datos) funcionen mejor.

En esta etapa del pipeline, creamos características que faciliten el consumo posterior de los datos.

```python
# Ejemplo 1: Extracción de información de fechas
df['fecha'] = pd.to_datetime(df['fecha_transaccion'])
df['mes'] = df['fecha'].dt.month
df['dia_semana'] = df['fecha'].dt.day_name()

# Ejemplo 2: Variables binarias (Flags) a partir de strings
# Crea una columna que vale 1 si es compra internacional, 0 si no
df['es_internacional'] = df['pais_origen'].apply(lambda x: 1 if x != 'MX' else 0)
```
Estas nuevas columnas ('features') permitirán analizar si las ventas suben los viernes o si las compras internacionales tienen un ticket promedio más alto.

---

## Validación de Resultados Transformados (ST10)

Una vez que hemos limpiado, filtrado y creado nuevas variables, el último paso en nuestra etapa de transformación es **validar**. Si no validamos, podemos arrastrar errores críticos al sistema de almacenamiento.

¿Qué debemos revisar?
1. ¿Las nuevas columnas tienen los tipos de datos correctos?
2. ¿Generamos valores nulos de forma accidental al hacer cálculos matemáticos? (ej. división por cero).
3. ¿La lógica de negocio se aplicó correctamente?

```python
# 1. Revisar una muestra de los datos transformados
print(df[['monto', 'cantidad', 'total_venta']].head())

# 2. Verificar que no se introdujeron nulos en la nueva columna
print("Nulos en total_venta:", df['total_venta'].isnull().sum())

# 3. Validación lógica (Sanity check) mediante assert
# Si esto falla, el script arrojará un error, deteniendo un pipeline defectuoso
assert df['total_venta'].min() >= 0, "Error: Hay ventas totales negativas"
```

---

<!-- _class: code -->
## Practica: Crear variables derivadas del monto y fecha

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar transformaciones y generación de variables con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap1/1_2_3_Script.py
import pandas as pd
import numpy as np

# Configurar semilla para reproducibilidad
np.random.seed(987654)

# ==============================================================================
# ST8, ST11: Contexto de negocio y preparación de datos iniciales
# Generar un dataset simulado de transacciones
# ==============================================================================
def generar_datos_transacciones():
    """
    Generar un DataFrame con datos de transacciones simuladas
    para aplicar transformaciones.
    """
    n_registros = 100
    
    # Generar fechas aleatorias en el último mes

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap1/1_2_3_Script.ipynb)

---

## Errores comunes en el Bloque 1.2.3

- **Usar apply() con lambda donde basta una operación vectorizada**
  → muy lento

- **Olvidar resetear el índice tras groupby()**
  → índice jerárquico inesperado

- **Crear columnas con nombres que contienen espacios**
  → sintaxis incómoda

---

## Resumen: Bloque 1.2.3

**Lo que aprendiste:**
- Crear columnas derivadas con operaciones vectorizadas
- Categorizar transacciones con np.where() y condiciones
- Calcular resúmenes con groupby() y agg()

**Lo que construiste:**
El script `1_2_3_Script.py` que crear variables derivadas del monto y fecha usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 1.2.4: Guardado de datos (CSV y Parquet)

---

<!-- ============================================================ -->
<!-- BLOQUE 1.2.4 — Guardado de datos (CSV y Parquet)            -->
<!-- Scripts: scripts/cap1/1_2_4_Script.py                    -->
<!-- Notebook: notebooks/cap1/1_2_4_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 1.2.4
## Guardado de datos (CSV y Parquet)

> Cerramos el primer ciclo del pipeline: los datos limpios y transformados se persisten.

**Al terminar este bloque podrás:**
- Guardar un DataFrame en CSV con to_csv() y controlar el índice
- Guardar en formato Parquet con to_parquet() para eficiencia
- Comparar tamaño y velocidad de lectura entre CSV y Parquet

---

## Definición formal de ETL (Extract, Transform, Load)

El acrónimo **ETL** representa el corazón de la ingeniería de datos clásica. Describe el proceso de mover datos desde su origen hasta un destino final donde aporten valor.

*   **Extract (Extracción):** Leer los datos desde múltiples sistemas de origen (bases de datos, archivos, APIs). En nuestro caso, leer el dataset original con Pandas.
*   **Transform (Transformación):** Aplicar reglas de negocio, limpieza, filtrado, cálculos y cruces de información. Aquí ocurren el manejo de nulos y la creación de nuevas variables.
*   **Load (Carga):** Escribir o guardar los datos procesados en un sistema de destino (Data Warehouse, Data Lake, o simplemente nuevos archivos) para que puedan ser consumidos.

Comprender el ETL nos ayuda a estructurar mentalmente cualquier pipeline de datos en etapas modulares y claramente definidas.

---

## Exportación a CSV y Escritura de DataFrames

El formato **CSV (Comma-Separated Values)** es el estándar más universal y legible por humanos para el intercambio de datos tabulares.

Una vez que hemos limpiado y transformado nuestro DataFrame en Pandas, el paso natural es exportarlo para no perder el trabajo realizado.

### ¿Cómo exportar a CSV en Pandas?
Pandas nos ofrece el método `.to_csv()`, el cual convierte el DataFrame tabular en un archivo de texto estructurado.

```python
import pandas as pd

# Supongamos que df_limpio es nuestro DataFrame ya transformado
# Guardamos el archivo omitiendo el índice de Pandas (index=False)
df_limpio.to_csv("transacciones_procesadas.csv", index=False, encoding="utf-8")
```

**Consideraciones importantes:**
*   Siempre utilizar `index=False` a menos que el índice contenga información valiosa (de lo contrario, se creará una columna extra sin nombre).
*   Definir el `encoding="utf-8"` previene problemas con caracteres especiales (como acentos o la letra ñ).

---

## Introducción a Parquet

A medida que los datos crecen, los archivos CSV muestran sus limitaciones (son pesados, lentos de leer y no preservan los tipos de datos). Aquí es donde entra **Parquet**.

**Apache Parquet** es un formato de almacenamiento de código abierto, diseñado para ser altamente eficiente. 
*   **Almacenamiento Columnar:** A diferencia del CSV (que guarda datos fila por fila), Parquet guarda los datos por columnas. Esto lo hace ideal para consultas analíticas donde solo necesitamos leer ciertas columnas.
*   **Tipos de datos preservados:** Al guardar en Parquet, si una columna es `datetime` o `int`, al leerla seguirá siéndolo.
*   **Compresión:** Parquet comprime los datos de forma nativa, reduciendo drásticamente el espacio en disco.

```python
# Requiere instalar dependencias adicionales: pip install pyarrow fastparquet
df_limpio.to_parquet("transacciones_procesadas.parquet", engine="pyarrow")
```

---

## Comparación: CSV vs Parquet

Elegir el formato de salida correcto es una decisión fundamental en la ingeniería de datos. 

| Característica | CSV | Parquet |
| :--- | :--- | :--- |
| **Legibilidad** | Alta (Leíble por humanos y Excel) | Nula (Es un archivo binario) |
| **Estructura** | Orientado a filas | Orientado a columnas |
| **Tamaño en disco** | Grande (Texto plano) | Muy pequeño (Compresión nativa) |
| **Velocidad de lectura** | Lenta | Muy rápida |
| **Tipos de datos** | Se pierden (todo es texto al inicio) | Se preservan (esquema estricto) |
| **Caso de uso ideal** | Intercambio de datos simple, debugging | Pipelines de Big Data, Data Lakes, consultas analíticas |

---

## Persistencia de datos procesados

La **persistencia** es la acción de guardar el estado de los datos de forma permanente (en un disco, en la nube, o en una base de datos) para que sobrevivan a la finalización del script de Python.

### ¿Por qué persistir los datos?
1.  **Evitar el reprocesamiento:** Si nuestro script tarda 30 minutos en limpiar los datos, no queremos ejecutar la limpieza cada vez que necesitemos consultarlos.
2.  **Trazabilidad:** Nos permite auditar cómo estaban los datos en un punto específico del tiempo.
3.  **Desacoplamiento:** Quien limpia los datos no tiene por qué ser la misma persona o sistema que los visualiza.

---

## Importancia del almacenamiento en pipelines

En un pipeline de datos robusto, el almacenamiento no solo ocurre al final, sino también entre etapas. 

*   **Tolerancia a fallos:** Si un pipeline consta de 5 pasos y falla en el paso 4, tener los datos guardados al final del paso 3 nos permite reanudar desde ese punto sin empezar de cero.
*   **Manejo de estados:** En sistemas complejos, distinguimos claramente los datos *Raw* (crudos, tal cual llegaron) de los *Processed* (limpios y transformados).

Un pipeline bien diseñado trata al almacenamiento como su columna vertebral: es el medio de comunicación entre los distintos módulos.

---

## Versionado básico de datos (Sobrescritura vs Append)

Cuando diseñamos la fase de carga (Load), debemos decidir qué hacer si el archivo de destino ya existe. Tenemos dos enfoques principales:

### 1. Sobrescritura (Overwrite)
Se reemplaza el archivo viejo por uno nuevo. Es útil si procesamos siempre la totalidad de los datos (ej. un catálogo de clientes actual).
*   *Riesgo:* Si el nuevo procesamiento tiene un error, perdemos los datos anteriores.

### 2. Adición (Append)
Se agregan los registros nuevos al archivo o sistema existente. Ideal para datos históricos o transaccionales.
```python
# Ejemplo de append en CSV
df_nuevos_registros.to_csv("historico.csv", mode='a', header=False, index=False)
```
*   *Estrategia alternativa (Versionado por partición):* En lugar de hacer un *append* real, se guardan archivos con la fecha de procesamiento.
    *   Ejemplo: `ventas_20260427.parquet`

---

## Organización de datos procesados

El éxito de un ingeniero de datos radica no solo en el código, sino en cómo organiza los activos de datos. Una práctica común es estructurar los directorios (o buckets en la nube) en distintas "zonas" o "capas" (arquitectura tipo Medallón o Data Lake):

1.  **`/data/raw/`**: Datos crudos originales. **Nunca se modifican ni se sobrescriben.** Si algo sale mal, esta es tu copia de seguridad.
2.  **`/data/interim/`** *(Opcional)*: Datos en proceso de limpieza.
3.  **`/data/processed/`**: Datos limpios, normalizados y listos para su uso. Generalmente almacenados en Parquet.
4.  **`/data/output/`** *(o Reporting)*: Datos altamente agregados listos para un dashboard específico o envío a un cliente (a menudo en CSV).

---

## Integración del Flujo ETL Completo

Ahora unimos todas las piezas. Un mini script de ETL estructurado se ve de la siguiente manera:

```python
import pandas as pd
from datetime import datetime

def run_mini_etl():
    # 1. EXTRACT
    print("Extrayendo datos...")
    df = pd.read_csv("data/raw/transacciones.csv")
    
    # 2. TRANSFORM
    print("Transformando datos...")
    # Limpieza de nulos
    df['monto'] = df['monto'].fillna(0)
    # Generación de variables
    df['fecha_procesamiento'] = datetime.now().strftime("%Y-%m-%d")
    df = df[df['estado'] == 'COMPLETADO'] # Filtrado
    
    # 3. LOAD
    print("Cargando datos...")
    # Guardamos en formato eficiente
    df.to_parquet("data/processed/transacciones_limpias.parquet", engine="pyarrow")
```

---

```python
    
    print("¡Pipeline ETL ejecutado con éxito!")

if __name__ == "__main__":
    run_mini_etl()

```

---

## Preparación para consumo en siguientes etapas

El objetivo final de procesar y almacenar datos es que alguien, o algo, los **consuma**. Al dejar nuestros datos persistidos correctamente (en una carpeta de `/processed/` en formato CSV o Parquet), abrimos la puerta a las siguientes fases del curso:

1.  **Bases de Datos (SQL):** Podremos tomar este archivo limpio e insertarlo en una base de datos MySQL para que usuarios puedan hacer consultas estructuradas.
2.  **APIs (FastAPI):** Expondremos estos datos de forma programática para que aplicaciones web o móviles consulten el saldo o historial de un cliente.
3.  **Visualización (Streamlit):** Construiremos dashboards interactivos leyendo directamente los archivos procesados sin preocuparnos por lidiar con datos sucios o nulos en la capa de interfaz.

---

<!-- _class: code -->
## Practica: Guardar el DataFrame limpio en CSV y Parquet

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar guardado de datos (csv y parquet) con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap1/1_2_4_Script.py
"""
Este script demuestra el cierre de un flujo Mini ETL (Extract, Transform, Load).
Se aborda la persistencia de datos procesados, la exportación a formatos CSV y Parquet,
la comparación entre ambos y la organización básica de archivos.
"""

import pandas as pd
import numpy as np
import os

# Establecer semilla aleatoria solicitada
np.random.seed(987654)

# Crear directorios para organizar los datos procesados (ST8)
# Utilizar verbos neutros: Crear, Generar, Guardar
def crear_directorios():
    rutas = ['datos/crudos', 'datos/procesados']
    for ruta in rutas:

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap1/1_2_4_Script.ipynb)

---

## Errores comunes en el Bloque 1.2.4

- **Guardar con to_csv() sin index=False**
  → columna de índice no deseada en el archivo

- **No instalar pyarrow/fastparquet**
  → to_parquet() falla silenciosamente

- **Sobrescribir el archivo fuente original**
  → pérdida de datos crudos

---

## Resumen: Bloque 1.2.4

**Lo que aprendiste:**
- Guardar un DataFrame en CSV con to_csv() y controlar el índice
- Guardar en formato Parquet con to_parquet() para eficiencia
- Comparar tamaño y velocidad de lectura entre CSV y Parquet

**Lo que construiste:**
El script `1_2_4_Script.py` que guardar el dataframe limpio en csv y parquet usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 2.3.1: Fundamentos SQL (SELECT, WHERE)