# 🐳 Guía de Docker - MoveTracker

Esta guía explica cómo usar Docker para ejecutar el proyecto MoveTracker.

## 📋 Requisitos Previos

- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado

## 🚀 Inicio Rápido

### 1. Clonar el repositorio
```bash
git clone https://github.com/Cristhian036/MoveTracker.git
cd MoveTracker
```

### 2. Levantar los servicios
```bash
docker-compose up --build
```

### 3. Acceder a la aplicación
- **Aplicación web**: http://localhost:8000
- **Panel de admin**: http://localhost:8000/admin

## 🛠️ Comandos Útiles

### Gestión de Contenedores

```bash
# Iniciar servicios en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f web

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ borra la BD)
docker-compose down -v
```

### Comandos Django

```bash
# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Configurar roles
docker-compose exec web python manage.py setup_roles

# Shell de Django
docker-compose exec web python manage.py shell

# Crear nueva migración
docker-compose exec web python manage.py makemigrations

# Recolectar archivos estáticos
docker-compose exec web python manage.py collectstatic
```

### Base de Datos

```bash
# Acceder a PostgreSQL
docker-compose exec db psql -U postgres -d movetracker

# Backup de la base de datos
docker-compose exec db pg_dump -U postgres movetracker > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U postgres movetracker < backup.sql
```

### Debugging

```bash
# Ver contenedores en ejecución
docker-compose ps

# Acceder al contenedor web
docker-compose exec web bash

# Ver uso de recursos
docker stats

# Reiniciar un servicio
docker-compose restart web
```

## 📁 Estructura de Archivos Docker

```
MoveTracker/
├── Dockerfile              # Definición de la imagen de la aplicación
├── docker-compose.yml      # Orquestación de servicios
├── .dockerignore          # Archivos ignorados en build
├── .env.example           # Variables de entorno de ejemplo
└── docker-entrypoint.sh   # Script de inicialización
```

## ⚙️ Servicios

### Web (Django)
- **Puerto**: 8000
- **Imagen**: Python 3.11-slim
- **Volumen**: Código montado en `/app`

### DB (PostgreSQL)
- **Puerto**: 5432
- **Imagen**: PostgreSQL 15-Alpine
- **Datos**: Persistidos en volumen `postgres_data`
- **Credenciales por defecto**:
  - Usuario: `postgres`
  - Contraseña: `postgres`
  - Base de datos: `movetracker`

## 🔒 Variables de Entorno

Copia `.env.example` a `.env` y personaliza:

```bash
cp .env.example .env
```

Variables principales:
- `DEBUG`: Modo debug (True/False)
- `SECRET_KEY`: Clave secreta de Django
- `DB_NAME`: Nombre de la base de datos
- `DB_USER`: Usuario de PostgreSQL
- `DB_PASSWORD`: Contraseña de PostgreSQL

## 🧪 Ejecutar Tests

```bash
# Ejecutar todos los tests
docker-compose exec web python manage.py test

# Ejecutar tests de una app específica
docker-compose exec web python manage.py test user

# Ejecutar tests con coverage
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

## 🏭 Producción

Para producción, considera:

1. **Usar Gunicorn** en lugar de runserver:
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]
```

2. **Configurar nginx** como proxy inverso

3. **Usar secretos seguros**:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

4. **Habilitar HTTPS y seguridad**:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🐛 Solución de Problemas

### Puerto 8000 ya en uso
```bash
# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess
Stop-Process -Id <PID>

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Reconstruir desde cero
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Limpiar Docker
```bash
# Limpiar contenedores detenidos
docker container prune

# Limpiar imágenes no usadas
docker image prune -a

# Limpiar todo (⚠️ cuidado)
docker system prune -a --volumes
```

## 📚 Recursos

- [Documentación Docker](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Deploying Django with Docker](https://docs.docker.com/samples/django/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
