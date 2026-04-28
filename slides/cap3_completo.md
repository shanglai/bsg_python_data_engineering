---
marp: true
theme: bsg
size: 16:9
paginate: true
footer: 'Python para Ingeniería de Datos · Capítulo 3: Exposición y consumo de datos · BSG Institute'
---

---

<!-- _class: title -->
# Capítulo 3: Exposición y consumo de datos
## APIs con FastAPI

---

<!-- _class: section -->
# Sección 5: APIs con FastAPI
## En esta sección construiremos la capa de apis con fastapi del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de apis con fastapi en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 3.5.1: Introducción a APIs y FastAPI
- Bloque 3.5.2: Endpoints básicos
- Bloque 3.5.3: Conexión API → base de datos
- Bloque 3.5.4: Filtros y validaciones

---

<!-- ============================================================ -->
<!-- BLOQUE 3.5.1 — Introducción a APIs y FastAPI                -->
<!-- Scripts: scripts/cap3/3_5_1_Script.py                    -->
<!-- Notebook: notebooks/cap3/3_5_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 3.5.1
## Introducción a APIs y FastAPI

> El pipeline ya procesa datos; ahora los exponemos al mundo a través de una API.

**Al terminar este bloque podrás:**
- Entender qué es una API REST y sus verbos HTTP (GET, POST, PUT, DELETE)
- Instalar FastAPI y Uvicorn y crear el primer servidor en ejecución
- Distinguir entre endpoint, request y response

---

## ¿Qué es un API?

**Application Programming Interface (Interfaz de Programación de Aplicaciones)**

Un API es un conjunto de reglas y definiciones que permite que distintas aplicaciones de software se comuniquen entre sí.

En términos sencillos:
- Imagina que vas a un restaurante. Tú (el cliente) quieres comida, pero no vas directamente a la cocina a prepararla.
- Le pides lo que deseas al **mesero** (el API).
- El mesero lleva tu pedido a la cocina (el sistema/base de datos), la cocina prepara la orden y el mesero te trae tu plato de vuelta.

En ingeniería de datos, un API permite que otros usuarios o sistemas accedan a los datos que hemos procesado sin darles acceso directo a nuestras bases de datos o código interno.

---

## APIs como interfaz entre sistemas

Las APIs actúan como una capa de abstracción. Ocultan la complejidad del sistema interno y exponen solo lo necesario de forma segura y estructurada.

**Ejemplos de comunicación:**
- **Frontend >> Backend:** Una página web de un banco pide el saldo de un cliente al servidor.
- **Script >> Servicio Cloud:** Tu código en Python envía un archivo CSV a un servicio de machine learning externo para obtener predicciones.
- **Sistema A >> Sistema B:** Nuestro pipeline de datos procesa transacciones y otro equipo de la empresa utiliza nuestra API para generar reportes automatizados.

Esta interfaz garantiza que ambas partes puedan cambiar su tecnología interna (por ejemplo, cambiar de MySQL a PostgreSQL) sin romper la comunicación, siempre y cuando respeten las reglas del API.

---

## Protocolo HTTP (Request / Response)

La mayoría de las APIs web funcionan sobre el protocolo **HTTP** (Hypertext Transfer Protocol), el mismo que usan los navegadores web.

La comunicación HTTP se basa en un ciclo muy sencillo:
1. **Request (Petición):** El cliente hace una solicitud al servidor. Incluye la dirección a la que quiere ir y qué quiere hacer.
2. **Response (Respuesta):** El servidor procesa la petición y devuelve un resultado junto con un código de estado (ej. 200 OK, 404 No Encontrado).

**Estructura de un Request:**
- URL (A dónde voy)
- Método (Qué quiero hacer)
- Headers (Metadatos, credenciales)
- Body (Datos enviados, opcional)

---

## Métodos HTTP (GET, POST, PUT, DELETE)

El protocolo HTTP define verbos o métodos que indican la intención de la petición. Estos se alinean directamente con las operaciones CRUD (Create, Read, Update, Delete) en bases de datos.

- **GET (Leer):** Solicita datos del servidor. *Ej: Obtener la lista de las últimas transacciones.* No modifica datos.
- **POST (Crear):** Envía datos nuevos al servidor para crear un registro. *Ej: Enviar una nueva transacción al sistema.*
- **PUT (Actualizar):** Modifica o reemplaza un registro existente completo. *Ej: Actualizar los datos de un cliente.*
- **DELETE (Borrar):** Elimina un recurso del servidor. *Ej: Borrar una transacción duplicada.*

En nuestro caso de exposición de datos, el método **GET** será el más utilizado.

---

## Concepto de Endpoint

Un **Endpoint** es la dirección URL específica donde un API recibe peticiones para un recurso particular. 

Si el API es una central telefónica, los endpoints son las extensiones.

**Ejemplo aplicado a nuestro pipeline:**
- URL Base: `https://api.miempresa.com/v1`
- Endpoint de clientes: `/clientes` >> `GET https://api.miempresa.com/v1/clientes`
- Endpoint de transacciones: `/transacciones` >> `GET https://api.miempresa.com/v1/transacciones`

Cada endpoint está asociado a uno o más métodos HTTP (puedes tener un `GET /transacciones` y un `POST /transacciones`).

---

## Formato JSON como estándar de intercambio

Para que los sistemas se entiendan, deben hablar un "idioma" común. El estándar absoluto hoy en día para APIs web es **JSON** (JavaScript Object Notation).

**¿Por qué JSON?**
- Es ligero, basado en texto plano.
- Es fácil de leer para humanos y rápido de procesar para las máquinas.
- Se mapea perfectamente con los diccionarios de Python.

**Ejemplo de una transacción en JSON:**
```json
{
  "id_transaccion": "TXN-987654",
  "fecha": "2023-10-25",
  "monto": 1500.50,
  "moneda": "MXN",
  "status": "completada"
}
```

---

## El rol de las APIs en Pipelines de Datos

Hasta ahora, nuestro pipeline extrajo datos, los limpió, los transformó y los guardó en una base de datos MySQL o en un archivo Parquet. 

**¿Qué sigue?**
Los datos no tienen valor si no se utilizan. El API es la puerta de salida.

**Flujo Completo:**
Ingesta (CSV) >> Transformación (Pandas) >> Almacenamiento (MySQL) >> **Exposición (API)** >> Consumo (Dashboards, Analistas, Otros Sistemas).

El API permite que un analista consulte las "transacciones de alto valor de hoy" sin tener que saber SQL, instalar librerías de bases de datos o tener credenciales del servidor.

---

## Introducción a FastAPI

Para construir nuestra API utilizaremos **FastAPI**, un framework moderno y de alto rendimiento para construir APIs en Python.

**¿Qué es un framework web?**
Es un conjunto de herramientas y librerías que nos ahorran escribir desde cero todo el código necesario para manejar conexiones HTTP, validaciones y rutas.

A diferencia de frameworks más antiguos como Flask o Django, FastAPI fue diseñado específicamente para la creación de APIs (como su nombre indica) aprovechando las características modernas de Python.

---

## Ventajas de FastAPI

Elegimos FastAPI para este curso por tres razones fundamentales:

1. **Velocidad:** Es uno de los frameworks de Python más rápidos disponibles, comparable con NodeJS o Go, gracias a que es asíncrono por diseño.
2. **Tipado estricto (Pydantic):** Utiliza los *type hints* de Python. Si declaras que un monto debe ser un `float`, FastAPI validará automáticamente que el usuario no envíe un texto, devolviendo un error claro si lo hace.
3. **Documentación automática:** Al escribir el código, FastAPI genera automáticamente una interfaz visual (Swagger UI) donde cualquier persona puede leer cómo usar tu API y probarla desde el navegador.

---

## APIs como productos de datos (Data as a Product)

En la ingeniería de datos moderna, existe el concepto de tratar los datos como un producto.

Esto significa que nuestro trabajo no termina simplemente dejando un archivo en una carpeta. Debemos pensar en el usuario final. 

Una API bien diseñada, rápida y documentada es un **Producto de Datos**.
- Tiene consumidores (clientes internos o externos).
- Tiene un nivel de calidad esperado (uptime, tiempos de respuesta).
- Resuelve un problema de negocio (ej. "Necesito acceso en tiempo real a las transacciones limpias").

---

## Concepto de contrato (Entrada / Salida)

Al diseñar un API, establecemos un **contrato** con quienes la van a consumir.

Un contrato de API es una promesa explícita:
- **Entrada requerida:** "Si quieres consultar transacciones por fecha, debes enviarme un parámetro llamado `fecha_inicio` en formato `YYYY-MM-DD`."
- **Salida garantizada:** "A cambio, prometo devolverte una lista en JSON con los campos `id_transaccion`, `monto` y `cliente`."

Si nosotros, como ingenieros de datos, cambiamos la estructura de la base de datos subyacente, **el contrato del API no debe romperse**. El consumidor del API debe seguir enviando lo mismo y recibiendo lo mismo. Esta es la base de un pipeline robusto y escalable.

---

