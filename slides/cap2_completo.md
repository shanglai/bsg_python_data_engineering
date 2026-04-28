---
marp: true
theme: bsg
size: 16:9
paginate: true
footer: 'Python para Ingeniería de Datos · Capítulo 2: Almacenamiento y consultas de datos · BSG Institute'
---

---

<!-- _class: title -->
# Capítulo 2: Almacenamiento y consultas de datos
## SQL y MySQL

---

<!-- _class: section -->
# Sección 3: SQL y MySQL
## En esta sección construiremos la capa de sql y mysql del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de sql y mysql en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 2.3.1: Fundamentos SQL (SELECT, WHERE)
- Bloque 2.3.2: JOINs y agregaciones
- Bloque 2.3.3: Conexión Python → MySQL
- Bloque 2.3.4: Inserción y consulta del pipeline

---

<!-- ============================================================ -->
<!-- BLOQUE 2.3.1 — Fundamentos SQL (SELECT, WHERE)              -->
<!-- Scripts: scripts/cap2/2_3_1_Script.py                    -->
<!-- Notebook: notebooks/cap2/2_3_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 2.3.1
## Fundamentos SQL (SELECT, WHERE)

> Pasamos de archivos planos a bases de datos: SQL es el lenguaje universal para consultar datos.

**Al terminar este bloque podrás:**
- Entender la estructura de una tabla SQL (columnas, filas, tipos)
- Escribir consultas SELECT con WHERE para filtrar transacciones
- Distinguir PRIMARY KEY, tipos de datos SQL y el concepto de esquema

---

# Capítulo 2: Almacenamiento y consultas de datos, Sesión 3: SQL y MySQL, Bloque 1: Fundamentos SQL (SELECT, WHERE)

## Introducción a bases de datos relacionales

En nuestro pipeline de datos, no siempre basta con guardar información en archivos sueltos. Cuando el volumen crece o necesitamos buscar información específica rápidamente, entran en juego las **Bases de Datos Relacionales (RDBMS)**.

* **¿Qué son?** Son sistemas diseñados para almacenar y gestionar datos estructurados de manera organizada y eficiente, estableciendo relaciones lógicas entre ellos.
* **Paradigma Relacional:** Los datos se guardan de forma tabular (muy parecido a los DataFrames que vimos en Pandas).
* **Ejemplos populares:** MySQL, PostgreSQL, SQL Server, Oracle.

En la Ingeniería de Datos, las bases de datos relacionales son el pan de cada día: suelen ser la fuente principal (de donde extraemos los datos) o el destino final (donde guardamos los datos limpios para que sean consumidos).

## Concepto de tabla, fila y columna

El corazón de una base de datos relacional es la **Tabla**. Piénsala como una hoja de cálculo altamente estructurada.

* **Tabla:** Es la estructura principal que agrupa datos sobre una entidad específica (ej. `clientes`, `transacciones`, `productos`).
* **Columna (Atributo/Campo):** Define qué tipo de información guarda la tabla. Todas las entradas en una columna deben ser del mismo tipo de dato. Por ejemplo: `monto` (numérico), `fecha` (datetime).
* **Fila (Registro/Tupla):** Es una entrada individual en la tabla. Representa un caso único de la entidad. Por ejemplo, una transacción específica de $500 realizada por el cliente X el día de hoy.

| id_transaccion | id_cliente | monto | fecha | estado |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 105 | 250.50 | 2023-10-01 | completada |
| 2 | 108 | 15.00 | 2023-10-01 | fallida |

## Claves primarias y unicidad

¿Cómo nos aseguramos de no confundir dos transacciones que tienen el mismo monto y la misma fecha? Necesitamos un identificador único. Aquí entra el concepto de **Clave Primaria (Primary Key - PK)**.

* **Unicidad:** Una clave primaria es una columna (o conjunto de columnas) que identifica de manera *única* a cada fila en una tabla.
* **No nulos:** Una PK jamás puede estar vacía (NULL). Cada registro debe existir por sí mismo.
* **Ejemplo práctico:** En nuestra tabla de transacciones, `id_transaccion` es nuestra clave primaria. 

Mantener la unicidad es crucial en Ingeniería de Datos para evitar duplicados al momento de cargar datos a nuestro destino final (el "Load" del ETL).

## Concepto de esquema de base de datos

Un archivo CSV solo tiene un encabezado, pero una base de datos necesita reglas estrictas. Estas reglas conforman el **Esquema (Schema)**.

El esquema es el "plano arquitectónico" de nuestra base de datos. Define:
* El nombre de las tablas.
* Las columnas exactas de cada tabla.
* El tipo de dato permitido por cada columna (ej. `VARCHAR(50)`, `INT`, `DECIMAL(10,2)`).
* Las relaciones entre tablas (que veremos en los JOINs) y restricciones (como las claves primarias).

Un esquema bien diseñado previene que "basura" entre a nuestra base de datos. Si una columna está definida como `INT` e intentamos insertar el texto `"veinte"`, la base de datos rechazará la operación, protegiendo la integridad de la información.

## Introducción a SQL como lenguaje de consulta

**SQL (Structured Query Language)** es el lenguaje universal para comunicarnos con bases de datos relacionales. No importa si usas MySQL o PostgreSQL, la esencia de SQL es la misma.

* **Lenguaje declarativo:** A diferencia de Python donde le dices *cómo* hacer las cosas paso a paso (iterando), en SQL le dices a la base de datos *qué* resultados quieres, y el motor de la base de datos decide cómo buscarlo de la manera más eficiente.
* **Funciones de SQL en datos:** Nos permite realizar operaciones CRUD:
  * **C**reate (Insertar registros)
  * **R**ead (Consultar datos - ¡Nuestra prioridad de hoy!)
  * **U**pdate (Actualizar registros)
  * **D**elete (Borrar registros)

## Sintaxis básica de SELECT

La instrucción `SELECT` es la más utilizada en análisis e ingeniería de datos. Sirve para extraer información de la base de datos.

**Sintaxis general:**
```sql
SELECT columna1, columna2
FROM nombre_tabla;
```

**Ejemplos en nuestro caso de transacciones:**
```sql
-- Traer solo los montos y los estados de todas las transacciones
SELECT monto, estado 
FROM transacciones;

-- Traer TODAS las columnas (usando el asterisco *)
SELECT * 
FROM transacciones;
```
*Nota: En entornos productivos con millones de registros, evita usar `SELECT *` para no saturar la red y la memoria; selecciona solo las columnas que realmente necesitas.*

## Uso de WHERE para filtrado

Casi nunca necesitamos toda la tabla; generalmente buscamos un subconjunto específico de datos. La cláusula `WHERE` actúa como nuestro filtro lógico.

```sql
SELECT id_transaccion, id_cliente, monto
FROM transacciones
WHERE estado = 'completada';
```

Podemos combinar múltiples condiciones usando operadores lógicos (`AND`, `OR`, `NOT`) y de comparación (`=`, `>`, `<`, `>=`, `<=`, `!=`):

```sql
-- Buscar transacciones grandes y completadas
SELECT id_cliente, monto, fecha
FROM transacciones
WHERE estado = 'completada' AND monto > 1000.00;
```

## Comparación entre procesamiento en Python vs SQL

A este punto del curso podrías preguntarte: *¿Por qué filtrar en SQL si ya sé hacerlo en Pandas?*

| Característica | SQL (Base de datos) | Python (Pandas) |
| :--- | :--- | :--- |
| **Dónde ocurre** | En el servidor de base de datos | En la memoria RAM de tu computadora/servidor |
| **Velocidad de filtrado** | Extremadamente rápido (usa índices) | Rápido, pero limitado por la memoria RAM disponible |
| **Transformaciones complejas** | Posible, pero puede volverse ilegible | Excelente, lógica muy expresiva y testable |
| **Cuándo usarlo** | Para filtrar y reducir el volumen de datos *antes* de extraerlos | Para transformaciones de negocio complejas, machine learning o limpieza avanzada |

**Regla de oro del Data Engineer:** "Empuja" el filtrado y las operaciones sencillas lo más cerca posible de la base de datos (SQL), y usa Python para la transformación compleja del dataset ya reducido.

## Casos de uso de SQL en ingeniería de datos

SQL no es solo para "analistas que hacen reportes". Como Ingenieros de Datos, usamos SQL de manera intensiva para:

1. **Extracción (Ingesta):** Escribir queries eficientes para sacar el delta de datos (lo nuevo) de un sistema transaccional hacia nuestro pipeline.
2. **Validación de Calidad (Data Quality):** Contar nulos, buscar duplicados o validar que el total de ventas en la fuente coincida con el destino.
3. **Transformaciones in-database (dbt / ELT):** Cada vez es más común cargar los datos crudos al destino y usar SQL puro para transformarlos internamente, evitando mover los datos de un lado a otro.

## Importancia de consultas eficientes

En una tabla de 100 filas, cualquier consulta se ejecuta al instante. En el mundo de Big Data, una tabla transaccional puede tener miles de millones de filas.

* **El costo computacional:** Una consulta mal escrita puede consumir el 100% de la CPU del servidor, afectando a otros usuarios y a la aplicación principal (imagina botar el sistema de pagos del banco porque hiciste un `SELECT *` masivo).
* **Costos económicos:** En la nube (como BigQuery o Snowflake), te cobran por la cantidad de datos que procesas. Una mala consulta literal cuesta dinero real.
* **Tiempos del Pipeline:** Un ETL no puede demorar 10 horas si los datos se necesitan en tiempo real. Saber hacer filtros eficientes y elegir las columnas correctas es vital.

