"""
Script para crear un usuario administrador en la base de datos.

Este script crea un superusuario con rol de administrador para el sistema de estacionamiento.

Ejecutar:
    python create_admin_user.py
"""

import os
import sys
import django

# Setup Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("\n" + "="*80)
print("CREAR USUARIO ADMINISTRADOR")
print("="*80 + "\n")

# Datos del administrador
admin_data = {
    'username': 'admin',
    'email': 'admin@estacionamiento.com',
    'first_name': 'Administrador',
    'last_name': 'Sistema',
    'is_staff': True,
    'is_superuser': True,
    'is_active': True
}

password = 'admin123'

# Verificar si el usuario ya existe
if User.objects.filter(username=admin_data['username']).exists():
    print(f"AVISO: El usuario '{admin_data['username']}' ya existe en la base de datos.")
    user = User.objects.get(username=admin_data['username'])
    
    response = input("\n¿Desea actualizar la contraseña? (s/n): ")
    if response.lower() == 's':
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        print(f"\nEXITO: Contraseña actualizada para '{admin_data['username']}'")
    else:
        print("\nOPERACION CANCELADA: Usuario existente no modificado.")
else:
    # Crear el usuario
    user = User.objects.create_user(
        username=admin_data['username'],
        email=admin_data['email'],
        password=password,
        first_name=admin_data['first_name'],
        last_name=admin_data['last_name']
    )
    
    # Asignar permisos de superusuario
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    
    print("EXITO: Usuario administrador creado exitosamente!")

print("\n" + "="*80)
print("INFORMACION DEL USUARIO")
print("="*80)
print(f"Usuario:       {admin_data['username']}")
print(f"Contraseña:    {password}")
print(f"Email:         {admin_data['email']}")
print(f"Nombre:        {admin_data['first_name']} {admin_data['last_name']}")
print(f"Staff:         {'Sí' if user.is_staff else 'No'}")
print(f"Superusuario:  {'Sí' if user.is_superuser else 'No'}")
print(f"Activo:        {'Sí' if user.is_active else 'No'}")

# Verificar si tiene el campo 'role' (cuando se implemente)
if hasattr(user, 'role'):
    print(f"Rol:           {user.role}")

print("="*80)

print("\nACCESO AL SISTEMA:")
print(f"   1. Ejecutar servidor: python manage.py runserver")
print(f"   2. Acceder a: http://localhost:8000/login/")
print(f"   3. Usuario: {admin_data['username']}")
print(f"   4. Contraseña: {password}")

print("\nACCESO AL DASHBOARD DE PARKING:")
print(f"   URL: http://localhost:8000/parking/")

print("\nACCESO AL ADMIN DE DJANGO:")
print(f"   URL: http://localhost:8000/admin/")

print("\n" + "="*80 + "\n")