<!-- _class: code -->
## Practica: Crear y lanzar el primer servidor FastAPI

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar introducción a apis y fastapi con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap3/3_5_1_Script.py
import random
from fastapi import FastAPI
from pydantic import BaseModel

# Fijar semilla aleatoria para garantizar reproducibilidad en datos simulados
random.seed(987654)

# =============================================================================
# ST1 a ST7: Conceptos de API, HTTP, Endpoints y JSON
# Una API (Application Programming Interface) actúa como un puente entre 
# sistemas. Utiliza el protocolo HTTP mediante un modelo de Petición/Respuesta.
# Los datos viajan comúnmente en formato JSON, el estándar en pipelines modernos.
# =============================================================================

# ST8 y ST9: Introducción a FastAPI y sus ventajas
# FastAPI es un framework moderno, rápido y basado en tipado estático.
# Generar la instancia principal de la aplicación:
app = FastAPI(

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap3/3_5_1_Script.ipynb)

---

## Errores comunes en el Bloque 3.5.1

- **Confundir puerto ocupado con error de código**
  → revisar qué proceso usa el puerto

- **No usar async def en FastAPI**
  → pérdida de rendimiento en producción

- **Olvidar el parámetro 'reload=True' en desarrollo**
  → cambios no se reflejan

---

## Resumen: Bloque 3.5.1

**Lo que aprendiste:**
- Entender qué es una API REST y sus verbos HTTP (GET, POST, PUT, DELETE)
- Instalar FastAPI y Uvicorn y crear el primer servidor en ejecución
- Distinguir entre endpoint, request y response

**Lo que construiste:**
El script `3_5_1_Script.py` que crear y lanzar el primer servidor fastapi usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 3.5.2: Endpoints básicos

---

<!-- ============================================================ -->
<!-- BLOQUE 3.5.2 — Endpoints básicos                            -->
<!-- Scripts: scripts/cap3/3_5_2_Script.py                    -->
<!-- Notebook: notebooks/cap3/3_5_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 3.5.2
## Endpoints básicos

> Con el servidor en marcha, definimos los primeros endpoints que devuelven datos reales.

**Al terminar este bloque podrás:**
- Crear endpoints GET que devuelven JSON con datos del pipeline
- Usar parámetros de ruta ({id}) y de consulta (?status=) en los endpoints
- Documentar la API automáticamente con Swagger UI en /docs

---

## Definición de endpoints básicos en FastAPI

Un **endpoint** es un punto de acceso específico en una API, definido por una URL y un método HTTP (como GET, POST, PUT, DELETE). Es la puerta mediante la cual un cliente solicita o envía información a nuestro sistema.

En **FastAPI**, definir un endpoint es sumamente intuitivo y se apoya directamente en la sintaxis nativa de Python. 

* **Operación de ruta (Path Operation):** Es la combinación del path (URL) y el método HTTP.
* **Función de ruta:** Es la función en Python que se ejecuta cuando la API recibe una petición en ese endpoint específico.

FastAPI se encarga de conectar la petición web con nuestra función, ejecutar la lógica de negocio y devolver la respuesta al cliente.

---

## Creación de rutas (Path operations)

Para crear una ruta en FastAPI, utilizamos **decoradores** que envuelven nuestras funciones. El decorador indica a la aplicación qué URL y qué método HTTP deben activar la función.

```python
from fastapi import FastAPI

app = FastAPI()

# Decorador que define la ruta y el método (GET)
@app.get("/estado")
def obtener_estado():
    return {"status": "El pipeline de datos está funcionando correctamente"}
```

**Anatomía de la ruta:**
1. `@app`: Referencia a la instancia de nuestra API.
2. `.get(...)`: El método HTTP que estamos habilitando.
3. `"/estado"`: El path o URL relativa.
4. `def obtener_estado():`: La lógica que procesa nuestra aplicación de datos.

---

## Parámetros de entrada simples

Las APIs necesitan ser dinámicas, lo que logramos enviando parámetros. FastAPI maneja dos tipos principales de forma automática basándose en la firma de la función:

**1. Parámetros de Ruta (Path Parameters):**
Van incrustados directamente en la URL. Útiles para identificar recursos específicos.
```python
@app.get("/transacciones/{tx_id}")
def obtener_transaccion(tx_id: int):
    return {"transaccion_id": tx_id, "monto": 150.50}
```

**2. Parámetros de Consulta (Query Parameters):**
Van al final de la URL después de un `?`, separados por `&`. Útiles para filtrar o paginar datos.
```python
# Ejemplo de llamada: /transacciones?limite=10
@app.get("/transacciones/")
def listar_transacciones(limite: int = 5):
    return {"mensaje": f"Devolviendo las últimas {limite} transacciones"}
```

---

## Retorno de datos en JSON y Serialización

**JSON (JavaScript Object Notation)** es el estándar de oro para el intercambio de datos en la web debido a su ligereza y legibilidad.

**Serialización** es el proceso de convertir objetos complejos de Python (como diccionarios, listas o modelos de datos) a un formato de texto (JSON) que pueda ser enviado por la red.

* En frameworks antiguos, la serialización debía hacerse manualmente.
* **En FastAPI, la serialización es automática.**

```python
@app.get("/resumen")
def obtener_resumen():
    # Python dict
    datos_pipeline = {
        "total_filas": 10500,
        "nulos_removidos": 23,
        "columnas": ["id", "fecha", "monto"]
    }
    # FastAPI lo convierte a JSON automáticamente
    return datos_pipeline 
```

---

## Estructura básica de una aplicación FastAPI

Para que un script de FastAPI funcione correctamente y esté listo para escalar en nuestro proyecto de ingeniería de datos, requiere una estructura mínima:

1. **Importación de dependencias:** Traer `FastAPI` (y herramientas de tipado si es necesario).
2. **Instanciación:** Crear el objeto `app = FastAPI()`.
3. **Definición de rutas:** Escribir los endpoints mediante decoradores (`@app.get()`).
4. **Ejecución (Servidor ASGI):** Usar un servidor como `uvicorn` para correr la app.

