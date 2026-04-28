---
marp: true
theme: bsg
size: 16:9
paginate: true
footer: 'Python para Ingeniería de Datos · Capítulo 6: Integración, despliegue y proyecto final · BSG Institute'
---

---

<!-- _class: title -->
# Capítulo 6: Integración, despliegue y proyecto final
## CI/CD y monitoreo

---

<!-- _class: section -->
# Sección 11: CI/CD y monitoreo
## En esta sección construiremos la capa de ci/cd y monitoreo del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de ci/cd y monitoreo en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 6.11.1: Introducción a GitHub y repositorios
- Bloque 6.11.2: CI/CD con GitHub Actions
- Bloque 6.11.3: Monitoreo (logs, health checks)
- Bloque 6.11.4: Seguimiento del proyecto

---

<!-- ============================================================ -->
<!-- BLOQUE 6.11.1 — Introducción a GitHub y repositorios         -->
<!-- Scripts: scripts/cap6/6_11_1_Script.py                    -->
<!-- Notebook: notebooks/cap6/6_11_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 6.11.1
## Introducción a GitHub y repositorios

> El pipeline está listo; ahora aprendemos a versionarlo y colaborar con el equipo.

**Al terminar este bloque podrás:**
- Crear un repositorio Git y conectarlo a GitHub
- Hacer commits atómicos con mensajes descriptivos
- Usar ramas (branches) para desarrollar features sin afectar main

---

## Introducción al control de versiones

### ¿Qué es el control de versiones?
El control de versiones es un sistema que registra los cambios realizados sobre un archivo o conjunto de archivos a lo largo del tiempo. Esto permite recuperar versiones específicas en cualquier momento.

### Adiós al caos
En lugar de tener carpetas llenas de archivos como:
* `pipeline_final.py`
* `pipeline_final_v2.py`
* `pipeline_final_ahora_si.py`

El control de versiones (como Git) mantiene un único archivo y un historial ordenado e invisible en el directorio de trabajo que documenta cada modificación de forma estructural.

---

## Importancia de versionar código en ingeniería de datos

### ¿Por qué es crítico en nuestro campo?
Los pipelines de datos son sistemas vivos. Las fuentes de datos cambian, las reglas de negocio evolucionan y los esquemas se actualizan. 

* **Trazabilidad:** Permite saber exactamente qué línea de código se modificó, quién la cambió y por qué.
* **Recuperación de desastres:** Si un cambio reciente rompe el procesamiento de datos de esta mañana, el control de versiones permite regresar a la versión de ayer en segundos (rollback).
* **Trabajo en equipo:** Facilita que múltiples ingenieros de datos trabajen sobre el mismo proyecto sin sobrescribir el trabajo del otro.

---

## Concepto de repositorio (GitHub)

### El Repositorio
Un repositorio (o "repo") es el directorio donde se almacenan los archivos de tu proyecto junto con todo el historial de cambios de Git. 

### ¿Qué es GitHub?
Mientras que Git es la herramienta de línea de comandos que gestiona las versiones de forma local, GitHub es una plataforma en la nube diseñada para alojar repositorios de Git.

### Beneficios de GitHub en la nube
* Actúa como respaldo de tu código.
* Proporciona una interfaz gráfica para visualizar el historial.
* Ofrece herramientas avanzadas para la colaboración y automatización.

---

## Commits y mensajes claros

### El concepto de Commit
Un `commit` es como una "fotografía" o captura de pantalla del estado actual de tus archivos. Cada commit guarda los cambios exactos realizados desde la versión anterior.

### La importancia de los mensajes
Al hacer esta captura, debes adjuntar un mensaje. Un mensaje claro es documentación viva del proyecto.

* **Mal mensaje:** "Arreglo cosas" o "Actualización".
* **Buen mensaje:** "Corrige error de nulos en el módulo de limpieza de transacciones".

El buen mensaje responde al "por qué" y "qué" del cambio, ahorrando horas de investigación en el futuro.

---

## Flujo básico (add, commit, push)

El trabajo diario con Git y GitHub se resume en tres pasos fundamentales:

1. **git add:** Selecciona los archivos modificados que quieres incluir en tu próxima captura. Esto se conoce como pasar los cambios al "staging area".
2. **git commit:** Crea la captura permanente en tu historial local con un mensaje descriptivo.
3. **git push:** Sincroniza tu historial local subiendo los nuevos commits al repositorio remoto en GitHub.

Flujo: Modificación >> Add >> Commit >> Push.

---

## Estructura de un repositorio de datos

Un repositorio de ingeniería de datos debe estar estructurado de manera que cualquier persona entienda dónde está cada componente.

### Ejemplo de estructura estándar:
* `/src` o `/pipeline`: Scripts principales (ingesta.py, transformacion.py, db.py).
* `/notebooks`: Archivos de exploración o prototipado.
* `/data`: Carpeta para guardar datos locales (¡Esta carpeta generalmente se excluye del control de versiones!).
* `requirements.txt` o `Dockerfile`: Definición de dependencias y entorno.
* `.gitignore`: Archivo crucial que le dice a Git qué archivos no debe rastrear (ej. contraseñas, archivos CSV pesados).
* `README.md`: La portada del proyecto con instrucciones de ejecución.

---

## Manejo de ramas (conceptual)

### Aislamiento del desarrollo
En un proyecto real, nunca se trabaja directamente sobre la línea de código de producción (generalmente llamada `main` o `master`).

### Ramas (Branches)
Una rama es una desviación del código principal. Te permite crear una copia virtual del proyecto donde puedes experimentar, agregar una nueva función o corregir un error, sin afectar el código que actualmente funciona en producción.

Una vez que la nueva funcionalidad está lista y probada en la rama, se "fusiona" (merge) de vuelta a la rama principal.

---

## Colaboración básica

### Pull Requests (PR)
Cuando trabajas en equipo y terminas tu código en una rama, no lo unes directamente al `main`. En su lugar, abres un "Pull Request".

* Un PR es una petición formal que dice: "He terminado este cambio en mi rama, por favor revísenlo para integrarlo al proyecto principal".
* Permite que otros ingenieros lean el código, dejen comentarios, sugieran mejoras y aprueben los cambios.
* Es el mecanismo principal para garantizar la calidad del código antes de que llegue a producción.

---

## Buenas prácticas de versionado

Para que el control de versiones sea verdaderamente útil, se deben seguir ciertas convenciones:

* **Commits atómicos:** Un commit debe representar una unidad de trabajo completa pero pequeña. No mezcles la creación de la API y la conexión a la base de datos en un solo commit.
* **Nunca subir credenciales:** El archivo `.gitignore` debe excluir configuraciones locales, contraseñas o llaves de acceso (`.env`).
* **Sincronización constante:** Haz `pull` (descargar cambios remotos) frecuentemente para evitar conflictos de código con tus compañeros.
* **Código limpio:** Revisa tus propios cambios antes de solicitar que alguien más lo haga.

---

## Versionado de código vs datos (conceptual)

### Una regla de oro
**Git es para código, no para datos.**

### El problema
Git está diseñado para rastrear cambios en archivos de texto (scripts). Si intentas versionar archivos CSV, Parquet o bases de datos SQLite dentro de Git, el repositorio se volverá lento, pesado y eventualmente colapsará. 

### La solución
El código fuente vive en GitHub. Los datos viven en bases de datos (MySQL) o en almacenamiento en la nube (GCS, AWS S3). En el repositorio solo guardamos la *lógica* de cómo procesar esos datos, no los datos en sí.

---

## Preparación para CI/CD

### El puente hacia la automatización
Tener el código versionado en GitHub no es solo para colaborar, es el cimiento de la ingeniería moderna.

Una vez que nuestro pipeline de datos vive en un repositorio organizado, podemos conectar herramientas que "escuchen" cada vez que hacemos un `push`.

Esto abre la puerta al CI/CD (Integración y Entrega Continua), donde la simple acción de aprobar un Pull Request puede detonar pruebas automáticas y el despliegue del código directamente a un servidor de producción.

---

<!-- _class: code -->
## Practica: Publicar el pipeline en GitHub con buenas prácticas Git

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar introducción a github y repositorios con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap6/6_11_1_Script.py
import os

