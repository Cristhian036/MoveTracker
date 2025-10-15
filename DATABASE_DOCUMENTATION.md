# 📊 DOCUMENTACIÓN COMPLETA DE LA BASE DE DATOS

## 🗃️ Información General
- **Motor:** SQLite3
- **Archivo:** `db.sqlite3`
- **Framework:** Django 4.2.25
- **Total de Tablas:** 12

---

## 📋 ESTRUCTURA DE TABLAS

### 1. 🔐 **auth_group** (Grupos/Roles)
**Descripción:** Almacena los roles del sistema para control de acceso

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER (PK) | Identificador único del grupo |
| name | VARCHAR(150) | Nombre del grupo/rol |

**📊 Datos Actuales:**
- **admin** (ID: 1)
- **usuario** (ID: 2)
- **trabajador** (ID: 3)

**Total de registros:** 3

---

### 2. 👥 **auth_user** (Usuarios)
**Descripción:** Tabla principal de usuarios del sistema Django

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER (PK) | Identificador único del usuario |
| username | VARCHAR(150) | Nombre de usuario (único) |
| password | VARCHAR(128) | Contraseña hasheada |
| email | VARCHAR(254) | Correo electrónico |
| first_name | VARCHAR(150) | Primer nombre |
| last_name | VARCHAR(150) | Apellido |
| is_staff | BOOLEAN | Si puede acceder al admin de Django |
| is_superuser | BOOLEAN | Si tiene todos los permisos |
| is_active | BOOLEAN | Si la cuenta está activa |
| date_joined | DATETIME | Fecha de registro |
| last_login | DATETIME | Último inicio de sesión |

**📊 Usuarios Registrados:**

1. **root** (ID: 8)
   - Email: (vacío)
   - Es staff: ✅ Sí
   - Es superusuario: ✅ Sí
   - Activo: ✅ Sí
   - Fecha registro: 2019-10-10

2. **dany** (ID: 9)
   - Email: dany@gmail.com
   - Es staff: ❌ No
   - Es superusuario: ❌ No
   - Activo: ✅ Sí
   - Fecha registro: 2025-10-15

**Total de registros:** 2

---

### 3. 👥🔐 **auth_user_groups** (Relación Usuarios-Grupos)
**Descripción:** Tabla de relación muchos a muchos entre usuarios y grupos

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER (PK) | Identificador único |
| user_id | INTEGER (FK) | ID del usuario |
| group_id | INTEGER (FK) | ID del grupo |

**Estado Actual:** No hay usuarios asignados a grupos aún

**Total de registros:** 0

---

### 4. 🔒 **auth_permission** (Permisos)
**Descripción:** Permisos disponibles en el sistema

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER (PK) | Identificador único |
| content_type_id | INTEGER (FK) | Tipo de contenido relacionado |
| codename | VARCHAR(100) | Código del permiso |
| name | VARCHAR(255) | Nombre descriptivo del permiso |

**Ejemplos de permisos:**
- add_logentry, change_logentry, delete_logentry, view_logentry
- add_user, change_user, delete_user, view_user
- add_group, change_group, delete_group, view_group
- add_permission, change_permission, delete_permission, view_permission

**Total de registros:** 32

---

### 5. 🔐🔒 **auth_group_permissions** (Permisos de Grupos)
**Descripción:** Relación muchos a muchos entre grupos y permisos

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER (PK) | Identificador único |
| group_id | INTEGER (FK) | ID del grupo |
| permission_id | INTEGER (FK) | ID del permiso |

**Estado Actual:** No hay permisos asignados a grupos aún

**Total de registros:** 0

---

### 6. 👤🔒 **auth_user_user_permissions** (Permisos de Usuarios)
**Descripción:** Permisos específicos asignados directamente a usuarios

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER (PK) | Identificador único |
| user_id | INTEGER (FK) | ID del usuario |
| permission_id | INTEGER (FK) | ID del permiso |

**Estado Actual:** No hay permisos específicos asignados a usuarios

**Total de registros:** 0

---

### 7. 🔑 **authtoken_token** (Tokens de Autenticación)
**Descripción:** Tokens de autenticación para API REST (Django REST Framework)

| Columna | Tipo | Descripción |
|---------|------|-------------|
| key | VARCHAR(40) (PK) | Token de autenticación |
| user_id | INTEGER (FK) | Usuario asociado al token |
| created | DATETIME | Fecha de creación del token |

**📊 Tokens Activos:**
- **Usuario:** root
- **Token:** 7641bb9229cd2e0c7736cf903dcee403c91fe24e
- **Creado:** 2019-10-10

**Total de registros:** 1

---

### 8. 📝 **django_content_type** (Tipos de Contenido)
**Descripción:** Registro de todos los modelos de la aplicación

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER (PK) | Identificador único |
| app_label | VARCHAR(100) | Nombre de la aplicación |
| model | VARCHAR(100) | Nombre del modelo |

**Apps Registradas:**
- **admin**: logentry
- **auth**: group, permission, user
- **authtoken**: token, tokenproxy
- **contenttypes**: contenttype
- **sessions**: session

**Total de registros:** 8

---

