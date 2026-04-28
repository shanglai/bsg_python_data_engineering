---
marp: true
theme: bsg
size: 16:9
paginate: true
footer: 'Python para Ingeniería de Datos · Capítulo 5: Automatización y orquestación · BSG Institute'
---

---

<!-- _class: title -->
# Capítulo 5: Automatización y orquestación
## Automatización de procesos

---

<!-- _class: section -->
# Sección 9: Automatización de procesos
## En esta sección construiremos la capa de automatización de procesos del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de automatización de procesos en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 5.9.1: Scripts automatizados
- Bloque 5.9.2: Cronjobs
- Bloque 5.9.3: Logs y ejecución programada
- Bloque 5.9.4: Integración con pipeline

---

<!-- ============================================================ -->
<!-- BLOQUE 5.9.1 — Scripts automatizados                        -->
<!-- Scripts: scripts/cap5/5_9_1_Script.py                    -->
<!-- Notebook: notebooks/cap5/5_9_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 5.9.1
## Scripts automatizados

> El pipeline ya funciona; ahora lo convertimos en un proceso que corre sin intervención humana.

**Al terminar este bloque podrás:**
- Convertir el pipeline en un script ejecutable desde la línea de comandos
- Usar argparse para configurar parámetros de ejecución (fecha, modo, entorno)
- Manejar códigos de salida (exit codes) para indicar éxito o fallo

---

## ¿Qué es la Automatización en Ingeniería de Datos?

La automatización en la ingeniería de datos es el proceso de diseñar sistemas y flujos de trabajo que se ejecutan sin intervención humana directa. 

En etapas anteriores, construimos un pipeline funcional para procesar un dataset de transacciones. Sin embargo, ejecutar estos scripts requería nuestra acción explícita. Al automatizar, delegamos la responsabilidad de la ejecución a un sistema o programa.

**Beneficios principales:**
* **Escalabilidad:** Permite procesar mayores volúmenes de datos sin requerir más tiempo del ingeniero.
* **Reducción de errores:** Elimina el factor del error humano asociado a la ejecución manual repetitiva.
* **Disponibilidad:** Garantiza que los datos estén listos para el consumo (APIs, Dashboards) antes de que el negocio los necesite.

---

## Diferencia entre Ejecución Manual y Automática

El paso de un entorno de desarrollo a un entorno productivo requiere cambiar la forma en la que interactuamos con nuestro código.

**Ejecución Manual:**
* Depende de que un desarrollador abra la terminal y ejecute: `python main_pipeline.py`
* Alto riesgo de olvidos o de ejecutar los scripts en el orden incorrecto.
* Las fallas solo se detectan si el desarrollador está observando la consola.

**Ejecución Automática:**
* Un proceso de fondo o herramienta (como cron) dispara el comando según reglas definidas.
* El orden de ejecución está codificado y garantizado por el sistema.
* Las fallas se registran en archivos de logs para su posterior análisis, permitiendo alertas proactivas.

---

## Pipelines Batch (Procesos por Lotes)

En ingeniería de datos, un pipeline Batch es un sistema que procesa un bloque finito de datos a intervalos regulares. Es el enfoque más común frente al procesamiento en tiempo real (streaming).

**Características del procesamiento Batch:**
* **Volumen:** Procesa grandes cantidades de datos acumulados (ej. todas las transacciones de un día).
* **Ventana de tiempo:** Define el inicio y fin del bloque de datos a evaluar.
* **Eficiencia:** Aprovecha los recursos del sistema al máximo durante la ventana de ejecución programada.

Para nuestro caso de transacciones, un pipeline batch tomará el archivo CSV generado el día anterior, lo limpiará, lo transformará y lo cargará en la base de datos MySQL de una sola vez.

---

## Frecuencia de Actualización de Datos

Determinar cada cuánto tiempo debe ejecutarse un script automatizado depende completamente de la necesidad del negocio (Acuerdos de Nivel de Servicio o SLAs).

**Criterios de definición:**
* **Actualización Diaria (T+1):** Ejecutar a la medianoche para procesar las transacciones del día cerrado. Es el estándar para reportes financieros y dashboards diarios.
* **Actualización por Horas:** Útil para monitoreo operativo, donde las decisiones se toman a lo largo de la jornada laboral.
* **Actualización Semanal/Mensual:** Común para el cierre de periodos contables o entrenamientos de modelos analíticos pesados.

*Nota matemática conceptual:*
Si `T_ejecucion` es el tiempo que tarda el script y `F_frecuencia` es la ventana de tiempo (ej. 24 horas), siempre debemos garantizar que `T_ejecucion < F_frecuencia` para evitar que las ejecuciones se traslapen y colapsen el sistema.

---

## Estructuración y Preparación de Scripts Ejecutables

Un script desarrollado en un entorno interactivo (como un Jupyter Notebook) no está listo para la automatización. Debe estructurarse como un programa de consola independiente.

**Reglas de estructuración:**
* **Punto de entrada claro:** Usar la convención `if __name__ == '__main__':` para definir el inicio de la ejecución.
* **Modularidad estricta:** Todo el código debe estar contenido en funciones (ej. `extraer_datos()`, `limpiar_transacciones()`).
* **Sin variables globales:** Evitar variables sueltas en el código que puedan alterar el estado entre diferentes partes del script.
* **Códigos de salida:** Un script debe terminar exitosamente (código 0) o devolver un error explícito (código mayor a 0) si falla, para que el sistema de automatización lo detecte.

---

## Parametrización Básica de Scripts

Para que un script automatizado sea útil a lo largo del tiempo, no puede tener valores estáticos ("hardcodeados"). Debe poder recibir parámetros dinámicos.

**El problema:**
Si escribimos en nuestro código `archivo = "transacciones_2023_10_01.csv"`, el script solo servirá para ese día. Al día siguiente fallará o procesará datos viejos.

**La solución:**
Usar librerías de Python como `argparse` o `sys.argv` para pasar parámetros desde la línea de comandos.

**Ejemplo de uso:**
`python pipeline.py --fecha 2023-10-02`

El script lee el parámetro `--fecha` y busca el archivo correspondiente, permitiendo que el sistema automatizado simplemente cambie la fecha cada día al invocar el comando.

---

## Reproducibilidad y Consistencia en Ejecuciones

Cuando un proceso se ejecuta sin supervisión cientos de veces, la consistencia y la reproducibilidad se vuelven obligatorias.

* **Reproducibilidad (Idempotencia):** Propiedad que asegura que si ejecutamos el mismo script automatizado varias veces con los mismos parámetros de entrada (ej. la misma fecha), el resultado final en la base de datos será idéntico al de ejecutarlo una sola vez. No deben crearse registros duplicados.
* **Consistencia:** El pipeline no debe dejar los datos a medias. Si el proceso de ingesta y transformación funciona, pero la carga a MySQL falla, la base de datos no debe quedar con información incompleta. 

Una forma de asegurar esto en operaciones SQL es utilizar comandos de tipo *UPSERT* (Update or Insert) en lugar de *INSERT* directo, o borrar los datos del periodo a procesar antes de insertar los nuevos.

---

## Casos de Uso Reales de Automatización

Para aterrizar estos conceptos, veamos cómo operan estas prácticas en la industria:

* **Ingestión Periódica de APIs:** Un script programado para ejecutarse cada hora que consulta un endpoint REST, obtiene el tipo de cambio de divisas actualizado y lo guarda en formato Parquet en el servidor.
* **Limpieza y Carga Nocturna:** A las 02:00 AM, un proceso batch lee todos los archivos CSV de transacciones de los cajeros automáticos del día anterior, filtra los nulos, normaliza los montos y los inserta en la base de datos corporativa.
* **Generación de Agregados:** Un script semanal que toma toda la tabla de transacciones de MySQL y calcula un resumen de "ventas por categoría", dejándolo listo para que Streamlit lo lea rápidamente el lunes por la mañana.

---

## La Automatización como Primer Paso Hacia Producción

Automatizar un script marca la frontera entre un "proyecto de análisis de datos" y un "producto de ingeniería de datos". 

Este es el primer nivel de madurez operativa:
1. **Desarrollo:** Código funcional, requiere ejecución y revisión manual.
2. **Automatización (Nivel Actual):** Código estructurado y programado, se ejecuta solo.
3. **Orquestación y Monitoreo (Próximos pasos):** Sistemas que no solo automatizan, sino que manejan dependencias complejas, reintentos automáticos y emiten alertas si algo falla.

Al estructurar nuestros scripts hoy, sentamos las bases técnicas necesarias para herramientas de nivel empresarial como cronjobs y Apache Airflow que veremos más adelante.

---