def generar_estructura_repositorio():
    """
    Crear la estructura de directorios estándar para un proyecto de ingeniería de datos.
    Esto permite mantener el código organizado antes de inicializar Git.
    """
    directorios = [
        "mi_proyecto_datos/data/raw",
        "mi_proyecto_datos/data/processed",
        "mi_proyecto_datos/src",
        "mi_proyecto_datos/tests",
        "mi_proyecto_datos/notebooks"
    ]
    
    print("Iniciando la creacion de la estructura del repositorio...")
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap6/6_11_1_Script.py`

---

## Errores comunes en el Bloque 6.11.1

- **Hacer commits gigantes con cientos de archivos**
  → imposible hacer code review

- **Commitear archivos sensibles (.env, credenciales)**
  → riesgo de seguridad

- **No usar .gitignore**
  → archivos temporales y de datos contaminan el repo

---

## Resumen: Bloque 6.11.1

**Lo que aprendiste:**
- Crear un repositorio Git y conectarlo a GitHub
- Hacer commits atómicos con mensajes descriptivos
- Usar ramas (branches) para desarrollar features sin afectar main

**Lo que construiste:**
El script `6_11_1_Script.py` que publicar el pipeline en github con buenas prácticas git usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 6.11.2: CI/CD con GitHub Actions

---

<!-- ============================================================ -->
<!-- BLOQUE 6.11.2 — CI/CD con GitHub Actions                     -->
<!-- Scripts: scripts/cap6/6_11_2_Script.py                    -->
<!-- Notebook: notebooks/cap6/6_11_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 6.11.2
## CI/CD con GitHub Actions

> Con el código en GitHub, automatizamos las pruebas y el despliegue con CI/CD.

**Al terminar este bloque podrás:**
- Crear un workflow de GitHub Actions que ejecuta el pipeline en cada push
- Configurar secretos de GitHub para credenciales de BD y servicios
- Entender el ciclo CI (test) → CD (deploy) en el contexto del pipeline

---

## Introducción a CI/CD

### ¿Qué es CI/CD?
En la ingeniería de software y de datos, a medida que los equipos y los proyectos crecen, mover el codigo desde la computadora del desarrollador hasta un entorno de produccion se vuelve un proceso complejo y propenso a errores.

CI/CD son las siglas de **Continuous Integration** (Integración Continua) y **Continuous Delivery/Deployment** (Entrega/Despliegue Continuo). 

### Propósito principal
* Crear un puente automatizado entre la escritura del codigo y su despliegue.
* Reducir la intervencion manual en los procesos de prueba y puesta en marcha.
* Garantizar que los cambios en el codigo no rompan la funcionalidad existente del pipeline de datos.

---

## Concepto de Integración Continua (CI)

### Integrando el trabajo de forma segura
La **Integración Continua** es la practica de fusionar (merge) el codigo de todos los desarrolladores en un repositorio central de forma frecuente, idealmente varias veces al dia.

### ¿Cómo funciona?
1. El ingeniero escribe un nuevo codigo (por ejemplo, una nueva funcion de limpieza de datos).
2. Sube los cambios al repositorio.
3. Un sistema automatico detecta el cambio y ejecuta una serie de pruebas (tests).
4. Si las pruebas fallan, el codigo es rechazado. Si pasan, se acepta la integracion.

### Objetivo
Detectar errores (bugs) lo mas rapido posible, cuando aun son faciles de localizar y solucionar, evitando el "infierno de integracion" al final del proyecto.

---

## Concepto de Entrega Continua (CD)

### Llevando el código a producción
La **Entrega Continua** toma el relevo donde termina la Integracion Continua. Una vez que el codigo ha sido integrado y probado automaticamente, el siguiente paso es prepararlo para su liberacion.

### Características clave
* El codigo siempre esta en un estado listo para ser desplegado.
* Los despliegues a entornos de prueba (staging) o produccion se realizan mediante un proceso automatizado con solo presionar un boton, o incluso de forma completamente automatica (Despliegue Continuo).
* En ingenieria de datos, esto podria significar actualizar automaticamente la imagen de Docker de nuestro pipeline o desplegar una nueva version de nuestra API en FastAPI.

---

## Automatización de procesos de código

### De lo manual a lo automático
Hasta ahora, hemos ejecutado nuestros scripts de Python, construido nuestras imagenes de Docker y levantado nuestros contenedores de forma manual en la terminal.

### El problema de lo manual
* Depende de la memoria del desarrollador (¿olvidaste ejecutar las pruebas antes de subir el codigo?).
* No es escalable cuando trabajan multiples personas.
* Genera cuellos de botella.

### La solución
Automatizar los procesos del codigo significa delegar estas tareas a un servidor externo. Le damos instrucciones precisas (una receta) de lo que debe hacer cada vez que detecte un cambio en el repositorio.

---

## Introducción a GitHub Actions

### ¿Qué es GitHub Actions?
Es la plataforma de CI/CD integrada directamente dentro de GitHub. Permite automatizar flujos de trabajo (workflows) de software sin necesidad de configurar servidores de terceros.

### Ventajas para el curso
* **Integración nativa:** Como ya usamos GitHub para nuestro repositorio, no requerimos cuentas adicionales.
* **Infraestructura gestionada:** GitHub nos presta servidores virtuales (runners) con Linux, Windows o macOS para ejecutar nuestro codigo.
* **Comunidad:** Existe un vasto ecosistema de acciones preconstruidas (por ejemplo, "instalar Python", "configurar credenciales") que podemos reutilizar.

---

## Estructura de un workflow

### Archivos YAML
Los flujos de trabajo en GitHub Actions se definen mediante archivos YAML (`.yml` o `.yaml`) que deben guardarse en una carpeta especifica del repositorio: `.github/workflows/`.

### Componentes de un workflow
* **Name (Nombre):** Identificador del flujo de trabajo.
* **On (Eventos):** Define que accion desencadena el flujo.
* **Jobs (Trabajos):** Un flujo puede tener uno o varios trabajos que se ejecutan en paralelo o de forma secuencial.
* **Steps (Pasos):** Cada trabajo se divide en pasos, que son tareas individuales (ej. revisar el codigo, instalar librerias, ejecutar un script).

---

## Eventos desencadenadores (push, pull request)

### ¿Cuándo se ejecuta nuestro workflow?
La directiva `on` en nuestro archivo YAML le indica a GitHub Actions que eventos debe escuchar. Los mas comunes en ingenieria de datos son:

### push
Se activa cada vez que alguien sube codigo (hace un push) a una rama especifica, generalmente la rama principal (`main` o `master`).
* *Uso típico:* Despliegue de codigo o ejecucion de pipelines programados.

### pull_request
Se activa cuando alguien propone fusionar cambios de una rama secundaria a la rama principal.
* *Uso típico:* Ejecutar pruebas para asegurar que el nuevo codigo no rompera el sistema antes de aceptarlo.

---

## Ejecución de scripts en CI

### Un entorno desde cero
Cada vez que GitHub Actions inicia un job, levanta una maquina virtual limpia. Por lo tanto, debemos darle instrucciones paso a paso, al igual que hariamos en una computadora nueva:

1. **Checkout del código:** Traer los archivos del repositorio a la maquina virtual.
2. **Configurar Python:** Instalar la version correcta de Python.
3. **Instalar dependencias:** Ejecutar `pip install -r requirements.txt`.
4. **Ejecutar el script:** Correr nuestro codigo (ej. `python src/transformacion.py`).

Si el script de Python termina con un error (exit code distinto de cero), GitHub Actions marcara el trabajo como fallido (una X roja).

---

## Validación automática de código

### Asegurando la calidad antes de integrar
Antes de ejecutar el pipeline de datos en si, la automatizacion de codigo (CI) se utiliza para aplicar controles de calidad.

### Prácticas comunes:
* **Linter (ej. Flake8 o Pylint):** Analiza el codigo buscando errores de sintaxis o violaciones a las convenciones de estilo (PEP 8).
* **Formateadores (ej. Black):** Verifica que el codigo tenga el formato correcto.
* **Pruebas unitarias (ej. Pytest):** Ejecuta funciones aisladas del pipeline para comprobar que devuelven el resultado esperado.

Implementar estas validaciones garantiza que solo el codigo estructurado y funcional llegue a produccion.

---

## Integración CI con pipelines de datos

### Pipelines de código vs Pipelines de datos
Es crucial entender la diferencia y como interactuan:
* **Pipeline de código (CI/CD):** Mueve el *código fuente* desde el repositorio hasta el entorno de produccion.
* **Pipeline de datos:** Mueve y transforma los *datos* (Extract >> Transform >> Load).

### La integración
El CI/CD protege al pipeline de datos. Cuando modificamos una regla de negocio en Python (ej. cambiar como se calculan los impuestos en las transacciones), el pipeline de codigo (CI) ejecutara pruebas con datos falsos de muestra. Solo si estas pruebas pasan, la nueva logica se desplegara, actualizando el pipeline de datos real.

---

## Beneficios de CI/CD en proyectos reales

### Impacto en la Ingeniería de Datos
* **Confiabilidad:** Menos sorpresas en produccion. Sabemos que si el codigo paso la integracion continua, cumple con los estandares de calidad.
* **Velocidad de desarrollo:** Los ingenieros dedican menos tiempo a configurar entornos y desplegar de forma manual, enfocandose en crear valor (transformar datos).
* **Trazabilidad:** Cualquier fallo queda registrado en los logs de GitHub Actions. Si una subida de codigo rompio algo, es facil saber quien lo hizo, que cambios introdujo y revertirlo rapidamente.
* **Cultura de calidad:** Fomenta la escritura de codigo modular y testeable, atributos fundamentales de un buen pipeline de datos.

---

<!-- _class: code -->
## Practica: Crear un workflow de GitHub Actions para el pipeline

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar ci/cd con github actions con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap6/6_11_2_Script.py
import os
import random

# Configurar semilla aleatoria
random.seed(987654)

# -----------------------------------------------------------------------------
# ST1, ST2, ST3, ST4: Conceptos de CI/CD y Automatización de procesos de código
# En este script vamos a generar la estructura de archivos necesaria para 
# simular y configurar un flujo de Integración Continua (CI) básico localmente,
# preparándolo para su uso en un repositorio real.
# -----------------------------------------------------------------------------

def generar_estructura_directorios():
    """
    Generar la estructura de carpetas requerida para el flujo de GitHub Actions
    y los scripts del proyecto de datos.
    """

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap6/6_11_2_Script.py`

