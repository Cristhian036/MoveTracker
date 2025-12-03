import os
import django
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from parking.models import VehicleTariff, VehicleType

def check_tariffs():
    print("Checking existing tariffs...")
    tariffs = VehicleTariff.objects.all()
    if not tariffs:
        print("No tariffs found.")
    else:
        for t in tariffs:
            print(f"Found tariff: {t.vehicle_type} ({t.get_vehicle_type_display()}) - Rate: {t.rate_per_hour} - Active: {t.is_active}")

    print("\nChecking for missing default tariffs...")
    for type_code, type_label in VehicleType.choices:
        exists = VehicleTariff.objects.filter(vehicle_type=type_code, is_active=True).exists()
        if not exists:
            print(f"Missing active tariff for: {type_label} ({type_code})")
        else:
            print(f"Active tariff exists for: {type_label} ({type_code})")

if __name__ == '__main__':
    check_tariffs()