## Introducción a performance (Índices)

¿Cómo hace la base de datos para buscar una transacción específica entre 50 millones en milisegundos? Utiliza **Índices**.

* **Concepto básico:** Un índice en SQL funciona exactamente igual que el índice alfabético al final de un libro. En lugar de leer cada página (Full Table Scan) para encontrar la palabra "Python", vas al índice, buscas la "P", y te dice la página exacta.
* **Aplicación:** Si frecuentemente filtramos las transacciones por `id_cliente`, el administrador de la base de datos (o nosotros) crearemos un índice sobre esa columna.
* **El trade-off:** Los índices aceleran drásticamente el `SELECT` y el `WHERE`, pero hacen que los `INSERT` sean ligeramente más lentos (porque hay que actualizar el índice cada vez que entra un dato nuevo). Como ingenieros de datos, debemos encontrar ese balance.

---

<!-- _class: code -->
## Practica: Escribir consultas SELECT sobre la tabla de transacciones

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar fundamentos sql (select, where) con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap2/2_3_1_Script.py
"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 3: SQL y MySQL
Bloque 1: Fundamentos SQL (SELECT, WHERE)

Descripción: Script para demostrar los conceptos básicos de bases de datos
relacionales, creación de esquemas, y consultas fundamentales utilizando
SQL estándar. Para facilitar la ejecución sin configuración previa, 
utilizaremos SQLite (integrado en Python), cuyos conceptos son 
directamente aplicables a MySQL.
"""

import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

# Configurar semilla para reproducibilidad

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap2/2_3_1_Script.ipynb)

---

## Errores comunes en el Bloque 2.3.1

- **Usar comillas dobles en SQL donde se esperan simples**
  → error de sintaxis

- **Olvidar WHERE en un UPDATE/DELETE**
  → modifica toda la tabla

- **Confundir = (asignación en SQL) con == (comparación de Python)**

---

## Resumen: Bloque 2.3.1

**Lo que aprendiste:**
- Entender la estructura de una tabla SQL (columnas, filas, tipos)
- Escribir consultas SELECT con WHERE para filtrar transacciones
- Distinguir PRIMARY KEY, tipos de datos SQL y el concepto de esquema

**Lo que construiste:**
El script `2_3_1_Script.py` que escribir consultas select sobre la tabla de transacciones usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 2.3.2: JOINs y agregaciones

---

<!-- ============================================================ -->
<!-- BLOQUE 2.3.2 — JOINs y agregaciones                         -->
<!-- Scripts: scripts/cap2/2_3_2_Script.py                    -->
<!-- Notebook: notebooks/cap2/2_3_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 2.3.2
## JOINs y agregaciones

> Con las bases de SELECT, ahora combinamos tablas y calculamos métricas agregadas.

**Al terminar este bloque podrás:**
- Usar INNER JOIN para combinar la tabla de transacciones con la de clientes
- Aplicar COUNT, SUM, AVG con GROUP BY para obtener KPIs del negocio
- Filtrar grupos con HAVING (distinto de WHERE)

---

## ¿Qué es un JOIN y por qué es importante?

En un entorno real de ingeniería de datos, la información rara vez vive en una sola tabla. Por lo general, los sistemas dividen los datos para ser eficientes (normalización). 

Por ejemplo, los datos personales de nuestros usuarios viven en una tabla de `clientes`, mientras que sus compras viven en una tabla de `transacciones`.

**¿Qué hace un JOIN?**
* Es una operación de SQL que nos permite **combinar filas** de dos o más tablas basándose en una columna relacionada entre ellas (normalmente un ID).
* Nos ayuda a **reconstruir** la historia completa de los datos para su posterior análisis o transformación.
* Es el puente fundamental que establece la **relación entre tablas**.

---

## Tipos de JOIN: INNER vs. LEFT

Existen varias formas de cruzar tablas, pero en el 90% de los casos de ingeniería de datos usarás estas dos:

### INNER JOIN (La intersección)
* Devuelve **únicamente** los registros que tienen coincidencias en **ambas** tablas.
* Si un cliente no tiene transacciones, o una transacción no tiene un cliente válido asociado, ambos desaparecen del resultado.
* *Uso ideal:* Cuando necesitas información estricta y completa de ambos lados.

### LEFT JOIN (Prioridad a la izquierda)
* Devuelve **todos** los registros de la tabla de la izquierda (la primera que mencionas), y los registros coincidentes de la tabla de la derecha.
* Si no hay coincidencia, el resultado mostrará valores `NULL` del lado derecho.
* *Uso ideal:* Cuando quieres ver todas las transacciones, incluso si por error de sistema el cliente no existe en la base de datos.

---

## Integrando Datasets: Ejemplo Práctico

Imagina que tenemos nuestro dataset de transacciones y queremos enriquecerlo con el nombre del cliente.

**Nuestras tablas:**
1. `transacciones`: `id_transaccion`, `id_cliente`, `monto`, `fecha`
2. `clientes`: `id_cliente`, `nombre_completo`, `email`

**El Query SQL:**
```sql
SELECT 
    t.id_transaccion,
    t.fecha,
    c.nombre_completo,
    t.monto
FROM transacciones t
INNER JOIN clientes c 
    ON t.id_cliente = c.id_cliente;
```

*Nota: Usamos alias (`t` y `c`) para hacer el código más limpio y especificar de qué tabla viene cada columna.*

---

## Resumiendo datos: Funciones de Agregación y GROUP BY

Tener el dato a nivel de transacción es útil, pero el valor real para el negocio suele estar en los **resúmenes y métricas**. Aquí entran las funciones de agregación.

**Funciones principales:**
* `COUNT()`: Cuenta el número de filas (ej. ¿Cuántas transacciones hubo?).
* `SUM()`: Suma los valores numéricos de una columna (ej. Ingresos totales).
* `AVG()`: Calcula el promedio de una columna (ej. Ticket promedio).

**El poder del GROUP BY:**
Las funciones de agregación por sí solas te dan un único resultado total. El `GROUP BY` te permite calcular esas agregaciones **por categorías**.
Por ejemplo: *Ingresos totales* **por** *cliente*.

---

## Generación de Métricas y Lógica de Negocio

La combinación de `JOIN` y `GROUP BY` nos permite traducir datos crudos en respuestas concretas a preguntas de negocio. 

**Pregunta de Negocio:** *¿Cuáles son nuestros clientes que más ingresos generan y cuántas compras han hecho?*

```sql
SELECT 
    c.nombre_completo,
    COUNT(t.id_transaccion) AS numero_de_transacciones,
    SUM(t.monto) AS ingresos_totales,
    AVG(t.monto) AS ticket_promedio
FROM clientes c
LEFT JOIN transacciones t 
    ON c.id_cliente = t.id_cliente
GROUP BY 
    c.nombre_completo
ORDER BY 
    ingresos_totales DESC;
```

De esta forma, pasamos de simples registros en bases de datos a verdaderos indicadores de rendimiento (KPIs) listos para el consumo.

---

## Errores Comunes y Validación de Resultados

Realizar cruces y agregaciones parece sencillo, pero es donde ocurren la mayoría de los errores lógicos en la ingeniería de datos.

**1. Duplicación de filas (Efecto abanico)**
* Ocurre al hacer un JOIN con una tabla que tiene múltiples coincidencias imprevistas. 
* *Ejemplo:* Si la tabla clientes tuviera dos registros para el mismo `id_cliente`, ¡cada transacción de ese cliente se duplicaría en el resultado!

**2. Agregaciones Incorrectas**
* Sumar una columna sobre un dataset que ya sufrió duplicación inflará tus ingresos artificialmente.
* Olvidar colocar una columna no agregada dentro de la cláusula `GROUP BY` (SQL te arrojará un error, o peor, resultados inconsistentes dependiendo del motor).

**3. La regla de oro: Validación**
* Siempre realiza un `COUNT` de tu tabla principal antes del JOIN, y compara con el `COUNT` de la salida. 
* Si usaste un `LEFT JOIN`, el número de filas **debe ser exactamente el mismo** (asumiendo relación 1 a 1 o 1 a muchos desde la izquierda). Si tienes más filas, acabas de duplicar datos.

---

<!-- _class: code -->
## Practica: Calcular ventas por tienda con GROUP BY y JOIN

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar joins y agregaciones con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap2/2_3_2_Script.py
"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 3: SQL y MySQL
Bloque 2: JOINs y agregaciones

Descripción:
Este script ilustra los conceptos de combinación de tablas (JOINs) y funciones 
de agregación (GROUP BY, SUM, COUNT, AVG). Se utiliza SQLite como motor en memoria 
para demostrar la sintaxis estándar de SQL, preparando el terreno para la conexión 
a MySQL del siguiente bloque.

Subtemas cubiertos:
- ST1 a ST4: Concepto, tipos (INNER, LEFT) y ejemplo de JOINs.
- ST5 a ST7: Funciones de agregación y agrupaciones para métricas.
- ST8 a ST11: Errores comunes, problemas de agregación y validación de negocio.
"""