---

## Errores comunes en el Bloque 6.11.2

- **Hardcodear credenciales en el .yml del workflow**
  → expuestas en el historial de git

- **No definir qué rama dispara el workflow**
  → CI corre en branches de prueba

- **No verificar el exit code del pipeline en el workflow**
  → CI siempre pasa aunque el pipeline falle

---

## Resumen: Bloque 6.11.2

**Lo que aprendiste:**
- Crear un workflow de GitHub Actions que ejecuta el pipeline en cada push
- Configurar secretos de GitHub para credenciales de BD y servicios
- Entender el ciclo CI (test) → CD (deploy) en el contexto del pipeline

**Lo que construiste:**
El script `6_11_2_Script.py` que crear un workflow de github actions para el pipeline usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 6.11.3: Monitoreo (logs, health checks)

---

<!-- ============================================================ -->
<!-- BLOQUE 6.11.3 — Monitoreo (logs, health checks)              -->
<!-- Scripts: scripts/cap6/6_11_3_Script.py                    -->
<!-- Notebook: notebooks/cap6/6_11_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 6.11.3
## Monitoreo (logs, health checks)

> El pipeline corre en CI/CD; ahora monitoreamos su salud en tiempo real.

**Al terminar este bloque podrás:**
- Implementar health checks que verifican la BD, el storage y el API
- Centralizar los logs en un sistema consultable (archivo rotado o servicio)
- Definir métricas clave del pipeline (rows procesadas, latencia, errores)

---

# Capítulo 6: Integración, despliegue y proyecto final, Sesión 11: CI/CD y monitoreo, Bloque 3: Monitoreo (logs, health checks)

## Introducción al monitoreo en sistemas de datos

Cuando construimos un pipeline de datos o una API, nuestro trabajo no termina al desplegar el código. En un entorno real, los sistemas fallan: las bases de datos se desconectan, los archivos CSV llegan corruptos o los servidores se quedan sin memoria.

El monitoreo es la práctica de observar continuamente el estado y el comportamiento de nuestros sistemas. En ingeniería de datos, esto significa tener visibilidad sobre:
* El estado de las ingestas de datos (¿terminaron a tiempo?).
* La calidad de las transformaciones (¿hubo registros descartados?).
* La disponibilidad de nuestras APIs de consumo.

Sin monitoreo, operamos a ciegas. Nos enteraremos de los errores únicamente cuando el usuario final se queje de que los datos no están actualizados.

---

## Diferencia entre Logging y Monitoreo

Es común confundir estos términos, pero cumplen funciones distintas y complementarias en nuestro ecosistema de datos.

**Logging (Registro de eventos):**
* Es la acción de escribir mensajes descriptivos sobre lo que está ocurriendo en el código en un momento específico.
* Responde a la pregunta: *¿Qué evento acaba de ocurrir y cuál es su contexto?*
* Ejemplo: "Se inició la lectura del archivo ventas.csv a las 10:00 AM".

**Monitoreo:**
* Es la recolección, agregación y análisis de métricas y logs a lo largo del tiempo para evaluar la salud general del sistema.
* Responde a la pregunta: *¿El sistema está funcionando correctamente en este momento?*
* Ejemplo: "La tasa de uso de CPU ha superado el 90% durante los últimos 5 minutos".

---

## El Concepto de Observabilidad

La observabilidad es un paso más allá del monitoreo tradicional. Mientras que el monitoreo nos avisa que algo falló (por ejemplo, un dashboard en rojo), la observabilidad nos permite entender **por qué** falló basándonos en los datos que el propio sistema genera.

Un sistema es "observable" si podemos entender su estado interno únicamente mirando sus salidas externas (logs, métricas y trazas).

Para lograr observabilidad en nuestros pipelines, necesitamos instrumentar el código desde el principio, asegurándonos de que cada paso crítico genere información útil y estructurada que podamos consultar cuando las cosas salgan mal.

---

## Logs Estructurados

En los primeros scripts, usábamos `print()` para ver qué pasaba. En producción, esto es insuficiente. Un log estructurado es un registro de eventos que tiene un formato predecible, generalmente JSON, lo que permite que otras herramientas lo lean y filtren automáticamente.

**Log tradicional (Texto plano):**
`2026-04-28 10:00:05 - Error al procesar el cliente 15234 por tipo de dato incorrecto.`

**Log estructurado (JSON):**
```json
{
  "timestamp": "2026-04-28T10:00:05Z",
  "level": "ERROR",
  "module": "transformacion_clientes",
  "cliente_id": 15234,
  "mensaje": "Tipo de dato incorrecto en columna 'edad'",
  "codigo_error": "TYPE_ERR_01"
}
```

Los logs estructurados permiten realizar búsquedas complejas, como: *Muéstrame todos los errores del módulo "transformacion_clientes" en la última hora.*

---

## Niveles de Log

Para no inundar nuestros sistemas con información irrelevante, los logs se clasifican por niveles de severidad. Esto nos permite filtrar qué queremos ver dependiendo del entorno (desarrollo vs. producción).

* **DEBUG:** Información muy detallada, útil solo para diagnosticar problemas durante el desarrollo.
* **INFO:** Confirma que las cosas funcionan como se esperaba. Ej. "Pipeline finalizado con éxito".
* **WARNING:** Indica que ocurrió algo inesperado, pero el sistema puede seguir funcionando. Ej. "Falta el valor 'correo', se usó un valor por defecto".
* **ERROR:** Un problema más grave que impidió que una función específica se ejecutara. Ej. "Fallo de conexión a la base de datos MySQL al intentar insertar registros".
* **CRITICAL:** Un error catastrófico que detiene por completo la ejecución del programa.

---

## Implementación de Logging en Scripts y APIs

Python incluye una librería estándar llamada `logging` que facilita la implementación de registros con niveles y formatos.

**Ejemplo en un script de pipeline:**
```python
import logging

# Configuración básica
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("PipelineIngesta")

def procesar_datos():
    logger.info("Iniciando el procesamiento de datos...")
    try:
        # Lógica de procesamiento
        resultado = 10 / 0
    except ZeroDivisionError as e:
        logger.error(f"Fallo en la transformación matemática: {e}")

procesar_datos()
```
En una API con FastAPI, podemos usar esta misma lógica para registrar cada petición, cuánto tiempo tardó y si devolvió un error, manteniendo un rastro auditable de las operaciones.

---

## Endpoint de Salud (/health)

En el mundo de las APIs y los contenedores, un "Health Check" (verificación de salud) es un endpoint específico diseñado únicamente para decirnos si la aplicación está viva y lista para recibir tráfico.

Por convención, suele ser una ruta `GET /health`.

**Ejemplo en FastAPI:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    # Aquí podríamos verificar si hay conexión a la base de datos
    return {"status": "ok", "message": "API funcionando correctamente"}
