# Proyecto 4: Docker Multi-Container App

**Aplicación Full Stack con Docker Compose que demuestra orquestación de múltiples servicios.**

## 📋 Descripción

Este proyecto implementa una **aplicación de gestión de tareas (Task Manager)** utilizando Docker Compose. Combina tres servicios independientes en una arquitectura containerizada:

- **Frontend:** React con Axios para consumir API
- **Backend:** Flask REST API con SQLAlchemy y psycopg2
- **Base de datos:** PostgreSQL 15 (Alpine)

Todos los servicios se comunican a través de una red Docker personalizada y utilizan volúmenes nombrados para asegurar la persistencia de los datos.

---

## 🏗️ Arquitectura
```text
┌─────────────────────────────────────────────────────┐
│           Docker Compose Network                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐   │
│  │   Frontend   │  │   Backend    │  │    DB    │   │
│  │   (React)    │──│   (Flask)    │──│(Postgres)│   │
│  │   :3000      │  │   :5000      │  │  :5432   │   │
│  └──────────────┘  └──────────────┘  └──────────┘   │
│       Port 3000         Port 5000       Port 5432   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Tecnologías Utilizadas

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Frontend | React | 18.2.0 |
| Backend | Flask | 3.0.0 |
| Database | PostgreSQL | 15-alpine |
| Orquestación | Docker Compose | v2.20+ |

---

## 📦 Estructura del Proyecto
```text

proyecto4-docker-compose/
├── frontend/                    # Aplicación React
│   ├── public/
│   │   └── index.html          # Punto de entrada HTML
│   ├── src/
│   │   ├── App.jsx             # Componente principal
│   │   ├── App.css             # Estilos
│   │   └── index.js            # Root de React
│   ├── Dockerfile              # Imagen del frontend
│   └── package.json            # Dependencias Node.js
│
├── backend/                     # API Flask
│   ├── app.py                  # Aplicación principal (Endpoints)
│   ├── requirements.txt         # Dependencias Python (Flask, SQLAlchemy)
│   └── Dockerfile              # Imagen del backend
│
├── database/                    # Configuración de BD
│   └── init.sql                # Script de inicialización estructural
│
├── docker-compose.yml          # Orquestación de servicios y redes
└── README.md                   # Este archivo
```

---

## 🚀 Inicio Rápido

### Prerrequisitos

- **Docker Desktop** (Debe incluir soporte para Docker Compose v2 o superior)
- **Git** (Para clonar el repositorio)

### Instalación

1. **Clona el repositorio:**
git clone https://github.com/Ferdev49/Docker-compose.git
cd Docker-compose

2. **Inicia los servicios en segundo plano:**
docker-compose up -d --build

3. **Monitorea los logs para verificar el arranque exitoso:**
docker-compose logs -f

Deberías ver que el backend levanta tras validar el estado de la base de datos:
[INFO] ✅ DB ready / healthy
[INFO] Running on http://0.0.0.0:5000
[INFO] webpack compiled successfully

4. **Accede a la aplicación:**
- **Interfaz de Usuario (Frontend):** http://localhost:3000
- **Health Check de la API (Backend):** http://localhost:5000/health

---

## 🎮 Uso y API Endpoints

### Endpoints de la API REST

Base URL: http://localhost:5000

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/tasks | Obtiene todas las tareas |
| POST | /api/tasks | Crea una nueva tarea |
| PUT | /api/tasks/<id> | Actualiza estado de una tarea |
| DELETE | /api/tasks/<id> | Elimina una tarea por ID |
| GET | /health | Estado de salud del Backend |

### Pruebas rápidas con curl

# Obtener todas las tareas
curl http://localhost:5000/api/tasks

# Crear una nueva tarea
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Configurar Github Actions"}'

---

## 📊 Variables de Entorno y Credenciales

Las credenciales se encuentran centralizadas en el archivo docker-compose.yml para el aprovisionamiento de la base de datos y la inyección en el Backend de Flask:

### Base de Datos & Backend Link
POSTGRES_USER: appuser
POSTGRES_PASSWORD: app_password
POSTGRES_DB: app_db
DATABASE_URL: postgresql://appuser:app_password@db:5432/app_db

---

## 🔧 Comandos Útiles

### Gestión de Contenedores

### Iniciar servicios construyendo imágenes desde cero
```
docker-compose up -d --build
```

### Ver estado y salud actual de los servicios
```
docker-compose ps
```
### Revisar logs en tiempo real de un servicio específico
```
docker-compose logs backend
```
### Detener los contenedores manteniendo el almacenamiento
```
docker-compose down
```
### Destruir contenedores y borrar volúmenes (Reinicializar base de datos)
```
docker-compose down -v
```
### Conexión Directa a la Base de Datos

Si necesitas interactuar directamente con el motor de PostgreSQL persistido dentro de Docker, ejecuta:

### Acceso interactivo mediante CLI psql
```
docker-compose exec db psql -U appuser -d app_db
```
## Comando de prueba en la consola de Postgres
```
SELECT * FROM tasks;
```
---

## 📝 Características de Infraestructura Implementadas

- ✅ **Orquestación Multi-contenedor:** Flujo automatizado unificando Frontend, Backend y BD en un solo comando.
- ✅ **Aislamiento de Red:** Uso de redes bridge nativas de Docker para denegar tráfico externo directo a la BD y permitir resolución por DNS interno (@db:5432).
- ✅ **Persistencia del Estado:** Volúmenes nombrados (postgres_data) para prevenir la pérdida de información en ciclos de down/up.
- ✅ **Arranque Secuencial Resiliente:** Uso de depends_on condicionado a service_healthy con pg_isready, garantizando que Flask no inicie hasta que Postgres acepte conexiones.
- ✅ **Inicialización Automatizada:** Montaje de scripts SQL estructurales directo al punto de entrada (/docker-entrypoint-initdb.d/).

---

## 🗄️ Estructura SQL Base (init.sql)

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---

## 🎓 Aprendizajes Clave

Este proyecto consolida conceptos fundamentales de ingeniería DevOps:
1. **Containerización Avanzada:** Construcción y empaquetado de entornos Python y Node de forma aislada.
2. **Políticas de Red y Seguridad en Docker:** Exposición controlada de puertos y manejo de variables de entorno de forma segura.
3. **Depuración de Sistemas Distribuidos:** Análisis de trazas de error en entornos desacoplados mediante logs de contenedores.