import sqlite3

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap2/2_3_2_Script.ipynb)

---

## Errores comunes en el Bloque 2.3.2

- **Confundir LEFT JOIN con INNER JOIN**
  → registros perdidos o duplicados

- **Usar WHERE para filtrar agregaciones en lugar de HAVING**
  → error SQL

- **Olvidar GROUP BY al usar funciones de agregación**
  → error en la consulta

---

## Resumen: Bloque 2.3.2

**Lo que aprendiste:**
- Usar INNER JOIN para combinar la tabla de transacciones con la de clientes
- Aplicar COUNT, SUM, AVG con GROUP BY para obtener KPIs del negocio
- Filtrar grupos con HAVING (distinto de WHERE)

**Lo que construiste:**
El script `2_3_2_Script.py` que calcular ventas por tienda con group by y join usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 2.3.3: Conexión Python → MySQL

---

<!-- ============================================================ -->
<!-- BLOQUE 2.3.3 — Conexión Python → MySQL                      -->
<!-- Scripts: scripts/cap2/2_3_3_Script.py                    -->
<!-- Notebook: notebooks/cap2/2_3_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 2.3.3
## Conexión Python → MySQL

> Ya sabemos SQL; ahora conectamos Python con MySQL para automatizar las consultas.

**Al terminar este bloque podrás:**
- Establecer una conexión a MySQL con mysql-connector-python
- Ejecutar consultas SELECT desde Python y obtener los resultados
- Cerrar la conexión correctamente y manejar errores de conexión

---

## Integración entre Python y bases de datos

En el ecosistema de la ingeniería de datos, rara vez trabajamos con sistemas aislados. La verdadera potencia se desata cuando conectamos nuestros lenguajes de programación (como Python) con nuestros sistemas de almacenamiento (como MySQL).

**¿Por qué integrar Python y SQL?**
* **Automatización:** Permite consultar y transformar datos programáticamente sin interacción humana manual.
* **Escalabilidad:** Podemos procesar lotes de datos estructurados directamente desde la base de datos hacia nuestro pipeline.
* **Flexibilidad:** Usamos SQL para lo que hace mejor (filtrar, agrupar, unir) y Python para lo que hace mejor (lógica compleja, machine learning, APIs).

Esta integración es el puente que convierte un script de análisis en un verdadero componente de un pipeline de datos.

---

## Introducción a librerías de conexión

Para que Python se comunique con MySQL, necesitamos un "driver" o librería que traduzca nuestras instrucciones al protocolo que la base de datos entiende. Existen dos enfoques principales:

### 1. Librerías nativas/drivers (`mysql-connector-python`, `PyMySQL`)
* Son directas y ligeras.
* Ejecutan SQL puro enviado como cadenas de texto.
* Ideales para scripts sencillos y para aprender cómo funciona la comunicación a bajo nivel.

### 2. ORMs y herramientas avanzadas (`SQLAlchemy`)
* Actúan como una capa de abstracción.
* Permiten interactuar con la base de datos utilizando objetos de Python en lugar de escribir SQL crudo (aunque también lo soportan).
* Manejan eficientemente conexiones múltiples (connection pooling) y son estándar en aplicaciones robustas.

En este curso, aprenderemos los conceptos con conectores directos por su simplicidad para ejecutar nuestras consultas.

---

## Configuración de la conexión

Para establecer una conexión exitosa, siempre necesitaremos las "credenciales" de nuestra base de datos. Estos parámetros son universales, sin importar la librería que usemos:

* **Host:** La dirección donde vive la base de datos (ej. `localhost` o `127.0.0.1` si es local).
* **Port:** El puerto de comunicación (el estándar en MySQL es `3306`).
* **User:** El nombre de usuario (ej. `root`).
* **Password:** La contraseña de acceso.
* **Database:** El nombre de la base de datos específica que queremos consultar.

**Ejemplo conceptual de conexión:**
```python
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password123",
    database="tienda_db"
)
```

---

## Ejecución de queries desde Python

Una vez que la conexión está abierta, necesitamos un canal para enviar nuestras consultas de SQL y recibir los resultados. Este canal se conoce como **Cursor**.

### El ciclo de vida de una consulta:
1. **Crear el cursor:** Se genera a partir de la conexión activa.
2. **Ejecutar (Execute):** Se envía la cadena de texto con la instrucción SQL.
3. **Recuperar (Fetch):** Se extraen los resultados hacia la memoria de Python.
4. **Cerrar:** Se cierra el cursor para liberar recursos.

```python
cursor = conexion.cursor()
query = "SELECT id_cliente, total FROM transacciones LIMIT 5;"
cursor.execute(query)
# Aquí la base de datos ya procesó la consulta, falta traer los datos.
```

---

## Lectura de resultados en estructuras de Python

El método `execute()` no nos devuelve los datos directamente; simplemente le dice a la base de datos que corra el comando. Para traer los datos a Python, usamos los métodos de extracción (`fetch`).

* `fetchone()`: Trae únicamente la primera fila (útil para validaciones o conteos únicos).
* `fetchall()`: Trae todas las filas resultantes de la consulta.

**¿Cómo se ven los datos en Python?**
Típicamente, el resultado de un `fetchall()` es una lista de tuplas, donde cada tupla representa una fila de la tabla:

```python
resultados = cursor.fetchall()

for fila in resultados:
    print(f"Cliente: {fila[0]}, Monto: {fila[1]}")
    
# Salida esperada:
# Cliente: 101, Monto: 250.50
# Cliente: 102, Monto: 100.00
```

---

## Conversión de resultados a DataFrames

Trabajar con listas de tuplas puede ser limitante si queremos hacer limpieza o transformaciones complejas. La mejor práctica en un pipeline moderno es convertir esos resultados directamente a un DataFrame de Pandas.

Pandas nos facilita la vida con métodos integrados como `read_sql()`, que manejan la conexión, la ejecución y la conversión de tipos automáticamente.

```python
import pandas as pd
from sqlalchemy import create_engine

# Creamos el motor de conexión
engine = create_engine("mysql+pymysql://root:password123@localhost:3306/tienda_db")

# Ejecutamos la consulta y la guardamos en un DataFrame
query = "SELECT * FROM transacciones WHERE estado = 'completado';"
df_transacciones = pd.read_sql(query, con=engine)

print(df_transacciones.head())
```
De esta forma, pasamos de datos crudos en la base a una estructura lista para análisis en solo un par de líneas.

---

## Manejo de errores de conexión

Las bases de datos son sistemas externos, y las conexiones pueden fallar por muchas razones (red caída, credenciales inválidas, base de datos apagada). Es vital que nuestro pipeline no "explote" de forma incontrolable.

Utilizamos bloques `try-except-finally` para capturar estos errores y asegurarnos de que la conexión se cierre correctamente, incluso si hay un fallo.

```python
import mysql.connector
from mysql.connector import Error

try:
    conexion = mysql.connector.connect(host="localhost", user="root", database="tienda")
    if conexion.is_connected():
        print("Conexión exitosa")
        
except Error as e:
    print(f"Error al conectar a MySQL: {e}")
    
finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("Conexión cerrada de forma segura")
```

---

## Concepto de capa de acceso a datos

En ingeniería de software y datos, no es buena idea mezclar todo el código en un solo archivo inmenso. Se introduce el patrón de diseño llamado **Data Access Layer (DAL)** o Capa de Acceso a Datos.

**¿Qué es?**
Es un módulo o sección de tu código cuya única responsabilidad es hablar con la base de datos. 

* El resto del pipeline no necesita saber si usas MySQL, PostgreSQL o un archivo plano.
* Solo llama a funciones como `obtener_transacciones()` o `guardar_cliente()`.
* Si en el futuro cambias de base de datos, solo actualizas esta capa, protegiendo el resto de tu pipeline.

---

## Buenas prácticas de separación de lógica

Siguiendo con la idea de la Capa de Acceso a Datos, nuestro código debería dividirse por responsabilidades.

**Ejemplo de lo que NO se debe hacer (código espagueti):**
Mezclar en la misma función la conexión a la base de datos, el cálculo matemático del promedio y la exportación a un CSV.

**Ejemplo de lo que SÍ se debe hacer (código modular):**
1. **Módulo de Configuración:** Guarda las credenciales (idealmente en variables de entorno).
2. **Módulo de Extracción (DAL):** Se conecta a MySQL y devuelve un DataFrame.
3. **Módulo de Transformación:** Recibe el DataFrame, limpia nulos y calcula métricas.
4. **Módulo de Carga:** Toma el DataFrame procesado y lo escribe en un nuevo archivo o tabla.

Esto facilita encontrar errores, realizar pruebas automáticas y trabajar en equipo.

---

## Introducción a seguridad: SQL Injection (Conceptual)

La Inyección SQL es una de las vulnerabilidades más antiguas y peligrosas al integrar aplicaciones con bases de datos.

**¿Cómo ocurre?**
Sucede cuando construimos consultas SQL concatenando directamente texto (strings) proveniente de variables externas o entradas de usuario.

```python
# PELIGROSO: Concatenación directa
id_ingresado = "105 OR 1=1" 
query = f"SELECT * FROM clientes WHERE id_cliente = {id_ingresado};"

# La base de datos evaluará:
# SELECT * FROM clientes WHERE id_cliente = 105 OR 1=1;
# Como 1=1 siempre es verdad, devolverá TODOS los clientes de la base de datos.
```
En un pipeline, si tomamos nombres de archivos o datos crudos sin validar y los concatenamos, corremos el riesgo de borrar tablas (`DROP TABLE`) o corromper información de manera accidental o maliciosa.

