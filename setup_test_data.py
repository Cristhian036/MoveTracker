"""
Script para crear datos de prueba para el sistema de parking.

Ejecutar:
    python setup_test_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from parking.models import (
    ParkingConfiguration, VehicleTariff, Vehicle,
    ParkingFloor, ParkingSpace, ParkingAssignment,
    ParkingReservation, VehicleType
)

User = get_user_model()

print("\n" + "="*80)
print("CONFIGURANDO DATOS DE PRUEBA PARA EL SISTEMA DE PARKING")
print("="*80 + "\n")

# 1. Obtener usuario admin
print("1. Verificando usuario administrador...")
try:
    admin = User.objects.get(username='admin')
    print(f"   Usuario admin encontrado: {admin.username}")
except User.DoesNotExist:
    print("   ERROR: Usuario admin no existe. Ejecuta create_admin_user.py primero")
    sys.exit(1)

# 2. Crear usuario de prueba
print("\n2. Creando usuario de prueba...")
test_user, created = User.objects.get_or_create(
    username='test_user',
    defaults={
        'email': 'test@parking.com',
        'first_name': 'Usuario',
        'last_name': 'Prueba',
        'is_active': True
    }
)
if created:
    test_user.set_password('test123')
    test_user.save()
    print(f"   Usuario creado: {test_user.username}")
else:
    print(f"   Usuario ya existe: {test_user.username}")

# 3. Crear configuración de parking
print("\n3. Creando configuracion de parking...")
config, created = ParkingConfiguration.objects.get_or_create(
    is_active=True,
    defaults={
        'total_floors': 3,
        'created_by': admin
    }
)
if created:
    print(f"   Configuracion creada: {config.total_floors} pisos")
else:
    print(f"   Configuracion ya existe: {config.total_floors} pisos")

# 4. Crear pisos
print("\n4. Creando pisos de estacionamiento...")
floors = []
for floor_num in range(1, 4):
    floor, created = ParkingFloor.objects.get_or_create(
        configuration=config,
        floor_number=floor_num,
        defaults={
            'floor_name': f'Piso {floor_num}'
        }
    )
    floors.append(floor)
    if created:
        print(f"   Piso {floor_num} creado")
    else:
        print(f"   Piso {floor_num} ya existe")

# 5. Crear espacios de estacionamiento
print("\n5. Creando espacios de estacionamiento...")
total_spaces_created = 0
for floor in floors:
    for space_num in range(1, 11):  # 10 espacios por piso
        space, created = ParkingSpace.objects.get_or_create(
            floor=floor,
            space_number=space_num,
            defaults={
                'status': ParkingSpace.SpaceStatus.AVAILABLE,
                'is_active': True
            }
        )
        if created:
            total_spaces_created += 1

print(f"   Total de espacios creados: {total_spaces_created}")
print(f"   Total de espacios en sistema: {ParkingSpace.objects.count()}")

# 6. Crear tarifas
print("\n6. Creando tarifas para tipos de vehiculo...")
tariffs_data = {
    VehicleType.MOTORCYCLE: {'hourly': '2.00', 'daily': '15.00', 'monthly': '300.00'},
    VehicleType.CAR: {'hourly': '3.00', 'daily': '20.00', 'monthly': '400.00'},
    VehicleType.TRUCK: {'hourly': '5.00', 'daily': '35.00', 'monthly': '700.00'},
}

for veh_type, rates in tariffs_data.items():
    tariff, created = VehicleTariff.objects.get_or_create(
        vehicle_type=veh_type,
        defaults={
            'hourly_rate': Decimal(rates['hourly']),
            'daily_rate': Decimal(rates['daily']),
            'monthly_rate': Decimal(rates['monthly'])
        }
    )
    if created:
        print(f"   Tarifa para {veh_type} creada")
    else:
        print(f"   Tarifa para {veh_type} ya existe")

# 7. Crear vehiculos de prueba
print("\n7. Creando vehiculos de prueba...")
vehicles_data = [
    {
        'owner': test_user,
        'vehicle_type': VehicleType.CAR,
        'brand': 'Toyota',
        'model': 'Corolla',
        'year': 2020,
        'color': 'Rojo',
        'license_plate': 'ABC-123'
    },
    {
        'owner': test_user,
        'vehicle_type': VehicleType.MOTORCYCLE,
        'brand': 'Honda',
        'model': 'CBR',
        'year': 2021,
        'color': 'Negro',
        'license_plate': 'XYZ-789'
    },
    {
        'owner': admin,
        'vehicle_type': VehicleType.CAR,
        'brand': 'Ford',
        'model': 'Explorer',
        'year': 2022,
        'color': 'Azul',
        'license_plate': 'DEF-456'
    }
]

vehicles_created = 0
for veh_data in vehicles_data:
    vehicle, created = Vehicle.objects.get_or_create(
        license_plate=veh_data['license_plate'],
        defaults={
            **veh_data,
            'registered_by': admin,
            'is_active': True
        }
    )
    if created:
        vehicles_created += 1
        print(f"   Vehiculo creado: {vehicle.license_plate} - {vehicle.brand} {vehicle.model}")
    else:
        print(f"   Vehiculo ya existe: {vehicle.license_plate}")

# 8. Crear algunas reservas de prueba
print("\n8. Creando reservas de prueba...")
reservations_created = 0

# Reserva normal
vehicle1 = Vehicle.objects.filter(license_plate='ABC-123').first()
space1 = ParkingSpace.objects.filter(status=ParkingSpace.SpaceStatus.AVAILABLE).first()

if vehicle1 and space1:
    res1, created = ParkingReservation.objects.get_or_create(
        user=test_user,
        vehicle=vehicle1,
        parking_space=space1,
        defaults={
            'reservation_date': timezone.now() + timedelta(hours=2),
            'duration_hours': 3,
            'status': ParkingReservation.ReservationStatus.PENDING,
            'is_quick_reservation': False,
            'created_by': admin,
            'notes': 'Reserva de prueba normal'
        }
    )
    if created:
        reservations_created += 1
        print(f"   Reserva normal creada para {vehicle1.license_plate}")

# Reserva rapida
space2 = ParkingSpace.objects.filter(
    status=ParkingSpace.SpaceStatus.AVAILABLE
).exclude(id=space1.id).first() if space1 else ParkingSpace.objects.filter(
    status=ParkingSpace.SpaceStatus.AVAILABLE
).first()

if space2:
    res2, created = ParkingReservation.objects.get_or_create(
        customer_name='Juan Perez',
        customer_phone='+51999888777',
        vehicle_plate='RST-999',
        defaults={
            'customer_email': 'juan@ejemplo.com',
            'vehicle_type_temp': VehicleType.CAR,
            'parking_space': space2,
            'reservation_date': timezone.now() + timedelta(days=1),
            'duration_hours': 2,
            'status': ParkingReservation.ReservationStatus.PENDING,
            'is_quick_reservation': True,
            'created_by': admin,
            'notes': 'Reserva rapida de prueba'
        }
    )
    if created:
        reservations_created += 1
        print(f"   Reserva rapida creada para {res2.customer_name}")

print("\n" + "="*80)
print("RESUMEN DE CONFIGURACION")
print("="*80)
print(f"Usuarios: {User.objects.count()}")
print(f"Configuraciones: {ParkingConfiguration.objects.count()}")
print(f"Pisos: {ParkingFloor.objects.count()}")
print(f"Espacios: {ParkingSpace.objects.count()}")
print(f"  - Disponibles: {ParkingSpace.objects.filter(status=ParkingSpace.SpaceStatus.AVAILABLE).count()}")
print(f"  - Ocupados: {ParkingSpace.objects.filter(status=ParkingSpace.SpaceStatus.OCCUPIED).count()}")
print(f"  - Reservados: {ParkingSpace.objects.filter(status=ParkingSpace.SpaceStatus.RESERVED).count()}")
print(f"Tarifas: {VehicleTariff.objects.count()}")
print(f"Vehiculos: {Vehicle.objects.count()}")
print(f"Reservas: {ParkingReservation.objects.count()}")
print("="*80)

print("\nCREDENCIALES DE ACCESO:")
print("-" * 40)
print("Administrador:")
print("  Usuario: admin")
print("  Contrasena: admin123")
print("\nUsuario de Prueba:")
print("  Usuario: test_user")
print("  Contrasena: test123")
print("\nURL del Sistema:")
print("  http://127.0.0.1:8000/")
print("  http://127.0.0.1:8000/parking/")
print("="*80 + "\n")

print("CONFIGURACION COMPLETADA!")