<!-- _class: code -->
## Practica: Convertir el pipeline en script ejecutable con argumentos

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar scripts automatizados con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap5/5_9_1_Script.py
"""
Este script demuestra la estructuración de un pipeline de datos para su
automatización. Se resalta la diferencia entre ejecución manual (hardcoded)
y una ejecución automatizada, parametrizada y reproducible (procesos batch).

Subtemas cubiertos:
- ST1: Concepto de automatización en ingeniería de datos.
- ST2: Diferencia entre ejecución manual y automática.
- ST3: Pipelines batch (procesos por lotes).
- ST4: Frecuencia de actualización de datos.
- ST5: Estructuración de scripts ejecutables.
- ST6: Parametrización básica de scripts.
- ST7: Reproducibilidad en ejecuciones.
- ST8: Importancia de consistencia en pipelines.
- ST9: Preparación de scripts para automatización.
- ST10: Casos de uso reales (actualización diaria).
- ST11: Automatización como primer paso hacia producción.
"""

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap5/5_9_1_Script.py`

---

## Errores comunes en el Bloque 5.9.1

- **No añadir __main__ guard**
  → el código se ejecuta al importar el módulo

- **Hardcodear la fecha de proceso**
  → el script siempre procesa el mismo día

- **No retornar exit code != 0 en caso de error**
  → el scheduler cree que todo fue bien

---

## Resumen: Bloque 5.9.1

**Lo que aprendiste:**
- Convertir el pipeline en un script ejecutable desde la línea de comandos
- Usar argparse para configurar parámetros de ejecución (fecha, modo, entorno)
- Manejar códigos de salida (exit codes) para indicar éxito o fallo

**Lo que construiste:**
El script `5_9_1_Script.py` que convertir el pipeline en script ejecutable con argumentos usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 5.9.2: Cronjobs

---

<!-- ============================================================ -->
<!-- BLOQUE 5.9.2 — Cronjobs                                     -->
<!-- Scripts: scripts/cap5/5_9_2_Script.py                    -->
<!-- Notebook: notebooks/cap5/5_9_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 5.9.2
## Cronjobs

> Con el script listo, lo programamos para que corra automáticamente en horarios definidos.

**Al terminar este bloque podrás:**
- Configurar un cron job en Linux/Codespaces para ejecutar el pipeline
- Entender la sintaxis de cron (minuto, hora, día, mes, día_semana)
- Verificar que el cron job se ejecutó correctamente con crontab -l

---

### Introducción a Cron y Tareas Programadas

**¿Qué es cron?**
En ingeniería de datos, no basta con tener un script que funcione; necesitamos que se ejecute sin intervención humana. `cron` es un administrador de procesos en sistemas basados en Unix (como Linux y macOS) que ejecuta comandos o scripts en intervalos de tiempo regulares. 

**Concepto de tareas programadas (Cronjobs)**
Un "cronjob" es simplemente una tarea específica que le decimos a `cron` que ejecute en un momento determinado. En el contexto de nuestro pipeline, un cronjob tomará nuestro script de ingesta o transformación y lo ejecutará diaria o semanalmente para procesar los nuevos datos que van llegando.

---

### La Sintaxis de Cron

Para decirle a `cron` cuándo ejecutar una tarea, usamos una sintaxis basada en 5 campos separados por espacios, seguidos del comando a ejecutar.

**Estructura básica:**
```text
* * * * * comando_a_ejecutar
| | | | |
| | | | +-- Día de la semana (0 - 7) (Domingo es 0 o 7)
| | | +---- Mes (1 - 12)
| | +------ Día del mes (1 - 31)
| +-------- Hora (0 - 23)
+---------- Minuto (0 - 59)
```

**Valores especiales:**
* `*`: Significa "todos" (cada minuto, cada hora, etc.).
* `,`: Separa valores (ej. `1,15` en el campo de minutos significa en el minuto 1 y 15).
* `-`: Define un rango (ej. `1-5` en el día de la semana significa de lunes a viernes).
* `/`: Define incrementos (ej. `*/5` en minutos significa cada 5 minutos).

---

### Ejemplos Prácticos de Sintaxis

Entender la sintaxis toma un poco de práctica. Veamos los casos más comunes en pipelines de datos:

**Cada 5 minutos** (Ideal para micro-batches o monitoreo)
`*/5 * * * * python script.py`

**Cada hora en el minuto cero** (Ej. 1:00, 2:00, etc.)
`0 * * * * python script.py`

**Todos los días a las 2:30 AM** (Ventana nocturna de procesamiento)
`30 2 * * * python script.py`

**Todos los lunes a las 8:00 AM** (Reportes semanales)
`0 8 * * 1 python script.py`

---

### Configuración y Ejecución Periódica

Para configurar un cronjob en un entorno local (o en un servidor de paso), utilizamos la terminal.

**Comandos básicos:**
* `crontab -e`: Abre el editor para añadir o modificar tus cronjobs.
* `crontab -l`: Lista todos los cronjobs configurados actualmente para tu usuario.

**Ejecución de un script de Python:**
Una vez dentro del editor (`crontab -e`), agregamos una nueva línea. Para ejecutar nuestro pipeline todos los días a medianoche, escribiríamos:
```bash
0 0 * * * /usr/bin/python3 /ruta/al/proyecto/pipeline.py
```
*Nota: Al guardar y salir del editor, cron instalará la nueva tarea y comenzará a ejecutarla automáticamente en segundo plano.*

---

### Manejo de Rutas y Entorno

Este es el punto donde el 90% de los cronjobs fallan la primera vez. 

**El problema del entorno de Cron**
Cuando ejecutas un script en tu terminal, tienes cargadas variables de entorno y estás en una carpeta específica. `cron` se ejecuta en un entorno mínimo y **no conoce tu directorio de trabajo actual**.

**Reglas de oro para rutas en cron:**
1. **Rutas absolutas para el ejecutable:** Usa la ruta completa de Python (`/usr/bin/python3` o la ruta de tu entorno virtual).
2. **Rutas absolutas para el script:** No uses `python pipeline.py`. Usa `python /home/usuario/proyecto/pipeline.py`.
3. **Rutas absolutas dentro del código:** Si tu código de Python lee un CSV con `pd.read_csv('datos.csv')`, fallará. Asegúrate de que el código maneje rutas absolutas usando librerías como `os` o `pathlib`.

---

### Logs Básicos en Cron

Cuando `cron` ejecuta una tarea, no hay una pantalla donde imprimir los comandos `print()` o los errores. Si algo falla, el fallo es silencioso. 

**Redirección de salidas:**
Debemos redirigir la salida estándar (stdout) y la salida de errores (stderr) a un archivo de texto para poder auditar qué sucedió.

```bash
0 2 * * * /usr/bin/python3 /ruta/pipeline.py >> /ruta/logs/pipeline.log 2>&1
```

**Explicación:**
* `>> /ruta/logs/pipeline.log`: Añade la salida normal del script al final del archivo de log.
* `2>&1`: Redirige los errores (2) al mismo lugar que la salida estándar (1). De esta forma, tanto los mensajes de éxito como los rastreos de errores de Python quedan guardados en `pipeline.log`.

---

### Problemas Comunes en Cron

Al implementar tu primer pipeline automatizado con cron, revisa esta lista si algo no funciona:

* **Paths (Rutas):** Como mencionamos, usar rutas relativas es el error más frecuente.
* **Permisos de ejecución:** El script o los archivos que intenta modificar no tienen permisos suficientes (`chmod +x script.py`).
* **Variables de Entorno:** Si tu script usa credenciales almacenadas en variables de entorno (ej. contraseñas de base de datos), `cron` no las leerá por defecto. Debes cargarlas explícitamente en el script o en el comando cron.
* **Zonas horarias:** Los servidores en la nube suelen estar en UTC. Si programas algo a las "14:00", asegúrate de saber en qué zona horaria está operando el servidor.

---

### Limitaciones y Uso en Pipelines Simples

`cron` es una herramienta fantástica y robusta para empezar, pero tiene limitantes en arquitecturas de datos modernas.

**Limitaciones de cron:**
* **Sin manejo de dependencias:** Si el Paso B depende del Paso A, cron solo los ejecuta por horario, no sabe si el Paso A falló o aún no termina.
* **No hay reintentos automáticos (Retries):** Si la base de datos se desconecta un segundo y el script falla, cron no lo volverá a intentar hasta su siguiente horario programado.
* **Visibilidad nula:** No hay un panel de control (Dashboard) nativo para ver si la tarea tuvo éxito; debes revisar los archivos de log manualmente.

**Conclusión para nuestro caso:**
Para pipelines simples y lineales (como nuestra versión actual de extracción >> transformación >> carga), `cron` es más que suficiente. Es el primer gran paso hacia la automatización total antes de migrar a orquestadores avanzados.

---

<!-- _class: code -->
## Practica: Configurar un cron job para el pipeline ETL

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar cronjobs con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap5/5_9_2_Script.py
"""
===============================================================================
Capítulo 5: Automatización y orquestación
Sección 9: Automatización de procesos
Bloque 2: Cronjobs
===============================================================================

Este script representa una tarea automatizada (pipeline simple) preparada para
ser ejecutada mediante una herramienta de programación de tareas como cron. 
Aborda conceptos clave como el manejo de rutas absolutas, la generación de logs 
básicos y la consistencia en ejecuciones periódicas.

Al final del script se incluyen las instrucciones y ejemplos de sintaxis para 
programar este archivo en cron.
"""

import os
import sys

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap5/5_9_2_Script.py`