```

Herramientas como Docker, Kubernetes o balanceadores de carga consultan este endpoint constantemente (por ejemplo, cada 10 segundos). Si el endpoint devuelve un error (ej. HTTP 500) o tarda demasiado, el sistema de orquestación sabe que el contenedor falló y puede reiniciarlo automáticamente.

---

## Detección de fallos en sistemas

La combinación de un endpoint de salud y logs bien definidos nos da un mecanismo robusto para detectar fallos.

Cuando el sistema de orquestación (o una herramienta externa) nota que el endpoint `/health` dejó de responder `{"status": "ok"}`, levanta una alerta. En ese momento, el ingeniero de datos entra a revisar los logs.

Gracias a que usamos niveles de log (buscamos directamente los `ERROR` o `CRITICAL`) y, de ser posible, logs estructurados, podemos identificar rápidamente si el fallo se debe a una caída de la base de datos, a un problema de memoria, o a un cambio inesperado en el formato de los datos de entrada.

---

## Concepto de Métricas (Intro)

Mientras que los logs nos cuentan "la historia" de eventos discretos, las métricas son medidas numéricas tomadas a lo largo del tiempo. 

En un pipeline de datos, nos interesan métricas como:
* **Duración:** ¿Cuántos segundos tardó el proceso de limpieza?
* **Volumen:** ¿Cuántos registros se procesaron por minuto?
* **Tasa de errores:** ¿Qué porcentaje de peticiones a la API devolvieron un código 400 o 500?
* **Recursos:** Consumo de CPU y memoria RAM.

Las métricas nos ayudan a establecer una línea base de rendimiento. Si nuestro pipeline usualmente procesa 10,000 registros por segundo y de repente baja a 500, sabemos que hay un problema de rendimiento, incluso si no hay errores explícitos en los logs.

---

## Introducción a Herramientas (Prometheus conceptual)

Para recolectar y almacenar métricas de forma eficiente, la industria utiliza herramientas especializadas. **Prometheus** es el estándar de facto en el mundo del monitoreo moderno.

¿Cómo funciona a nivel conceptual?
1. Nuestra API o pipeline expone un endpoint (generalmente `/metrics`) que muestra las métricas actuales en un formato de texto específico.
2. Prometheus actúa como un "scraper": se conecta a ese endpoint cada ciertos segundos y guarda los valores en su propia base de datos optimizada para series temporales.
3. Posteriormente, herramientas de visualización (como Grafana) leen los datos de Prometheus y generan dashboards en tiempo real con gráficos y alertas visuales.

Esto desacopla la generación de métricas (responsabilidad de nuestro código Python) del almacenamiento y alerta de las mismas (responsabilidad de Prometheus).

---

## Importancia de Monitoreo en Producción

El paso de un entorno local a uno de producción marca un cambio en nuestras responsabilidades. En producción, la confiabilidad de los datos es crítica para el negocio.

Razones clave para implementar monitoreo sólido:
1. **Resolución proactiva:** Solucionar los problemas antes de que afecten a los equipos de análisis o a los clientes finales.
2. **Confianza en los datos:** Si no sabemos si el pipeline se ejecutó correctamente, no podemos garantizar la veracidad de los reportes.
3. **Capacidad de escalar:** Las métricas nos indican cuándo nuestros servidores se están quedando pequeños frente al aumento del volumen de datos.

Un pipeline sin monitoreo, logs estructurados ni health checks es una bomba de tiempo. Al integrar estas prácticas, pasamos de hacer simples scripts a crear software de ingeniería de datos profesional y resiliente.

---

<!-- _class: code -->
## Practica: Implementar health checks y centralización de logs

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar monitoreo (logs, health checks) con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap6/6_11_3_Script.py
"""
Script demostrativo para implementar monitoreo basico,
logs estructurados y un endpoint de health check usando FastAPI.
"""

import json
import logging
import random
import time
import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configurar semilla aleatoria para consistencia en simulaciones
random.seed(987654)

# =============================================================================

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap6/6_11_3_Script.py`

---

## Errores comunes en el Bloque 6.11.3

- **No tener un endpoint /health en la API**
  → los balanceadores no saben si el servicio vive

- **Mezclar logs de diferentes componentes en el mismo archivo**
  → imposible filtrar

- **No establecer alertas**
  → el equipo se entera de los fallos por los usuarios

---

## Resumen: Bloque 6.11.3

**Lo que aprendiste:**
- Implementar health checks que verifican la BD, el storage y el API
- Centralizar los logs en un sistema consultable (archivo rotado o servicio)
- Definir métricas clave del pipeline (rows procesadas, latencia, errores)

**Lo que construiste:**
El script `6_11_3_Script.py` que implementar health checks y centralización de logs usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 6.11.4: Seguimiento del proyecto

---

<!-- ============================================================ -->
<!-- BLOQUE 6.11.4 — Seguimiento del proyecto                     -->
<!-- Scripts: scripts/cap6/6_11_4_Script.py                    -->
<!-- Notebook: notebooks/cap6/6_11_4_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 6.11.4
## Seguimiento del proyecto

> Con el pipeline en producción, establecemos cómo hacer seguimiento del progreso del proyecto.

**Al terminar este bloque podrás:**
- Usar GitHub Issues y Projects para gestionar el backlog del pipeline
- Documentar decisiones técnicas en el README y en ADRs
- Establecer un proceso de code review para cambios en el pipeline

---

# Capítulo 6: Integración, despliegue y proyecto final, Sesión 11: CI/CD y monitoreo, Bloque 4: Seguimiento del proyecto

## Seguimiento del Proyecto Final

El proyecto final es la culminación de todos los conceptos aprendidos a lo largo del curso. En esta etapa, el objetivo principal es consolidar el conocimiento mediante la construcción de una solución de datos funcional.

El seguimiento continuo permite identificar bloqueos tempranos y asegurar que el desarrollo se mantenga alineado con los requerimientos técnicos. Un proyecto de ingeniería de datos requiere planificación, ya que involucra múltiples piezas móviles que deben comunicarse de manera eficiente.

Durante esta fase, es fundamental priorizar el progreso iterativo: construir una versión básica que funcione y, posteriormente, agregar complejidad o robustez al sistema.

---

## Revisión de Arquitectura del Proyecto

Antes de escribir código o configurar contenedores, la arquitectura del proyecto debe estar claramente definida. Un buen diseño arquitectónico sirve como mapa para el desarrollo.

Elementos clave a revisar en la arquitectura:
* **Origen de datos:** ¿De dónde provienen los datos? (Archivos CSV, APIs externas, bases de datos).
* **Procesamiento:** ¿Qué transformaciones se aplicarán usando Python y Pandas?
* **Almacenamiento:** ¿Dónde residirán los datos procesados? (MySQL, archivos Parquet/CSV en la nube o local).
* **Consumo:** ¿Cómo se accederá a la información? (A través de una API con FastAPI o un Dashboard con Streamlit).

Tener un diagrama claro (por ejemplo: Extracción >> Limpieza >> Carga >> API >> Dashboard) previene problemas de integración en etapas posteriores.

---

## Validación de Componentes (Pipeline, API, Dashboard)

Un proyecto robusto se construye asegurando que cada componente funcione correctamente de manera aislada antes de intentar unirlos.

* **Pipeline de Datos:** Debe ser capaz de leer datos crudos, aplicar las reglas de limpieza (manejo de nulos, corrección de tipos) y guardar el resultado sin errores. Se debe verificar que los datos resultantes tengan la forma y calidad esperada.
* **API (FastAPI):** Los endpoints deben responder correctamente (código HTTP 200). Se debe validar que los contratos de datos (JSON) retornen la información precisa y que los filtros funcionen adecuadamente.
* **Dashboard (Streamlit):** La interfaz debe cargar sin errores de compilación, mostrando métricas coherentes. Los gráficos deben reflejar la realidad de los datos procesados, sin distorsionar la información.

---

## Resolución de Dudas Técnicas

Durante la construcción del proyecto es común enfrentarse a desafíos técnicos. Esta etapa está diseñada para resolver los cuellos de botella más frecuentes.

Problemas comunes a resolver:
* **Conexiones a bases de datos:** Errores de autenticación, puertos bloqueados o cadenas de conexión mal formateadas.
* **Contenedores y Docker:** Problemas de red interna (docker-compose) donde la API no logra "ver" a la base de datos.
* **Manejo de dependencias:** Conflictos en el archivo requirements.txt o librerías incompatibles entre el entorno local y el contenedor.
* **Lógica de Pandas:** Transformaciones complejas o agrupaciones que retornan valores inesperados (DataFrames vacíos o con índices desalineados).

Abordar estos errores de manera metódica (revisando logs y aislando el fallo) es una habilidad esencial en la ingeniería de datos.

---

## Integración de Módulos

Una vez que los componentes individuales funcionan, el siguiente paso es la integración. Un módulo aislado no aporta valor si no se comunica con el resto del ecosistema.

El flujo de integración debe probarse paso a paso:
1. El script de ingesta descarga o lee los datos.
2. El script de transformación los procesa y los inserta en la base de datos (MySQL).
3. La API se conecta a MySQL y expone los datos transformados.
4. El Dashboard consume los endpoints de la API para visualizar los datos.

