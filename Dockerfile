# Usar Python 3.11 (versión estable y moderna)
FROM python:3.11-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copiar el proyecto
COPY . .

# Crear usuario no-root para seguridad
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Script de inicio
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


