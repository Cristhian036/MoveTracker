# Guía de Instalación y Ejecución - MoveTracker

Esta guía detalla paso a paso cómo configurar y ejecutar el proyecto web **MoveTracker** desde cero en un entorno Windows.

## 1. Instalación de Python

Si no tienes Python instalado:

1.  Ve al sitio oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2.  Descarga la última versión estable (ej. 3.10, 3.11, 3.12 o 3.13).
3.  Ejecuta el instalador.
    *   **IMPORTANTE**: Asegúrate de marcar la casilla **"Add Python to PATH"** antes de hacer clic en "Install Now". Esto permitirá ejecutar python desde la terminal.

Para verificar la instalación, abre una terminal (PowerShell o CMD) y escribe:
```bash
python --version
```

## 2. Preparación del Proyecto

1.  Descarga o clona el código fuente del proyecto en tu computadora.
2.  Abre una terminal en la carpeta raíz del proyecto (donde se encuentra el archivo `manage.py`).

   Ejemplo:
   ```bash
   cd "C:\Ruta\A\Tu\Carpeta\detection"
   ```

## 3. Crear un Entorno Virtual (Recomendado)

Es recomendable usar un entorno virtual para no mezclar las librerías del proyecto con las de tu sistema.

1.  Crea el entorno virtual:
    ```bash
    python -m venv venv
    ```
2.  Activa el entorno virtual:
    *   **En Windows (PowerShell):**
        ```bash
        .\venv\Scripts\Activate
        ```
    *   **En Windows (CMD):**
        ```bash
        venv\Scripts\activate
        ```
    *   *Nota: Si en PowerShell recibes un error de permisos, ejecuta `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` y vuelve a intentar.*

## 4. Instalación de Dependencias

Con el entorno virtual activado (verás `(venv)` al inicio de la línea de comandos), instala las librerías necesarias:

```bash
pip install -r requirements.txt
```

Esto instalará Django, OpenCV, Pandas, y otras herramientas necesarias.

## 5. Configuración de la Base de Datos

El proyecto incluye un script automatizado para generar la base de datos `bd.sqlite3` a partir del archivo SQL base (`db.sql`).

Ejecuta el siguiente comando:

```bash
python scripts/generar_db.py
```

**¿Qué hace este script?**
1.  Elimina cualquier base de datos `bd.sqlite3` existente para asegurar una instalación limpia.
2.  Crea una nueva base de datos e importa la estructura y datos desde `db.sql`.
3.  Configura las migraciones de Django automáticamente.

Si ves el mensaje **"Migrations applied successfully."**, todo ha salido bien.

## 6. Ejecución del Servidor Web

Finalmente, inicia el servidor de desarrollo de Django:

```bash
python manage.py runserver
```

Si todo es correcto, verás un mensaje indicando que el servidor está corriendo en `http://127.0.0.1:8000/`.

## 7. Acceso a la Aplicación

1.  Abre tu navegador web (Chrome, Edge, Firefox).
2.  Ingresa a la dirección: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
3.  Inicia sesión con tus credenciales (si ya están configuradas en la base de datos) o regístrate si la opción está habilitada.

---

### Solución de Problemas Comunes

*   **Error "Module not found"**: Asegúrate de haber activado el entorno virtual y ejecutado `pip install -r requirements.txt`.
*   **Error de base de datos**: Si tienes problemas con la DB, vuelve a ejecutar `python scripts/generar_db.py` para reiniciarla.