```python
# main.py
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="API del Pipeline de Datos")

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la API de datos"}

if __name__ == "__main__":
    # Ejecución local: python main.py
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

## Pruebas de endpoints y Documentación automática

Una de las grandes ventajas de FastAPI es la generación de **documentación interactiva y automática** basada en el estándar OpenAPI. No necesitas escribir documentación manual para tus endpoints.

Una vez que tu servidor está corriendo (ej. en `localhost:8000`), puedes acceder a:

* **Swagger UI (`/docs`):** Interfaz gráfica que permite ver todos los endpoints, sus parámetros esperados, y lo más importante: **ejecutarlos y probarlos** directamente desde el navegador.
* **ReDoc (`/redoc`):** Un formato de documentación alternativo, ideal para entregar especificaciones claras a otros equipos que vayan a consumir tu API.

Esto acelera enormemente el ciclo de desarrollo en ingeniería de datos, permitiendo a los analistas saber exactamente qué datos están disponibles.

---

## Uso de datos estáticos vs dinámicos

Al construir una API, solemos pasar por dos fases de madurez en nuestros endpoints:

**1. Datos Estáticos (Mocking):**
Durante el prototipado, devolvemos diccionarios o listas "hardcodeadas" (escritas a mano en el código).
* *Uso:* Validar la estructura del JSON, probar el contrato de la API sin depender de que el pipeline haya terminado.

**2. Datos Dinámicos (Integración real):**
El endpoint lee la información directamente de la salida de nuestro pipeline (por ejemplo, cargando un archivo Parquet con Pandas o consultando la base de datos MySQL).
* *Uso:* Producción. Los datos cambian automáticamente conforme el pipeline de ingeniería procesa nueva información.

---

## Buenas prácticas y Organización inicial del código API

A medida que el pipeline y la API crecen, un solo archivo `main.py` se vuelve insostenible. Se deben aplicar buenas prácticas de organización:

* **Nomenclatura RESTful:** Usa sustantivos en plural para las rutas (`/clientes` en lugar de `/obtener_clientes`).
* **Separación de responsabilidades:** 
  * Un archivo o módulo para las rutas (`routers/`).
  * Un archivo para la lógica de lectura de datos.
  * Un archivo principal `main.py` limpio que solo inicialice la app e importe los routers.
* **Tipado estricto:** Aprovecha las anotaciones de tipo de Python (`int`, `str`, `List`) en los parámetros. FastAPI los usará para validar las entradas automáticamente y rechazar peticiones mal formadas.

---

<!-- _class: code -->
## Practica: Crear endpoints GET para listar y filtrar transacciones

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar endpoints básicos con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap3/3_5_2_Script.py
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any

# 1. Generar la instancia principal de la aplicación FastAPI.
# Esta variable 'app' es el componente central que Uvicorn utilizará 
# para levantar el servidor y mapear las rutas.
app = FastAPI(
    title="API de Transacciones Básica",
    description="API inicial para exponer datos estructurados de un pipeline de datos.",
    version="1.0.0"
)

# =============================================================================
# Datos estáticos (Simulación de la salida del pipeline)
# =============================================================================
# Hacer una pequeña base de datos en memoria utilizando diccionarios.
# En bloques posteriores, esto será sustituido por la conexión a MySQL o archivos.

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap3/3_5_2_Script.ipynb)

---

## Errores comunes en el Bloque 3.5.2

- **Retornar un objeto no serializable por defecto**
  → ValidationError de FastAPI

- **Olvidar el tipo de retorno en la firma de la función**
  → sin validación automática

- **Confundir path parameter con query parameter**
  → error 422 en el cliente

---

## Resumen: Bloque 3.5.2

**Lo que aprendiste:**
- Crear endpoints GET que devuelven JSON con datos del pipeline
- Usar parámetros de ruta ({id}) y de consulta (?status=) en los endpoints
- Documentar la API automáticamente con Swagger UI en /docs

**Lo que construiste:**
El script `3_5_2_Script.py` que crear endpoints get para listar y filtrar transacciones usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 3.5.3: Conexión API → base de datos

---

<!-- ============================================================ -->
<!-- BLOQUE 3.5.3 — Conexión API → base de datos                 -->
<!-- Scripts: scripts/cap3/3_5_3_Script.py                    -->
<!-- Notebook: notebooks/cap3/3_5_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 3.5.3
## Conexión API → base de datos

> Los endpoints ya funcionan; ahora los conectamos a la base de datos real del pipeline.

**Al terminar este bloque podrás:**
- Integrar mysql-connector con FastAPI para leer datos desde MySQL
- Manejar el ciclo de vida de la conexión a BD por request
- Devolver datos de la BD como respuesta JSON estructurada

---

## Conexión de la API con la base de datos

Hasta ahora, hemos construido endpoints en FastAPI que devuelven datos estáticos o simulados ("hardcodeados"). El siguiente paso lógico en nuestro pipeline es **conectar la API a la base de datos MySQL** que alimentamos en la etapa de carga (Load).

### ¿Por qué es necesario?
* **Datos centralizados:** La API debe consumir la misma "fuente de la verdad" que genera nuestro pipeline de ingeniería de datos.
* **Persistencia real:** Los datos expuestos ya no se pierden al reiniciar la aplicación web.
* **Integración del ciclo de vida:** Permite que sistemas externos (dashboards, aplicaciones móviles, analistas) consuman los datos transformados y limpios sin acceder directamente a la infraestructura de base de datos.

---

## Ejecución de queries desde la API

Para interactuar con la base de datos desde FastAPI, utilizaremos las mismas librerías de conexión que aplicamos en nuestro pipeline (por ejemplo, `mysql-connector-python` o `SQLAlchemy`). 

### Mecánica de una consulta en la API
1. El cliente hace una petición HTTP (ej. `GET /transacciones`).
2. El endpoint recibe la petición.
3. Se abre un cursor hacia la base de datos.
4. Se ejecuta una sentencia SQL (`SELECT * FROM transacciones_limpias`).
5. Se procesan los resultados y se devuelven al cliente.

El uso de SQL tradicional (SELECT, WHERE, LIMIT) nos permite delegar el filtrado y cálculo a la base de datos, optimizando los recursos de la API.

---

## Recuperación de resultados dinámicos

La principal ventaja de conectar nuestra API a MySQL es la capacidad de ofrecer **resultados dinámicos**. 

* **Datos actualizados:** Si el pipeline automatizado inserta nuevos registros a las 3:00 AM, la API reflejará esos datos inmediatamente a las 3:01 AM sin necesidad de reiniciar o modificar código.
* **Filtros en tiempo real:** Los usuarios pueden solicitar parámetros específicos en el endpoint (ej. ventas de la última semana), y la API traducirá esto dinámicamente en consultas SQL adaptadas al momento.

Dejamos atrás los diccionarios estáticos en memoria para dar paso a un sistema vivo que reacciona al estado actual del almacenamiento.

---

## Conversión de resultados a JSON

Las bases de datos relacionales devuelven resultados en forma de filas y columnas (generalmente tuplas en Python). Sin embargo, el estándar de comunicación de las APIs modernas es **JSON**.

### Proceso de serialización
Para que FastAPI devuelva correctamente la información, debemos transformar las tuplas de MySQL en diccionarios de Python.

* **El problema:** `cursor.fetchall()` suele devolver `[(1, 'Cliente A', 150.5), (2, 'Cliente B', 99.0)]`.
* **La solución:** Mapear estos valores a sus nombres de columna, resultando en `[{"id": 1, "cliente": "Cliente A", "monto": 150.5}, ...]`.
* **FastAPI:** Una vez que tenemos una lista de diccionarios, FastAPI la convierte automáticamente a un string JSON válido y agrega las cabeceras HTTP necesarias.

---

## Concepto de Capa de Acceso a Datos (DAL)

Escribir código SQL directamente dentro de las funciones de nuestros endpoints (las rutas) es una mala práctica. Aquí introducimos la **Capa de Acceso a Datos** (DAL, por sus siglas en inglés: Data Access Layer).

### ¿Qué es la DAL?
Es un módulo o archivo específico (por ejemplo, `database.py` o `crud.py`) cuya única responsabilidad es interactuar con la base de datos.

* Contiene las funciones que ejecutan los `INSERT`, `SELECT`, `UPDATE` y `DELETE`.
* Oculta los detalles técnicos (cursores, sentencias SQL exactas) al resto de la aplicación.
* Si mañana cambiamos MySQL por PostgreSQL, solo modificamos la DAL; los endpoints de la API se mantienen intactos.

---

## Separación entre lógica de negocio y acceso a DB

Derivado del uso de la DAL, establecemos un principio fundamental en la ingeniería de software y datos: **la separación de responsabilidades**.

### Estructura recomendada
1. **Controlador (Rutas/Endpoints):** Su único trabajo es recibir la petición HTTP, validar los parámetros de entrada y devolver la respuesta. No sabe nada de SQL.
2. **Lógica de negocio:** Funciones intermedias que aplican reglas (ej. calcular un descuento o verificar permisos).
3. **Capa de acceso (DAL):** Habla con MySQL. Solo recibe instrucciones como "dame el cliente 5" y devuelve un diccionario.

Mantener esto separado hace que el código de la API sea testeable, mantenible y mucho más fácil de leer.

---

## Performance básica en consultas

Cuando la API comienza a recibir múltiples peticiones, las consultas ineficientes pueden colapsar el sistema. 

### Reglas básicas de performance para APIs:
* **Evitar el `SELECT *`:** Solicitar únicamente las columnas que la API va a devolver al usuario (ej. `SELECT id, monto, fecha FROM transacciones`). Reducimos el uso de memoria y red.
* **Paginación:** Nunca devolver toda la tabla de golpe. Usar siempre `LIMIT` y `OFFSET` en SQL para entregar los datos en bloques pequeños (ej. 100 registros por página).
* **Uso de Índices:** Asegurarse de que las columnas usadas frecuentemente para filtrar (ej. `fecha`, `cliente_id`) estén indexadas en la base de datos.

---

## Manejo de conexiones

Abrir y cerrar una conexión a la base de datos es una operación "costosa" en términos de tiempo y recursos. En el contexto de una API que recibe cientos de peticiones, debemos manejar las conexiones con cuidado.

### Buenas prácticas
* **Cierre seguro:** Utilizar bloques `try...finally` o context managers (`with`) para garantizar que el cursor y la conexión se cierren, incluso si ocurre un error en la API.
* **Evitar conexiones fantasma:** Una conexión que se queda abierta sin cerrarse consumirá los límites de conexión de MySQL, provocando que la API deje de responder (Timeouts).
* **Pool de conexiones (Avanzado):** En lugar de abrir y cerrar conexiones, se mantiene un "grupo" (pool) de conexiones vivas que los endpoints toman prestadas y devuelven al terminar.

---

## Integración API + Pipeline

En esta etapa, logramos conectar el inicio y el final de nuestra arquitectura de datos.

### El flujo de vida del dato (End-to-End)
1. **Ingesta:** Un script de Python lee el CSV original (o API externa).
2. **Transformación:** Pandas limpia nulos, convierte tipos y calcula métricas (Mini ETL).
3. **Almacenamiento (Persistencia):** Los datos limpios se insertan en MySQL.
4. **Exposición:** Nuestra aplicación FastAPI se conecta a MySQL.
5. **Consumo:** Un cliente web o dashboard consulta los endpoints de FastAPI para graficar la información.

La API actúa como la "vitrina" de todo el esfuerzo de ingeniería de datos que hay detrás.

---

## Uso de DataFrames en APIs

Aunque lo común es trabajar con listas de diccionarios, **Pandas** también puede integrarse dentro de FastAPI si es necesario realizar transformaciones analíticas complejas antes de devolver el JSON.

### ¿Cómo funciona?
1. Usamos `pd.read_sql(query, conexion)` para cargar los datos desde MySQL directamente a un DataFrame.
2. Realizamos agrupaciones o cálculos de último minuto.
3. Convertimos el DataFrame a diccionario: `df.to_dict(orient="records")`.
4. Devolvemos el diccionario con FastAPI.

*Precaución:* Los DataFrames consumen mucha memoria. Este enfoque es útil para endpoints analíticos (métricas o resúmenes), pero no se recomienda para endpoints de alto tráfico transaccional.

---

## Preparación para escalabilidad

Nuestra API funcional está lista, pero a medida que el volumen de datos o de usuarios crezca, la implementación actual enfrentará cuellos de botella. 

### Conceptos a futuro
* **Consultas Asíncronas (Async):** Usar drivers asíncronos (como `aiomysql` o `SQLAlchemy Async`) para que la API pueda atender a otros usuarios mientras espera que la base de datos responda.
* **Caché:** Si un endpoint devuelve el resumen mensual y este no cambia a lo largo del día, podemos guardar la respuesta temporalmente (caché) para no consultar MySQL en cada petición.
* **Balanceo de carga:** Tener múltiples copias de la API corriendo en paralelo. 

La correcta separación de la Capa de Acceso a Datos (DAL) que implementamos hoy es lo que nos permitirá aplicar estas mejoras en el futuro sin reescribir todo el sistema.

---

<!-- _class: code -->
## Practica: Conectar FastAPI a MySQL y devolver transacciones

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar conexión api → base de datos con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap3/3_5_3_Script.py
"""
Capítulo 3: Exposición y consumo de datos
Sección 5: APIs con FastAPI
Bloque 3: Conexión API -> base de datos

Descripción:
Script para integrar una API construida con FastAPI a una base de datos MySQL.
Se implementa la capa de acceso a datos, ejecución de consultas dinámicas,
separación de responsabilidades y el uso de Pandas para retornar JSON.
"""

import uvicorn
from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error
import pandas as pd

# ==========================================

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap3/3_5_3_Script.ipynb)

---

## Errores comunes en el Bloque 3.5.3

- **Abrir una conexión nueva por cada request**
  → agotamiento del pool de conexiones

- **No manejar el caso en que la BD no responde**
  → el endpoint cuelga sin timeout

- **Serializar directamente objetos de la BD**
  → TypeError por tipos no serializables

---

## Resumen: Bloque 3.5.3

**Lo que aprendiste:**
- Integrar mysql-connector con FastAPI para leer datos desde MySQL
- Manejar el ciclo de vida de la conexión a BD por request
- Devolver datos de la BD como respuesta JSON estructurada

**Lo que construiste:**
El script `3_5_3_Script.py` que conectar fastapi a mysql y devolver transacciones usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 3.5.4: Filtros y validaciones

---

<!-- ============================================================ -->
<!-- BLOQUE 3.5.4 — Filtros y validaciones                       -->
<!-- Scripts: scripts/cap3/3_5_4_Script.py                    -->
<!-- Notebook: notebooks/cap3/3_5_4_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 3.5.4
## Filtros y validaciones

> Con la API funcional, añadimos validaciones y filtros para hacerla robusta y usable.

**Al terminar este bloque podrás:**
- Usar Pydantic para validar los datos de entrada en endpoints POST
- Implementar filtros por fecha, monto y status en los endpoints GET
- Devolver códigos de error HTTP apropiados (404, 422, 500)

---

## Haciendo nuestra API útil y flexible

Hasta ahora, nuestra API puede devolver datos completos o responder a consultas muy directas. Sin embargo, en un entorno real, los consumidores de la API (como un dashboard, una aplicación móvil u otro sistema) rara vez necesitan **todos** los datos de golpe. 

Para que una API sea verdaderamente útil, necesitamos darle la capacidad de **filtrar** y **buscar** información específica, así como asegurarnos de que las solicitudes de los usuarios tengan sentido.

En este bloque cubriremos:
* Parámetros de consulta (Query Params) para implementar filtros.
* Validación automática de datos utilizando el sistema de tipos de Python y Pydantic.
* Manejo adecuado de errores y códigos de estado HTTP.
* Construcción de una API robusta y segura para producción.

---

## Parámetros de Consulta (Query Params) y Filtros

Los **Query Parameters** (o parámetros de consulta) son un conjunto de pares clave-valor que se agregan al final de una URL para modificar o filtrar la solicitud. 

* **Estructura en la URL:** Se separan de la ruta principal con un signo de interrogación `?`, y si hay varios, se unen con un ampersand `&`.
  * Ejemplo: `http://api.midominio.com/transacciones?cliente_id=105&monto_min=500`