La clave de una buena integración es el uso de variables de entorno y archivos de configuración para evitar "hardcodear" rutas locales o credenciales de acceso, permitiendo que los módulos interactúen fluidamente.

---

## Validación de Funcionalidad End-to-End

La prueba end-to-end (de extremo a extremo) garantiza que el sistema completo cumple su propósito desde el origen hasta el consumidor final.

Para validar el sistema completo se debe simular un escenario real:
* ¿Qué sucede si se ingresa un nuevo archivo CSV en la carpeta de origen?
* Al ejecutar el pipeline maestro, ¿los datos fluyen hasta la base de datos de manera transparente?
* Al recargar el dashboard, ¿se actualizan los gráficos con la información recién ingresada?
* ¿Los logs muestran un rastro claro de que todo el proceso finalizó con éxito?

Esta validación confirma que no hemos construido solo scripts sueltos, sino un verdadero producto de datos automatizado y conectado.

---

## Mejores Prácticas de Presentación

Saber comunicar el valor técnico de una solución es tan importante como construirla. La presentación del proyecto final no debe ser solo un recorrido por el código fuente.

Estructura recomendada para presentar:
* **Contexto y Problema:** Explicar qué datos se están analizando y qué problema de negocio se busca resolver.
* **Arquitectura de la Solución:** Mostrar el diagrama de flujo de los datos (Ingesta >> Transformación >> Almacenamiento >> Consumo).
* **Decisiones Técnicas:** Explicar por qué se eligió cierta base de datos, por qué se particionaron los archivos o cómo se diseñaron los endpoints.
* **Demostración:** Mostrar el sistema funcionando.

El objetivo es demostrar dominio sobre la ingeniería de datos y la capacidad de traducir problemas técnicos en soluciones comprensibles.

---

## Ajustes Finales

Antes de considerar el proyecto como terminado, es necesario realizar una revisión exhaustiva del código y del entorno. Los detalles marcan la diferencia entre un prototipo y un proyecto profesional.

Lista de ajustes comunes:
* **Limpieza de código:** Eliminar sentencias "print" residuales, código comentado y variables no utilizadas.
* **Refactorización:** Asegurar que las funciones tengan un único propósito y nombres descriptivos.
* **Gestión de secretos:** Validar que ninguna contraseña, token o credencial esté en el código fuente. Se deben utilizar archivos .env.
* **Manejo de errores:** Confirmar que existen bloques try/except donde el sistema es susceptible a fallar (conexiones a red, lectura de archivos).

---

## Checklist de Entrega

Para asegurar que el proyecto cumple con todos los requerimientos, se debe verificar contra un checklist estructurado.

Elementos indispensables del entregable:
* **Repositorio de Código:** Estructura de carpetas limpia (separando src, data, notebooks, etc.).
* **Archivo README.md:** Documentación clara sobre el proyecto, cómo instalarlo y cómo ejecutarlo.
* **Gestión de Entorno:** Archivo requirements.txt actualizado con las versiones exactas de las librerías.
* **Contenedores (si aplica):** Dockerfile y docker-compose.yaml funcionales.
* **Scripts de Pipeline:** Código de extracción, transformación y carga (ETL).
* **Capa de Consumo:** Código de la API (FastAPI) o aplicación visual (Streamlit).

Si un tercero descarga el repositorio y sigue las instrucciones del README, el proyecto debería levantarse sin errores.

---

## Preparación para Demo

La demostración en vivo (Live Demo) es el momento crítico de la presentación. Requiere preparación para minimizar riesgos, ya que los entornos pueden fallar en el momento menos oportuno.

Consejos para una demo exitosa:
* **Limpiar el entorno:** Partir de un estado limpio (base de datos vacía o en estado inicial) para mostrar cómo el pipeline carga los datos.
* **Script de ejecución:** Tener los comandos listos para copiar y pegar, o mejor aún, un archivo Makefile o script bash (ej. run.sh) que levante todo.
* **Plan de contingencia:** Si un servicio como Docker falla por falta de memoria o la base de datos no levanta, tener capturas de pantalla o un video pregrabado del sistema funcionando como respaldo.
* **Pausas explicativas:** Mientras un proceso largo se ejecuta (como la descarga de una imagen Docker o una transformación pesada), aprovechar para explicar qué está sucediendo en segundo plano.

---

## Enfoque en Claridad y Funcionalidad

El objetivo principal de la evaluación del proyecto no es la complejidad innecesaria, sino la funcionalidad sólida y la claridad conceptual.

* **Menos es más:** Es preferible un pipeline sencillo que extrae, limpia y guarda datos de manera impecable y robusta, a un sistema extremadamente complejo lleno de errores de ejecución.
* **Robustez sobre cantidad:** Un solo endpoint de API bien diseñado, validado con Pydantic y que maneja errores HTTP adecuadamente, vale más que diez endpoints frágiles.
* **Claridad:** El código debe ser legible, la arquitectura debe tener sentido lógico y la presentación debe comunicar el valor del trabajo realizado.

La ingeniería de datos busca construir sistemas confiables; la claridad y la funcionalidad son los pilares fundamentales para lograrlo.

---

## Seguimiento del proyecto

> **Bloque de demostración** — el instructor ejecuta en vivo.
> No hay script para correr en este bloque.

---

## Errores comunes en el Bloque 6.11.4

- **No documentar las decisiones de diseño**
  → el equipo no entiende por qué se hizo así

- **No revisar el código antes de mergear a main**
  → bugs en producción

- **No tener un proceso de rollback definido**
  → imposible recuperarse de un deploy fallido

---

## Resumen: Bloque 6.11.4

**Lo que aprendiste:**
- Usar GitHub Issues y Projects para gestionar el backlog del pipeline
- Documentar decisiones técnicas en el README y en ADRs
- Establecer un proceso de code review para cambios en el pipeline

**Lo que construiste:**
Comprendiste los conceptos de seguimiento del proyecto a través de la demostración.

**Siguiente paso →** Bloque 6.12.1: Presentación de proyectos (parte 1)

---

<!-- _class: section -->
# Sección 12: Presentación de proyecto e IA aplicada
## En esta sección construiremos la capa de presentación de proyecto e ia aplicada del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de presentación de proyecto e ia aplicada en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 6.12.1: Presentación de proyectos (parte 1)
- Bloque 6.12.2: Presentación de proyectos (parte 2)
- Bloque 6.12.3: IA como acelerador de ingeniería

---

<!-- ============================================================ -->
<!-- BLOQUE 6.12.1 — Presentación de proyectos (parte 1)          -->
<!-- Scripts: scripts/cap6/6_12_1_Script.py                    -->
<!-- Notebook: notebooks/cap6/6_12_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 6.12.1
## Presentación de proyectos (parte 1)

> Llegamos al final del curso: presentamos lo construido ante el grupo.

**Al terminar este bloque podrás:**
- Estructurar una demo técnica de 10 minutos del pipeline propio
- Mostrar el flujo end-to-end: extracción, transformación, carga y visualización
- Recibir y dar feedback constructivo sobre los proyectos

---

## Estructura de la Presentación de Proyectos

La presentación de un proyecto de ingeniería de datos no solo trata de mostrar código, sino de contar la historia de cómo los datos se transformaron en valor. Para que una presentación técnica sea exitosa, debe seguir una estructura lógica que guíe a la audiencia desde el contexto inicial hasta el resultado final.

Una estructura recomendada para proyectos de datos incluye los siguientes puntos:
1. Contexto inicial y definición del problema.
2. Propuesta de solución.
3. Arquitectura del sistema y herramientas utilizadas.
4. Explicación detallada del flujo de datos.
5. Demostración en vivo (Demo).
6. Conclusiones y lecciones aprendidas.

Mantener este orden asegura que tanto perfiles técnicos como de negocio puedan comprender el valor de lo que hemos construido.

---

## Definición del Problema

Todo pipeline de datos nace de una necesidad. Antes de hablar de bases de datos, contenedores o APIs, es fundamental establecer qué problema estamos resolviendo.

Al definir el problema, debemos responder a preguntas clave:
* ¿De dónde provienen los datos originales y en qué estado se encuentran?
* ¿Qué limitaciones tiene el acceso o análisis de estos datos en su estado actual?
* ¿Quién es el usuario final (un analista, una aplicación, un modelo de machine learning)?

Ejemplo: "Actualmente, los registros de transacciones se generan en archivos CSV dispersos con valores nulos y formatos de fecha inconsistentes, lo que impide calcular métricas financieras diarias de forma confiable."

---

## Explicación de la Solución

Una vez claro el problema, pasamos a definir qué hemos construido para solucionarlo. En esta etapa, el enfoque debe mantenerse a un alto nivel, sin entrar todavía en detalles de código.