---

## Errores comunes en el Bloque 5.9.2

- **No usar rutas absolutas en el cron job**
  → el script no se encuentra

- **Olvidar redirigir la salida a un log**
  → no hay forma de saber si el cron corrió

- **Confundir la zona horaria del servidor con la local**
  → ejecución en el horario equivocado

---

## Resumen: Bloque 5.9.2

**Lo que aprendiste:**
- Configurar un cron job en Linux/Codespaces para ejecutar el pipeline
- Entender la sintaxis de cron (minuto, hora, día, mes, día_semana)
- Verificar que el cron job se ejecutó correctamente con crontab -l

**Lo que construiste:**
El script `5_9_2_Script.py` que configurar un cron job para el pipeline etl usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 5.9.3: Logs y ejecución programada

---

<!-- ============================================================ -->
<!-- BLOQUE 5.9.3 — Logs y ejecución programada                  -->
<!-- Scripts: scripts/cap5/5_9_3_Script.py                    -->
<!-- Notebook: notebooks/cap5/5_9_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 5.9.3
## Logs y ejecución programada

> Un pipeline automatizado sin logs es una caja negra; implementamos registro profesional.

**Al terminar este bloque podrás:**
- Usar el módulo logging de Python para registrar eventos del pipeline
- Configurar niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Rotar archivos de log para evitar que crezcan indefinidamente

---

# Capítulo 5: Automatización y orquestación, Sesión 9: Automatización de procesos, Bloque 3: Logs y ejecución programada

## Introducción al logging

Cuando ejecutamos un pipeline de datos manualmente, solemos utilizar funciones como `print()` para visualizar el progreso en la consola. Sin embargo, en un entorno automatizado, no hay un usuario observando la pantalla. 

El **logging** es el proceso de registrar de manera sistemática y estructurada los eventos que ocurren durante la ejecución de un programa. En la ingeniería de datos, el logging reemplaza al `print()` y se convierte en el mecanismo principal para entender qué hace el código de fondo.

Un registro (log) efectivo debe responder tres preguntas fundamentales:
* **Qué** ocurrió (el evento).
* **Cuándo** ocurrió (la marca de tiempo).
* **Dónde** ocurrió (el módulo o función específica).

---

## Importancia de monitoreo en pipelines

Los pipelines de datos automatizados (como los ejecutados mediante cronjobs) operan de forma silenciosa. Sin un mecanismo de monitoreo, un fallo en la ingesta o transformación pasará desapercibido hasta que un usuario final reporte datos faltantes o incorrectos.

El monitoreo a través de logs permite:
* Detectar fallos en el momento en que ocurren.
* Auditar el comportamiento del sistema.
* Garantizar que los procesos programados se completaron exitosamente.
* Medir tiempos de ejecución para detectar cuellos de botella (por ejemplo, si una consulta que tomaba 2 minutos comienza a tomar 45 minutos).

---

## Tipos de logs (Niveles de severidad)

No todos los eventos tienen la misma importancia. La librería estándar `logging` de Python categoriza los mensajes en diferentes niveles de severidad:

* **DEBUG:** Información detallada, típicamente de interés solo al diagnosticar problemas.
* **INFO:** Confirmación de que las cosas funcionan como se espera (ej. "Conexión a base de datos exitosa", "Se procesaron 1500 registros").
* **WARNING:** Indicación de que algo inesperado sucedió o de un problema en el futuro cercano, pero el software aún funciona (ej. "Espacio en disco al 85%").
* **ERROR:** Debido a un problema más grave, el software no ha podido realizar alguna función (ej. "Fallo al leer el archivo CSV").
* **CRITICAL:** Un error grave, indicando que el programa en sí puede no continuar ejecutándose (ej. "Caída total del servidor de base de datos").

---

## Inclusión de timestamps

Un mensaje de log sin contexto temporal carece de utilidad en un sistema automatizado. El **timestamp** (marca de tiempo) es el componente más crítico de un log.

Permite:
1. **Ordenar cronológicamente** los eventos de un pipeline.
2. **Calcular la duración** de tareas específicas restando el timestamp de inicio del timestamp de fin.
3. **Correlacionar eventos** entre distintos sistemas (ej. cruzar el log de la API con el log de la base de datos para ver qué pasó a las 14:35:02).

En Python, el formato estándar a configurar suele incluir la fecha y hora exacta: `%(asctime)s`.

---

## Registro de eventos clave en el pipeline

Para que el logging sea útil, debemos registrar los hitos importantes del flujo de datos, sin saturar el archivo de texto.

**Eventos clave a registrar:**
* Inicio y fin de la ejecución del pipeline.
* Conexiones exitosas (o fallidas) a fuentes de datos y bases de datos.
* Cantidad de registros extraídos, transformados y cargados.
* Cambios en la calidad de los datos (ej. "Se encontraron 50 valores nulos en la columna 'precio'").
* Rutas de archivos generados o leídos.

Ejemplo de configuración básica en Python:
```python
import logging

logging.basicConfig(
    filename='pipeline_ejecucion.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

logging.info("Iniciando extracción de datos desde CSV.")
```

---

## Manejo de errores en ejecución

En un proceso automatizado, si ocurre una excepción, el script fallará. Utilizar bloques `try/except` junto con el sistema de logging permite capturar el error, registrar sus detalles técnicos y, de ser posible, continuar con la ejecución o abortar de manera controlada.

```python
try:
    df = pd.read_csv("datos_transacciones.csv")
    logging.info(f"Archivo leído correctamente. {len(df)} filas encontradas.")
except FileNotFoundError as e:
    logging.error(f"Error de lectura: El archivo no existe. Detalles: {e}")
    # Abortar pipeline de forma segura
except Exception as e:
    logging.critical(f"Error inesperado durante la lectura: {e}")
```
Registrar el error explícitamente evita que el proceso muera en silencio y nos da la pista exacta para solucionarlo.

---

## Debugging mediante logs y Trazabilidad de procesos

**Debugging post-mortem:**
Cuando un pipeline falla de madrugada, no podemos utilizar el debugger interactivo. Los logs son la única herramienta para reconstruir el estado del sistema en el momento del fallo. 

**Trazabilidad:**
Es la capacidad de rastrear el ciclo de vida completo de un lote de datos. Si ingresan 1000 registros, el log debe contar la historia completa:
1. `INFO: 1000 registros leídos del API.`
2. `INFO: 50 registros descartados por valores nulos en transformación.`
3. `INFO: 950 registros insertados en MySQL tabla 'ventas'.`

Si un analista pregunta por qué faltan datos, la trazabilidad del log proporciona la respuesta inmediata sin necesidad de re-ejecutar el código.

---

## Análisis de ejecuciones pasadas

Un archivo de logs histórico es una mina de datos sobre el comportamiento de nuestro sistema. Analizar ejecuciones programadas pasadas nos permite:

* **Identificar intermitencias:** Fallos que ocurren solo los martes a las 3 AM (posiblemente debido a un mantenimiento de red).
* **Análisis de tendencias de rendimiento:** Observar si el tiempo de transformación aumenta día con día, lo que indicaría la necesidad de optimizar el código o escalar recursos.
* **Auditoría de datos:** Comprobar retroactivamente cuántos datos se procesaron el mes pasado.

---

## Buenas prácticas en logging

Para garantizar que los logs sean legibles y útiles a largo plazo, se deben seguir ciertas convenciones:

1. **Estructura consistente:** Usar siempre el mismo formato (Timestamp | Nivel | Mensaje). En sistemas más avanzados, se prefiere formato JSON.
2. **No registrar información sensible (PII):** Nunca escribir contraseñas, tokens de APIs, números de tarjetas de crédito o datos personales explícitos en los logs.
3. **Uso adecuado de niveles:** No usar ERROR para algo que es un comportamiento esperado (ej. un cliente que no tiene compras previas).
4. **Rotación de logs:** Evitar que un solo archivo `.log` crezca hasta ocupar gigabytes. Se deben segmentar por día o tamaño máximo.

---

## Preparación para observabilidad

El logging es el primer paso evolutivo. A medida que los sistemas de datos crecen y se vuelven más complejos, pasamos del simple "logging" a la **observabilidad**.

Mientras el monitoreo y los logs nos dicen *qué* se rompió, la observabilidad es una propiedad del sistema que nos permite entender *por qué* se rompió basándonos únicamente en sus salidas externas. 