### Implementación de filtros en FastAPI
En FastAPI, si declaramos un parámetro en nuestra función constructora del endpoint que **no** forma parte del path (la ruta principal), se interpreta automáticamente como un *Query Parameter*.

Esto nos permite flexibilizar nuestros endpoints. En lugar de crear:
* `/transacciones/cliente/105`
* `/transacciones/monto_mayor_a/500`

Creamos un único endpoint `/transacciones` que acepte los filtros opcionales de cliente, fechas o montos, permitiendo combinarlos libremente.

---

## El Poder del Tipado en FastAPI y Pydantic

Python es un lenguaje de tipado dinámico, pero en el mundo de las APIs, necesitamos **contratos estrictos**. Si esperamos un monto numérico y el usuario envía la palabra "cien", nuestro código fallará.

FastAPI resuelve esto brillantemente apoyándose en **Pydantic** y el sistema de *Type Hints* (pistas de tipado) nativo de Python.

### Validación de Entradas del Usuario
Al definir los tipos de datos en la función del endpoint (ej. `monto_min: float`), ocurren varias cosas automáticamente:
1. **Conversión de tipos (Casting):** Si el cliente envía `?monto_min=500` (que llega como texto HTTP), FastAPI lo convierte a un `float` de Python.
2. **Validación:** Si el cliente envía `?monto_min=hola`, FastAPI detiene la solicitud *antes* de que llegue a nuestro código.
3. **Respuesta de error automática:** FastAPI genera una respuesta clara en JSON indicando qué campo falló y por qué, sin que tengamos que programar esa lógica.

Podemos hacer validaciones aún más estrictas con Pydantic, como limitar que un string tenga un máximo de caracteres o que un número sea obligatoriamente mayor a cero.

---

## Manejo de Errores y Códigos de Estado HTTP

Cuando ocurre un error o una validación falla, no basta con enviar un texto diciendo "hubo un error". El protocolo HTTP tiene un estándar global para comunicar el resultado de una petición: los **Códigos de Estado (Status Codes)**.

Los más importantes para una API robusta son:

* **200 OK:** La petición se procesó exitosamente.
* **400 Bad Request:** El cliente (usuario) cometió un error. Por ejemplo, envió datos incompletos, mal formateados o que no cumplen las reglas de negocio (ej. fecha de inicio mayor a fecha de fin).
* **404 Not Found:** El recurso solicitado no existe. (ej. Buscar el cliente ID 9999 y que no esté en la base de datos).
* **500 Internal Server Error:** Ocurrió un error de nuestro lado (el servidor). Ej: se cayó la conexión a MySQL o el código de Python lanzó una excepción no manejada.

En FastAPI, controlamos esto de forma explícita levantando una excepción llamada `HTTPException`, donde especificamos el código y el detalle del error.

---

## Evitando Errores Comunes y Seguridad Básica

Construir una API robusta para consumo real (lista para producción) implica desconfiar de las entradas y manejar las fallas con elegancia.

### Buenas prácticas y mitigación de riesgos:
1. **Control estricto de inputs:** Nunca asumas que los datos enviados por el usuario son seguros. Al validar con Pydantic (tipos, límites, expresiones regulares), aplicas una capa de seguridad básica que previene ataques de inyección y comportamientos inesperados.
2. **No exponer detalles técnicos:** Si tu base de datos falla, el usuario debe recibir un error 500 genérico ("Error interno del servidor"), **no** el stack trace completo (el error crudo de Python) que podría revelar información sensible de tu arquitectura.
3. **Manejar valores nulos (None):** Al usar filtros opcionales (ej. `fecha_fin: str = None`), debes asegurarte de que la lógica SQL o de Pandas y la API sepan qué hacer si el usuario no proporciona ese filtro.

Al aplicar filtros inteligentes, validación de tipos estricta y un manejo correcto de códigos HTTP, pasamos de tener un "script expuesto en la web" a una verdadera **API profesional, robusta y segura**.

---

<!-- _class: code -->
## Practica: Añadir filtros y validaciones Pydantic a los endpoints

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar filtros y validaciones con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap3/3_5_4_Script.py
import random
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Path, status
from pydantic import BaseModel, Field

# Configurar semilla aleatoria estandarizada para el curso
random.seed(987654)

# =============================================================================
# ST8, ST11: Evitar errores comunes en APIs y creación de APIs robustas
# Inicializar la aplicación con metadatos descriptivos
# =============================================================================
app = FastAPI(
    title="API de Transacciones (Pipeline V1)",
    description="API robusta demostrando filtros, validaciones, Pydantic y manejo de errores HTTP.",
    version="1.0.0"
)

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap3/3_5_4_Script.ipynb)

---

## Errores comunes en el Bloque 3.5.4

- **No validar el rango de fechas**
  → consultas que devuelven millones de registros

- **Devolver siempre 200 aunque ocurra un error**
  → el cliente no detecta el fallo