La explicación de la solución debe detallar:
* Qué tipo de producto de datos entregamos (un pipeline automatizado, una API para consumo en tiempo real, un dashboard interactivo).
* Cómo esta solución mitiga el problema planteado inicialmente.
* El impacto de la solución (por ejemplo, reducir el tiempo de procesamiento de horas a segundos, o garantizar la integridad de los datos).

Es el momento de conectar la necesidad técnica con el valor real aportado.

---

## Arquitectura del Sistema

La arquitectura es el mapa de nuestra solución. Aquí presentamos los componentes tecnológicos que hacen posible el funcionamiento del proyecto.

En un proyecto de ingeniería de datos, la arquitectura suele dividirse en capas:
* **Extracción (Ingesta):** Lectura de APIs externas o archivos locales (CSV/Parquet).
* **Procesamiento:** Transformación y limpieza utilizando Python y Pandas.
* **Almacenamiento:** Bases de datos relacionales (MySQL) o almacenamiento en la nube (S3/GCS).
* **Exposición:** APIs creadas con FastAPI o dashboards con Streamlit.
* **Despliegue:** Contenerización del entorno usando Docker y Docker Compose.

Visualizar estas piezas conectadas ayuda a dimensionar la complejidad y el alcance del trabajo realizado.

---

## Flujo de Datos

A diferencia de la arquitectura, que muestra las herramientas, el flujo de datos explica el ciclo de vida de la información. Es el viaje de los datos desde su origen hasta su destino final.

Debemos explicar paso a paso qué ocurre con la información:
1. **Estado Crudo (Raw):** Cómo ingresan los datos al sistema.
2. **Transformación:** Qué reglas de negocio se aplican (ej. filtrado de clientes inactivos, conversión de divisas, manejo de nulos).
3. **Persistencia:** Cómo se estructuran las tablas o archivos resultantes.
4. **Consumo:** Qué consultas SQL se ejecutan o qué endpoints se consumen para obtener el resultado final.

El concepto clave es la trazabilidad: entender exactamente qué le pasa a un dato específico a lo largo de todo el pipeline (desde el origen >> transformación >> destino).

---

## Demostración Funcional (Demo)

La demostración en vivo es el momento de probar que el sistema funciona. En ingeniería de datos, una demo exitosa suele mostrar el sistema ejecutándose de extremo a extremo.

Puntos clave a mostrar durante una demo:
* Ejecución del script principal o activación del orquestador (ej. Airflow o script Python automatizado).
* Verificación en la base de datos de que los registros se insertaron correctamente (mostrando un SELECT en MySQL).
* Consumo de un endpoint de la API usando el navegador o Swagger UI, demostrando que los datos procesados están disponibles.
* Visualización del dashboard actualizándose con los nuevos datos.

Una regla de oro en las demos: tener siempre un entorno de respaldo o datos pre-procesados en caso de que ocurra un error inesperado.

---

## Justificación de Decisiones Técnicas

En ingeniería, rara vez hay una única forma correcta de hacer las cosas. Gran parte del valor de un ingeniero de datos radica en su capacidad para tomar decisiones informadas y justificarlas.

Durante la presentación, es vital explicar el por qué detrás de la implementación:
* ¿Por qué usamos Parquet en lugar de CSV para el almacenamiento intermedio? (Respuesta: eficiencia en lectura columnar y menor tamaño de almacenamiento).
* ¿Por qué dividimos el pipeline en módulos en lugar de un solo script largo? (Respuesta: mantenibilidad y separación de responsabilidades).
* ¿Por qué usamos Docker? (Respuesta: para garantizar que el entorno sea reproducible sin importar la máquina en la que se ejecute).

Justificar las decisiones demuestra madurez técnica y comprensión profunda de las herramientas.

---

## Comunicación Efectiva

Saber comunicar el trabajo técnico es tan importante como escribir buen código. Un pipeline perfectamente optimizado pierde valor si no podemos explicar su utilidad a los interesados en el proyecto.

Estrategias para una comunicación técnica efectiva:
* **Conocer a la audiencia:** Ajustar el nivel de detalle técnico según quién escucha.
* **Narrativa (Storytelling):** Usar un hilo conductor. Empezar con un problema que afecta al negocio y mostrar cómo el pipeline es la pieza clave que lo resuelve.
* **Claridad visual:** Evitar diapositivas llenas de código diminuto o ilegible. Es preferible mostrar diagramas claros de arquitectura y pequeños bloques lógicos de entrada >> salida de datos.

---

## Evaluación por Criterios

La presentación del proyecto se evalúa de manera integral, considerando no solo si el código funciona o no, sino cómo fue diseñado y construido basándose en el aprendizaje del curso.

Los criterios principales de evaluación incluyen:
* **Funcionalidad End-to-End:** El pipeline debe poder extraer, transformar y cargar datos de manera continua.
* **Calidad del Código:** Uso adecuado de funciones, modularidad, manejo de excepciones (try/except) y código descriptivo.
* **Arquitectura y Entorno:** Uso correcto de gestión de dependencias (requirements.txt) e infraestructura aislada (Docker).
* **Claridad en la Exposición:** Capacidad para articular el diseño del sistema y responder a las preguntas técnicas con seguridad.

---

## Identificación de Fortalezas

Cada proyecto tiene áreas donde destaca particularmente. Identificar y resaltar estas fortalezas es parte importante de la evaluación y del crecimiento profesional.

Algunos ejemplos de fortalezas técnicas a destacar:
* **Robustez en la ingesta:** Implementación de validaciones exhaustivas de tipos de datos antes del procesamiento.
* **Eficiencia:** Uso correcto de operaciones vectorizadas en Pandas, evitando iteraciones innecesarias sobre los datos.
* **Usabilidad:** Creación de APIs bien documentadas y con filtros dinámicos que facilitan el consumo de datos.
* **Despliegue:** Archivos de orquestación (docker-compose) claros que levantan toda la infraestructura de una vez sin configuraciones extrañas.

Reconocer estas áreas ayuda a afianzar las buenas prácticas desarrolladas durante las sesiones.

---

## Aprendizajes Obtenidos

Todo proyecto real implica enfrentarse a obstáculos y salir de la zona de confort. La ingeniería de datos se aprende en gran medida solucionando errores de red, dependencias rotas o formatos de datos imprevistos.

En esta sección de cierre, se reflexiona sobre:
* Los mayores desafíos encontrados (por ejemplo, hacer que el contenedor de FastAPI se comunicara exitosamente con el contenedor de MySQL).
* Cómo se resolvieron esos problemas (lectura de documentación técnica, debugging paso a paso).
* Mejoras para una próxima versión del proyecto (V2): agregar Airflow para orquestación compleja, implementar tests automatizados o migrar el almacenamiento de local a la nube.

Reconocer los errores, aprender de ellos y saber cómo mejorar el sistema es la marca distintiva de un buen ingeniero de datos.

---

## Presentación de proyectos (parte 1)

> **Bloque de demostración** — el instructor ejecuta en vivo.
> No hay script para correr en este bloque.

---

## Errores comunes en el Bloque 6.12.1

- **Hacer una demo sin datos reales cargados**
  → la presentación pierde impacto

- **No tener un plan B si el entorno falla durante la demo**

- **No mostrar el código, solo la UI**
  → el evaluador no puede verificar la implementación

---

## Resumen: Bloque 6.12.1

**Lo que aprendiste:**
- Estructurar una demo técnica de 10 minutos del pipeline propio
- Mostrar el flujo end-to-end: extracción, transformación, carga y visualización
- Recibir y dar feedback constructivo sobre los proyectos

**Lo que construiste:**
Comprendiste los conceptos de presentación de proyectos (parte 1) a través de la demostración.

**Siguiente paso →** Bloque 6.12.2: Presentación de proyectos (parte 2)

---

<!-- ============================================================ -->
<!-- BLOQUE 6.12.2 — Presentación de proyectos (parte 2)          -->
<!-- Scripts: scripts/cap6/6_12_2_Script.py                    -->
<!-- Notebook: notebooks/cap6/6_12_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 6.12.2
## Presentación de proyectos (parte 2)

> Continuamos con las presentaciones y el intercambio de aprendizajes del grupo.

**Al terminar este bloque podrás:**
- Presentar el componente más desafiante del proyecto propio
- Identificar las similitudes y diferencias entre los proyectos del grupo
- Documentar los aprendizajes clave en el README del proyecto

---

# Capítulo 6: Integración, despliegue y proyecto final, Sesión 12: Presentación de proyecto e IA aplicada, Bloque 2: Presentación de proyectos (parte 2)