Implementar logs estructurados hoy prepara el pipeline para que, en etapas futuras, estas líneas de texto puedan ser ingeridas por herramientas modernas de visualización (como Kibana o Grafana) o métricas de series de tiempo (como Prometheus), logrando una visión integral de la salud de nuestros datos.

---

<!-- _class: code -->
## Practica: Añadir logging profesional al pipeline automatizado

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar logs y ejecución programada con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap5/5_9_3_Script.py
"""
Capítulo 5: Automatización y orquestación
Sección 9: Automatización de procesos
Bloque 3: Logs y ejecución programada

Descripción: 
Este script demuestra cómo implementar un sistema de logging en un pipeline 
de datos. Se abordan los niveles de log (INFO, WARNING, ERROR), la inclusión 
de timestamps, el registro de eventos clave y el manejo de errores para 
garantizar la trazabilidad y facilitar el debugging de ejecuciones programadas.
"""

import logging
import pandas as pd
import numpy as np
import os
import sys

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap5/5_9_3_Script.py`

---

## Errores comunes en el Bloque 5.9.3

- **Usar print() en lugar de logging**
  → los mensajes no se guardan en producción

- **Loggear información sensible (contraseñas, tokens)**
  → riesgo de seguridad

- **No configurar un handler de archivo**
  → los logs solo van a la consola y se pierden

---

## Resumen: Bloque 5.9.3

**Lo que aprendiste:**
- Usar el módulo logging de Python para registrar eventos del pipeline
- Configurar niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Rotar archivos de log para evitar que crezcan indefinidamente

**Lo que construiste:**
El script `5_9_3_Script.py` que añadir logging profesional al pipeline automatizado usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 5.9.4: Integración con pipeline

---

<!-- ============================================================ -->
<!-- BLOQUE 5.9.4 — Integración con pipeline                     -->
<!-- Scripts: scripts/cap5/5_9_4_Script.py                    -->
<!-- Notebook: notebooks/cap5/5_9_4_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 5.9.4
## Integración con pipeline

> Combinamos script, cron y logs en un pipeline de automatización completo y observable.

**Al terminar este bloque podrás:**
- Integrar el logging con la ejecución programada por cron
- Añadir alertas por email o archivo cuando el pipeline falla
- Crear un script de health check que verifique el estado del pipeline

---

## Integración del Pipeline Completo (End-to-End)

La automatización alcanza su verdadero valor cuando conectamos todas las piezas desarrolladas de manera secuencial y sin intervención humana.

*   **Flujo integrado:** El pipeline ya no es un conjunto de scripts aislados. Consiste en un script maestro (o archivo por lotes) que coordina la ingestión, transformación y almacenamiento.
*   **Ejecución periódica:** Utilizando herramientas como `cron`, el pipeline se programa para ejecutarse en intervalos definidos (por ejemplo, diariamente a las 02:00 AM).
*   **Independencia:** Al ejecutarse "End-to-End", el sistema debe ser capaz de iniciar con datos crudos (desde un CSV o una API) y finalizar con datos estructurados persistidos en una base de datos o en formato Parquet, listos para ser consumidos.

---

## Pipeline de Desarrollo vs Pipeline Operativo

El paso hacia la automatización marca la frontera entre desarrollar un pipeline y tenerlo en "producción".

### Pipeline de Desarrollo
*   **Ejecución:** Manual, paso a paso.
*   **Objetivo:** Crear lógica, limpiar datos específicos, explorar y corregir errores inmediatos.
*   **Entorno:** Local, interactivo (Jupyter Notebooks, scripts probados manualmente).

### Pipeline Operativo (Producción)
*   **Ejecución:** Automática y periódica.
*   **Objetivo:** Mantener el flujo de datos actualizado y disponible sin intervención humana.
*   **Entorno:** Servidores dedicados, contenedores aislados (Docker), altamente dependiente de logs para la comunicación de estado.

---

## Validación y Monitoreo de Ejecuciones Automáticas

Cuando un proceso ocurre sin que lo veamos, necesitamos mecanismos para asegurarnos de que todo salio bien. 

*   **Monitoreo básico:** Revisar constantemente los archivos de registro (logs) generados en cada etapa del pipeline.
*   **Validación de resultados:** Incluir validaciones automáticas al final del proceso. Ejemplos de "Sanity Checks":
    *   ¿El numero de registros de entrada coincide con los procesados (considerando nulos eliminados)?
    *   ¿La fecha máxima en la base de datos corresponde a la ejecución actual?
*   **Evaluación continua:** Un pipeline automatizado exitoso requiere revisar periódicamente las métricas de ejecución para detectar anomalías (por ejemplo, si el tiempo de ejecución pasa de 2 minutos a 2 horas).

---

## Manejo de Fallos y el Concepto de Reintentos (Retry)

En un entorno automatizado, los fallos son inevitables: caídas de red, APIs inalcanzables o bases de datos bloqueadas.

*   **Identificación de errores:** El código debe usar bloques `try/except` para atrapar fallos específicos y registrarlos en el log, en lugar de simplemente detenerse de manera silenciosa.
*   **Concepto de Reintento (Retry):** Es una estrategia de resiliencia. Si un proceso falla por una causa temporal (ej. error de conexión a la API), el sistema espera un tiempo definido y vuelve a intentarlo.
*   **Lógica básica de reintento:**
    *   Intento 1: Falla (Timeout).
    *   Espera 5 segundos.
    *   Intento 2: Éxito.
    *   Si se supera el limite máximo de intentos, el pipeline registra un error crítico y alerta al equipo.

---

## Consistencia de Datos en Ejecuciones Múltiples

¿Qué ocurre si el pipeline automatizado se ejecuta dos veces por error, o si falla a la mitad y debe reiniciarse? Aquí entra el concepto de consistencia.

*   **Idempotencia:** Un principio fundamental en ingeniería de datos. Significa que ejecutar un proceso una vez tiene el mismo efecto en los datos finales que ejecutarlo múltiples veces.
    *   Matemáticamente: `f(f(x)) = f(x)`
*   **Estrategias para mantener consistencia:**
    *   **Sobrescritura segura (Overwrite):** Borrar los datos del periodo actual antes de volver a escribirlos.
    *   **Upsert (Update/Insert):** Si el registro ya existe (basado en un ID único), se actualiza; si no existe, se inserta.
*   **Evitar duplicados:** Sin estas estrategias, una ejecución doble de un script de inserción (Append) corrompería el dataset creando registros duplicados.

---

## Preparación para la Orquestación

Implementar automatización con `cron` y scripts maestros es el primer gran paso, pero tiene limitaciones cuando los pipelines crecen en complejidad.

*   **Límites de la automatización básica:** Dificultad para manejar dependencias complejas (ej. "el script C solo debe correr si A y B terminaron exitosamente, pero A y B corren en paralelo").
*   **Hacia la orquestación:** Necesitamos sistemas que no solo programen en el tiempo, sino que entiendan la relación lógica y el estado de cada tarea.
*   **Siguiente paso:** En la siguiente sección introduciremos herramientas formales de orquestación (como Apache Airflow) que permiten visualizar flujos, manejar reintentos de forma nativa y escalar estas prácticas de producción a múltiples pipelines simultáneos.

---

<!-- _class: code -->
## Practica: Integrar automatización completa con logs y alertas

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar integración con pipeline con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap5/5_9_4_Script.py
"""
Capítulo 5: Automatización y orquestación
Sección 9: Automatización de procesos
Bloque 4: Integración con pipeline

Este script consolida la ejecución de un pipeline completo (ingesta, transformación 
y almacenamiento) preparado para ser ejecutado periódicamente. Incluye mecanismos 
de reintentos, validaciones automáticas y monitoreo básico mediante logs, 
simulando un contexto operativo de producción.
"""

import pandas as pd
import sqlite3
import logging
import time
import random
import os
from datetime import datetime

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap5/5_9_4_Script.py`

---

## Errores comunes en el Bloque 5.9.4

- **No distinguir entre errores recuperables y errores fatales**
  → el pipeline se detiene innecesariamente

- **No purgar logs antiguos**
  → el disco se llena con el tiempo

- **No monitorear que el cron realmente ejecutó**
  → el pipeline deja de correr sin que nadie lo note

---

## Resumen: Bloque 5.9.4

**Lo que aprendiste:**
- Integrar el logging con la ejecución programada por cron
- Añadir alertas por email o archivo cuando el pipeline falla
- Crear un script de health check que verifique el estado del pipeline

**Lo que construiste:**
El script `5_9_4_Script.py` que integrar automatización completa con logs y alertas usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 5.10.1: Introducción a Airflow

---

<!-- _class: section -->
# Sección 10: Orquestación e infraestructura
## En esta sección construiremos la capa de orquestación e infraestructura del pipeline