- **Olvidar sanitizar parámetros de consulta**
  → SQL injection si se concatenan

---

## Resumen: Bloque 3.5.4

**Lo que aprendiste:**
- Usar Pydantic para validar los datos de entrada en endpoints POST
- Implementar filtros por fecha, monto y status en los endpoints GET
- Devolver códigos de error HTTP apropiados (404, 422, 500)

**Lo que construiste:**
El script `3_5_4_Script.py` que añadir filtros y validaciones pydantic a los endpoints usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 3.6.1: Introducción a Streamlit

---

<!-- _class: section -->
# Sección 6: Visualización con Streamlit
## En esta sección construiremos la capa de visualización con streamlit del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de visualización con streamlit en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 3.6.1: Introducción a Streamlit
- Bloque 3.6.2: Dashboard básico
- Bloque 3.6.3: Conexión a API o datos procesados
- Bloque 3.6.4: Métricas y visualizaciones

---

<!-- ============================================================ -->
<!-- BLOQUE 3.6.1 — Introducción a Streamlit                     -->
<!-- Scripts: scripts/cap3/3_6_1_Script.py                    -->
<!-- Notebook: notebooks/cap3/3_6_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 3.6.1
## Introducción a Streamlit

> La API está lista; ahora construimos la interfaz visual que la consume con Streamlit.

**Al terminar este bloque podrás:**
- Instalar Streamlit y entender el modelo de re-ejecución del script
- Mostrar texto, tablas y métricas básicas con st.write() y st.metric()
- Entender la diferencia entre widgets (st.button, st.selectbox) y outputs

---

## ¿Qué es Streamlit?

Las aplicaciones web tradicionales requieren conocimientos de múltiples lenguajes: HTML para la estructura, CSS para el diseño y JavaScript para la interactividad, además de un backend en Python, Node.js u otro lenguaje.

**Streamlit** cambia por completo este paradigma en el mundo de los datos:
* Es una librería de código abierto en Python.
* Permite crear aplicaciones web interactivas y dashboards en cuestión de minutos.
* **Cero experiencia en frontend requerida:** todo se escribe en Python puro.

Si sabes escribir un script de Python, ya sabes crear una aplicación web con Streamlit.

---

## El Rol de la Visualización en el Pipeline de Datos

Hasta ahora, nuestro pipeline hace el trabajo pesado en segundo plano, pero los datos procesados necesitan ser accesibles para los tomadores de decisiones. 

**Estructura de nuestro sistema:**
1. **Ingesta:** Leemos archivos CSV o consultamos APIs.
2. **Transformación:** Limpiamos y agregamos con Pandas.
3. **Almacenamiento:** Guardamos en MySQL o archivos Parquet.
4. **Consumo (El destino final):** Entregamos los datos vía API (FastAPI) o los mostramos en una interfaz visual (Streamlit).

La visualización es la "cara" de la ingeniería de datos. Es donde el negocio ve el valor de tener datos limpios, consistentes y actualizados (por ejemplo, ver en tiempo real el total de transacciones válidas).

---

## Ventajas para Prototipos y Comparación con Otras Herramientas

¿Por qué usar Streamlit en lugar de otras herramientas?

* **Frente a Frameworks Web (Flask, Django):** Streamlit es infinitamente más rápido para construir prototipos analíticos. No necesitas diseñar rutas complejas ni plantillas HTML.
* **Frente a Herramientas de BI (Tableau, Power BI):** Las herramientas de BI son excelentes y muy completas, pero a veces necesitas algo altamente personalizado, integrado directamente con tu código Python o modelos de Machine Learning. Streamlit te da esa flexibilidad como código.

**Ventaja principal:** Velocidad de iteración. Un ingeniero de datos puede levantar un dashboard funcional en menos de 50 líneas de código para validar los resultados de su pipeline.

---

## Integración Directa con Python y Ecosistema de Datos

Streamlit no intenta reinventar la rueda. Está diseñado para ser un "envoltorio" visual alrededor de las librerías que ya conoces.

* Habla el mismo idioma que **Pandas**: puedes pasarle un DataFrame y Streamlit sabrá cómo renderizarlo como una tabla interactiva.
* Se integra de forma nativa con librerías de visualización como **Matplotlib**, **Seaborn** o **Plotly**.
* Permite importar tus propios módulos. Puedes importar las funciones de limpieza o conexión a base de datos que creamos en sesiones anteriores.

---

## Estructura Básica y Flujo de Ejecución

Una aplicación en Streamlit es, en su esencia, un simple archivo de texto con extensión `.py`. 

### El Flujo de Ejecución (Top-Down)
A diferencia de otros frameworks interactivos, Streamlit tiene un modelo de ejecución muy particular y sencillo de entender:
1. Lee el código de **arriba hacia abajo**, línea por línea.
2. Cada vez que el usuario interactúa con un componente (por ejemplo, mueve un filtro de fecha o hace clic en un botón), **Streamlit vuelve a ejecutar todo el script** desde el principio.

Esto asegura que la interfaz siempre refleje el estado actual de los datos y las variables.

---

## Componentes Básicos: Texto y Tablas

Streamlit provee funciones intuitivas para renderizar elementos en la pantalla.

**Elementos de Texto:**
* `st.title("Mi Dashboard")`: Crea el título principal.
* `st.header("Ventas del Mes")`: Crea un subtítulo.
* `st.write("Cualquier texto o variable")`: Es la navaja suiza de Streamlit; detecta qué le estás pasando e intenta renderizarlo de la mejor manera.

**Elementos de Datos:**
* `st.dataframe(df)`: Renderiza un DataFrame de Pandas como una tabla interactiva (permite scroll y ordenar columnas).
* `st.table(df)`: Renderiza una tabla estática.

---

## Un Primer Vistazo al Código

Así se ve un script básico (por ejemplo, `app.py`) integrando Pandas y Streamlit para explorar nuestro dataset de transacciones:

```python
import streamlit as st
import pandas as pd

# Título de la app
st.title("Dashboard de Transacciones")
st.write("Bienvenido a la visualización de nuestro pipeline de datos.")

# Cargar datos (simulando la salida de nuestro ETL)
df = pd.read_csv("transacciones_limpias.csv")

# Mostrar los primeros registros
st.header("Vista de Datos Recientes")
st.dataframe(df.head(10))
```

---

## Ejecución de Aplicaciones con Streamlit

Una vez que tenemos nuestro script `app.py`, no lo ejecutamos con el clásico `python app.py`. Streamlit tiene su propio servidor integrado.

Para levantar la aplicación, usamos la terminal de comandos:

```bash
streamlit run app.py
```

**¿Qué sucede al ejecutar esto?**
1. Streamlit inicia un servidor web local.
2. Abre automáticamente una nueva pestaña en tu navegador predeterminado.
3. La aplicación estará disponible en una dirección local, generalmente: `http://localhost:8501`.
4. Si haces cambios en el código `.py` y guardas el archivo, Streamlit te preguntará en el navegador si deseas actualizar la vista al instante ("Rerun").

---

<!-- _class: code -->
## Practica: Crear la primera pantalla de Streamlit con métricas

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar introducción a streamlit con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap3/3_6_1_Script.py
"""
Capítulo 3: Exposición y consumo de datos
Sección 6: Visualización con Streamlit
Bloque 1: Introducción a Streamlit

Descripción: 
Script introductorio para Streamlit. Muestra cómo construir una aplicación web 
en Python, el uso de componentes básicos (texto, tablas) y la estructura general 
de una app para visualizar datos provenientes de un pipeline.

Instrucciones de ejecución:
1. Asegurar tener instalada la librería: pip install streamlit pandas numpy
2. Guardar este archivo como `app.py`
3. Ejecutar en la terminal: streamlit run app.py
"""

import streamlit as st
import pandas as pd

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap3/3_6_1_Script.ipynb)

---

## Errores comunes en el Bloque 3.6.1

- **Modificar variables globales en Streamlit**
  → comportamiento impredecible en reruns

- **Usar bucles costosos sin cache**
  → la app se vuelve lenta con cada interacción

- **Confundir st.write() con print()**
  → print no aparece en la UI

---

## Resumen: Bloque 3.6.1

**Lo que aprendiste:**
- Instalar Streamlit y entender el modelo de re-ejecución del script
- Mostrar texto, tablas y métricas básicas con st.write() y st.metric()
- Entender la diferencia entre widgets (st.button, st.selectbox) y outputs

**Lo que construiste:**
El script `3_6_1_Script.py` que crear la primera pantalla de streamlit con métricas usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 3.6.2: Dashboard básico

---

<!-- ============================================================ -->
<!-- BLOQUE 3.6.2 — Dashboard básico                             -->
<!-- Scripts: scripts/cap3/3_6_2_Script.py                    -->
<!-- Notebook: notebooks/cap3/3_6_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 3.6.2
## Dashboard básico

> Con los componentes básicos dominados, construimos un dashboard completo y navegable.

**Al terminar este bloque podrás:**
- Usar st.sidebar para navegación y filtros del usuario
- Mostrar gráficos con st.plotly_chart() o st.bar_chart()
- Organizar el layout con st.columns() y st.expander()

