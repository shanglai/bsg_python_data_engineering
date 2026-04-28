-- ============================================================
-- BSG Institute — Python para Ingeniería de Datos
-- Schema inicial del caso práctico: Dataset de Transacciones
-- ============================================================

CREATE DATABASE IF NOT EXISTS bsg_curso
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS bsg_airflow
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE bsg_curso;

-- Tabla principal de transacciones (raw)
CREATE TABLE IF NOT EXISTS transacciones_raw (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(20),
    fecha         VARCHAR(20),          -- raw: puede tener formatos inconsistentes
    customer_id   VARCHAR(20),
    amount        VARCHAR(20),          -- raw: puede ser string con $ o None
    status        VARCHAR(20),
    store         VARCHAR(50),
    cargado_en    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de transacciones limpias (procesadas por el pipeline)
CREATE TABLE IF NOT EXISTS transacciones_clean (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id   VARCHAR(20) UNIQUE NOT NULL,
    fecha            DATE NOT NULL,
    customer_id      INT,
    amount           DECIMAL(10,2) NOT NULL,
    status           ENUM('COMPLETADA','PENDIENTE','FALLIDA','CANCELADA') NOT NULL,
    store            VARCHAR(50),
    procesado_en     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de métricas agregadas (generada por el pipeline)
CREATE TABLE IF NOT EXISTS metricas_diarias (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    fecha            DATE NOT NULL,
    store            VARCHAR(50),
    total_ventas     DECIMAL(12,2),
    num_transacciones INT,
    ticket_promedio  DECIMAL(10,2),
    calculado_en     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_fecha_store (fecha, store)
);

-- Usuario de solo lectura para demos de FastAPI
GRANT SELECT ON bsg_curso.* TO 'bsg_user'@'%';
GRANT ALL PRIVILEGES ON bsg_airflow.* TO 'bsg_user'@'%';
FLUSH PRIVILEGES;