### 9. 📋 **django_admin_log** (Registro de Admin)
**Descripción:** Bitácora de acciones realizadas en el panel de administración de Django

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER (PK) | Identificador único |
| action_time | DATETIME | Fecha y hora de la acción |
| user_id | INTEGER (FK) | Usuario que realizó la acción |
| content_type_id | INTEGER (FK) | Tipo de contenido modificado |
| object_id | TEXT | ID del objeto modificado |
| object_repr | VARCHAR(200) | Representación del objeto |
| action_flag | SMALLINT | Tipo de acción (1=add, 2=change, 3=delete) |
| change_message | TEXT | Mensaje descriptivo del cambio |

**Total de registros:** 7

---

### 10. 🗂️ **django_migrations** (Migraciones)
**Descripción:** Registro de migraciones aplicadas a la base de datos

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER (PK) | Identificador único |
| app | VARCHAR(255) | Nombre de la aplicación |
| name | VARCHAR(255) | Nombre de la migración |
| applied | DATETIME | Fecha de aplicación |

**Total de registros:** 41 migraciones aplicadas

---

### 11. 🔐 **django_session** (Sesiones)
**Descripción:** Almacena las sesiones de usuario activas

| Columna | Tipo | Descripción |
|---------|------|-------------|
| session_key | VARCHAR(40) (PK) | Clave única de sesión |
| session_data | TEXT | Datos de sesión codificados |
| expire_date | DATETIME | Fecha de expiración de la sesión |

**Total de registros:** 3 sesiones activas

---

## 🔗 DIAGRAMA DE RELACIONES

```
┌─────────────────────┐
│   auth_user         │
│  (Usuarios)         │
│  - id (PK)          │
│  - username         │
│  - password         │
│  - email            │
│  - is_staff         │
│  - is_superuser     │
└──────────┬──────────┘
           │
           ├─────────────────────┐
           │                     │
           ▼                     ▼
┌──────────────────┐   ┌─────────────────────┐
│ authtoken_token  │   │ auth_user_groups    │
│ - key (PK)       │   │ - id (PK)           │
│ - user_id (FK)───┼───│ - user_id (FK)      │
│ - created        │   │ - group_id (FK)─────┼───┐
└──────────────────┘   └─────────────────────┘   │
                                                  │
                                                  ▼
                                       ┌──────────────────────┐
                                       │   auth_group         │
                                       │  (Roles)             │
                                       │  - id (PK)           │
                                       │  - name              │
                                       └──────────┬───────────┘
                                                  │
                                                  ▼
                                       ┌──────────────────────────┐
                                       │ auth_group_permissions   │
                                       │ - id (PK)                │
                                       │ - group_id (FK)          │
                                       │ - permission_id (FK)─────┼───┐
                                       └──────────────────────────┘   │
                                                                      │
┌─────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────┐
│   auth_permission        │
│  (Permisos)              │
│  - id (PK)               │
│  - codename              │
│  - name                  │
│  - content_type_id (FK)──┼───┐
└──────────────────────────┘   │
                               │
                               ▼
                    ┌──────────────────────┐
                    │ django_content_type  │
                    │ - id (PK)            │
                    │ - app_label          │
                    │ - model              │
                    └──────────────────────┘
```

---

## 🎯 RESUMEN EJECUTIVO

### Estado Actual del Sistema:

✅ **Sistema de Autenticación Configurado**
- 3 roles definidos: admin, usuario, trabajador
- 2 usuarios registrados (1 superusuario, 1 usuario normal)
- Sistema de tokens REST activo
- 32 permisos predefinidos disponibles

⚠️ **Pendientes:**
- Asignar usuarios a grupos/roles
- Configurar permisos específicos para cada grupo
- Asignar permisos personalizados si es necesario

### Funcionalidades Disponibles:

1. **Autenticación de Usuarios** ✅
   - Login/Logout
   - Registro de usuarios
   - Gestión de sesiones

2. **Autorización** 🔄 (Parcialmente configurado)
   - Roles creados pero no asignados
   - Permisos disponibles pero no configurados

3. **API REST** ✅
   - Sistema de tokens funcionando
   - Endpoint de autenticación disponible

4. **Panel de Administración** ✅
   - Activo para usuarios staff
   - Registro de acciones habilitado

---

## 📝 NOTAS IMPORTANTES

1. **Seguridad:** El usuario 'root' no tiene email configurado, se recomienda actualizar
2. **Roles:** Los grupos están creados pero ningún usuario está asignado a ellos
3. **Permisos:** Los permisos de grupo no están configurados
4. **Sesiones:** Hay 3 sesiones activas que expiran automáticamente

---

## 🔧 COMANDOS ÚTILES

### Ver los roles:
```bash
python manage.py shell -c "from django.contrib.auth.models import Group; [print(g.name) for g in Group.objects.all()]"
```

### Asignar un usuario a un grupo:
```python
from django.contrib.auth.models import User, Group
user = User.objects.get(username='dany')
group = Group.objects.get(name='usuario')
user.groups.add(group)
```

### Reconfigurar roles:
```bash
python manage.py setup_roles
```

---

**Fecha de generación:** 15 de Octubre de 2025
**Versión Django:** 4.2.25
