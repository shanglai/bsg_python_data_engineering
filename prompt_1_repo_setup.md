# PROMPT 1 — Estructura del repo y configuración de entorno
# Ejecutar primero, desde la raíz del repo clonado
# Repo: https://github.com/shanglai/bsg_python_data_engineering

## CONTEXTO

Estás configurando el repositorio base para un curso llamado
**"Python para Ingeniería de Datos"** de BSG Institute.

- Alumnos sin experiencia técnica previa (no tech-savvy)
- Duración: ~2 meses, inicio 2026-04-28
- Repo público en GitHub: shanglai/bsg_python_data_engineering
- Entorno principal: GitHub Codespaces
- Entorno secundario: Google Colab (capítulos 1-3)
- Entorno terciario: Play with Docker (capítulos 4-5, Docker)

---

## TAREA

Crea la estructura completa del repositorio y todos los archivos
de configuración de entorno. No toques archivos que ya existan.

---

## PASO 1 — Crear estructura de carpetas

Crea exactamente esta estructura (solo carpetas y .gitkeep donde se indica):

```
.devcontainer/
    mysql-init/
        .gitkeep
.github/
    workflows/
        .gitkeep
slides/
    .gitkeep
scripts/
    cap1/
    cap2/
    cap3/
    cap4/
    cap5/
    cap6/
data/
    raw/
        .gitkeep
    processed/
        .gitkeep
dags/
    .gitkeep
notebooks/
    cap1/
    cap2/
    cap3/
    cap4/
    cap5/
    cap6/
bsgfiles/
    .gitkeep
```

Si ya existe `bsgfiles/` con archivos, no la toques.
Si ya existe `bsg-theme.css`, no lo toques.

---

## PASO 2 — requirements.txt (entorno completo — Codespaces)

Crea `requirements.txt` en la raíz con exactamente estas versiones:

```
# ── Core data ──────────────────────────────────────────────
pandas==2.2.3
pyarrow==16.1.0
numpy==1.26.4

# ── Database ───────────────────────────────────────────────
mysql-connector-python==9.0.0
SQLAlchemy==2.0.35

# ── API ────────────────────────────────────────────────────
fastapi==0.115.5
uvicorn==0.30.6
pydantic==2.9.2
httpx==0.27.2

# ── Visualization ──────────────────────────────────────────
streamlit==1.39.0

# ── Orchestration ──────────────────────────────────────────
apache-airflow==2.10.3

# ── DevOps / Containers ────────────────────────────────────
# (Docker se instala en el devcontainer, no aquí)

# ── Notebooks ──────────────────────────────────────────────
jupytext==1.16.4
jupyter==1.1.1
ipykernel==6.29.5

# ── Utilities ──────────────────────────────────────────────
python-dotenv==1.0.1
requests==2.32.3
```

---

## PASO 3 — requirements-colab.txt (subset ligero para Colab)

Crea `requirements-colab.txt` en la raíz:

```
# Instalar en Colab con: !pip install -r requirements-colab.txt -q
# Capítulos 1-3 únicamente

pandas==2.2.3
pyarrow==16.1.0
mysql-connector-python==9.0.0
SQLAlchemy==2.0.35
fastapi==0.115.5
uvicorn==0.30.6
pydantic==2.9.2
httpx==0.27.2
streamlit==1.39.0
python-dotenv==1.0.1
requests==2.32.3
```

---

## PASO 4 — .devcontainer/devcontainer.json

Crea `.devcontainer/devcontainer.json`:

```json
{
  "name": "BSG Python Data Engineering",
  "dockerComposeFile": "docker-compose.yml",
  "service": "workspace",
  "workspaceFolder": "/workspace",

  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.12"
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },

  "postCreateCommand": "pip install -r requirements.txt && echo '✅ Entorno listo'",

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-toolsai.jupyter",
        "marp-team.marp-vscode",
        "mtxr.sqltools",
        "mtxr.sqltools-driver-mysql",
        "ms-azuretools.vscode-docker",
        "eamodio.gitlens"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "editor.formatOnSave": true,
        "editor.fontSize": 14,
        "terminal.integrated.fontSize": 13
      }
    }
  },

  "forwardPorts": [
    3306,
    8080,
    8501,
    8793
  ],

  "portsAttributes": {
    "3306": { "label": "MySQL" },
    "8080": { "label": "FastAPI / Airflow UI" },
    "8501": { "label": "Streamlit" },
    "8793": { "label": "Airflow API" }
  },

  "remoteEnv": {
    "MYSQL_HOST": "mysql",
    "MYSQL_PORT": "3306",
    "MYSQL_USER": "bsg_user",
    "MYSQL_PASSWORD": "bsg_pass",
    "MYSQL_DATABASE": "bsg_curso",
    "AIRFLOW_HOME": "/workspace/airflow_home",
    "AIRFLOW__CORE__LOAD_EXAMPLES": "False",
    "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN": "mysql+mysqlconnector://bsg_user:bsg_pass@mysql:3306/bsg_airflow"
  }
}
```

---

## PASO 5 — .devcontainer/docker-compose.yml

Crea `.devcontainer/docker-compose.yml`:

```yaml
version: "3.9"

services:

  # ── Espacio de trabajo principal ──────────────────────────
  workspace:
    image: mcr.microsoft.com/devcontainers/python:3.12
    volumes:
      - ..:/workspace:cached
    working_dir: /workspace
    command: sleep infinity
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_PORT=3306
      - MYSQL_USER=bsg_user
      - MYSQL_PASSWORD=bsg_pass
      - MYSQL_DATABASE=bsg_curso
    depends_on:
      mysql:
        condition: service_healthy
    networks:
      - bsg_net

  # ── MySQL 8 ───────────────────────────────────────────────
  mysql:
    image: mysql:8.0
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: root_pass
      MYSQL_DATABASE: bsg_curso
      MYSQL_USER: bsg_user
      MYSQL_PASSWORD: bsg_pass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql-init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "bsg_user", "-pbsg_pass"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - bsg_net

volumes:
  mysql_data:

networks:
  bsg_net:
    driver: bridge
```

---

## PASO 6 — .devcontainer/mysql-init/init.sql

Crea `.devcontainer/mysql-init/init.sql`:

```sql
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
```

---

## PASO 7 — .env.example

Crea `.env.example` en la raíz:

```bash
# Copia este archivo como .env y ajusta los valores
# Nunca subas .env a GitHub

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=bsg_user
MYSQL_PASSWORD=bsg_pass
MYSQL_DATABASE=bsg_curso

AIRFLOW_HOME=./airflow_home
AIRFLOW__CORE__LOAD_EXAMPLES=False
```

---

## PASO 8 — .gitignore

Crea `.gitignore` en la raíz:

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
venv/
env/

# Datos sensibles
.env
*.csv
*.parquet
!data/raw/.gitkeep
!data/processed/.gitkeep

# Airflow
airflow_home/
logs/
*.log

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/settings.json
.idea/
```

---

## PASO 9 — README.md

Crea `README.md` en la raíz con este contenido exacto:

````markdown
# Python para Ingeniería de Datos
### BSG Institute · 2026

Curso práctico de ingeniería de datos construido alrededor de un
**pipeline de transacciones de extremo a extremo**.

---

## 🗺️ Estructura del curso

| Capítulo | Tema | Entorno |
|---|---|---|
| 1 | Fundamentos de Python y Pandas | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap1/) |
| 2 | SQL, MySQL y Pipeline v1 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap2/) |
| 3 | FastAPI y Streamlit | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap3/) |
| 4 | Formatos, Storage y Docker | [![Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering) · [Play with Docker](https://labs.play-with-docker.com/) |
| 5 | Airflow y Automatización | [![Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering) |
| 6 | CI/CD, Monitoreo y Proyecto Final | [![Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering) |

---

## 🚀 Cómo empezar

### Opción A — Google Colab (Capítulos 1, 2 y 3)
1. Haz clic en el badge **Open in Colab** del capítulo correspondiente
2. En Colab: `Archivo → Guardar una copia en Drive`
3. En la primera celda del notebook, ejecuta:
   ```python
   !pip install -r requirements-colab.txt -q
   ```

### Opción B — GitHub Codespaces (Capítulos 4, 5 y 6)
1. Haz clic en el badge **Abrir en Codespaces**
2. Espera ~3 minutos mientras se instala el entorno
3. Abre la terminal integrada — todo estará listo

### Opción C — Local (avanzado)
```bash
git clone https://github.com/shanglai/bsg_python_data_engineering.git
cd bsg_python_data_engineering
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

---

## 📁 Estructura del repositorio

```
├── slides/          # Presentaciones Marpit por capítulo
├── scripts/         # Scripts .py por bloque (cap1/ cap2/ ...)
├── notebooks/       # Notebooks .ipynb para Colab (generados de scripts/)
├── data/            # Datos del caso práctico
│   ├── raw/         # Datos crudos generados en el Bloque 1.1.1
│   └── processed/   # Datos limpios generados por el pipeline
├── dags/            # DAGs de Apache Airflow (Capítulo 5)
├── bsgfiles/        # Archivos fuente originales de slides
└── .devcontainer/   # Configuración de GitHub Codespaces
```

---

## 🛠️ Stack tecnológico

| Herramienta | Versión | Uso en el curso |
|---|---|---|
| Python | 3.12 | Lenguaje principal |
| Pandas | 2.2.3 | Transformación de datos |
| MySQL | 8.0 | Base de datos relacional |
| FastAPI | 0.115.5 | API REST |
| Streamlit | 1.39.0 | Dashboard |
| Apache Airflow | 2.10.3 | Orquestación |
| Docker | latest | Contenedores |

---

*BSG Institute · Todos los derechos reservados · 2026*
````

---

## PASO 10 — Verificación final

Al terminar, ejecuta los siguientes comandos y muestra el output:

```bash
# Verificar estructura creada
find . -not -path './.git/*' -not -path './bsgfiles/*' | sort

# Verificar que no se tocaron archivos existentes
git status
```

Reporta:
- Archivos creados exitosamente
- Archivos que ya existían y no se tocaron
- Cualquier error encontrado