---

## Construcción de un Dashboard Básico

Un **dashboard** es una interfaz gráfica que centraliza y resume información clave. En un pipeline de datos, es el punto final donde el esfuerzo de ingesta, limpieza y transformación cobra sentido visual para el usuario final.

Con Streamlit, construir un dashboard básico pasa de ser un desarrollo web complejo a un script de Python estructurado paso a paso. 

**Componentes esenciales de un dashboard inicial:**
* **Título y contexto:** ¿Qué estamos viendo? (ej. `st.title("Dashboard de Transacciones")`).
* **Filtros globales:** Controles que afectan a toda la vista (ej. un selector de fechas).
* **Métricas de alto nivel (KPIs):** Resúmenes inmediatos del estado del negocio.
* **Vistas de detalle:** Gráficos o tablas para explorar la información.

El objetivo no es mostrar todos los datos, sino mostrar la información procesada de forma útil y accionable.

---

## Uso de Tablas y Selección de Métricas Relevantes

No todos los datos tienen el mismo impacto. Seleccionar las métricas adecuadas es crucial para que el dashboard tenga valor. En nuestro caso de transacciones, debemos enfocarnos en indicadores clave (KPIs).

**Métricas comunes (KPIs):**
Podemos definir operaciones matemáticas simples que agreguen gran valor, por ejemplo, el ingreso total:
$$Ingresos Totales = \sum_{i=1}^{n} Monto\_Transaccion_i$$

**Implementación en Streamlit:**
Streamlit ofrece `st.metric()` para destacar estos números y `st.dataframe()` para mostrar los registros.

* **Métricas (`st.metric`):** Ideales para mostrar totales, promedios o conteos en la parte superior del dashboard.
* **Tablas (`st.dataframe`):** Útiles para permitir al usuario explorar los últimos registros procesados o un top 10 de clientes. Evita mostrar millones de filas; usa `.head()` o filtros previos.

---

## Organización Visual (Layout) y Presentación Clara

Un dashboard desordenado confunde al usuario. Streamlit provee herramientas de *layout* para estructurar la información lógica y visualmente, imitando un diseño web profesional sin necesidad de CSS o HTML.

**Herramientas de Layout en Streamlit:**
* **Columnas (`st.columns`):** Permite organizar las métricas o gráficos uno al lado del otro. Es ideal para la fila de KPIs superior.
* **Barra lateral (`st.sidebar`):** El lugar estándar para colocar filtros (ej. selectores de fechas, categorías) sin ocupar el espacio principal de visualización.
* **Expansores (`st.expander`):** Útiles para ocultar información secundaria (como la tabla de datos crudos o notas técnicas) y mantener la pantalla limpia.

**Regla de oro:** Lee de arriba hacia abajo y de izquierda a derecha. Coloca lo más importante (filtros y métricas globales) arriba, y el detalle (gráficos y tablas) abajo.

---

## Introducción a Gráficos Simples

Los números crudos son difíciles de interpretar en grandes volúmenes. Los gráficos permiten identificar tendencias, picos y anomalías en un vistazo.

Para nuestro dataset de transacciones, podemos integrar gráficos nativos de Streamlit o librerías externas.

**Tipos de gráficos fundamentales:**
* **Gráfico de Barras (`st.bar_chart`):** Excelente para comparar categorías discretas (ej. *Número de transacciones por tipo de producto* o *Ventas por sucursal*).
* **Gráfico de Líneas (`st.line_chart`):** La mejor opción para series temporales (ej. *Evolución de los ingresos diarios*). 

*Nota:* Mantén la simplicidad. Un gráfico de barras o líneas bien etiquetado suele ser mucho más efectivo que un gráfico 3D o de pastel (pie chart) complejo.

---

## UX Básica y Cómo Evitar la Sobrecarga Visual

La Experiencia de Usuario (UX) en un dashboard de datos se basa en minimizar el esfuerzo cognitivo del lector. 

**Prácticas para evitar la sobrecarga visual:**
1. **Menos es más:** No intentes responder a todas las preguntas posibles en una sola pantalla. Si hay demasiados gráficos, divídelos en pestañas (`st.tabs`).
2. **Uso del color:** Utiliza el color para resaltar, no para decorar. Si todo es de colores brillantes, nada destaca. Las alertas en rojo (caída de ventas) o verde (crecimiento) deben tener un propósito.
3. **Consistencia:** Mantén un formato uniforme para las fechas, monedas y números (ej. siempre usar 2 decimales y el símbolo $).
4. **Espaciado en blanco:** Permite que los elementos "respiren". No apiles las tablas directamente pegadas a los gráficos.

---

## Storytelling e Interpretación de Resultados

Los datos por sí solos no comunican nada; necesitan narrativa. El **Data Storytelling** es la capacidad de guiar al usuario a través de los datos para que entienda el "por qué" detrás del "qué".

**Construyendo la narrativa:**
* **Contexto:** Usa `st.markdown()` para añadir breves textos explicativos antes de un gráfico. Ejemplo: *"El siguiente gráfico muestra el pico estacional de transacciones en diciembre"*.
* **Interpretación vs. Exposición:** No te limites a decir "Aquí están las ventas". Explica visualmente la tendencia general. 
* **Fluidez:** El dashboard debe contar una historia. Empieza por el gran resumen (KPIs), pasa por la tendencia general (gráficos temporales) y termina en el detalle específico (tablas filtradas).

---

## De la Visualización a la Toma de Decisiones

El propósito final de cualquier pipeline de datos y su posterior visualización no es crear gráficos bonitos, sino **facilitar la toma de decisiones**.

**Conectando visualización con acciones:**
* Si el dashboard muestra un aumento repentino de transacciones rechazadas (datos sucios o errores del sistema), el equipo de operaciones debe actuar de inmediato.
* Si vemos que el *ticket promedio* disminuye en una fecha específica, el equipo de negocio puede lanzar promociones.

Al diseñar el dashboard en Streamlit, siempre pregúntate: *¿Qué decisión va a tomar el usuario final al ver esta métrica?* Si la respuesta es "ninguna", probablemente ese gráfico no debería estar en la vista principal.

---

<!-- _class: code -->
## Practica: Construir un dashboard con gráficos y filtros laterales

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar dashboard básico con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap3/3_6_2_Script.py
"""
Capitulo 3: Exposicion y consumo de datos
Seccion 6: Visualizacion con Streamlit
Bloque 2: Dashboard basico

Descripcion:
Script para generar un dashboard basico utilizando la libreria Streamlit.
Demuestra la creacion de un layout estructurado, seleccion de metricas relevantes (KPIs),
introduccion a graficos simples, uso de tablas y principios de UX basica orientados 
a la presentacion clara de informacion y apoyo a la toma de decisiones.
"""

import streamlit as st
import pandas as pd
import numpy as np

# 1. Configurar pagina principal del dashboard
# Esto debe ejecutarse antes de cualquier otra instruccion de Streamlit

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap3/3_6_2_Script.ipynb)

---

## Errores comunes en el Bloque 3.6.2

- **No usar st.cache_data**
  → la BD se consulta con cada clic del usuario

- **Colocar filtros dentro del callback en lugar del sidebar**
  → UX confusa

- **Olvidar actualizar el DataFrame filtrado tras cambiar un widget**
  → datos obsoletos

---

## Resumen: Bloque 3.6.2

**Lo que aprendiste:**
- Usar st.sidebar para navegación y filtros del usuario
- Mostrar gráficos con st.plotly_chart() o st.bar_chart()
- Organizar el layout con st.columns() y st.expander()

**Lo que construiste:**
El script `3_6_2_Script.py` que construir un dashboard con gráficos y filtros laterales usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 3.6.3: Conexión a API o datos procesados

---

<!-- ============================================================ -->
<!-- BLOQUE 3.6.3 — Conexión a API o datos procesados            -->
<!-- Scripts: scripts/cap3/3_6_3_Script.py                    -->
<!-- Notebook: notebooks/cap3/3_6_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 3.6.3
## Conexión a API o datos procesados

> El dashboard ya existe; ahora lo alimentamos con datos reales desde la API del pipeline.

**Al terminar este bloque podrás:**
- Consumir la API FastAPI desde Streamlit usando la librería requests
- Manejar errores de conexión a la API con try/except y mensajes amigables
- Actualizar el dashboard automáticamente al cambiar los filtros del usuario

---

## Consumo de APIs desde Streamlit

Una vez que tenemos nuestra API construida con FastAPI, el siguiente paso es consumirla desde una interfaz gráfica. 

Streamlit actúa como la capa de presentación (frontend) que solicita los datos a nuestra API (backend) para mostrarlos al usuario final.

En lugar de que Streamlit procese los datos crudos o ejecute reglas de negocio complejas, su única responsabilidad es:
1. Hacer una petición (request) a la API.
2. Recibir los datos.
3. Renderizar tablas, gráficos y métricas.

Este enfoque asegura que las reglas de nuestro pipeline de transacciones se mantengan centralizadas en el backend.

