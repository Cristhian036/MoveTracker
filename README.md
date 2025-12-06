# Sistema de Gestión de Estacionamiento

Sistema de administración de estacionamiento desarrollado con Django. Permite gestionar espacios, controlar acceso de vehículos y administrar usuarios con roles diferenciados.

## Tecnologías

Django 4.2 • Python 3.x • SQLite • REST API

## Instalación

```bash
# Crear entorno virtual
python -m venv env
env\Scripts\activate  # Windows | source env/bin/activate (Linux/Mac)

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Configurar base de datos (Limpia)
python scripts/generar_bd.py

# Ejecutar servidor
python manage.py runserver
```

**Acceso:** http://127.0.0.1:8000/

## Base de Datos

**Tablas principales:**
- `auth_user` - Usuarios del sistema
- `auth_group` - Roles (admin, usuario, trabajador)
- `auth_user_groups` - Asignación de roles
- `authtoken_token` - Tokens de autenticación
- `django_session` - Sesiones activas


## Roadmap

- [ ] Gestión de espacios de estacionamiento
- [ ] Registro de vehículos con placas
- [ ] Sistema de tarifas y facturación
- [ ] Generación de tickets
- [ ] Dashboard con estadísticas
- [ ] Aplicación móvil

## Licencia

MIT License

## Librerías Principales

- **Django**: Framework web principal.
- **Django REST Framework**: API REST para comunicación.
- **Ultralytics (YOLO)**: Detección de objetos (vehículos y placas).
- **OpenCV**: Procesamiento de imágenes y video.
- **EasyOCR**: Reconocimiento óptico de caracteres (lectura de placas).
- **Supervision**: Utilidades para visión por computadora.
- **OpenPyXL**: Generación de reportes en Excel.
- **NumPy**: Operaciones numéricas y manejo de matrices.
