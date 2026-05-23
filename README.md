# Proyecto 4: Docker Multi-Container App
 
**Aplicación Full Stack con Docker Compose que demuestra orquestación de múltiples servicios.**
 
## 📋 Descripción
 
Este proyecto implementa una **aplicación de gestión de tareas (Task Manager)** utilizando Docker Compose. Combina tres servicios independientes en una arquitectura containerizada:
 
- **Frontend:** React con Axios para consumir API
- **Backend:** Flask REST API con psycopg2
- **Base de datos:** PostgreSQL 15
Todos los servicios se comunican a través de una red Docker personalizada y utilizan volúmenes para persistencia de datos.
 
---
 
## 🏗️ Arquitectura
 
```
┌─────────────────────────────────────────────────────┐
│           Docker Compose Network                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐   │
│  │   Frontend   │  │   Backend    │  │   DB     │   │
│  │   (React)    │──│  (Flask)     │──│(Postgres)│   │
│  │  :3000       │  │   :5000      │  │  :5432   │   │
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
| Containerization | Docker | 29.4.3+ |
| Orquestación | Docker Compose | 5.1.3+ |
 
---
 
## 📦 Estructura del Proyecto
 
```
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
│   ├── app.py                  # Aplicación principal
│   ├── requirements.txt         # Dependencias Python
│   └── Dockerfile              # Imagen del backend
│
├── database/                    # Configuración de BD
│   └── init.sql                # Script de inicialización
│
├── docker-compose.yml          # Orquestación de servicios
└── README.md                   # Este archivo
```
 
---
 
## 🚀 Inicio Rápido
 
### Prerequisitos
 
- **Docker** 29.0
- **Docker Compose** 5.0+ (incluido en Docker Desktop)
- **Git** (para clonar el repo)
### Instalación
 
1. **Clona el repositorio:**
```bash
git clone https://github.com/Ferdev49/Docker-compose.git
cd Docker-compose
```
 
2. **Inicia los servicios:**
```bash
docker-compose up -d
```
 
3. **Espera a que los servicios estén listos (~2 minutos):**
```bash
docker-compose logs -f
```
 
Deberías ver:
```
✅ DB ready
Running on http://0.0.0.0:5000
webpack compiled successfully
```
 
4. **Accede a la aplicación:**
```
http://localhost:3000
```
 
---
 
## 🎮 Uso
 
### Interfaz de Usuario
 
La aplicación permite:
 
- ✅ **Ver tareas:** Lista todas las tareas almacenadas
- ✅ **Crear tareas:** Añade nuevas tareas con un título
- ✅ **Marcar completadas:** Checkbox para marcar/desmarcar
- ✅ **Eliminar tareas:** Botón "×" para eliminar
### Endpoints de API
 
**Base URL:** `http://localhost:5000`
 
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks` | Obtiene todas las tareas |
| POST | `/api/tasks` | Crea una nueva tarea |
| PUT | `/api/tasks/<id>` | Actualiza estado de tarea |
| DELETE | `/api/tasks/<id>` | Elimina una tarea |
| GET | `/health` | Health check |
 
### Ejemplo de uso con curl
 
```bash
# Obtener tareas
curl http://localhost:5000/api/tasks
 
# Crear tarea
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Mi tarea"}'
 
# Marcar como completada
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
 
# Eliminar tarea
curl -X DELETE http://localhost:5000/api/tasks/1
```
 
---
 
## 📊 Variables de Entorno
 
### Base de Datos
 
```
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
POSTGRES_DB: taskdb
```
 
### Frontend
 
```
REACT_APP_API_URL: http://localhost:5000
```
 
---
 
## 🔧 Comandos Útiles
 
### Docker Compose
 
```bash
# Inicia servicios
docker-compose up -d
 
# Ve los logs
docker-compose logs -f
 
# Logs de un servicio específico
docker-compose logs backend
 
# Ver estado de servicios
docker-compose ps
 
# Detén servicios
docker-compose down
 
# Limpia volúmenes (resetea BD)
docker-compose down -v
```
 
### Debugging
 
```bash
# Accede a la consola de un contenedor
docker-compose exec backend sh
 
# Ve logs detallados
docker-compose logs --tail 100
 
# Reinicia un servicio
docker-compose restart frontend
```
 
---
 
## 🗄️ Base de Datos
 
### Tabla `tasks`
 
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE
);
```
 
### Conexión Directa
 
```bash
# Accede a PostgreSQL
docker-compose exec postgres psql -U postgres -d taskdb
 
# Consulta tareas
SELECT * FROM tasks;
```
 
---
 
## 🐛 Solución de Problemas
 
### El frontend no carga
 
```bash
# Reconstruye el contenedor
docker-compose down
docker-compose up -d --build
 
# Ve los logs
docker-compose logs frontend
```
 
### La API no responde
 
```bash
# Verifica el backend
docker-compose logs backend
 
# Prueba conexión
curl http://localhost:5000/health
```
 
### Problema de conexión a BD
 
```bash
# Reinicia la BD
docker-compose restart postgres
 
# Resetea volúmenes
docker-compose down -v
docker-compose up -d
```
 
---
 
## 📝 Características Implementadas
 
- ✅ **Múltiples contenedores orquestados** con Docker Compose
- ✅ **Networking entre servicios** a través de red bridge
- ✅ **Volúmenes persistentes** para datos de PostgreSQL
- ✅ **Health checks** para cada servicio
- ✅ **Variables de entorno** para configuración
- ✅ **Dependencias de servicios** definidas correctamente
- ✅ **CORS habilitado** en el backend para el frontend
- ✅ **Inicialización automática** de la base de datos
---
 
## 🎓 Aprendizajes Clave
 
Este proyecto demuestra:
 
1. **Containerización:** Crear y optimizar Dockerfiles
2. **Orquestación:** Usar Docker Compose para múltiples servicios
3. **Networking:** Comunicación entre contenedores
4. **Persistencia:** Volúmenes y bases de datos
5. **Full Stack:** Frontend, backend y base de datos
6. **API REST:** Operaciones CRUD completas
---
 
## 🤝 Contribuciones
 
Las contribuciones son bienvenidas. Para cambios mayores:
 
1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -m 'Añade mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request