---

## Lectura de datos procesados (CSV/Parquet)

Existe un enfoque alternativo al consumo de APIs: que Streamlit lea directamente los archivos resultantes de nuestro pipeline de datos (archivos CSV o Parquet).

Para implementar esto, Streamlit utiliza Pandas internamente:

```python
import pandas as pd
import streamlit as st

# Lectura directa del almacenamiento del pipeline
df_transacciones = pd.read_parquet("data/processed/transacciones_limpias.parquet")
st.dataframe(df_transacciones)
```

Este método es sumamente rápido de implementar y es muy útil para prototipos iniciales o cuando el dashboard es el único consumidor de los datos.

---

## Diferencias entre consumo directo vs API

Es importante entender cuándo utilizar cada enfoque en la ingeniería de datos:

**Consumo Directo (Lectura de Archivos):**
* **Implementación:** Muy rápida. Streamlit y los datos viven en el mismo entorno o tienen acceso al mismo almacenamiento.
* **Procesamiento:** El dashboard carga los datos en memoria y asume la carga de trabajo de cualquier filtrado adicional.
* **Recomendado para:** Prototipos, análisis exploratorio o arquitecturas locales simples.

**Consumo por API:**
* **Implementación:** Requiere construir y mantener el servicio de FastAPI.
* **Procesamiento:** La base de datos o la API filtran la información. El dashboard solo recibe lo necesario.
* **Recomendado para:** Sistemas en producción, múltiples consumidores (apps, dashboards, clientes externos) y arquitecturas distribuidas.

---

## Integración frontend-backend

La integración entre el frontend (Streamlit) y el backend (FastAPI) marca la creación de un sistema de software completo.

En este paradigma:
* **Backend (FastAPI):** Se conecta a MySQL o a los archivos Parquet, ejecuta consultas SQL y formatea los resultados según las peticiones.
* **Frontend (Streamlit):** Provee los controles interactivos (ej. selectores de fechas o clientes), envía estos parámetros al backend y dibuja los gráficos con la respuesta.

Esta separación de responsabilidades hace que el código sea más limpio y fácil de mantener. Si mañana cambiamos Streamlit por otra tecnología, la API sigue funcionando intacta.

---

## Manejo de requests en Python

Para comunicar Streamlit con la API, utilizamos la librería estandarizada `requests`. Esta librería nos permite realizar peticiones HTTP (GET, POST, etc.) desde nuestro script de Python.

Ejemplo de cómo Streamlit solicita los datos de transacciones a la API:

```python
import requests
import streamlit as st

url = "http://localhost:8000/transacciones"
respuesta = requests.get(url)

if respuesta.status_code == 200:
    st.success("Datos obtenidos correctamente")
else:
    st.error("Error al conectar con la API")
```

Es fundamental validar el código de estado HTTP (200 indica éxito) para manejar errores y evitar que el dashboard colapse si la API está inactiva.

---

## Procesamiento de respuestas JSON

Las APIs modernas, incluyendo las construidas con FastAPI, devuelven los datos en formato JSON. Para que Streamlit pueda graficarlos fácilmente, necesitamos convertir ese JSON nuevamente a un DataFrame de Pandas.

El flujo de transformación es el siguiente:
1. Extraer el contenido JSON de la respuesta.
2. Inyectarlo en la estructura de Pandas.

```python
import pandas as pd
import requests

url = "http://localhost:8000/api/v1/ventas"
respuesta = requests.get(url)

if respuesta.status_code == 200:
    datos_json = respuesta.json()
    # Conversión directa de JSON a DataFrame
    df = pd.DataFrame(datos_json)
    
    # Ahora 'df' está listo para visualizaciones en Streamlit
```

---

## Ventajas de desacoplar sistemas

Desacoplar la lógica de visualización de la lógica de acceso a datos trae beneficios fundamentales para la ingeniería de datos:

* **Mantenibilidad:** Los errores de base de datos se arreglan en la API; los errores visuales se arreglan en Streamlit.
* **Reutilización:** Los mismos datos de la API pueden alimentar el dashboard de Streamlit y, simultáneamente, una aplicación móvil.
* **Escalabilidad Independiente:** Si el dashboard recibe muchas visitas, podemos asignar más recursos solo al servidor de Streamlit, sin afectar al motor de base de datos.
* **Seguridad:** El frontend nunca conoce las credenciales de la base de datos MySQL; solo conoce la URL de la API.

---

## Limitaciones de lectura directa

Si decidimos omitir la API y leer archivos CSV/Parquet directamente desde Streamlit para un proyecto real, enfrentaremos varias limitaciones:

1. **Gestión de concurrencia:** Si el pipeline de datos intenta sobrescribir el archivo Parquet exactamente al mismo tiempo que Streamlit intenta leerlo, pueden ocurrir bloqueos (file locks) o lectura de datos corruptos.
2. **Consumo de memoria:** Leer un archivo de 5 GB obliga a Streamlit a cargar 5 GB en la memoria del servidor. Una API con una base de datos realizaría la agregación y solo enviaría los 10 KB de resultados necesarios.
3. **Falta de gobernanza:** Cualquier persona con acceso al código de Streamlit tiene acceso a los datos crudos en el almacenamiento, rompiendo el principio de menor privilegio.

---

## Arquitectura simple de sistema

En este punto, nuestro sistema completo se puede visualizar con la siguiente arquitectura simple:

**Fuente de Datos >> Transformación (Python) >> Almacenamiento (MySQL/Parquet)**

Esta es la primera parte (el Pipeline ETL). Luego viene la capa de consumo:

**Almacenamiento >> Backend (FastAPI) >> Frontend (Streamlit) >> Usuario Final**

Cada componente tiene un límite claro. La información fluye de izquierda a derecha, transformándose de datos crudos a conocimiento accionable.

---

## Flujo de datos completo

Integrando todos los conceptos, el ciclo de vida de un dato en nuestro sistema es:

1. Un archivo CSV de transacciones llega al sistema.
2. El script de ingesta y limpieza elimina nulos y estandariza los montos.
3. Los datos limpios se insertan en la base de datos MySQL.
4. Un usuario abre la aplicación de Streamlit en su navegador.
5. Streamlit hace un `requests.get()` a FastAPI pidiendo las ventas del día.
6. FastAPI ejecuta un `SELECT` en MySQL, obtiene los datos, los serializa a JSON y los devuelve.
7. Streamlit convierte el JSON a DataFrame y renderiza un gráfico de barras.

Este es un verdadero flujo de trabajo (workflow) en ingeniería de datos.

---

## Preparación para escalabilidad

Construir el sistema de esta manera modular (Pipeline >> DB >> API >> Dashboard) nos prepara para los siguientes desafíos en la nube.

Al tener las piezas separadas:
* Podemos empaquetar la API en un contenedor independiente.
* Podemos empaquetar Streamlit en otro contenedor.
* Podemos automatizar la ejecución del pipeline de limpieza sin afectar el acceso de los usuarios a la API.

El código ya está estructurado correctamente. El siguiente paso natural será asegurar que funcione de manera idéntica en cualquier máquina o servidor, introduciendo herramientas de despliegue y automatización.

---

<!-- _class: code -->
## Practica: Conectar el dashboard de Streamlit a la API FastAPI

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar conexión a api o datos procesados con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap3/3_6_3_Script.py
"""
Capítulo 3: Exposición y consumo de datos
Sección 6: Visualización con Streamlit
Bloque 3: Conexión a API o datos procesados

Este script demuestra cómo conectar una aplicación web en Streamlit
tanto a datos directamente almacenados en archivos (CSV) como a una API.
"""

import streamlit as st
import pandas as pd
import requests
import numpy as np
import os

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard de Transacciones", layout="wide")

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap3/3_6_3_Script.ipynb)

---

## Errores comunes en el Bloque 3.6.3

- **Hardcodear la URL de la API**
  → la app falla cuando cambia el entorno

- **No manejar el timeout en requests**
  → la app se congela si la API no responde

- **Mostrar el JSON crudo al usuario en lugar de un DataFrame formateado**

---

## Resumen: Bloque 3.6.3

**Lo que aprendiste:**
- Consumir la API FastAPI desde Streamlit usando la librería requests
- Manejar errores de conexión a la API con try/except y mensajes amigables
- Actualizar el dashboard automáticamente al cambiar los filtros del usuario

**Lo que construiste:**
El script `3_6_3_Script.py` que conectar el dashboard de streamlit a la api fastapi usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 3.6.4: Métricas y visualizaciones

---

<!-- ============================================================ -->
<!-- BLOQUE 3.6.4 — Métricas y visualizaciones                   -->
<!-- Scripts: scripts/cap3/3_6_4_Script.py                    -->
<!-- Notebook: notebooks/cap3/3_6_4_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 3.6.4
## Métricas y visualizaciones

> Finalizamos la capa de visualización con métricas clave y gráficos comparativos.

**Al terminar este bloque podrás:**
- Calcular y mostrar KPIs del negocio (ventas totales, ticket promedio, tasa de fallo)
- Crear gráficos de serie temporal y distribución con Plotly
- Añadir tablas descargables con st.download_button()

