# 🚗 Sistema de Gestión de Estacionamiento

Sistema de administración de estacionamiento desarrollado con Django. Permite gestionar espacios, controlar acceso de vehículos y administrar usuarios con roles diferenciados.

## 🛠️ Tecnologías

Django 4.2 • Python 3.x • SQLite • REST API

## 📦 Instalación

### 🐳 Con Docker (Recomendado)

```bash
# Clonar repositorio
git clone https://github.com/Cristhian036/MoveTracker.git
cd MoveTracker

# Construir y ejecutar contenedores
docker-compose up --build

# Crear superusuario (en otra terminal)
docker-compose exec web python manage.py createsuperuser
```

**Acceso:** 
- Aplicación: http://localhost:8000
- Admin: http://localhost:8000/admin

### 💻 Instalación Manual

```bash
# Crear entorno virtual
python -m venv env
env\Scripts\activate  # Windows | source env/bin/activate (Linux/Mac)

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Configurar base de datos
python manage.py migrate
python manage.py setup_roles

# Ejecutar servidor
python manage.py runserver
```

**Acceso:** http://127.0.0.1:8000/

## 📊 Base de Datos

**Tablas principales:**
- `auth_user` - Usuarios del sistema
- `auth_group` - Roles (admin, usuario, trabajador)
- `auth_user_groups` - Asignación de roles
- `authtoken_token` - Tokens de autenticación
- `django_session` - Sesiones activas

📖 Documentación completa: [DATABASE_DOCUMENTATION.md](DATABASE_DOCUMENTATION.md)

## 🚀 Roadmap

- [ ] Gestión de espacios de estacionamiento
- [ ] Registro de vehículos con placas
- [ ] Sistema de tarifas y facturación
- [ ] Generación de tickets QR
- [ ] Dashboard con estadísticas
- [ ] Aplicación móvil

## 📄 Licencia

MIT License
