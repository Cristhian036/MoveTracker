"""
Script para crear un usuario administrador en la base de datos.

Ejecutar: python scripts/create_admin_user.py
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

try:
    django.setup()
except Exception as e:
    print(f"ERROR: No se pudo inicializar Django.\nDetalle: {e}")
    sys.exit(1)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Configuración (variables de entorno o valores por defecto)
USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@estacionamiento.com')
PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
GROUP_NAME = os.environ.get('ADMIN_GROUP', 'administrador')
FIRST_NAME = os.environ.get('ADMIN_FIRST_NAME', 'Administrador')
LAST_NAME = os.environ.get('ADMIN_LAST_NAME', 'Sistema')


def create_or_update_admin():
    """Crea o actualiza un superusuario administrador."""
    print("\n" + "=" * 80)
    print("CREAR USUARIO ADMINISTRADOR")
    print("=" * 80 + "\n")
    
    # Verificar si el usuario existe
    user = User.objects.filter(username=USERNAME).first()
    
    if user:
        print(f"AVISO: El usuario '{USERNAME}' ya existe.")
        response = input("¿Actualizar contraseña y permisos? (s/n): ")
        if response.strip().lower() != 's':
            print("OPERACION CANCELADA.")
            return user
        
        # Actualizar usuario existente
        user.set_password(PASSWORD)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.first_name = FIRST_NAME
        user.last_name = LAST_NAME
        user.email = EMAIL
        user.save()
        print(f"\nEXITO: Usuario '{USERNAME}' actualizado.")
    else:
        # Crear nuevo usuario
        user = User.objects.create_superuser(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD,
            first_name=FIRST_NAME,
            last_name=LAST_NAME
        )
        print(f"EXITO: Usuario '{USERNAME}' creado exitosamente!")
    
    # Asignar al grupo
    group, _ = Group.objects.get_or_create(name=GROUP_NAME)
    if not user.groups.filter(name=GROUP_NAME).exists():
        user.groups.add(group)
        print(f"Usuario asignado al grupo: {GROUP_NAME}")
    else:
        print(f"Usuario ya pertenece al grupo: {GROUP_NAME}")
    
    return user


def show_user_info(user):
    """Muestra la información del usuario creado."""
    print("\n" + "=" * 80)
    print("INFORMACION DEL USUARIO")
    print("=" * 80)
    print(f"Usuario:       {user.username}")
    print(f"Contraseña:    {PASSWORD}")
    print(f"Email:         {user.email}")
    print(f"Nombre:        {user.first_name} {user.last_name}")
    print(f"Staff:         {'Sí' if user.is_staff else 'No'}")
    print(f"Superusuario:  {'Sí' if user.is_superuser else 'No'}")
    print(f"Activo:        {'Sí' if user.is_active else 'No'}")
    print(f"Grupos:        {', '.join(g.name for g in user.groups.all())}")
    print("=" * 80)
    
    print("\nACCESO AL SISTEMA:")
    print(f"  • Admin Django:  http://localhost:8000/admin/")
    print(f"  • Dashboard:     http://localhost:8000/parking/")
    print(f"  • Login:         http://localhost:8000/login/")
    print(f"\n  Usuario:    {user.username}")
    print(f"  Contraseña: {PASSWORD}")
    print("\n" + "=" * 80 + "\n")


if __name__ == '__main__':
    user = create_or_update_admin()
    show_user_info(user)