**En esta sección aprenderás a:**
- Aplicar los conceptos de orquestación e infraestructura en el pipeline de transacciones
- Usar las herramientas profesionales estándar del sector
- Integrar esta sección con las anteriores del pipeline

**Bloques:**
- Bloque 5.10.1: Introducción a Airflow
- Bloque 5.10.2: DAG simple
- Bloque 5.10.3: Infraestructura como código (demo)
- Bloque 5.10.4: Definición del proyecto final

---

<!-- ============================================================ -->
<!-- BLOQUE 5.10.1 — Introducción a Airflow                       -->
<!-- Scripts: scripts/cap5/5_10_1_Script.py                    -->
<!-- Notebook: notebooks/cap5/5_10_1_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 5.10.1
## Introducción a Airflow

> Los cron jobs tienen limitaciones; Airflow nos da visibilidad y control sobre flujos complejos.

**Al terminar este bloque podrás:**
- Entender qué es Apache Airflow y cuándo usarlo vs cron
- Identificar los componentes clave: DAG, Task, Scheduler, Webserver
- Acceder a la UI de Airflow y explorar los DAGs de ejemplo

---

## Limitaciones de cron en pipelines complejos

Hasta ahora, hemos visto que `cron` es una herramienta excelente para programar la ejecución de scripts en intervalos regulares. Sin embargo, a medida que los pipelines de datos crecen en complejidad, `cron` presenta limitaciones significativas:

* **Falta de contexto de dependencias:** Si un script de extraccion falla, `cron` ejecutara el script de transformacion de todos modos, procesando datos incompletos o vacios.
* **Manejo de errores manual:** Si una tarea falla, `cron` no tiene un mecanismo nativo inteligente para reintentar solo esa parte. Requiere intervencion manual para detectar y solucionar el problema.
* **Falta de visibilidad:** No existe un panel de control nativo en `cron` para ver que se esta ejecutando, que fallo y que esta pendiente. Todo se reduce a buscar en archivos de texto (logs).
* **Escalabilidad limitada:** Administrar decenas o cientos de scripts con `cron` se vuelve un caos de mantenimiento y cruce de horarios.

---

## Introduccion a la orquestacion

Para resolver los problemas de `cron` en sistemas complejos, introducimos el concepto de **orquestacion de datos**. 

La orquestacion va mucho mas alla de simplemente programar una tarea a una hora especifica. Se trata de coordinar un flujo de trabajo completo donde multiples tareas individuales se ejecutan en un orden especifico, respetando reglas de negocio, dependencias y condiciones de estado.

Imagina al orquestador como el director de una orquesta sinfonica: no toca los instrumentos (no procesa los datos directamente), pero se asegura de que cada musico (script o sistema) entre en el momento exacto, al ritmo correcto y solo si las condiciones previas se han cumplido.

---

## Definicion de DAG (Directed Acyclic Graph)

El concepto central de la orquestacion moderna es el **DAG** (Grafo Aciclico Dirigido, por sus siglas en ingles). Es la forma matematica e informatica de representar un flujo de trabajo.

Desglocemos el termino:
* **Grafo (Graph):** Es una estructura compuesta por nodos (que representan las tareas a ejecutar, como "Descargar datos" o "Limpiar datos") y aristas o lineas que los conectan.
* **Dirigido (Directed):** Las conexiones tienen una direccion especifica. Hay un flujo logico de principio a fin. La Tarea A apunta a la Tarea B (A >> B).
* **Aciclico (Acyclic):** No existen ciclos o bucles infinitos. Una vez que avanzas en el flujo, no puedes regresar a una tarea anterior creando un circulo cerrado. Esto garantiza que el pipeline eventualmente terminara.

---

## Concepto de dependencias entre tareas

En un DAG, las conexiones entre los nodos representan **dependencias**. Esto significa que la ejecucion de una tarea esta estrictamente condicionada por el estado de la tarea anterior.

Existen dos terminos fundamentales para referirse a la ubicacion de una tarea respecto a otra:
* **Upstream (Aguas arriba):** Tareas que deben ejecutarse ANTES que la tarea actual.
* **Downstream (Aguas abajo):** Tareas que dependen de la tarea actual y se ejecutaran DESPUES.

Ejemplo en nuestro pipeline:
Lectura de API (Upstream) >> Limpieza de datos >> Carga en Base de Datos (Downstream).
Si la "Lectura de API" falla, las tareas downstream no se ejecutaran, protegiendo asi la integridad de nuestra base de datos.

---

## Introduccion a Apache Airflow

**Apache Airflow** es la herramienta de orquestacion de codigo abierto mas popular y el estandar de facto en la industria de la ingenieria de datos. Fue desarrollado originalmente por Airbnb y ahora es parte de la Apache Software Foundation.

Caracteristicas principales:
* **Flujos de trabajo como codigo:** En Airflow, los pipelines (DAGs) se definen utilizando codigo Python estandar. Esto permite que los pipelines sean versionados, testeables y colaborativos.
* **Altamente extensible:** Tiene "operadores" y conectores para casi cualquier base de datos, servicio en la nube o API del mercado.
* **Centralizacion:** Actua como el cerebro de las operaciones de datos, supervisando trabajos en bases de datos locales, clusters en la nube o contenedores Docker.

---

## Comparacion cron vs Airflow

Para entender el salto evolutivo, comparemos directamente ambas herramientas:

| Caracteristica | `cron` | Apache Airflow |
| :--- | :--- | :--- |
| **Definicion** | Expresiones de tiempo en un archivo local | Codigo Python estructurado (DAGs) |
| **Dependencias** | Inexistentes. Basado solo en tiempo | Nativas. Una tarea espera a la anterior |
| **Monitoreo** | Logs de texto plano, sin interfaz grafica | Interfaz web rica, visual y en tiempo real |
| **Reintentos** | No soportados por defecto | Configurables por tarea, con tiempos de espera |
| **Escalabilidad** | Dificil de mantener con muchos scripts | Diseñado para miles de tareas distribuidas |
| **Caso de uso** | Tareas de sistema simples y aisladas | Pipelines de datos complejos y de mision critica |

---

## Visualizacion de flujos de trabajo

Una de las mayores ventajas de orquestadores como Airflow es su interfaz de usuario (UI). 

En lugar de adivinar en que estado se encuentra un proceso, la UI permite visualizar el DAG completo. Puedes ver un diagrama donde cada nodo cambia de color segun su estado:
* **Verde:** Ejecucion exitosa (Success).
* **Rojo:** Fallo en la ejecucion (Failed).
* **Amarillo/Naranja:** En reintento o dependencia no cumplida (Upstream failed / Up for retry).
* **Verde claro:** En ejecucion activa (Running).

Esta visualizacion reduce drasticamente el tiempo de respuesta ante incidentes, permitiendo al ingeniero de datos saber exactamente que nodo del sistema fallo y por que.

---

## Control de ejecucion

A diferencia de un script estatico, un orquestador otorga control total sobre como y cuando se ejecutan los datos, incluso retrospectivamente:

* **Pausar/Reanudar:** Puedes detener temporalmente un pipeline completo sin borrar su configuracion, util durante mantenimientos de bases de datos.
* **Trigger Manual:** Ejecucion a demanda de un DAG fuera de su horario programado.
* **Catchup y Backfill:** Si tu pipeline estuvo apagado durante tres dias, Airflow puede ejecutar automaticamente las tareas correspondientes a esos tres dias pasados en orden cronologico, para que no haya huecos en los datos.
* **Clear (Limpiar estado):** Si una tarea falla, se soluciona el error en el codigo y se "limpia" el estado de esa tarea en la UI, forzando a que Airflow la vuelva a ejecutar sin tocar lo que ya funciono antes.

---

## Reintentos y control de fallos

En el mundo de los datos, las fallas por problemas de red o APIs inestables son el pan de cada dia. Airflow maneja esto de forma robusta.

* **Reintentos automaticos (Retries):** Puedes configurar que si una tarea de descarga de datos falla por un timeout, Airflow espere 5 minutos y vuelva a intentarlo automaticamente hasta 3 veces antes de considerarla un fallo definitivo.
* **Notificaciones:** Si ocurre un fallo definitivo, el sistema puede estar configurado para enviar alertas via correo electronico o plataformas como Slack.
* **Aislamiento de fallos:** Un error en la Tarea B de un DAG detiene la Tarea C de ese mismo DAG, pero no afecta a otros pipelines completamente independientes que se esten ejecutando en el mismo orquestador.

---

## Escalabilidad de pipelines

A medida que una empresa crece, pasa de tener un solo pipeline a tener decenas o cientos. Airflow esta diseñado para escalar horizontalmente.