## Continuación de las Presentaciones de Proyectos

* Retomamos el espacio para la exposición de los proyectos finales desarrollados durante el curso.
* Cada proyecto representa la culminación del trabajo práctico y la aplicación directa de los conceptos de ingeniería de datos.
* El objetivo principal de esta sesión no es solo evaluar, sino observar cómo el conocimiento técnico (ingesta, transformación, almacenamiento y consumo) se ha materializado en soluciones reales y funcionales.
* Presten especial atención a cómo cada equipo estructuró su lógica de procesamiento y resolvió los problemas de datos inconsistentes.

---

## Comparación de Enfoques y Rutas de Solución

* En la ingeniería de datos rara vez existe una única respuesta correcta; un mismo problema puede abordarse desde múltiples ángulos.
* Durante estas presentaciones, analizaremos las diferencias entre las rutas elegidas por los alumnos:
  * **Enfoque en Pipeline (ETL puro):** Mayor énfasis en la limpieza profunda, uso de Parquet, bases de datos robustas y modularidad extrema.
  * **Enfoque en API (Consumo):** Foco en FastAPI, validaciones con Pydantic y respuestas rápidas para integraciones con otros sistemas.
  * **Enfoque en Visualización (Dashboard):** Prioridad en Streamlit, generación de KPIs claros y experiencia del usuario final.
* Comparar estas arquitecturas nos permite entender la flexibilidad y el alcance de las herramientas vistas en el curso.

---

## Observación de Patrones Comunes

* A medida que revisamos diferentes repositorios y soluciones, se hacen evidentes ciertos patrones de diseño.
* **Patrones recurrentes observados:**
  * Uso estandarizado de Pandas para la limpieza de datos y manejo de valores nulos.
  * Estructuración del pipeline en fases claras: Extracción >> Transformación >> Carga.
  * Integración casi universal de archivos CSV o Parquet como almacenamiento de resultados intermedios.
* Identificar estos patrones es fundamental, ya que representan los estándares de la industria y la forma en que los ingenieros de datos suelen estructurar su pensamiento.

---

## Retroalimentación entre Pares y Aprendizaje Colaborativo

* El desarrollo de software y la construcción de infraestructuras de datos es un esfuerzo inherentemente colaborativo.
* **Feedback constructivo:** Fomentamos un ambiente donde los comentarios técnicos de los compañeros ayuden a mejorar el diseño y la calidad del código.
* **Valor del aprendizaje colaborativo:**
  * Conocer los errores que otros enfrentaron (por ejemplo, problemas de dependencias en Docker o fallos de conexión en MySQL) y cómo los solucionaron acelera nuestro propio aprendizaje.
  * Las preguntas técnicas enriquecen la sesión: ¿Por qué decidiste procesar fila por fila en lugar de usar operaciones vectorizadas? ¿Cómo garantizaste que no hubiera duplicados al insertar en SQL?

---

## Identificación de Mejores Prácticas

* A partir del código presentado, destacaremos las prácticas que elevan la calidad del proyecto de un simple script a una solución profesional.
* **Ejemplos de mejores prácticas a buscar en los proyectos:**
  * **Modularidad:** Separación clara entre los módulos de ingesta, lógica de negocio (transformación) y acceso a datos.
  * **Robustez:** Uso adecuado de bloques `try/except` y un manejo de errores que impida que el pipeline colapse ante un dato corrupto.
  * **Reproducibilidad:** Presencia de archivos `requirements.txt`, Dockerfiles bien estructurados y uso de variables de entorno.
* Incorporar estas prácticas desde etapas tempranas garantiza que el pipeline sea escalable y mantenible.

---

## Discusión de Mejoras Posibles y Evaluación Crítica

* Ningún sistema es perfecto en su primera iteración. Todo diseño implica compromisos (trade-offs) entre velocidad, costo y complejidad.
* **Áreas de mejora comunes:**
  * Optimización en el uso de memoria en Pandas (por ejemplo, ajustando los tipos de datos con `astype`).
  * Reducción de la complejidad en las consultas SQL expuestas en la API.
  * Mejor cobertura en el manejo de excepciones no controladas.
* **Evaluación crítica:** Analizaremos objetivamente si las tecnologías y arquitecturas elegidas fueron las más adecuadas para el volumen de datos y el caso de uso particular de cada proyecto.

---

## Reflexión sobre Decisiones Técnicas

* Un ingeniero de datos no solo escribe código; toma decisiones arquitectónicas que impactan a toda la organización.
* Durante la sesión, reflexionaremos sobre los "por qué" detrás de cada proyecto:
  * ¿Por qué almacenar en formato Parquet en lugar de CSV para la capa analítica?
  * ¿Se justificaba levantar una base de datos relacional para una ingesta de datos puramente temporal?
  * ¿Cómo se decidió qué endpoints de la API debían incluir parámetros de filtrado?
* Articular y defender estas decisiones es una habilidad crucial en entrevistas técnicas y en entornos de trabajo reales.

---

## Consolidación de Conocimiento y Cierre

* Estas presentaciones sirven como el repaso integral y definitivo del curso.
* Hemos transitado un largo camino: desde entender qué es una variable en Python y leer un archivo local, hasta orquestar un pipeline completo con validaciones, persistencia en base de datos y exposición web.
* **Consolidación:** Ver todas las piezas del rompecabezas (Python, SQL, Pandas, FastAPI, Streamlit, Docker) funcionando como un sistema interconectado demuestra un dominio práctico real.
* **Cierre de la etapa de proyectos:** Con los pipelines validados, estamos listos para el último paso conceptual del curso: descubrir cómo la Inteligencia Artificial puede integrarse en este flujo para acelerar el trabajo del ingeniero de datos.

---

## Presentación de proyectos (parte 2)

> **Bloque de demostración** — el instructor ejecuta en vivo.
> No hay script para correr en este bloque.

---

## Errores comunes en el Bloque 6.12.2

- **No practicar la demo antes**
  → superar el tiempo asignado

- **No mencionar los errores encontrados y cómo se resolvieron**
  → la presentación pierde valor educativo

- **No subir el código final a GitHub antes de presentar**
  → el instructor no puede revisar

---

## Resumen: Bloque 6.12.2

**Lo que aprendiste:**
- Presentar el componente más desafiante del proyecto propio
- Identificar las similitudes y diferencias entre los proyectos del grupo
- Documentar los aprendizajes clave en el README del proyecto

**Lo que construiste:**
Comprendiste los conceptos de presentación de proyectos (parte 2) a través de la demostración.

**Siguiente paso →** Bloque 6.12.3: IA como acelerador de ingeniería

---

<!-- ============================================================ -->
<!-- BLOQUE 6.12.3 — IA como acelerador de ingeniería             -->
<!-- Scripts: scripts/cap6/6_12_3_Script.py                    -->
<!-- Notebook: notebooks/cap6/6_12_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 6.12.3
## IA como acelerador de ingeniería

> Cerramos el curso explorando cómo la IA amplifica las capacidades del ingeniero de datos.

**Al terminar este bloque podrás:**
- Usar Claude/ChatGPT para generar scripts ETL, consultas SQL y DAGs de Airflow
- Entender los límites de la IA: no reemplaza la comprensión, la amplifica
- Identificar casos de uso concretos de IA en el día a día del ingeniero de datos

---

# Capítulo 6: Integración, despliegue y proyecto final, Sección 12: Presentación de proyecto e IA aplicada, Bloque 3: IA como acelerador de ingeniería

## Introducción a la IA y el Concepto de Copiloto

La Inteligencia Artificial generativa ha transformado la forma en que construimos software, incluyendo la ingeniería de datos. Herramientas basadas en Grandes Modelos de Lenguaje (LLMs) actúan hoy como "copilotos" de desarrollo.

Un copiloto no es un reemplazo del ingeniero, sino un asistente avanzado que programa a tu lado. Ayuda a autocompletar código, sugerir arquitecturas y redactar documentación.

El objetivo principal es delegar la escritura de código repetitivo a la máquina, permitiendo que el desarrollador se enfoque en el diseño del sistema, la arquitectura y la lógica de negocio.

---

# Capítulo 6: Integración, despliegue y proyecto final, Sección 12: Presentación de proyecto e IA aplicada, Bloque 3: IA como acelerador de ingeniería

## Casos de Uso Prácticos en Ingeniería de Datos

En el desarrollo de pipelines de datos, la IA puede intervenir en múltiples etapas para reducir drásticamente el tiempo de ejecución de tareas estructuradas:

* **Generación de código:** Crear la estructura base (boilerplate) para scripts de Python, APIs o funciones de transformación.
* **Escritura de consultas SQL:** Traducir requerimientos complejos en lenguaje natural a consultas eficientes.
* **Creación de Infraestructura:** Generar archivos de configuración como Dockerfiles, compose.yaml o scripts de Terraform.
* **Documentación:** Explicar qué hace una función heredada o generar los comentarios técnicos de un módulo completo.

---

# Capítulo 6: Integración, despliegue y proyecto final, Sección 12: Presentación de proyecto e IA aplicada, Bloque 3: IA como acelerador de ingeniería

## Ejemplo de Prompts: Generación de una API

Crear una API desde cero implica código estructural repetitivo que un modelo de IA puede generar en segundos con las instrucciones correctas.

**Prompt sugerido:**
"Eres un experto en Python y FastAPI. Crea un script con un endpoint GET en la ruta '/transacciones'. El endpoint debe leer un archivo parquet llamado 'data.parquet', filtrar por un parámetro opcional 'cliente_id', y devolver los resultados en formato JSON. Incluye el manejo de errores HTTP 404 si el archivo no existe."

**Resultado esperado:**
Un código base funcional, con las importaciones correctas y la lógica estructurada, que el ingeniero solo requiere revisar y adaptar al entorno local.

---

# Capítulo 6: Integración, despliegue y proyecto final, Sección 12: Presentación de proyecto e IA aplicada, Bloque 3: IA como acelerador de ingeniería

## Ejemplo de Prompts: Limpieza de Datos

La limpieza de datos suele tener reglas específicas que podemos definir textualmente para generar transformaciones en Pandas.

**Prompt sugerido:**
"Tengo un DataFrame de Pandas con las columnas 'fecha', 'monto' y 'estado'. Genera el código de Python para: 
1) Convertir 'fecha' a tipo datetime, manejando errores (coerce). 
2) Rellenar los valores nulos en la columna 'monto' con la mediana. 
3) Filtrar las filas donde 'estado' sea distinto de 'completado'. 
Devuelve solo el código, sin texto explicativo."

Este enfoque nos proporciona un bloque exacto de código vectorizado, listo para integrarse en nuestro pipeline ETL.

---

# Capítulo 6: Integración, despliegue y proyecto final, Sección 12: Presentación de proyecto e IA aplicada, Bloque 3: IA como acelerador de ingeniería

## Generación de Queries SQL con IA

Traducir reglas de negocio a SQL puede ser un proceso iterativo y propenso a errores. Proveer el esquema de datos a la IA es clave para un buen resultado.

**Prompt sugerido:**
"Dada la tabla 'ventas' con columnas (id, fecha, monto, cliente_id) y la tabla 'clientes' con (id, nombre, pais), escribe una consulta SQL en dialecto MySQL. 
La consulta debe devolver el nombre del cliente y el monto total comprado, agrupado por cliente. 
Filtro: Solo incluir clientes de 'Mexico' que hayan comprado un total mayor a 1000 durante el año 2023."

La IA aplicará correctamente los JOINs, las funciones de agregación (SUM) y las cláusulas WHERE y HAVING necesarias.

---

# Capítulo 6: Integración, despliegue y proyecto final, Sección 12: Presentación de proyecto e IA aplicada, Bloque 3: IA como acelerador de ingeniería

## Refactorización de Código

Con frecuencia escribimos scripts monolíticos que funcionan pero son difíciles de mantener. La IA es una excelente herramienta para aplicar principios de ingeniería de software.

Podemos enviar un bloque de código y solicitar:
"Tengo este script de Python que extrae datos de un CSV, los limpia y los inserta en MySQL. Actualmente es un solo bloque de código continuo. Por favor, refactorizalo dividiéndolo en tres funciones bien definidas (extract, transform, load). Agrega type hints a las funciones y bloques try/except para el manejo de errores."

Esto transforma instantáneamente un código aficionado en uno modular y mantenible.

---

# Capítulo 6: Integración, despliegue y proyecto final, Sección 12: Presentación de proyecto e IA aplicada, Bloque 3: IA como acelerador de ingeniería

## Buenas Prácticas de Prompting

La calidad del código devuelto por la IA depende directamente de la calidad de nuestras instrucciones (prompts). Un buen prompt debe contener:

* **Contexto:** "Actúa como un Data Engineer senior..."
* **Claridad de la tarea:** Define exactamente qué quieres lograr paso a paso.
* **Restricciones:** "No uses librerías externas aparte de Pandas y SQLAlchemy. Usa Python 3.10."
* **Formato de salida:** "Devuelve únicamente el script de Python, sin saludos ni explicaciones."
* **Ejemplos:** "Si la entrada es '10-20-2023', la salida deseada es '2023-10-20'."

---

# Capítulo 6: Integración, despliegue y proyecto final, Sección 12: Presentación de proyecto e IA aplicada, Bloque 3: IA como acelerador de ingeniería

## Limitaciones de las Herramientas de IA

A pesar de su tremenda utilidad, los LLMs no son infalibles y presentan retos que el ingeniero debe conocer:

* **Alucinaciones:** Pueden inventar métodos de librerías que no existen o generar sintaxis inválida.
* **Falta de contexto del negocio:** La IA ignora las reglas no escritas de la empresa o los matices funcionales detrás de ciertos datos anómalos.
* **Desactualización:** Pueden sugerir código basado en versiones antiguas de librerías, usando métodos depreciados.
* **Riesgos de privacidad:** Jamás se deben incluir datos sensibles, contraseñas, tokens reales o información confidencial de clientes en un prompt.

---

# Capítulo 6: Integración, despliegue y proyecto final, Sección 12: Presentación de proyecto e IA aplicada, Bloque 3: IA como acelerador de ingeniería

## La Importancia de la Validación Humana

El código generado por IA nunca debe ir directo a un entorno productivo sin pasar por un escrutinio rigoroso. El ingeniero de datos sigue siendo el responsable final del sistema.

**Pasos de validación indispensables:**
1. **Revisión estática:** Leer y entender línea por línea para asegurar que la lógica coincide con el requerimiento.
2. **Pruebas locales:** Ejecutar el código en un entorno aislado de desarrollo con datos de prueba.
3. **Control de integración:** Garantizar que los tipos de datos generados empaten perfectamente con la siguiente etapa del pipeline.

La IA propone la solución; el ingeniero valida y toma la decisión.

---

# Capítulo 6: Integración, despliegue y proyecto final, Sección 12: Presentación de proyecto e IA aplicada, Bloque 3: IA como acelerador de ingeniería

## Conclusión: La IA como Acelerador, no Sustituto

La Inteligencia Artificial no reemplaza el entendimiento técnico. Si desconoces cómo funciona un JOIN en SQL o la diferencia entre un diccionario y un DataFrame, no tendrás el criterio para saber si la IA ha cometido un error sutil pero catastrófico.

El conocimiento sólido te permite usar la IA como un multiplicador de productividad:
* Búsqueda de sintaxis manual >> Generación instantánea.
* Escritura de código repetitivo >> Revisión de código generado.

El ingeniero moderno no es quien memoriza cada línea de código, sino quien sabe diseñar arquitecturas sólidas, orquestar soluciones y validar procesos complejos con la ayuda de la inteligencia artificial.

---

<!-- _class: code -->
## Practica: Usar IA para acelerar tareas de ingeniería de datos

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar ia como acelerador de ingeniería con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap6/6_12_3_Script.py
"""
Capítulo 6: Integración, despliegue y proyecto final
Sección 12: Presentación de proyecto e IA aplicada
Bloque 3: IA como acelerador de ingeniería

Este script demuestra cómo utilizar Inteligencia Artificial (LLMs) como
un copiloto en la ingeniería de datos. Contiene ejemplos de prompts
bien estructurados y el código resultante aplicable a pipelines.
"""

import pandas as pd
import numpy as np

# Establecer semilla para reproducibilidad
np.random.seed(987654)

# =============================================================================
# Subtema 8: Buenas prácticas de prompting

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap6/6_12_3_Script.py`

---

## Errores comunes en el Bloque 6.12.3

- **Copiar código de IA sin entenderlo**
  → bugs ocultos que no se saben depurar

- **Pedir a la IA que haga todo el proyecto**
  → no se desarrollan las habilidades del curso

- **No verificar el código generado por IA**
  → puede contener vulnerabilidades o errores sutiles

---

## Resumen: Bloque 6.12.3

**Lo que aprendiste:**
- Usar Claude/ChatGPT para generar scripts ETL, consultas SQL y DAGs de Airflow
- Entender los límites de la IA: no reemplaza la comprensión, la amplifica
- Identificar casos de uso concretos de IA en el día a día del ingeniero de datos

**Lo que construiste:**
El script `6_12_3_Script.py` que usar ia para acelerar tareas de ingeniería de datos usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque Fin del capítulo