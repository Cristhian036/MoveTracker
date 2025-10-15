from django.core.management.base import BaseCommand
from parking.models import VehicleTariff, VehicleType


class Command(BaseCommand):
    help = 'Inicializa las tarifas por defecto para los tipos de vehículos'

    def handle(self, *args, **options):
        tariffs = [
            {
                'vehicle_type': VehicleType.MOTORCYCLE,
                'hourly_rate': 2.00,
                'daily_rate': 15.00,
                'monthly_rate': 300.00,
            },
            {
                'vehicle_type': VehicleType.CAR,
                'hourly_rate': 3.00,
                'daily_rate': 25.00,
                'monthly_rate': 500.00,
            },
            {
                'vehicle_type': VehicleType.TRUCK,
                'hourly_rate': 5.00,
                'daily_rate': 40.00,
                'monthly_rate': 800.00,
            },
        ]

        for tariff_data in tariffs:
            tariff, created = VehicleTariff.objects.get_or_create(
                vehicle_type=tariff_data['vehicle_type'],
                defaults={
                    'hourly_rate': tariff_data['hourly_rate'],
                    'daily_rate': tariff_data['daily_rate'],
                    'monthly_rate': tariff_data['monthly_rate'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Tarifa creada para {tariff.get_vehicle_type_display()}: '
                        f'${tariff.hourly_rate}/hora, ${tariff.daily_rate}/día, ${tariff.monthly_rate}/mes'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'○ Tarifa ya existe para {tariff.get_vehicle_type_display()}'
                    )
                )

        self.stdout.write(self.style.SUCCESS('\n✓ Inicialización de tarifas completada'))