* **Arquitectura distribuida:** Airflow puede separar su servidor web, su programador (scheduler) y sus trabajadores (workers) en maquinas distintas.
* **Executors:** Son el mecanismo que usa Airflow para decidir como correr las tareas.
  * *LocalExecutor / SequentialExecutor:* Para pruebas locales o volumenes muy bajos.
  * *CeleryExecutor / KubernetesExecutor:* Para entornos de produccion masivos, distribuyendo las tareas a traves de multiples contenedores o servidores en la nube.
* **Paralelismo:** Permite ejecutar multiples tareas de forma concurrente, optimizando el tiempo total de procesamiento.

---

## Airflow en entornos reales

En la industria actual, Apache Airflow rara vez procesa los datos pesados por si mismo. Actua como un "gestor de trafico".

Casos de uso reales:
* **Integracion de nubes:** Airflow le dice a AWS S3 que envile datos a Snowflake, luego le dice a la base de datos que corra una query, y finalmente dispara un proceso de Machine Learning. Todo desde un solo DAG.
* **Pipelines Hibridos:** Un nodo del DAG puede ejecutar un script de Python local (nuestro mini ETL), el siguiente nodo puede correr un contenedor Docker, y el ultimo nodo hacer una peticion POST a nuestra API de FastAPI.
* **Soporte de SLA (Service Level Agreement):** Airflow permite configurar tiempos maximos de ejecucion. Si un pipeline tarda mas de 2 horas (violando un acuerdo de negocio), lanza alertas antes de fallar.

---

<!-- _class: code -->
## Practica: Explorar la interfaz de Airflow y sus conceptos clave

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar introducción a airflow con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap5/5_10_1_Script.py
import random
from datetime import datetime, timedelta

# Nota: Para ejecutar este script de forma funcional se requiere Apache Airflow.
# Instalar mediante: pip install apache-airflow
try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except ImportError:
    print("Advertencia: Apache Airflow no esta instalado. El script se ejecutara en modo mock.")
    # Generar clases mock para permitir la ejecucion estructural del script sin errores
    class DAG:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
    class PythonOperator:
        def __init__(self, *args, **kwargs): pass

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap5/5_10_1_Script.py`

---

## Errores comunes en el Bloque 5.10.1

- **Instalar Airflow con pip sin virtualenv**
  → conflictos de dependencias graves

- **Confundir el DAG (la definición del flujo) con su ejecución (DAG run)**

- **No usar la variable AIRFLOW_HOME**
  → los archivos de configuración se pierden

---

## Resumen: Bloque 5.10.1

**Lo que aprendiste:**
- Entender qué es Apache Airflow y cuándo usarlo vs cron
- Identificar los componentes clave: DAG, Task, Scheduler, Webserver
- Acceder a la UI de Airflow y explorar los DAGs de ejemplo

**Lo que construiste:**
El script `5_10_1_Script.py` que explorar la interfaz de airflow y sus conceptos clave usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 5.10.2: DAG simple

---

<!-- ============================================================ -->
<!-- BLOQUE 5.10.2 — DAG simple                                   -->
<!-- Scripts: scripts/cap5/5_10_2_Script.py                    -->
<!-- Notebook: notebooks/cap5/5_10_2_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 5.10.2
## DAG simple

> Con Airflow configurado, creamos nuestro primer DAG que ejecuta el pipeline ETL.

**Al terminar este bloque podrás:**
- Escribir un DAG Python con PythonOperator que ejecuta las funciones del pipeline
- Configurar el schedule y el start_date del DAG correctamente
- Monitorear la ejecución del DAG en la UI de Airflow

---

# Capítulo 5: Automatización y orquestación, Sección 10: Orquestación e infraestructura, Bloque 2: DAG simple

## Estructura de un DAG en Airflow

Un DAG (Directed Acyclic Graph) en Apache Airflow se define mediante un script de Python. Este archivo no procesa los datos por sí mismo, sino que actúa como un archivo de configuración que especifica qué tareas deben ejecutarse, cuándo y en qué orden.

La estructura básica se compone de:
* **Argumentos por defecto (default_args):** Un diccionario que define el comportamiento base de las tareas (reintentos, alertas, fecha de inicio).
* **Instanciación del objeto DAG:** Se define el nombre del flujo, su intervalo de programación y parámetros generales.
* **Definición de tareas:** Los pasos individuales del proceso.
* **Definición de dependencias:** El orden de ejecución de las tareas.

---

## Definición de tareas (Operators)

En Airflow, una tarea es la instanciación de un "Operator". Un Operator define qué tipo de trabajo se va a realizar. 

Existen múltiples tipos de Operators, siendo los más comunes para pipelines básicos:
* **BashOperator:** Permite ejecutar comandos de terminal o scripts bash. Ideal para invocar scripts de Python externos.
* **PythonOperator:** Permite ejecutar funciones nativas de Python directamente dentro del archivo del DAG.

Ejemplo de definición:
```python
tarea_ingesta = BashOperator(
    task_id='ingesta_datos',
    bash_command='python src/ingesta.py',
    dag=mi_dag
)
```

---

## Dependencias entre tareas

Para que el pipeline no se ejecute al azar, es fundamental establecer el orden secuencial o paralelo de las tareas. Esto se logra definiendo las dependencias.

En las versiones modernas de Airflow, se utilizan los operadores de desplazamiento de bits de Python (`>>` y `<<`) para establecer el flujo direccional.

Ejemplos de dependencias:
* Ejecución secuencial básica: `tarea_1 >> tarea_2 >> tarea_3`
* Ejecución en paralelo y convergencia: `[tarea_1, tarea_2] >> tarea_3`

Esto garantiza que la transformación no inicie hasta que la ingesta haya terminado exitosamente.

---

## Ejecución y Visualización en la UI de Airflow

Una de las mayores ventajas de Airflow es su interfaz gráfica de usuario (UI), que permite monitorear el estado real de los pipelines.

* **Vista de Grafo (Graph View):** Muestra el DAG de forma visual con sus nodos (tareas) y aristas (dependencias). Permite ver rápidamente si el flujo está bien estructurado.
* **Vista de Cuadrícula (Grid View):** Muestra el historial de ejecuciones en el tiempo. Cada cuadrado representa una tarea en una corrida específica, con colores indicando su estado (verde para éxito, rojo para fallo, amarillo para reintento).

---

## Integración con scripts del pipeline

Al orquestar un pipeline, no queremos reescribir toda la lógica de limpieza y carga dentro del archivo del DAG. La mejor práctica es integrar los scripts que ya construimos.

Usando el `BashOperator`, podemos llamar a los módulos de nuestro proyecto de la siguiente manera:

```python
ingesta = BashOperator(
    task_id='ejecutar_ingesta',
    bash_command='python /app/src/ingestion/extract.py'
)

transformacion = BashOperator(
    task_id='ejecutar_transformacion',
    bash_command='python /app/src/transform/clean.py'
)
```
Esto mantiene el código modular y separa la lógica de orquestación de la lógica de procesamiento.

---

## Manejo de errores y Logs en Airflow

Airflow ofrece mecanismos robustos para manejar fallos en la ejecución de tareas:

* **Reintentos automáticos (Retries):** Se configuran en los `default_args`. Si una tarea falla por una caída temporal de la red o de la base de datos, Airflow esperará un tiempo definido (retry_delay) y volverá a intentarlo.
* **Logs detallados:** Cada tarea ejecutada genera un archivo de log independiente. A través de la UI de Airflow, es posible hacer clic en una tarea fallida y leer el output exacto de la consola (stdout/stderr) para diagnosticar el problema sin necesidad de acceder al servidor.

---

## Ejecución manual vs programada

Airflow permite múltiples formas de iniciar (trigger) un DAG:

* **Ejecución Programada:** Definida por el parámetro `schedule_interval`. Puede usar una expresión cron (ej. `0 8 * * *` para todos los días a las 8 AM) o presets de Airflow (`@daily`, `@hourly`).
* **Ejecución Manual:** A través de la interfaz gráfica haciendo clic en el botón "Trigger DAG", útil para pruebas, reprocesamientos o pipelines a demanda.
* **Parámetro Catchup:** Si un DAG programado se activa tarde, el parámetro `catchup=True` obliga a Airflow a ejecutar todas las corridas pasadas que no sucedieron. En proyectos simples suele configurarse como `False` para evitar sobrecarga.

---

## Ejemplo de pipeline orquestado

A continuación, un DAG completo integrando nuestro caso práctico:

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_engineer',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'pipeline_transacciones_v1',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    extraer = BashOperator(task_id='extraer_datos', bash_command='python /opt/airflow/scripts/extract.py')
    transformar = BashOperator(task_id='transformar_datos', bash_command='python /opt/airflow/scripts/transform.py')
```

---

```python
    cargar = BashOperator(task_id='cargar_datos', bash_command='python /opt/airflow/scripts/load.py')

    extraer >> transformar >> cargar

```

---

## Buenas prácticas en DAGs

