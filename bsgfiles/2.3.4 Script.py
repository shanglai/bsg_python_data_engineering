```python
# -*- coding: utf-8 -*-

# =============================================================================
# Capítulo 2: Almacenamiento y consultas de datos
# Sección 3: SQL y MySQL
# Bloque 4: Inserción y consulta de datos del pipeline
# =============================================================================

# Descripción:
# Este script implementa la fase final del flujo ETL (Extract, Transform, Load).
# Se genera un conjunto de datos, se transforma y se carga (INSERT) en una 
# base de datos MySQL. Finalmente, se realizan consultas (SELECT) para 
# validar la consistencia de los datos almacenados.

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
    fechas = [datetime.now() - timedelta(days=i) for i in range(100)]
    
    datos = []
    for i in range(1, 101):
        datos.append({
            'id_transaccion': i,
            'id_cliente': random.randint(100, 150),
            'monto': round(random.uniform(10.0, 500.0), 2) if random.random() > 0.05 else None, # 5% nulos
            'fecha': random.choice(fechas).strftime('%Y-%m-%d'),
            'estado': random.choice(['completado', 'pendiente', 'fallido', 'completado'])
        })
    
    df = pd.DataFrame(datos)
    print(f"Datos extraídos: {len(df)} registros.")
    return df

# =============================================================================
# 2. TRANSFORMAR (Transform)
# =============================================================================
def transformar_datos(df):
    """
    Limpiar y transformar los datos extraídos.
    Manejar nulos y filtrar transacciones válidas.
    """
    print("Iniciando transformación de datos...")
    
    # Copiar el DataFrame para no modificar el original
    df_clean = df.copy()
    
    # Manejar valores nulos rellenando con 0 (o imputando la media, según negocio)
    df_clean['monto'] = df_clean['monto'].fillna(0.0)
    
    # Filtrar solo transacciones completadas
    df_clean = df_clean[df_clean['estado'] == 'completado']
    
    # Asegurar tipos de datos correctos
    df_clean['monto'] = df_clean['monto'].astype(float)
    
    print(f"Datos transformados: {len(df_clean)} registros listos para cargar.")
    return df_clean

# =============================================================================
# 3. CARGAR (Load) - Configuración y Conexión a MySQL
# =============================================================================
def crear_conexion_mysql(host, usuario, contrasena, base_datos):
    """
    Establecer la conexión con la base de datos MySQL.
    Incluye manejo de errores para asegurar la consistencia.
    """
    conexion = None
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=usuario,
            password=contrasena,
            database=base_datos
        )
        if conexion.is_connected():
            print("Conexión exitosa a MySQL.")
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
    
    return conexion

def crear_tabla_si_no_existe(conexion):
    """
    Crear la tabla de destino para asegurar que la estructura (esquema) 
    esté lista antes de la inserción de datos.
    """
    query_creacion = """
    CREATE TABLE IF NOT EXISTS transacciones_procesadas (
        id_transaccion INT PRIMARY KEY,
        id_cliente INT,
        monto DECIMAL(10, 2),
        fecha DATE,
        estado VARCHAR(50)
    );
    """
    try:
        cursor = conexion.cursor()
        cursor.execute(query_creacion)
        conexion.commit()
        print("Tabla 'transacciones_procesadas' verificada/creada exitosamente.")
    except Error as e:
        print(f"Error al crear la tabla: {e}")

def cargar_datos_mysql(conexion, df):
    """
    Insertar datos desde el DataFrame hacia la tabla en MySQL.
    Se utiliza executemany para inserciones por lotes (batch), mejorando la performance.
    """
    print("Iniciando carga de datos en base de datos...")
    
    # Convertir el DataFrame a una lista de tuplas para ejecutemany
    datos_a_insertar = [tuple(x) for x in df.to_numpy()]
    
    # Consulta SQL parametrizada para prevenir SQL Injection y errores de formato
    query_insercion = """
    INSERT INTO transacciones_procesadas (id_transaccion, id_cliente, monto, fecha, estado)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    monto = VALUES(monto), estado = VALUES(estado);
    """
    
    try:
        cursor = conexion.cursor()
        # Inserción masiva
        cursor.executemany(query_insercion, datos_a_insertar)
        # Confirmar la transacción (consistencia de datos)
        conexion.commit()
        print(f"Carga exitosa: {cursor.rowcount} registros insertados o actualizados.")
    except Error as e:
        print(f"Error durante la carga de datos: {e}")
        # Revertir cambios en caso de error
        conexion.rollback()

# =============================================================================
# 4. VALIDAR (Consultar)
# =============================================================================
def validar_datos_cargados(conexion):
    """
    Realizar consultas SQL desde Python para asegurar la integridad
    de los datos almacenados (conteo, métricas básicas).
    """
    print("Validando datos persistidos...")
    try:
        cursor = conexion.cursor(dictionary=True)
        
        # Validación 1: Conteo total de registros
        cursor.execute("SELECT COUNT(*) AS total_registros FROM transacciones_procesadas;")
        resultado_conteo = cursor.fetchone()
        print(f"Total de registros en DB: {resultado_conteo['total_registros']}")
        
        # Validación 2: Métrica de negocio (Ingresos totales y ticket promedio)
        query_metricas = """
        SELECT 
            SUM(monto) AS ingresos_totales,
            AVG(monto) AS ticket_promedio
        FROM transacciones_procesadas;
        """
        cursor.execute(query_metricas)
        resultado_metricas = cursor.fetchone()
        print(f"Ingresos Totales: ${resultado_metricas['ingresos_totales']:,.2f}")
        print(f"Ticket Promedio: ${resultado_metricas['ticket_promedio']:,.2f}")
        
    except Error as e:
        print(f"Error al validar los datos: {e}")

# =============================================================================
# 5. INTEGRACIÓN DEL PIPELINE COMPLETO
# =============================================================================
def ejecutar_pipeline():
    """
    Función principal que orquesta el flujo ETL completo.
    """
    print("=== INICIANDO PIPELINE DE DATOS V1 ===")
    
    # 1. Extracción
    df_raw = extraer_datos_transacciones()
    
    # 2. Transformación
    df_transformed = transformar_datos(df_raw)
    
    # Configuración de base de datos (NOTA: Reemplazar con credenciales reales)
    # Para fines de este script se usan credenciales de ejemplo (localhost)
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'password'
    DB_NAME = 'curso_de'
    
    # 3. Conexión y Carga
    # Nota de ejecución: Si no tienes MySQL corriendo, las siguientes líneas 
    # generarán el mensaje de error gestionado por nuestro bloque try/except.
    conexion = crear_conexion_mysql(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    
    if conexion and conexion.is_connected():
        # Preparar almacenamiento estructurado
        crear_tabla_si_no_existe(conexion)
        
        # Cargar los datos
        cargar_datos_mysql(conexion, df_transformed)
        
        # 4. Validación post-carga (Base para el consumo vía API)
        validar_datos_cargados(conexion)
        
        # Cerrar conexión de forma segura
        conexion.cursor().close()
        conexion.close()
        print("Conexión a MySQL cerrada. Pipeline finalizado.")
    else:
        print("Pipeline finalizado con advertencias: No se pudo conectar a la base de datos para la etapa de Carga.")

# Ejecutar el script principal
if __name__ == "__main__":
    ejecutar_pipeline()
```