---

## Uso de parámetros en queries

La forma definitiva de evitar la inyección SQL (y además hacer que nuestro código maneje automáticamente caracteres extraños, comillas o fechas) es usar **Consultas Parametrizadas**.

En lugar de concatenar cadenas, colocamos un marcador (usualmente `%s` en los conectores de MySQL) y le pasamos los valores como una tupla separada. La librería se encarga de escapar y asegurar los datos antes de enviarlos.

```python
# FORMA SEGURA: Uso de parámetros
query_segura = "SELECT * FROM transacciones WHERE id_cliente = %s AND estado = %s;"

# Los valores se entregan en una tupla
valores = (105, "completado")

# El cursor une el query y los valores de forma segura en el backend
cursor.execute(query_segura, valores)
resultados = cursor.fetchall()
```
*Regla de oro en ingeniería de datos:* Nunca confíes en el origen de los datos al construir instrucciones SQL dinámicas. Usa siempre parámetros.

---

<!-- _class: code -->
## Practica: Conectar Python a MySQL y ejecutar consultas

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar conexión python → mysql con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap2/2_3_3_Script.py
"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 3: SQL y MySQL
Bloque 3: Conexión Python -> MySQL

Descripción:
Script para demostrar la conexión entre Python y una base de datos MySQL. 
Se incluyen ejemplos utilizando las librerías `mysql-connector-python` y `SQLAlchemy`.
Se abordan buenas prácticas como el manejo de errores, prevención de inyección SQL 
(uso de parámetros) y la conversión directa de resultados a DataFrames de Pandas 
para su uso en un pipeline de datos.

Requisitos previos (ejecutar en terminal):
> pip install mysql-connector-python sqlalchemy pandas