Para asegurar que el sistema de orquestación funcione correctamente a escala, se deben seguir principios clave de diseño:

* **Idempotencia:** Una tarea debe producir exactamente el mismo resultado final sin importar cuántas veces se ejecute para un periodo determinado.
* **Código ligero en el DAG:** El archivo de Python del DAG es parseado por Airflow constantemente. Evite colocar procesamiento de datos, lecturas a bases de datos o lógica pesada en la definición global del DAG.
* **Nomenclatura clara:** Utilice nombres descriptivos tanto para los `task_id` como para los nombres del DAG.
* **Separación de entornos:** Mantenga parámetros como credenciales o rutas absolutas como variables de entorno, no estáticas en el código.

---

<!-- _class: code -->
## Practica: Crear un DAG de Airflow para el pipeline ETL

**¿Qué vas a hacer?**
Ejecuta el script de este bloque para practicar dag simple con el dataset de transacciones del curso.

```python
# Extraído de: scripts/cap5/5_10_2_Script.py
"""
Capítulo 5: Automatización y orquestación
Sección 10: Orquestación e infraestructura
Bloque 2: DAG simple

Descripción:
Script de ejemplo para definir un DAG (Directed Acyclic Graph) en Apache Airflow.
Cubre la estructura del DAG, definición de tareas, establecimiento de dependencias, 
configuración de reintentos (manejo de errores) y buenas prácticas de logging.
"""

from datetime import datetime, timedelta
import logging
import random

# Bloque de importación seguro para evitar fallos si se ejecuta fuera de Airflow
try:
    from airflow import DAG

```

**Para ejecutarlo:**
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap5/5_10_2_Script.py`

---

## Errores comunes en el Bloque 5.10.2

- **Usar datetime.now() como start_date**
  → el DAG ejecuta todos los runs atrasados al activarse

- **Olvidar catchup=False**
  → Airflow intenta correr todas las fechas pasadas

- **No esperar a que las tasks upstream terminen**
  → dependencias rotas en el DAG

---

## Resumen: Bloque 5.10.2

**Lo que aprendiste:**
- Escribir un DAG Python con PythonOperator que ejecuta las funciones del pipeline
- Configurar el schedule y el start_date del DAG correctamente
- Monitorear la ejecución del DAG en la UI de Airflow

**Lo que construiste:**
El script `5_10_2_Script.py` que crear un dag de airflow para el pipeline etl usando el dataset de transacciones del curso.

**Siguiente paso →** Bloque 5.10.3: Infraestructura como código (demo)

---

<!-- ============================================================ -->
<!-- BLOQUE 5.10.3 — Infraestructura como código (demo)           -->
<!-- Scripts: scripts/cap5/5_10_3_Script.py                    -->
<!-- Notebook: notebooks/cap5/5_10_3_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 5.10.3
## Infraestructura como código (demo)

> Vemos cómo la infraestructura se define como código para hacer los entornos reproducibles.

**Al terminar este bloque podrás:**
- Entender qué es Infrastructure as Code (IaC) y sus beneficios
- Ver ejemplos de Terraform y Kubernetes para gestionar entornos de datos
- Comparar IaC con la configuración manual de servidores

---

# Capítulo 5: Automatización y orquestación, Sesión 10: Orquestación e infraestructura, Bloque 3: Infraestructura como código (Terraform demo)

## Introducción a la Infraestructura como Código (IaC)

La creación de recursos en la nube (bases de datos, servidores, almacenamiento) tradicionalmente se realizaba de forma manual a través de interfaces web o consolas. Este enfoque presenta un problema grave de provisión manual: es propenso a errores humanos, es difícil de replicar en distintos entornos (desarrollo, pruebas, producción) y carece de un historial de cambios.

La Infraestructura como Código (IaC) resuelve este problema permitiendo definir, desplegar y gestionar recursos de infraestructura utilizando archivos de configuración de texto plano. Al tratar la infraestructura como si fuera código de software, podemos aplicar las mismas buenas prácticas que usamos en Python: control de versiones, revisión de código y pruebas automáticas.

## Paradigmas de Código: Declarativo vs Imperativo e Introducción a Terraform

Existen dos enfoques principales al escribir código para infraestructura:

*   **Imperativo:** Define los pasos exactos que el sistema debe seguir para alcanzar el estado deseado (ej. "Ejecuta este comando para crear un servidor, luego ejecuta este otro para asignarle una IP").
*   **Declarativo:** Define el estado final deseado, y la herramienta se encarga de calcular los pasos necesarios para llegar a él (ej. "Quiero que exista un servidor con esta IP"). 

Terraform es una de las herramientas de IaC más populares de la industria y utiliza el paradigma declarativo. Su propósito no es atarnos a un solo proveedor de nube (como AWS, Google Cloud o Azure), sino ofrecernos un lenguaje estandarizado (HCL - HashiCorp Configuration Language) para comunicarnos con las APIs de cualquiera de ellos de manera uniforme.

## Estructura Básica de Terraform: Providers y Resources

Para que Terraform entienda qué debe crear y dónde, sus archivos de configuración se estructuran utilizando dos conceptos fundamentales:

*   **Provider:** Es el complemento (plugin) que permite a Terraform interactuar con una plataforma específica. Le indica a Terraform cómo autenticarse y cómo comunicarse con la API del proveedor de nube (por ejemplo, Google Cloud Platform o AWS).
*   **Resource:** Es el bloque de construcción básico. Representa un componente de infraestructura específico que queremos crear, como una máquina virtual, una base de datos MySQL o un bucket de almacenamiento.

En un archivo de Terraform, primero declaramos el `provider` con nuestras credenciales o región, y luego definimos uno o más bloques `resource` describiendo las propiedades de los recursos que nuestro pipeline de datos necesita.

## Flujo de Trabajo: Init, Plan, Apply y Demostración

El ciclo de vida básico al trabajar con Terraform consta de tres comandos secuenciales que garantizan un despliegue seguro:

1.  **terraform init:** Inicializa el directorio de trabajo descargando los binarios del *provider* especificado.
2.  **terraform plan:** Compara el estado actual de la infraestructura con el código que hemos escrito y muestra un plan de ejecución detallado con los cambios que se van a realizar (qué se creará, modificará o eliminará).
3.  **terraform apply:** Ejecuta el plan y realiza las llamadas a la API de la nube para aprovisionar la infraestructura real.

**Ejemplo demostrativo (Concepto de Bucket en la Nube):**

```text
provider "google" {
  project = "mi-proyecto-datos"
  region  = "us-central1"
}

