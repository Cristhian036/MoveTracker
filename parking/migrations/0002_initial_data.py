# Generated migration for initial parking data

from django.db import migrations
from decimal import Decimal


def create_initial_data(apps, schema_editor):
    """Crear tarifas de vehículos y configuración inicial del estacionamiento"""
    VehicleTariff = apps.get_model('parking', 'VehicleTariff')
    ParkingConfiguration = apps.get_model('parking', 'ParkingConfiguration')
    User = apps.get_model('user', 'User')
    
    # Crear tarifas para cada tipo de vehículo (por hora)
    tariffs = [
        {
            'vehicle_type': 'car',
            'rate_per_hour': Decimal('3.00'),
            'is_active': True,
        },
        {
            'vehicle_type': 'camioneta',
            'rate_per_hour': Decimal('5.00'),
            'is_active': True,
        },
        {
            'vehicle_type': 'moto',
            'rate_per_hour': Decimal('2.00'),
            'is_active': True,
        },
    ]
    
    for tariff_data in tariffs:
        VehicleTariff.objects.get_or_create(
            vehicle_type=tariff_data['vehicle_type'],
            defaults={
                'rate_per_hour': tariff_data['rate_per_hour'],
                'is_active': tariff_data['is_active'],
            }
        )
    
    # Crear configuración inicial del estacionamiento (3 pisos, 50 espacios por piso)
    # Intentar obtener el primer usuario administrador para asignarlo como creador
    admin_user = User.objects.filter(is_superuser=True).first()
    
    ParkingConfiguration.objects.get_or_create(
        id=1,
        defaults={
            'total_floors': 3,
            'spaces_per_floor': 50,
            'is_active': True,
            'created_by': admin_user,
        }
    )


def reverse_initial_data(apps, schema_editor):
    """Eliminar datos iniciales en caso de rollback"""
    VehicleTariff = apps.get_model('parking', 'VehicleTariff')
    ParkingConfiguration = apps.get_model('parking', 'ParkingConfiguration')
    
    VehicleTariff.objects.filter(vehicle_type__in=['car', 'camioneta', 'moto']).delete()
    ParkingConfiguration.objects.filter(id=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
        ('user', '0002_create_user_groups'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_initial_data),
    ]
