from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ParkingConfiguration, ParkingFloor, ParkingSpace


@receiver(post_save, sender=ParkingConfiguration)
def create_parking_structure(sender, instance, created, **kwargs):
    """
    Cuando se crea o actualiza una configuración activa,
    genera automáticamente los pisos y espacios correspondientes.
    """
    if instance.is_active:
        # Crear pisos
        for floor_num in range(1, instance.total_floors + 1):
            floor, floor_created = ParkingFloor.objects.get_or_create(
                configuration=instance,
                floor_number=floor_num,
                defaults={
                    'floor_name': f'Piso {floor_num}',
                    'is_active': True
                }
            )
            
            # Crear espacios para cada piso
            if floor_created or floor.spaces.count() < instance.spaces_per_floor:
                # Determinar cuántos espacios crear
                existing_spaces = floor.spaces.count()
                spaces_to_create = instance.spaces_per_floor - existing_spaces
                
                for space_num in range(existing_spaces + 1, existing_spaces + spaces_to_create + 1):
                    ParkingSpace.objects.create(
                        floor=floor,
                        space_number=space_num,
                        status='AVAILABLE',
                        is_active=True
                    )


@receiver(post_save, sender=ParkingFloor)
def create_floor_spaces(sender, instance, created, **kwargs):
    """
    Cuando se crea un piso, genera automáticamente los espacios
    según la configuración.
    """
    if created and instance.configuration:
        for space_num in range(1, instance.configuration.spaces_per_floor + 1):
            ParkingSpace.objects.get_or_create(
                floor=instance,
                space_number=space_num,
                defaults={
                    'status': 'AVAILABLE',
                    'is_active': True
                }
            )