Nota: Se asume que existe un servidor MySQL en ejecución con una base de datos 
llamada 'curso_data_engineering' y una tabla 'transacciones'.
"""

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap2/2_3_3_Script.ipynb)

---

## Errores comunes en el Bloque 2.3.3

- **Dejar credenciales de BD en el código fuente**
  → riesgo de seguridad

- **No cerrar el cursor ni la conexión**
  → agotamiento del pool de conexiones

- **Olvidar commit() tras INSERT/UPDATE**
  → cambios no persisten en la BD

---

## Resumen: Bloque 2.3.3

**Lo que aprendiste:**
- Establecer una conexión a MySQL con mysql-connector-python
- Ejecutar consultas SELECT desde Python y obtener los resultados
- Cerrar la conexión correctamente y manejar errores de conexión

**Lo que construiste:**
El script `2_3_3_Script.py` que conectar python a mysql y ejecutar consultas usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 2.3.4: Inserción y consulta del pipeline

---

<!-- ============================================================ -->
<!-- BLOQUE 2.3.4 — Inserción y consulta del pipeline            -->
<!-- Scripts: scripts/cap2/2_3_4_Script.py                    -->
<!-- Notebook: notebooks/cap2/2_3_4_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 2.3.4
## Inserción y consulta del pipeline

> Con la conexión establecida, insertamos los datos del pipeline en la base de datos.

**Al terminar este bloque podrás:**
- Insertar múltiples filas con executemany() para eficiencia
- Leer datos de la BD con fetchall() y convertirlos a DataFrame
- Manejar duplicados con INSERT IGNORE o ON DUPLICATE KEY UPDATE

---

## Inserción de datos en MySQL (INSERT)

Una vez que hemos limpiado y transformado nuestros datos, el siguiente paso lógico es almacenarlos. En SQL, utilizamos el comando `INSERT` para agregar nuevos registros a una tabla existente.

La sintaxis básica es:

```sql
INSERT INTO nombre_tabla (columna1, columna2, columna3)
VALUES (valor1, valor2, valor3);
```

**Puntos clave:**
*   Las columnas listadas deben coincidir en orden y tipo de dato con los valores provistos.
*   En ingeniería de datos, rara vez insertamos fila por fila de forma manual; en su lugar, realizamos **inserciones masivas (bulk inserts)** que optimizan los tiempos de ejecución.

---

## Carga de datos desde Python

Para automatizar la carga de datos transformados desde Python hacia MySQL, usamos librerías como `mysql-connector` o el motor de `SQLAlchemy` en conjunto con Pandas.

Si utilizamos el método nativo de Pandas (`to_sql`), podemos cargar un DataFrame entero en cuestión de segundos:

```python
import pandas as pd
from sqlalchemy import create_engine

# Crear el motor de conexión
engine = create_engine("mysql+mysqlconnector://usuario:password@localhost/mi_base")

# Cargar el DataFrame 'df_limpio' a la tabla 'transacciones'
# if_exists='append' agrega las filas, 'replace' sobrescribe
df_limpio.to_sql(name='transacciones', con=engine, if_exists='append', index=False)
```

Este enfoque reduce drásticamente las líneas de código y asegura que los tipos de datos mapeen correctamente.

---

## Validación y consulta de datos persistidos

Insertar la información no es el paso final. Siempre debemos validar que los registros se hayan guardado como esperábamos mediante la **consulta de datos persistidos**.

Podemos hacer una consulta simple desde Python para leer los primeros registros de la base de datos y comprobar que la carga fue exitosa.

```python
# Validando que los datos existan en la tabla
query = "SELECT * FROM transacciones LIMIT 5"
df_validacion = pd.read_sql(query, con=engine)

print(df_validacion.head())
```

Consultar los datos inmediatamente después de la carga nos ayuda a confirmar que no hay columnas desplazadas ni pérdida de información.

---

## Integración del flujo ETL completo

Con la inserción de datos, cerramos formalmente el ciclo **ETL**:

1.  **Extract (Extracción):** Leemos los datos transaccionales desde un archivo CSV o fuente inicial.
2.  **Transform (Transformación):** Limpiamos valores nulos, ajustamos tipos de datos y generamos nuevas métricas usando Pandas.
3.  **Load (Carga):** Escribimos este conjunto resultante en nuestra base de datos relacional (MySQL).

El pipeline ahora no son solo scripts sueltos, sino un sistema secuencial donde la salida de la transformación es directamente la entrada del proceso de carga.

---

## Manejo de errores y consistencia de datos

Al interactuar con bases de datos, los errores son inevitables (caídas de red, llaves primarias duplicadas, tipos de datos incompatibles). 

*   **Manejo de excepciones:** Utiliza bloques `try/except` en Python para capturar problemas de conexión o ejecución sin que tu script colapse por completo.
*   **Consistencia de datos:** Para asegurar que la base de datos no quede en un estado corrupto (ej. se cargó la mitad de los datos y falló), se emplean **transacciones**. Si algo falla, se ejecuta un *rollback* para deshacer los cambios; si todo sale bien, se hace un *commit*.

```python
try:
    # Intento de carga de datos...
    df_limpio.to_sql(...)
    print("Carga exitosa.")
except Exception as e:
    print(f"Error durante la carga: {e}")
    # En un script nativo de BD aquí haríamos connection.rollback()
```

---

## Validación post-carga (conteo y métricas)

Una práctica fundamental en ingeniería de datos es realizar *sanity checks* (pruebas de cordura) tras una carga masiva de datos. No basta con saber que el código no falló; debemos saber que la lógica de negocio se mantuvo.

**Métricas comunes a validar:**
*   **Conteo de filas:** ¿Las filas cargadas en MySQL coinciden con las filas del DataFrame? (`SELECT COUNT(*) FROM transacciones;`)
*   **Sumatorias:** ¿El total de ingresos cuadra entre Pandas y MySQL? (`SELECT SUM(monto) FROM transacciones;`)

Si tu DataFrame tenía 10,000 registros y MySQL solo reporta 8,000, tienes un problema silencioso que debe ser investigado.

---

## Persistencia como base de consumo y preparación para APIs

El **almacenamiento estructurado** es el pilar que permite que el resto de la organización consuma los datos. Sin datos limpios guardados de forma confiable, los equipos de BI o Data Science no pueden trabajar.

**Importancia de este almacenamiento:**
1.  **Persistencia confiable:** MySQL actúa como la única fuente de la verdad para este pipeline.
2.  **Preparación para la exposición:** En etapas futuras, no leeremos archivos CSV crudos para alimentar nuestras aplicaciones. Crearemos una **API** que consulte directamente a esta base de datos MySQL para entregar métricas e información procesada en tiempo real a los usuarios finales.

---

<!-- _class: code -->
## Practica: Insertar el DataFrame de transacciones en MySQL

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar inserción y consulta del pipeline con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap2/2_3_4_Script.py
import pandas as pd
import random
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

# Configurar semilla para reproducibilidad
random.seed(987654)

# =============================================================================
# 1. EXTRAER (Extract)
# =============================================================================
def extraer_datos_transacciones():
    """
    Generar un DataFrame simulado de transacciones para el pipeline.
    Representa la ingesta de datos desde una fuente externa (CSV o API).
    """
    print("Iniciando extracción de datos...")

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap2/2_3_4_Script.ipynb)

---

## Errores comunes en el Bloque 2.3.4

- **Usar concatenación de strings en SQL**
  → riesgo de SQL injection

- **Olvidar commit()**
  → los datos no se guardan aunque el script termina sin error

- **No manejar IntegrityError**
  → el script falla si el registro ya existe

---

## Resumen: Bloque 2.3.4

**Lo que aprendiste:**
- Insertar múltiples filas con executemany() para eficiencia
- Leer datos de la BD con fetchall() y convertirlos a DataFrame
- Manejar duplicados con INSERT IGNORE o ON DUPLICATE KEY UPDATE

**Lo que construiste:**
El script `2_3_4_Script.py` que insertar el dataframe de transacciones en mysql usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 2.4.1: Integración CSV/API → transformación

---

<!-- _class: section -->
# Sección 4: Pipeline de datos v1
## En esta sección construiremos la capa de pipeline de datos v1 del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de pipeline de datos v1 en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 2.4.1: Integración CSV/API → transformación
- Bloque 2.4.2: Persistencia en MySQL y archivos
- Bloque 2.4.3: Modularización del pipeline
- Bloque 2.4.4: Ejecución completa del pipeline

---

<!-- ============================================================ -->
<!-- BLOQUE 2.4.1 — Integración CSV/API → transformación         -->
<!-- Scripts: scripts/cap2/2_4_1_Script.py                    -->
<!-- Notebook: notebooks/cap2/2_4_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 2.4.1
## Integración CSV/API → transformación

> Construimos la primera versión real del pipeline: extracción desde múltiples fuentes.

**Al terminar este bloque podrás:**
- Leer datos desde CSV y simular una llamada a una API externa
- Combinar y normalizar registros de fuentes distintas en un solo DataFrame
- Aplicar las transformaciones aprendidas en el capítulo 1

---

## Integración de fuentes de datos (CSV, API)

En el mundo real, los datos rara vez provienen de un solo lugar o en un único formato. Para construir un pipeline robusto, debemos ser capaces de unificar información de distintas fuentes.

* **Archivos estáticos (CSV):** Ideales para exportaciones históricas, registros de sistemas legados o datos compartidos internamente.
* **Servicios web (APIs):** Esenciales para obtener datos en tiempo real, interactuar con aplicaciones de terceros (ej. tipo de cambio actual, clima) o sistemas modernos.

El objetivo de esta integración es leer datos de ambas naturalezas y llevarlos a un formato común en Python (como un DataFrame de Pandas) para poder procesarlos de manera uniforme.

---

## El concepto de Ingesta de Datos

La **ingesta de datos** es la primera fase formal de cualquier pipeline. Consiste en el proceso de extraer y mover datos desde su lugar de origen hacia un entorno donde podamos procesarlos.

Existen diferentes formas de ingesta:
* **Batch (Por lotes):** Traer grandes volúmenes de datos de una vez (ej. un archivo CSV diario con todas las transacciones).
* **Streaming (En tiempo real):** Traer los datos evento por evento conforme ocurren.

En nuestro caso práctico, nos enfocaremos en la ingesta Batch, que es el estándar fundamental en la ingeniería de datos clásica, asegurando que extraemos la información de forma segura antes de alterarla.

---

## Lectura de múltiples fuentes en Python

Para manejar un flujo de datos moderno, nuestro código debe ser capaz de "hablar" con distintos orígenes. 

* **Para archivos CSV:** Utilizamos Pandas mediante `pd.read_csv()`, lo cual nos permite cargar gigabytes de datos en memoria estructurada rápidamente.
* **Para APIs:** Utilizamos la librería `requests` para hacer llamadas HTTP (ej. `requests.get()`) y extraer el JSON de respuesta. Luego, convertimos ese JSON a un DataFrame con `pd.DataFrame()`.

Al dominar ambas lecturas, nuestro script de Python se convierte en un puente que conecta el mundo exterior con nuestro motor de procesamiento.

---

## Preparación de datos para transformación

Una vez que los datos son ingeridos, rara vez están listos para aplicarse la lógica de negocio directamente. Existe una fase intermedia de "preparación".

En esta etapa buscamos:
* **Estandarizar estructuras:** Asegurarnos de que los nombres de las columnas coincidan si estamos uniendo un CSV con datos de una API.
* **Homologar formatos:** Resolver problemas de codificación de caracteres (el famoso *encoding* UTF-8 vs Latin-1).
* **Consolidar:** Unir las fuentes en una sola estructura manejable antes de iniciar la limpieza profunda.

---

## Manejo de errores en la ingesta

La regla de oro en la ingeniería de datos es: **los sistemas externos siempre pueden fallar**. 

Si intentamos leer un archivo que no existe o una API que está caída, nuestro pipeline entero colapsará si no estamos preparados.

* **Bloques `try / except`:** Son nuestra principal defensa. Nos permiten intentar (`try`) una lectura y, si falla (`except`), tomar una ruta alternativa, como registrar el error en lugar de detener todo el programa.
* **Timeouts en APIs:** Siempre debemos configurar un tiempo máximo de espera para no dejar nuestro pipeline congelado esperando una respuesta que nunca llegará.

---

## Validación inicial de datos

Antes de invertir tiempo y recursos computacionales en transformar los datos, debemos verificar si lo que trajimos tiene sentido. A esto le llamamos *Sanity Check* o validación inicial.

¿Qué debemos preguntarnos justo después de la ingesta?
* **¿Llegaron datos?** Verificar si el DataFrame está vacío (`df.empty`).
* **¿Están las columnas esperadas?** Validar que las llaves principales existan.
* **¿El volumen tiene sentido?** Si ayer procesamos 10,000 registros y hoy solo 5, podría haber un problema en la fuente.

Descartar datos inválidos desde el inicio evita errores en cadena (efecto dominó) más adelante.

---

## Flujo continuo vs Ejecución aislada

Hasta ahora, hemos escrito scripts individuales: uno para leer, otro para limpiar. Sin embargo, en la ingeniería de datos profesional, esto no es suficiente.

* **Ejecución aislada:** Correr un script manualmente, esperar a que termine, guardar un CSV y pasárselo a otro script. Es propenso a errores humanos y nada escalable.
* **Flujo continuo (Pipeline):** Un proceso automatizado donde la salida de la Fase A (Ingesta) es automáticamente la entrada de la Fase B (Transformación). El código orquesta el paso de los datos sin intervención manual.

El objetivo de esta sesión es migrar nuestra mentalidad de "scripts sueltos" a un "pipeline continuo".

---

## El Pipeline como un sistema integrado

Cuando pensamos en el pipeline como un sistema integrado, entendemos que sus partes son interdependientes. 

Si la API cambia el nombre de una variable (de `fecha_tx` a `fecha_transaccion`), esto impactará nuestra fase de transformación y, subsecuentemente, la base de datos. 

Por ello, un buen diseño de pipeline debe ser:
* **Trazable:** Si algo falla, sabemos exactamente en qué fase ocurrió.
* **Resiliente:** Un error en una fila no debe botar el procesamiento del resto del millón de filas.
* **Modular:** Si cambiamos la base de datos de destino, no deberíamos tener que reescribir la ingesta.

---

## Buenas prácticas de ingestión

Para asegurar que nuestra etapa de extracción sea de nivel profesional, debemos seguir estas reglas:

1. **Datos Crudos (Raw Data):** Nunca modifiques los datos directamente en la fuente. Extrae una copia exacta y guárdala tal cual llegó.
2. **Idempotencia:** Si corres el proceso de ingesta dos veces para el mismo día, el resultado debe ser el mismo, sin duplicar los datos en el sistema destino.
3. **Gestión de credenciales:** Nunca escribas contraseñas o *tokens* de APIs directamente en el código. Usa variables de entorno o archivos de configuración ocultos.

---

## Conexión entre Ingesta y Transformación

El punto de entrega entre la extracción (Extract) y la transformación (Transform) es un momento crítico en la memoria de nuestro entorno Python.

Una vez que pasamos la validación inicial, los datos dejan de verse como "archivos" o "respuestas web" y se convierten puramente en **estructuras de datos en memoria** (DataFrames).

Es aquí donde llamamos a nuestras funciones modulares de limpieza, pasándoles los datos crudos. Debemos tener cuidado con el uso de la memoria RAM: en pipelines muy masivos, debemos asegurarnos de no duplicar DataFrames innecesariamente durante este traspaso.

---

## Preparación para la persistencia

El último paso de nuestra integración actual es mirar hacia el futuro: la carga (Load). Todo lo que ingerimos y comenzamos a transformar necesita un destino final.

* **Conocer el esquema final:** Debemos transformar los datos teniendo en mente la base de datos MySQL o el formato Parquet que los recibirá. Si MySQL espera un entero (INT), no podemos dejar la columna como texto.
* **Diseño del destino:** Definir si vamos a sobrescribir los datos de ayer o si vamos a añadir las filas nuevas (Append vs Overwrite).

La correcta ingesta y transformación son solo el preludio para almacenar información que genere verdadero valor de negocio.

---

<!-- _class: code -->
## Practica: Extraer y combinar datos CSV + API simulada

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar integración csv/api → transformación con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap2/2_4_1_Script.py
"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 4: Pipeline de datos v1
Bloque 1: Integración CSV/API -> transformación

Descripción:
Se construye el primer flujo completo de datos integrando fuentes externas (CSV, API) 
con el procesamiento en Python. Se establece la ingesta con control de errores, 
validación y conexión hacia la etapa de transformación, demostrando un pipeline 
como un flujo continuo integrado.
"""