---

## Creación de métricas clave (KPIs)

En la capa final de un pipeline de datos, la información procesada debe traducirse en valor. Aquí es donde entran los Indicadores Clave de Rendimiento (KPIs).

Un KPI es una métrica cuantificable que refleja el rendimiento de un negocio en relación con sus objetivos estratégicos. No cualquier número es un KPI; debe ser accionable y fundamental para la toma de decisiones. 

En nuestro caso práctico de transacciones, algunos KPIs críticos podrían ser:
* Volumen total de ventas.
* Cantidad de clientes activos.
* Tasa de transacciones fallidas o nulas.

En Streamlit, destacamos estos valores numéricos críticos utilizando el componente `st.metric()`, que permite mostrar el valor actual y su variación respecto a un periodo anterior.

---

## Cálculo de agregados (sum, avg, count)

Para construir nuestros KPIs, necesitamos reducir miles o millones de registros a un solo número representativo mediante funciones de agregación.

Las operaciones fundamentales son:
* **SUM (Suma):** Útil para totales acumulados. Ejemplo: Ingresos totales del mes.
* **COUNT (Conteo):** Útil para volúmenes. Ejemplo: Número total de transacciones procesadas.
* **AVG (Promedio):** Útil para entender el comportamiento típico. 

Un ejemplo clásico es el "Ticket Promedio". Matemáticamente se define como:
Ticket Promedio = SUM(Ingresos Totales) / COUNT(Numero de Transacciones)

A nivel de código, esto se realiza combinando Pandas (`df['monto'].sum()`) y pasando el resultado a la interfaz de Streamlit.

---

## Uso de gráficos (barras, líneas)

Los números por sí solos no siempre cuentan toda la historia. Las visualizaciones permiten identificar tendencias, patrones y valores atípicos rápidamente.

Streamlit ofrece integraciones nativas y sencillas para los gráficos más comunes:
* **Gráficos de Líneas (`st.line_chart`):** Ideales para mostrar la evolución de una variable a lo largo del tiempo (series temporales). Por ejemplo, los ingresos diarios durante el último mes.
* **Gráficos de Barras (`st.bar_chart`):** Perfectos para comparar categorías discretas. Por ejemplo, el volumen de ventas segmentado por tipo de producto o por sucursal.

La elección del gráfico correcto es vital: usar un gráfico de líneas para datos categóricos sin relación secuencial generará confusión visual.

---

## Filtros interactivos (fecha, cliente)

Un dashboard estático tiene un valor limitado. La interactividad permite a los usuarios explorar los datos bajo sus propios criterios sin necesidad de solicitar nuevas consultas a la base de datos.

En Streamlit, la interactividad se logra capturando el input del usuario y usándolo para filtrar el DataFrame subyacente antes de renderizar los gráficos.

Componentes comunes para filtros:
* `st.date_input`: Para seleccionar rangos de fechas (ej. "Ver transacciones del último trimestre").
* `st.selectbox` / `st.multiselect`: Para elegir una o varias categorías, como un ID de cliente específico o una región.
* `st.sidebar`: Un contenedor lateral muy utilizado para agrupar todos los controles de filtrado y no saturar la vista principal.

---

## Segmentación de datos

La segmentación es el proceso de dividir el conjunto de datos global en subgrupos más pequeños y homogéneos basados en ciertas características. 

Al aplicar filtros interactivos, dinámicamente estamos segmentando la información. Esto es crucial porque las métricas globales a menudo ocultan problemas locales. 

Por ejemplo:
* Los ingresos totales (globales) pueden estar subiendo.
* Sin embargo, al segmentar por "tipo de cliente", podríamos descubrir que los clientes nuevos están gastando menos, y el crecimiento depende solo de clientes antiguos.

La segmentación transforma un reporte genérico en una herramienta de diagnóstico.

---

## Interpretación de visualizaciones

Crear el gráfico es solo la mitad del trabajo; la otra mitad es saber leerlo y ayudar al usuario a interpretarlo.

Una correcta interpretación busca responder preguntas más allá de "qué pasó", acercándose al "por qué pasó":
* **Picos y valles:** ¿A qué se debe un aumento repentino en las transacciones un martes específico? (Podría ser una campaña de marketing o un error de duplicación de datos).
* **Tendencias:** ¿El ticket promedio va a la baja de forma constante durante el año?
* **Anomalías:** Valores que se escapan drásticamente de la norma y requieren una revisión en etapas anteriores del pipeline (¿hubo un error en la transformación de la moneda?).

---

## Errores comunes en dashboards

Es fácil caer en malas prácticas al diseñar interfaces de datos. Los errores más frecuentes que arruinan la experiencia del usuario incluyen:

* **Sobrecarga visual (Clutter):** Intentar mostrar demasiados gráficos en una sola pantalla. Si todo resalta, nada resalta.
* **Mala elección de escalas:** Ejes Y que no empiezan en cero (cuando corresponde) exagerando variaciones mínimas.
* **Falta de contexto:** Un KPI que dice "Ventas: 50,000" no significa nada si no sabemos si la meta era 10,000 o 100,000.
* **Uso excesivo de gráficos de pastel (Pie charts):** Son difíciles de leer cuando hay más de tres o cuatro categorías con tamaños similares.

---

## Validación de métricas

Un dashboard atractivo pierde toda su utilidad si los datos que muestra son incorrectos. La validación de métricas asegura la confianza del usuario final en el pipeline.

Prácticas de validación (Sanity Checks):
* **Comparación cruzada:** ¿El total de ventas mostrado en el dashboard coincide exactamente con una consulta `SELECT SUM(monto)` en la base de datos MySQL?
* **Consistencia de filtros:** Asegurarse de que al cruzar múltiples filtros interactivos (ej. Fecha + Cliente) el cálculo de las métricas no genere errores de división por cero o datos nulos no manejados.
* **Trazabilidad:** Si un usuario reporta un número extraño, debe ser posible rastrear ese dato desde Streamlit >> API >> Base de Datos >> Archivo Raw.

---

## Comunicación efectiva de datos

El diseño del dashboard debe guiar el ojo del usuario a través de una historia lógica. A esto se le conoce como *Storytelling con datos*.

La jerarquía visual típica en occidente sigue un patrón en "Z" o "F" (de arriba a abajo, de izquierda a derecha):
1. **Nivel Superior:** KPIs principales y globales (Ticket promedio, Ingresos Totales).
2. **Nivel Medio:** Gráficos de tendencias y contexto histórico (Líneas de tiempo).
3. **Nivel Inferior / Detalle:** Tablas con registros individuales o segmentaciones muy específicas.

El uso de `st.columns` en Streamlit es la herramienta perfecta para maquetar esta estructura y organizar la información de manera limpia y profesional.

---

## Conexión con lógica de negocio

La ingeniería de datos no ocurre en el vacío. Cada transformación en Pandas y cada endpoint en FastAPI existen para resolver un problema de negocio.

Las visualizaciones deben reflejar directamente las reglas y definiciones de la empresa. 
* Si el negocio define un "cliente inactivo" como aquel que no ha comprado en 30 días, el dashboard debe reflejar exactamente esa lógica.
* Si hay reglas impositivas que restan un porcentaje al ingreso bruto, el cálculo del KPI de "Ingreso Neto" debe incorporar esa fórmula de negocio explícitamente.

El desarrollador del pipeline debe hablar el mismo idioma que el analista de negocio o el gerente que consumirá el dashboard.

---

## Dashboard como herramienta de decisión

El objetivo final de todo el esfuerzo invertido en el pipeline (extracción, limpieza, almacenamiento en la nube, despliegue con Docker y orquestación) culmina aquí.

Un dashboard bien construido permite a los tomadores de decisiones:
* Monitorear la salud del negocio en tiempo casi real.
* Identificar cuellos de botella u oportunidades de venta.
* Reducir el tiempo empleado en generar reportes manuales en hojas de cálculo.

Cuando el usuario interactúa fluidamente con Streamlit y toma una decisión informada, el pipeline de datos ha cumplido exitosamente su propósito completo.

---

<!-- _class: code -->
## Practica: Añadir KPIs, gráficos temporales y exportación de datos

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar métricas y visualizaciones con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap3/3_6_4_Script.py
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

```

**Para ejecutarlo:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap3/3_6_4_Script.ipynb)

---

## Errores comunes en el Bloque 3.6.4

- **No redondear flotantes antes de mostrar**
  → métricas con 12 decimales

- **Usar colores sin escala consistente**
  → gráficos confusos para el usuario

- **No etiquetar los ejes en los gráficos**
  → el usuario no entiende las unidades

---

## Resumen: Bloque 3.6.4

**Lo que aprendiste:**
- Calcular y mostrar KPIs del negocio (ventas totales, ticket promedio, tasa de fallo)
- Crear gráficos de serie temporal y distribución con Plotly
- Añadir tablas descargables con st.download_button()

**Lo que construiste:**
El script `3_6_4_Script.py` que añadir kpis, gráficos temporales y exportación de datos usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 4.7.1: CSV vs Parquet