resource "google_storage_bucket" "datalake_crudo" {
  name     = "curso-datos-raw-987654"
  location = "US"
}
```
*Al ejecutar apply sobre este código, Terraform asegurará la existencia de un bucket para nuestros archivos CSV o Parquet.*

## Reproducibilidad y la IaC como Práctica Moderna en Ingeniería

La mayor ventaja de la Infraestructura como Código es la **reproducibilidad**. Si el día de mañana ocurre un desastre y se borra nuestra infraestructura, o si un nuevo ingeniero de datos entra al equipo y necesita su propio entorno de pruebas, basta con ejecutar el código de Terraform para tener una réplica exacta de la arquitectura original en minutos.

En el contexto de nuestro pipeline de datos, la integración con IaC significa que antes de que Airflow o nuestros scripts de Python comiencen a mover y transformar datos, existe un proceso automatizado que garantiza que la base de datos MySQL y los buckets de almacenamiento ya existan y estén configurados correctamente con los permisos adecuados. 

Adoptar IaC es hoy una práctica moderna e indispensable en la ingeniería de datos, ya que unifica el desarrollo del software (transformaciones, APIs) con el entorno donde este software se ejecuta, creando sistemas verdaderamente robustos y escalables.

---

## Infraestructura como código (demo)

> **Bloque de demostración** — el instructor ejecuta en vivo.
> No hay script para correr en este bloque.

---

## Errores comunes en el Bloque 5.10.3

- **No versionar los archivos de infraestructura**
  → cambios no rastreables

- **Aplicar cambios directamente en producción sin test en staging**
  → riesgo alto

- **Ignorar el state de Terraform**
  → divergencia entre el código y la infraestructura real

---

## Resumen: Bloque 5.10.3

**Lo que aprendiste:**
- Entender qué es Infrastructure as Code (IaC) y sus beneficios
- Ver ejemplos de Terraform y Kubernetes para gestionar entornos de datos
- Comparar IaC con la configuración manual de servidores

**Lo que construiste:**
Comprendiste los conceptos de infraestructura como código (demo) a través de la demostración.

**Siguiente paso →** Bloque 5.10.4: Definición del proyecto final

---

<!-- ============================================================ -->
<!-- BLOQUE 5.10.4 — Definición del proyecto final                -->
<!-- Scripts: scripts/cap5/5_10_4_Script.py                    -->
<!-- Notebook: notebooks/cap5/5_10_4_Script.ipynb                -->
<!-- ============================================================ -->

<!-- _class: section -->
# Bloque 5.10.4
## Definición del proyecto final

> Con todas las piezas del curso aprendidas, definimos el proyecto final integrador.

**Al terminar este bloque podrás:**
- Entender los requisitos y criterios de evaluación del proyecto final
- Elegir el caso de uso de negocio para el proyecto personal
- Planificar las etapas del proyecto usando los conceptos del curso

---

## Introducción al proyecto final

El proyecto final representa la culminación de todo el aprendizaje adquirido a lo largo del curso. Hasta ahora, hemos construido componentes individuales y los hemos ido conectando paso a paso: desde la lectura de un archivo CSV hasta la orquestación de contenedores con Docker y Airflow.

El propósito de esta etapa es consolidar ese conocimiento mediante la construcción de un producto de datos funcional. Ya no se trata de seguir instrucciones paso a paso, sino de tomar decisiones de diseño, resolver problemas técnicos reales y demostrar que pueden construir un sistema de ingeniería de datos desde cero.

---

## Objetivo del proyecto

El objetivo principal es resolver un problema de datos simulando un entorno real de trabajo. Deberán demostrar su capacidad para:

*   Extraer datos de una fuente cruda (archivos, APIs o bases de datos).
*   Limpiar, transformar y preparar la información para su consumo.
*   Almacenar los datos de manera estructurada y eficiente.
*   Exponer o visualizar los datos procesados para generar valor.

Se busca evaluar tanto el funcionamiento técnico como la lógica detrás de las decisiones arquitectónicas que tomen.

---

## Rutas posibles para el proyecto

Reconociendo que la ingeniería de datos es un campo amplio, el proyecto final ofrece tres rutas distintas. Podrán seleccionar la que más se alinee con sus intereses o su perfil profesional:

*   **Ruta 1: Enfoque en Pipeline Backend:** Fuerte énfasis en la extracción, transformación compleja, manejo de errores y orquestación. Ideal para quienes buscan un perfil puro de Data Engineer.
*   **Ruta 2: Enfoque en Exposición (API):** Énfasis en la creación de servicios robustos con FastAPI, validación de datos, filtros avanzados y conexión eficiente a bases de datos.
*   **Ruta 3: Enfoque en Visualización (Dashboard):** Énfasis en la creación de una aplicación interactiva con Streamlit, cálculo de métricas de negocio y comunicación efectiva de insights a partir de datos procesados.

---

## Selección de enfoque por alumno

La elección de la ruta debe basarse en el área que deseen fortalecer o en la que se sientan más cómodos explorando a profundidad. 

Independientemente de la ruta elegida, todos los proyectos deben incluir un componente mínimo de procesamiento (leer datos, limpiarlos y guardarlos). La diferencia radica en dónde invertirán la mayor parte del tiempo de desarrollo y cuál será el entregable principal a demostrar durante las presentaciones.

---

## Definición de entregables mínimos

Para que un proyecto sea considerado completo, deberá contar con los siguientes entregables técnicos obligatorios:

1.  **Repositorio de código:** Estructurado, modular y con control de versiones.
2.  **Scripts de ejecución:** Archivos Python ejecutables (ingesta, transformación, carga).
3.  **Persistencia:** Evidencia de almacenamiento de datos (MySQL o archivos Parquet/CSV).
4.  **Reproducibilidad:** Archivo `requirements.txt` y/o `Dockerfile` y `docker-compose.yaml`.
5.  **Documentación:** Un archivo `README.md` que explique qué hace el proyecto, cómo configurarlo y cómo ejecutarlo.

---

## Criterios de evaluación

El proyecto final será evaluado bajo cuatro pilares fundamentales:

*   **Funcionalidad (40%):** El código se ejecuta sin errores fatales y cumple el objetivo propuesto. Los datos se procesan y exponen correctamente.
*   **Calidad del código (20%):** El código es modular, legible y utiliza buenas prácticas (nombres descriptivos, manejo de excepciones).
*   **Reproducibilidad (20%):** Cualquier persona con el repositorio y las instrucciones del README puede levantar el entorno y ejecutar el proyecto (uso correcto de Docker o entornos virtuales).
*   **Documentación y Presentación (20%):** Claridad al explicar el flujo de datos y justificación de las decisiones técnicas adoptadas.

---

## Ejemplos de proyectos

Para ayudarles a dimensionar el alcance, aquí presentamos algunos ejemplos válidos:

*   **Ejemplo 1 (Ruta Pipeline):** Ingesta diaria de un dataset público de crímenes, limpieza de coordenadas y fechas, almacenamiento en PostgreSQL y orquestación para generar un reporte automatizado.
*   **Ejemplo 2 (Ruta API):** Pipeline que procesa datos históricos de clima, los guarda en MySQL y levanta una API con FastAPI que permite consultar promedios de temperatura por ciudad y rango de fechas.
*   **Ejemplo 3 (Ruta Dashboard):** Procesamiento de un log de transacciones bancarias simuladas para limpiar nulos y categorizar gastos, conectado a un dashboard interactivo en Streamlit que muestra el flujo de caja.

---

## Integración de componentes del curso

El proyecto debe reflejar un sistema integrado. No se trata de scripts aislados, sino de un flujo de trabajo continuo:

1.  **Fundamentos y Pandas:** Para la lógica de limpieza y transformación (DataFrames, control de nulos, métricas).
2.  **Bases de Datos y SQL:** Para el almacenamiento estructurado y consultas eficientes.
3.  **FastAPI o Streamlit:** Como capa de exposición de los resultados.
4.  **Docker:** Para encapsular todo el sistema y garantizar que funcione en cualquier máquina.

La conexión fluida entre estas herramientas es el verdadero reto de la ingeniería de datos.

---

## Buenas prácticas para el proyecto

Para asegurar el éxito en el desarrollo, mantengan presentes las siguientes recomendaciones:

*   **Modularidad:** Eviten archivos de mil líneas. Separen la configuración, la extracción, la transformación y las bases de datos en distintos módulos o carpetas.
*   **Manejo de errores:** Utilicen bloques `try/except` donde sea crítico, especialmente en la lectura de datos y conexiones a bases de datos.
*   **Control de rutas:** Usen librerías como `os` o `pathlib` para manejar rutas relativas, garantizando que los archivos se encuentren sin importar la máquina.
*   **Semillas y determinismo:** Si generan datos aleatorios para pruebas, fijen una semilla (ej. 987654) para que los resultados sean predecibles.

---

## Planificación del desarrollo

Un proyecto de ingeniería requiere planificación. Eviten escribir código sin antes entender el flujo de datos. Se sugiere el siguiente cronograma de desarrollo:

1.  **Fase 1 (Diseño):** Definir la ruta, buscar el dataset y dibujar en papel la arquitectura de los datos (de dónde vienen, qué transformaciones sufren, a dónde van).
2.  **Fase 2 (Desarrollo Core):** Escribir los scripts de extracción y transformación con Pandas. Validar que los datos queden limpios.
3.  **Fase 3 (Almacenamiento y Exposición):** Conectar la base de datos y desarrollar la API o el Dashboard.
4.  **Fase 4 (Empaquetado):** Generar los archivos de Docker y pulir el README.

---

## Preparación para implementación y presentación

Una vez finalizado el desarrollo, la etapa final es la presentación. El trabajo de un ingeniero de datos no es solo escribir código, sino saber comunicarlo.

*   **Preparen una demostración (Demo):** Asegúrense de tener el entorno listo para mostrar el código en acción. Tengan datos de prueba preparados.
*   **Estructuren su discurso:** Comiencen por el problema que resuelve su sistema, pasen por la arquitectura de alto nivel y terminen con la demostración funcional.
*   **Anticipen fallos:** En las presentaciones en vivo, los sistemas pueden fallar. Tengan los logs accesibles para demostrar que, si algo falla, saben dónde buscar el error.

---

## Definición del proyecto final

> **Bloque de demostración** — el instructor ejecuta en vivo.
> No hay script para correr en este bloque.

---

## Errores comunes en el Bloque 5.10.4

- **Elegir un caso de uso demasiado amplio**
  → el proyecto no se termina a tiempo

- **No definir el schema del dato desde el principio**
  → refactorizaciones costosas

- **Trabajar sin control de versiones desde el día 1**
  → pérdida de trabajo

---

## Resumen: Bloque 5.10.4

**Lo que aprendiste:**
- Entender los requisitos y criterios de evaluación del proyecto final
- Elegir el caso de uso de negocio para el proyecto personal
- Planificar las etapas del proyecto usando los conceptos del curso

**Lo que construiste:**
Comprendiste los conceptos de definición del proyecto final a través de la demostración.

**Siguiente paso →** Bloque 6.11.1: Introducción a GitHub y repositorios