from django.core.management.base import BaseCommand
from parking.models import VehicleTariff, VehicleType


class Command(BaseCommand):
    help = 'Inicializa las tarifas por defecto para los tipos de vehículos (por minuto)'

    def handle(self, *args, **options):
        tariffs = [
            {
                'vehicle_type': VehicleType.MOTORCYCLE,
                'rate_per_minute': 0.05,  # $0.05 por minuto ($3.00 por hora)
            },
            {
                'vehicle_type': VehicleType.CAR,
                'rate_per_minute': 0.10,  # $0.10 por minuto ($6.00 por hora)
            },
            {
                'vehicle_type': VehicleType.TRUCK,
                'rate_per_minute': 0.15,  # $0.15 por minuto ($9.00 por hora)
            },
        ]

        for tariff_data in tariffs:
            tariff, created = VehicleTariff.objects.get_or_create(
                vehicle_type=tariff_data['vehicle_type'],
                defaults={
                    'rate_per_minute': tariff_data['rate_per_minute'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Tarifa creada para {tariff.get_vehicle_type_display()}: '
                        f'${tariff.rate_per_minute}/minuto (${tariff.rate_per_minute * 60}/hora)'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'○ Tarifa ya existe para {tariff.get_vehicle_type_display()}'
                    )
                )

        self.stdout.write(self.style.SUCCESS('\n✓ Inicialización de tarifas completada'))