import pandas as pd
import requests
import numpy as np
import logging
import os

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap2/2_4_1_Script.ipynb)

---

## Errores comunes en el Bloque 2.4.1

- **No validar el esquema antes de unir fuentes**
  → columnas con nombres distintos

- **Ignorar duplicados al combinar fuentes**
  → inflación de métricas

- **No manejar errores de red al llamar una API**
  → el pipeline falla completamente

---

## Resumen: Bloque 2.4.1

**Lo que aprendiste:**
- Leer datos desde CSV y simular una llamada a una API externa
- Combinar y normalizar registros de fuentes distintas en un solo DataFrame
- Aplicar las transformaciones aprendidas en el capítulo 1

**Lo que construiste:**
El script `2_4_1_Script.py` que extraer y combinar datos csv + api simulada usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 2.4.2: Persistencia en MySQL y archivos

---

<!-- ============================================================ -->
<!-- BLOQUE 2.4.2 — Persistencia en MySQL y archivos             -->
<!-- Scripts: scripts/cap2/2_4_2_Script.py                    -->
<!-- Notebook: notebooks/cap2/2_4_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 2.4.2
## Persistencia en MySQL y archivos

> Con los datos ya transformados, los persistimos tanto en MySQL como en archivos locales.

**Al terminar este bloque podrás:**
- Guardar el DataFrame procesado en MySQL y en Parquet simultáneamente
- Implementar una estrategia de upsert para evitar duplicados
- Verificar la consistencia entre la BD y el archivo guardado

---

## Persistencia Dual: El poder de combinar mundos

En nuestro pipeline de datos, la **persistencia** se refiere a cómo y dónde guardamos la información una vez procesada. 

Adoptar una estrategia de **persistencia dual** significa guardar nuestros datos limpios y transformados tanto en una Base de Datos (ej. MySQL) como en archivos estructurados (ej. CSV o Parquet). 

**¿Por qué hacerlo?**
* **Resiliencia:** Si la base de datos se cae, tenemos un respaldo en archivos.
* **Flexibilidad:** Diferentes consumidores necesitan distintos formatos.
* **Desacoplamiento:** Separa el almacenamiento a largo plazo del acceso rápido para consultas.

---

## Ventajas de las Bases de Datos (MySQL)

Almacenar los resultados finales de nuestro pipeline en una base de datos relacional ofrece beneficios únicos enfocados en la disponibilidad y la estructura:

* **Consultas estructuradas:** Permite usar SQL para responder preguntas de negocio rápidamente (ej. *¿Cuáles fueron las ventas totales de ayer?*).
* **Concurrencia:** Múltiples usuarios o sistemas (como una API) pueden leer la información al mismo tiempo sin bloquearse.
* **Integridad de datos:** Las llaves primarias y restricciones evitan datos duplicados o relaciones huérfanas en nuestras transacciones.
* **Actualizaciones puntuales:** Es fácil actualizar un solo registro si el estado de una transacción cambia (ej. de "Pendiente" a "Completada").

---

## Ventajas de los Archivos Estructurados (CSV, Parquet)

Guardar el mismo dataset en un archivo (como un archivo `.parquet` en disco) brilla en escenarios donde la base de datos se queda corta:

* **Portabilidad:** Un archivo se puede enviar por correo, compartir en la nube o cargar en otra herramienta sin configurar conexiones de red.
* **Eficiencia en volumen:** Formatos como **Parquet** están comprimidos y optimizados para lectura masiva, ideal para algoritmos de Machine Learning.
* **Inmutabilidad:** Un archivo guardado es una "fotografía" exacta de los datos en ese momento, muy útil para auditorías.
* **Costo:** El almacenamiento en disco (local o en la nube) es significativamente más barato que mantener un servidor de base de datos encendido.

---

## Casos de uso: ¿Cuándo usar cuál?

Tener ambos formatos nos permite atender a diferentes "clientes" de nuestro pipeline:

### Base de Datos (MySQL)
* **Consumo transaccional:** Aplicaciones web o móviles que necesitan consultar un registro específico por ID.
* **Dashboards en vivo:** Herramientas de BI (Business Intelligence) que se conectan para mostrar los datos más recientes.

### Archivos Estructurados (Parquet/CSV)
* **Data Science:** Un científico de datos prefiere leer un archivo Parquet masivo con Pandas en segundos para entrenar un modelo.
* **Respaldo Histórico (Cold Storage):** Datos de transacciones de hace 5 años que ya no se consultan a diario, pero deben guardarse por regulaciones legales.

---

## Escritura de datos procesados

En Python, la escritura de los datos transformados al final de nuestro ETL es muy sencilla gracias a Pandas. Pasamos de tener un DataFrame en memoria a persistirlo físicamente.

```python
# Suponiendo que 'df_limpio' es nuestro dataset de transacciones ya procesado

# 1. Escritura a archivo (Parquet es recomendado por eficiencia)
df_limpio.to_parquet("output/transacciones_procesadas.parquet", index=False)

# 2. Escritura a Base de Datos (requiere conexión con SQLAlchemy)
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://usuario:password@localhost/tienda")

df_limpio.to_sql(name="transacciones", con=engine, if_exists="append", index=False)
```

Ambas líneas representan la **"L" (Load)** en nuestro proceso ETL.

---

## Manejo de resultados intermedios

Un pipeline robusto no solo guarda el resultado final, sino también **pasos intermedios**. 

Imagina un pipeline complejo que tarda 2 horas:
1. Extrae datos de una API externa.
2. Limpia formatos y cruza datos (tarda 1 hora).
3. Calcula métricas de machine learning.

Si el paso 3 falla, **no quieres volver a descargar y limpiar todo**. 
Guardar el DataFrame en un archivo temporal después del paso 2 (resultado intermedio) permite reanudar el pipeline desde ese punto, ahorrando tiempo y capacidad de cómputo.

---

## Versionado básico de datos

Cuando guardamos archivos a diario, no queremos sobreescribir el trabajo de ayer. El versionado básico implica agregar marcas de tiempo (*timestamps*) o fechas al nombre del archivo.

**Ejemplo de nomenclatura:**
* `transacciones_raw_2026-04-26.csv`
* `transacciones_raw_2026-04-27.csv`

```python
import datetime

fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
nombre_archivo = f"output/transacciones_{fecha_hoy}.parquet"

df_limpio.to_parquet(nombre_archivo, index=False)
```
Esto crea un historial inmutable y rastreable en nuestro sistema de archivos.

---

## Estrategias de almacenamiento: Append vs Overwrite

Al cargar datos en nuestro destino, debemos decidir cómo se integrarán con la información existente:

### Overwrite (Sobrescribir)
* **Qué hace:** Borra la tabla o archivo anterior y escribe los datos completos nuevamente.
* **Uso ideal:** Tablas de dimensiones pequeñas (ej. Catálogo de tiendas, Lista de empleados actualizados).

### Append (Añadir)
* **Qué hace:** Mantiene los datos existentes y agrega los nuevos registros al final.
* **Uso ideal:** Tablas de hechos (ej. Registros de ventas, Logs de transacciones diarias). Es la estrategia más común en pipelines incrementales.

---

## Trade-offs: Costo, Velocidad y Acceso

Toda decisión en Ingeniería de Datos implica un balance (*trade-off*).

| Característica | MySQL (Base de Datos) | Archivos (Parquet en Disco) |
| :--- | :--- | :--- |
| **Costo** | Alto (Requiere CPU/RAM dedicada) | Muy Bajo (Solo costo por GB de almacenamiento) |
| **Velocidad de Escritura** | Lenta (Por validación de constraints) | Muy Rápida (Escritura directa a disco) |
| **Acceso a 1 Registro** | Inmediato (usando índices) | Lento (Requiere leer o escanear el archivo) |
| **Acceso a Millones** | Moderado (Puede saturar el servidor) | Extremadamente rápido (Especialmente Parquet) |

Conocer esto nos permite diseñar pipelines que sean económicamente viables y técnicamente eficientes.

---

## Integración con el Pipeline

El pipeline deja de ser una serie de scripts sueltos y se convierte en un flujo unificado. En esta versión de nuestro ETL, el flujo se ve así:

1. **Ingesta:** Pandas lee `transacciones_raw.csv` o consume una API.
2. **Transformación:** Limpiamos nulos, estandarizamos tipos (ej. strings a *datetime*) y calculamos el total de venta.
3. **Persistencia en Archivo:** Se guarda un backup inmutable `transacciones_20260427.parquet`.
4. **Persistencia en MySQL:** Se hace un `append` en la tabla de la base de datos para que quede disponible.

El dato entra sucio y sale limpio, empaquetado y listo en dos formatos.

---

## Preparación para consumo posterior

Al finalizar este bloque, nuestro trabajo como Ingenieros de Datos ha generado un producto confiable. Los datos ya no están "secuestrados" en un archivo confuso, sino que están **democratizados**:

* Si el equipo de **Backend** necesita consultar las transacciones de un usuario, apuntarán a MySQL.
* Si el equipo de **Analytics** necesita crear un dashboard de ingresos mensuales, conectarán su herramienta a la base de datos o leerán los archivos Parquet.

