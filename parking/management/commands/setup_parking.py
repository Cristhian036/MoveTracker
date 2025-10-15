from django.core.management.base import BaseCommand
from parking.models import ParkingConfiguration
from user.models import User


class Command(BaseCommand):
    help = 'Configura el estacionamiento con pisos y espacios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--floors',
            type=int,
            default=3,
            help='Número de pisos del estacionamiento (por defecto: 3)'
        )
        parser.add_argument(
            '--spaces',
            type=int,
            default=20,
            help='Número de espacios por piso (por defecto: 20)'
        )

    def handle(self, *args, **options):
        floors = options['floors']
        spaces = options['spaces']

        self.stdout.write(f'\nConfigurando estacionamiento...')
        self.stdout.write(f'Pisos: {floors}')
        self.stdout.write(f'Espacios por piso: {spaces}')
        self.stdout.write(f'Capacidad total: {floors * spaces}\n')

        # Obtener el primer superusuario o crear uno temporal
        admin_user = User.objects.filter(is_superuser=True).first()
        
        if not admin_user:
            self.stdout.write(
                self.style.WARNING('No se encontró un superusuario. Creando configuración sin usuario.')
            )

        # Desactivar configuraciones anteriores
        ParkingConfiguration.objects.filter(is_active=True).update(is_active=False)

        # Crear nueva configuración
        config = ParkingConfiguration.objects.create(
            total_floors=floors,
            spaces_per_floor=spaces,
            is_active=True,
            created_by=admin_user
        )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Configuración creada: {config}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✓ Capacidad total: {config.total_capacity} espacios')
        )

        # Los pisos y espacios se crean automáticamente mediante signals
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Los pisos y espacios se están generando automáticamente...')
        )
        
        # Verificar la creación
        total_floors = config.floors.count()
        total_spaces = sum(floor.spaces.count() for floor in config.floors.all())
        
        self.stdout.write(
            self.style.SUCCESS(f'✓ Pisos creados: {total_floors}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✓ Espacios creados: {total_spaces}')
        )
        self.stdout.write(
            self.style.SUCCESS('\n✓ Configuración del estacionamiento completada')
        )
