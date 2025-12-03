import os
import django
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from parking.models import VehicleTariff, VehicleType

def fix_tariffs():
    print("Fixing tariff vehicle types...")
    
    # Map old values to new values
    mapping = {
        'car': VehicleType.CAR,
        'camioneta': VehicleType.TRUCK,
        'moto': VehicleType.MOTORCYCLE
    }
    
    tariffs = VehicleTariff.objects.all()
    for t in tariffs:
        print(f"Processing tariff: {t.vehicle_type}")
        if t.vehicle_type in mapping:
            new_type = mapping[t.vehicle_type]
            # Check if a tariff with the new type already exists to avoid unique constraint error
            if VehicleTariff.objects.filter(vehicle_type=new_type).exists():
                print(f"  WARNING: Tariff for {new_type} already exists. Deleting old duplicate {t.vehicle_type}...")
                t.delete()
            else:
                print(f"  Updating {t.vehicle_type} -> {new_type}")
                t.vehicle_type = new_type
                t.save()
        elif t.vehicle_type in [VehicleType.CAR, VehicleType.TRUCK, VehicleType.MOTORCYCLE]:
            print(f"  {t.vehicle_type} is already correct.")
        else:
            print(f"  Unknown type: {t.vehicle_type}")

    # Create missing default tariffs if any
    for type_code, type_label in VehicleType.choices:
        if not VehicleTariff.objects.filter(vehicle_type=type_code).exists():
            print(f"Creating missing tariff for {type_label} ({type_code})")
            VehicleTariff.objects.create(
                vehicle_type=type_code,
                rate_per_hour=5.00, # Default rate
                description=f"Tarifa estándar para {type_label}",
                is_active=True
            )

if __name__ == '__main__':
    fix_tariffs()