En las siguientes sesiones, daremos el paso final: construir una **API** para exponer estos datos y automatizar todo el proceso.

---

<!-- _class: code -->
## Practica: Persistir datos limpios en MySQL y Parquet

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar persistencia en mysql y archivos con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap2/2_4_2_Script.py
"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 4: Pipeline de datos v1
Bloque 2: Persistencia en MySQL y archivos

Descripción: Script para implementar la persistencia dual del pipeline. 
Se aborda la escritura de datos procesados (resultados intermedios y finales) 
tanto en archivos estructurados (CSV, Parquet) como en bases de datos (MySQL),
comparando estrategias de 'append' vs 'overwrite'.
"""

# Importar librerías necesarias
import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap2/2_4_2_Script.ipynb)

---

## Errores comunes en el Bloque 2.4.2

- **No controlar el encoding al escribir CSV**
  → caracteres rotos en Windows

- **Olvidar el índice al guardar**
  → columna extra en el próximo ciclo de lectura

- **No verificar el row_count tras el INSERT**
  → no detectar inserciones fallidas

---

## Resumen: Bloque 2.4.2

**Lo que aprendiste:**
- Guardar el DataFrame procesado en MySQL y en Parquet simultáneamente
- Implementar una estrategia de upsert para evitar duplicados
- Verificar la consistencia entre la BD y el archivo guardado

**Lo que construiste:**
El script `2_4_2_Script.py` que persistir datos limpios en mysql y parquet usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 2.4.3: Modularización del pipeline

---

<!-- ============================================================ -->
<!-- BLOQUE 2.4.3 — Modularización del pipeline                  -->
<!-- Scripts: scripts/cap2/2_4_3_Script.py                    -->
<!-- Notebook: notebooks/cap2/2_4_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 2.4.3
## Modularización del pipeline

> Un pipeline que funciona una vez es bueno; uno modular que se puede mantener es profesional.

**Al terminar este bloque podrás:**
- Separar el código en funciones con responsabilidad única (extract, transform, load)
- Crear un módulo Python reutilizable importable desde otros scripts
- Documentar cada función con docstrings claros

---

## Modularización de código

**¿Qué es la modularización?**
En ingeniería de datos, es común empezar escribiendo un script largo ("monolito") que hace todo: lee, limpia, transforma y guarda. A medida que el proyecto crece, este enfoque se vuelve insostenible.

La **modularización** consiste en dividir ese código monolítico en bloques más pequeños, lógicos y manejables llamados módulos. En Python, un módulo es simplemente un archivo `.py` que contiene funciones, clases y variables relacionadas.

**Ventajas iniciales:**
*   **Lectura más fácil:** Entender 50 líneas de código es más sencillo que entender 500.
*   **Aislamiento de errores:** Si la lectura falla, sabes exactamente en qué archivo buscar.

---

## Separación de responsabilidades

Un principio clave en la ingeniería de software y datos es la **Separación de Responsabilidades** (Separation of Concerns). Cada módulo debe tener un único propósito claro.

En nuestro pipeline de datos, dividiremos las responsabilidades en tres pilares:
1.  **Ingesta (Extract):** Código dedicado única y exclusivamente a conectarse a las fuentes de datos (CSV, APIs, Bases de datos) y extraer la información cruda.
2.  **Transformación (Transform):** Código que recibe datos, aplica reglas de negocio, limpia nulos, filtra y estructura. No le importa de dónde vienen los datos ni a dónde van.
3.  **Almacenamiento (Load / Storage):** Código responsable de tomar un DataFrame o estructura final y persistirlo (guardar en MySQL, exportar a Parquet/CSV).

---

## Organización de carpetas en proyectos de datos

Un proyecto de datos profesional no puede tener todos los archivos sueltos en una sola carpeta. Requiere una estructura jerárquica clara.

**Ejemplo de estructura básica:**
```text
mi_proyecto_pipeline/
|-- data/
|   |-- raw/          # Datos crudos originales (no se modifican)
|   |-- processed/    # Datos limpios y transformados
|-- src/              # Código fuente (nuestros módulos)
|   |-- ingesta.py
|   |-- transformacion.py
|   |-- almacenamiento.py
|   |-- db_config.py
|-- main.py           # Script principal que orquesta el pipeline
|-- requirements.txt  # Dependencias del proyecto
```

Mantener los datos separados del código fuente es una regla de oro en la ingeniería de datos.

---

## Reutilización de código y evitar duplicación (DRY)

El principio **DRY** (*Don't Repeat Yourself* - No te repitas) es fundamental al modularizar.

Si tienes que limpiar valores nulos de la misma manera en tres datasets distintos, no copies y pegues el código tres veces. 

**Enfoque modular:**
*   Escribe una función general en un módulo de utilidades (ej. `limpiar_nulos(df, columnas)`).
*   Importa esta función en todos los scripts que la necesiten.

**Impacto:** Si mañana la regla de negocio para limpiar nulos cambia, solo actualizas el código en un lugar, no en tres.

---

## Estructuración de scripts

¿Cómo interactúan nuestros módulos entre sí? Necesitamos un "director de orquesta".

Aquí es donde entra el script `main.py` (o `run.py`). Su trabajo no es procesar datos, sino **coordinar las funciones** importadas de los otros módulos.

**Ejemplo conceptual de un main.py:**
```python
from src.ingesta import leer_csv
from src.transformacion import limpiar_datos, calcular_metricas
from src.almacenamiento import guardar_en_mysql

def ejecutar_pipeline():
    # 1. Ingesta
    df_crudo = leer_csv('data/raw/transacciones.csv')
    
    # 2. Transformación
    df_limpio = limpiar_datos(df_crudo)
    df_final = calcular_metricas(df_limpio)
    
    # 3. Almacenamiento
    guardar_en_mysql(df_final, 'tabla_transacciones')

if __name__ == "__main__":
    ejecutar_pipeline()
```

---

## Introducción a la arquitectura de proyectos

La estructura de carpetas y módulos que acabamos de ver es la base de la **Arquitectura de Software** aplicada a datos.

Una buena arquitectura define:
*   **Flujo de información:** Cómo viajan los datos (Ingesta >> Transformación >> Almacenamiento).
*   **Dependencias:** Quién llama a quién. El `main.py` depende de los submódulos, pero los submódulos (idealmente) no dependen entre sí.
*   **Configuraciones:** Parámetros como credenciales de base de datos o rutas de archivos deben aislarse en archivos de configuración, no escribirse directamente en el código ("hardcoding").

---

## Beneficios de modularidad y Mantenibilidad del código

La verdadera ganancia de la modularidad se nota meses después de haber escrito el código:

*   **Mantenibilidad:** Si hay un cambio en la base de datos (por ejemplo, migramos de MySQL a PostgreSQL), solo tocamos el módulo `almacenamiento.py`. El resto del pipeline ni se entera.
*   **Trabajo en equipo:** Dos ingenieros de datos pueden trabajar en el mismo proyecto al mismo tiempo. Uno mejora la ingesta y el otro la transformación, sin causar conflictos en el mismo archivo.
*   **Testing (Pruebas):** Es mucho más fácil probar automáticamente una función pequeña que un script gigante de mil líneas.

---

## Escalabilidad del pipeline

Un código modular está preparado para crecer.

*   **¿Qué pasa si agregamos una nueva fuente de datos (ej. una API)?**
    Simplemente creamos un archivo `api_ingesta.py` y lo conectamos a nuestro módulo de transformación existente.
*   **¿Qué pasa si los datos crecen masivamente?**
    Podemos reemplazar la lógica interna de `transformacion.py` por una herramienta más robusta (como Spark o Polars) sin cambiar la estructura general del pipeline.

La modularidad nos permite cambiar piezas del motor sin tener que construir un auto nuevo.

---

## Preparación para la automatización

La modularidad no es solo por orden, es un **requisito indispensable** para el futuro del curso.

En las siguientes secciones y capítulos, querremos que este pipeline se ejecute automáticamente todos los días a las 3:00 AM usando herramientas como Cron o Apache Airflow.

Estas herramientas de orquestación esperan ejecutar comandos limpios (como `python main.py`) o importar funciones específicas como "Tareas". Un script monolítico y desordenado es casi imposible de automatizar de forma segura y confiable. 

¡Modularizar hoy es garantizar la automatización de mañana!

---

<!-- _class: code -->
## Practica: Refactorizar el pipeline en módulos ETL

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar modularización del pipeline con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap2/2_4_3_Script.py
import os
import pandas as pd
import numpy as np

def generar_estructura_directorios(base_path="proyecto_pipeline"):
    """
    Generar la estructura de carpetas necesaria para un proyecto modular.
    Separa el código fuente (src) de los datos (data).
    """
    directorios = [
        f"{base_path}/data/raw",         # Datos crudos, inmutables
        f"{base_path}/data/processed",   # Datos limpios y procesados
        f"{base_path}/src"               # Código fuente modularizado
    ]
    
    print("-> Generando estructura de directorios...")
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap2/2_4_3_Script.ipynb)

---

## Errores comunes en el Bloque 2.4.3

- **Crear funciones con demasiados parámetros**
  → difícil de llamar y testear

- **Mezclar la lógica de negocio con el manejo de archivos en la misma función**

- **Usar variables globales en lugar de parámetros**
  → comportamiento impredecible

---

## Resumen: Bloque 2.4.3

**Lo que aprendiste:**
- Separar el código en funciones con responsabilidad única (extract, transform, load)
- Crear un módulo Python reutilizable importable desde otros scripts
- Documentar cada función con docstrings claros

**Lo que construiste:**
El script `2_4_3_Script.py` que refactorizar el pipeline en módulos etl usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 2.4.4: Ejecución completa del pipeline

---

<!-- ============================================================ -->
<!-- BLOQUE 2.4.4 — Ejecución completa del pipeline              -->
<!-- Scripts: scripts/cap2/2_4_4_Script.py                    -->
<!-- Notebook: notebooks/cap2/2_4_4_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 2.4.4
## Ejecución completa del pipeline

> Integramos todo: el pipeline completo extrae, transforma y carga en una sola ejecución.

**Al terminar este bloque podrás:**
- Orquestar las funciones ETL en un script principal que corre de inicio a fin
- Añadir logging básico para registrar el estado de cada etapa
- Verificar la ejecución completa con una consulta de validación final

---

### Ejecución End-to-End (E2E)

Una vez que hemos construido los módulos de ingesta, transformación y almacenamiento, ha llegado el momento de unirlos. La **ejecución end-to-end (extremo a extremo)** significa correr todo el proceso desde el inicio hasta el fin sin intervención manual entre los pasos.

* **El objetivo:** Verificar que los datos fluyan correctamente a través de todo el sistema.
* **El escenario:** Ejecutamos un script principal (`main.py`) que orquesta las funciones modulares que construimos previamente.
* **El flujo real:** 
  1. Lectura del archivo CSV o API externa.
  2. Limpieza y generación de nuevas métricas.
  3. Guardado en formato Parquet local y carga simultánea en la base de datos MySQL.

---

### Integración Completa: El flujo continuo

El pipeline deja de ser un conjunto de scripts aislados y se convierte en un **sistema integrado**.

* **Acoplamiento de módulos:** La salida del módulo de ingesta (un DataFrame crudo) se convierte en la entrada estricta del módulo de transformación. A su vez, la salida de la transformación (un DataFrame limpio) es la entrada del módulo de almacenamiento.
* **Gestión de memoria:** En un flujo continuo, los datos viajan por la memoria RAM de nuestra máquina. Es vital asegurar que las transformaciones sean eficientes para que el proceso completo no colapse cuando manejamos grandes volúmenes de datos.
* **Ventaja principal:** Evitamos la fricción de tener que ejecutar tres programas distintos, reduciendo el error humano.

---

### Validación de Resultados

Una vez que el pipeline finaliza, no basta con ver que el script terminó sin errores (código de salida 0). Necesitamos validar que los datos resultantes tienen sentido.

* **Consistencia de datos:** ¿Coincide el número de registros ingresados con los guardados? (Considerando los que eliminamos intencionalmente durante la limpieza).
* **Verificación cruzada:** Consultar la base de datos MySQL y comparar contra el archivo Parquet recién creado.
* **Integridad referencial:** Validar que no se hayan generado campos nulos donde no deberían existir.

---

### Sanity Checks (Pruebas de Cordura)

Los *Sanity Checks* son validaciones rápidas, lógicas y matemáticas que nos dicen si los datos procesados son razonables.

**Ejemplos en Python o SQL post-carga:**
* **Conteo total (Count):** Si mi archivo original tenía 10,000 transacciones y eliminé 50 nulas, mi base de datos debe tener exactamente 9,950 registros.
* **Métricas agregadas:** La suma total de ventas en el archivo original debe ser muy similar o idéntica a la suma total en MySQL (`SELECT SUM(monto) FROM transacciones`).
* **Límites de negocio:** Verificar que no existan fechas de transacciones en el futuro o montos de venta negativos si el negocio no lo permite.

---

### Manejo de Errores en Ejecución Completa

Cuando un pipeline corre de principio a fin, las posibilidades de fallo se multiplican. ¿Qué pasa si la base de datos se desconecta justo en el último paso?

* **Punto de fallo único:** Si no controlamos los errores (con `try/except`), un fallo en el almacenamiento destruye el progreso de la transformación.
* **Identificación del problema:** Usamos mensajes claros en nuestras excepciones para saber **dónde** falló el pipeline (ej. "Error en módulo de ingesta: Archivo no encontrado" vs "Error en base de datos: Credenciales inválidas").
* **Rollback conceptual:** Si el proceso de carga a MySQL falla a la mitad, ¿se quedan los datos a medias? En sistemas maduros, buscamos revertir los cambios para no dejar bases de datos inconsistentes.

---

### Identificación de Fallos

Detectar el origen de un error rápidamente es una habilidad esencial en Ingeniería de Datos.

1. **Revisión de Tracebacks:** Leer el error de Python de abajo hacia arriba. A menudo, el error final (ej. `TypeError`) fue provocado por una falla más arriba (ej. la API devolvió un JSON vacío).
2. **Uso de prints estratégicos:** Mientras desarrollamos, imprimir mensajes como ">> Iniciando limpieza de datos" o ">> 500 registros procesados" ayuda a ubicar exactamente en qué paso se detuvo el código.
3. **Aislamiento del problema:** Si el pipeline completo falla, prueba los módulos por separado para identificar al culpable.

---

### El Pipeline Reproducible

Un principio fundamental de la ingeniería de datos moderna es la **reproducibilidad**.

* **Mismos datos, mismos resultados:** Si ejecutas el pipeline hoy con un archivo "ventas_enero.csv", y lo vuelves a ejecutar mañana con el mismo archivo, el resultado final debe ser idéntico.
* **Entornos controlados:** Para que sea verdaderamente reproducible, el código no puede depender de configuraciones ocultas en "tu computadora". Todo (rutas de carpetas, credenciales, librerías) debe estar explícito o parametrizado.
* **Idempotencia (Concepto clave):** Una operación es idempotente si correrla una o múltiples veces produce exactamente el mismo estado en la base de datos (por ejemplo, usando `INSERT IGNORE` o actualizando registros en lugar de duplicarlos).

---

### Documentación Básica del Flujo

El código no se explica solo. Un buen pipeline incluye documentación para que otros ingenieros (o tu "yo" del futuro) entiendan el flujo.

* **Docstrings:** Comentar qué hace cada función, qué recibe y qué retorna.
* **README.md:** Un archivo de texto en la raíz del proyecto que explique:
  * Propósito del pipeline.
  * Requisitos (librerías necesarias, versión de Python).
  * Instrucciones para ejecutarlo (`python main.py`).
  * Estructura de carpetas (`/data/raw`, `/data/processed`).

---

### Análisis de Resultados y Pipeline Funcional

Llegamos a la meta de esta primera gran fase: tenemos un **Pipeline Funcional**.

* **¿Qué lo hace funcional?** No solo mueve datos, sino que automatiza un proceso que antes requería intervención manual, aporta valor transformando datos crudos en información útil y los deja listos para su consumo.
* **Análisis del ciclo completo:** Hemos cubierto la extracción, la transformación y la carga (ETL). Observar cómo los datos "cobran vida" desde un CSV desordenado hasta una tabla limpia en SQL es el núcleo del Data Engineering.

---

### Siguientes pasos: Preparación para Automatización y APIs

Nuestro pipeline v1 está listo, pero actualmente tenemos que ejecutarlo manualmente dando clic o escribiendo comandos en la terminal. Además, los datos están atrapados en la base de datos o en archivos locales.

**¿Hacia dónde vamos en las siguientes sesiones?**
1. **Exposición (APIs y Dashboards):** Usaremos FastAPI y Streamlit para que otros usuarios o sistemas puedan consultar nuestros datos limpios en tiempo real.
2. **Entornos Aislados (Docker):** Empaquetaremos nuestro pipeline para que no haya problemas de compatibilidad en otras máquinas.
3. **Automatización y Orquestación:** Haremos que el pipeline se ejecute solo a las 3:00 AM todos los días usando herramientas como Cronjobs y Apache Airflow.

---

<!-- _class: code -->
## Practica: Ejecutar el pipeline ETL completo end-to-end

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar ejecución completa del pipeline con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap2/2_4_4_Script.py
"""
Capítulo 2: Almacenamiento y consultas de datos
Sección 4: Pipeline de datos v1
Bloque 4: Ejecución completa del pipeline

Descripción: Script para ejecutar el pipeline de datos end-to-end.
Incluye ingesta, transformación, almacenamiento dual (MySQL y CSV/Parquet)
y validación de resultados (sanity checks).
"""

import os
import logging
import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error

# ==========================================

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap2/2_4_4_Script.ipynb)

---

## Errores comunes en el Bloque 2.4.4

- **No registrar errores en un log**
  → imposible diagnosticar fallas en producción

- **No manejar el caso en que la fuente de datos no está disponible**

- **Hardcodear rutas de archivos**
  → el pipeline falla en otro entorno

---

## Resumen: Bloque 2.4.4

**Lo que aprendiste:**
- Orquestar las funciones ETL en un script principal que corre de inicio a fin
- Añadir logging básico para registrar el estado de cada etapa
- Verificar la ejecución completa con una consulta de validación final

**Lo que construiste:**
El script `2_4_4_Script.py` que ejecutar el pipeline etl completo end-to-end usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 3.5.1: Introducción a APIs y FastAPI