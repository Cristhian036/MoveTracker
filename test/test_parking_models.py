"""
Tests para los modelos del sistema de estacionamiento.

Este archivo contiene tests para verificar el correcto funcionamiento de:
- ParkingConfiguration
- VehicleTariff
- Vehicle
- ParkingFloor
- ParkingSpace
- ParkingAssignment
- ParkingReservation

Ejecutar:
    python -m pytest test/test_parking_models.py -v
    O
    python manage.py test test.test_parking_models
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from parking.models import (
    ParkingConfiguration, VehicleTariff, Vehicle,
    ParkingFloor, ParkingSpace, ParkingAssignment,
    ParkingReservation, VehicleType
)

User = get_user_model()


class ParkingConfigurationTestCase(TestCase):
    """Tests para el modelo ParkingConfiguration"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='admin123',
            is_staff=True
        )

    def test_create_parking_configuration(self):
        """Test: Crear configuración de estacionamiento"""
        config = ParkingConfiguration.objects.create(
            total_floors=5,
            spaces_per_floor=25,
            is_active=True,
            created_by=self.user
        )

        self.assertEqual(config.total_floors, 5)
        self.assertEqual(config.spaces_per_floor, 25)
        self.assertTrue(config.is_active)
        self.assertEqual(config.created_by, self.user)
        print("Test crear configuración: PASS")

    def test_configuration_string_representation(self):
        """Test: Representación en string de la configuración"""
        config = ParkingConfiguration.objects.create(
            total_floors=3,
            spaces_per_floor=20,
            created_by=self.user
        )

        expected = "3 pisos - 20 espacios/piso"
        self.assertEqual(str(config), expected)
        print("Test representación string configuración: PASS")

    def test_total_capacity_property(self):
        """Test: Propiedad de capacidad total"""
        config = ParkingConfiguration.objects.create(
            total_floors=4,
            spaces_per_floor=15,
            created_by=self.user
        )

        self.assertEqual(config.total_capacity, 60)
        print("Test capacidad total: PASS")

    def test_only_one_active_configuration(self):
        """Test: Solo puede haber una configuración activa"""
        # Crear primera configuración activa
        config1 = ParkingConfiguration.objects.create(
            total_floors=3,
            spaces_per_floor=20,
            is_active=True,
            created_by=self.user
        )

        # Crear segunda configuración activa
        config2 = ParkingConfiguration.objects.create(
            total_floors=5,
            spaces_per_floor=30,
            is_active=True,
            created_by=self.user
        )

        # Verificar que solo hay una activa
        active_configs = ParkingConfiguration.objects.filter(is_active=True).count()
        self.assertGreaterEqual(active_configs, 1)
        print("Test configuración única activa: PASS")


class VehicleTariffTestCase(TestCase):
    """Tests para el modelo VehicleTariff"""

    def test_create_vehicle_tariff(self):
        """Test: Crear tarifa de vehículo"""
        tariff = VehicleTariff.objects.create(
            vehicle_type=VehicleType.CAR,
            hourly_rate=Decimal('3.00'),
            daily_rate=Decimal('20.00'),
            monthly_rate=Decimal('400.00')
        )

        self.assertEqual(tariff.vehicle_type, VehicleType.CAR)
        self.assertEqual(tariff.hourly_rate, Decimal('3.00'))
        self.assertEqual(tariff.daily_rate, Decimal('20.00'))
        self.assertEqual(tariff.monthly_rate, Decimal('400.00'))
        print("Test crear tarifa: PASS")

    def test_tariff_string_representation(self):
        """Test: Representación en string de la tarifa"""
        tariff = VehicleTariff.objects.create(
            vehicle_type=VehicleType.MOTORCYCLE,
            hourly_rate=Decimal('2.00')
        )

        expected = "Moto - $2.00/hora"
        self.assertEqual(str(tariff), expected)
        print("Test representación string tarifa: PASS")

    def test_unique_vehicle_type_tariff(self):
        """Test: Cada tipo de vehículo tiene una tarifa única"""
        VehicleTariff.objects.create(
            vehicle_type=VehicleType.TRUCK,
            hourly_rate=Decimal('5.00')
        )

        # Intentar crear otra tarifa para el mismo tipo
        with self.assertRaises(Exception):
            VehicleTariff.objects.create(
                vehicle_type=VehicleType.TRUCK,
                hourly_rate=Decimal('6.00')
            )
        print("Test tarifa única por tipo: PASS")

    def test_all_vehicle_types_tariffs(self):
        """Test: Crear tarifas para todos los tipos de vehículo"""
        tariffs = {
            VehicleType.MOTORCYCLE: Decimal('2.00'),
            VehicleType.CAR: Decimal('3.00'),
            VehicleType.TRUCK: Decimal('5.00'),
        }

        for vehicle_type, rate in tariffs.items():
            VehicleTariff.objects.create(
                vehicle_type=vehicle_type,
                hourly_rate=rate
            )

        self.assertEqual(VehicleTariff.objects.count(), 3)
        print("Test tarifas para todos los tipos: PASS")


class VehicleTestCase(TestCase):
    """Tests para el modelo Vehicle"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.owner = User.objects.create_user(
            username='owner_test',
            email='owner@test.com',
            password='owner123'
        )
        self.admin = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='admin123',
            is_staff=True
        )

    def test_create_vehicle(self):
        """Test: Crear vehículo"""
        vehicle = Vehicle.objects.create(
            owner=self.owner,
            vehicle_type=VehicleType.CAR,
            brand='Toyota',
            model='Corolla',
            year=2020,
            color='Rojo',
            license_plate='ABC-123',
            registered_by=self.admin
        )

        self.assertEqual(vehicle.owner, self.owner)
        self.assertEqual(vehicle.vehicle_type, VehicleType.CAR)
        self.assertEqual(vehicle.brand, 'Toyota')
        self.assertEqual(vehicle.license_plate, 'ABC-123')
        self.assertTrue(vehicle.is_active)
        print("Test crear vehículo: PASS")

    def test_vehicle_string_representation(self):
        """Test: Representación en string del vehículo"""
        vehicle = Vehicle.objects.create(
            owner=self.owner,
            vehicle_type=VehicleType.MOTORCYCLE,
            brand='Honda',
            model='CBR',
            year=2021,
            color='Negro',
            license_plate='XYZ-789',
            registered_by=self.admin
        )

        expected = "XYZ-789 - Moto (owner_test)"
        self.assertEqual(str(vehicle), expected)
        print("Test representación string vehículo: PASS")

    def test_unique_license_plate(self):
        """Test: La placa debe ser única"""
        Vehicle.objects.create(
            owner=self.owner,
            vehicle_type=VehicleType.CAR,
            brand='Ford',
            model='Fiesta',
            year=2019,
            color='Azul',
            license_plate='DEF-456',
            registered_by=self.admin
        )

        # Intentar crear otro vehículo con la misma placa
        with self.assertRaises(Exception):
            Vehicle.objects.create(
                owner=self.owner,
                vehicle_type=VehicleType.TRUCK,
                brand='Chevrolet',
                model='Colorado',
                year=2020,
                color='Blanco',
                license_plate='DEF-456',
                registered_by=self.admin
            )
        print("Test placa única: PASS")

    def test_vehicle_year_validation(self):
        """Test: Validación del año del vehículo"""
        # Año válido
        vehicle = Vehicle.objects.create(
            owner=self.owner,
            vehicle_type=VehicleType.CAR,
            brand='Nissan',
            model='Sentra',
            year=2022,
            color='Gris',
            license_plate='GHI-789',
            registered_by=self.admin
        )

        self.assertGreaterEqual(vehicle.year, 1900)
        self.assertLessEqual(vehicle.year, 2100)
        print("Test validación año: PASS")

    def test_vehicle_deactivation(self):
        """Test: Desactivar vehículo"""
        vehicle = Vehicle.objects.create(
            owner=self.owner,
            vehicle_type=VehicleType.CAR,
            brand='Mazda',
            model='3',
            year=2020,
            color='Rojo',
            license_plate='JKL-012',
            registered_by=self.admin
        )

        # Desactivar vehículo
        vehicle.is_active = False
        vehicle.save()

        self.assertFalse(vehicle.is_active)
        print("Test desactivar vehículo: PASS")


class ParkingFloorTestCase(TestCase):
    """Tests para el modelo ParkingFloor"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='admin123',
            is_staff=True
        )
        self.config = ParkingConfiguration.objects.create(
            total_floors=3,
            spaces_per_floor=20,
            is_active=True,
            created_by=self.user
        )

    def test_create_parking_floor(self):
        """Test: Crear piso de estacionamiento"""
        floor = ParkingFloor.objects.create(
            configuration=self.config,
            floor_number=1,
            total_spaces=20
        )

        self.assertEqual(floor.configuration, self.config)
        self.assertEqual(floor.floor_number, 1)
        self.assertEqual(floor.total_spaces, 20)
        print("Test crear piso: PASS")

    def test_floor_string_representation(self):
        """Test: Representación en string del piso"""
        floor = ParkingFloor.objects.create(
            configuration=self.config,
            floor_number=2,
            total_spaces=20
        )

        expected = "Piso 2 (20 espacios)"
        self.assertEqual(str(floor), expected)
        print("Test representación string piso: PASS")

    def test_floor_number_uniqueness(self):
        """Test: El número de piso debe ser único por configuración"""
        ParkingFloor.objects.create(
            configuration=self.config,
            floor_number=1,
            total_spaces=20
        )

        # Intentar crear otro piso con el mismo número
        with self.assertRaises(Exception):
            ParkingFloor.objects.create(
                configuration=self.config,
                floor_number=1,
                total_spaces=25
            )
        print("Test número de piso único: PASS")


class ParkingSpaceTestCase(TestCase):
    """Tests para el modelo ParkingSpace"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='admin123',
            is_staff=True
        )
        self.config = ParkingConfiguration.objects.create(
            total_floors=3,
            spaces_per_floor=20,
            is_active=True,
            created_by=self.user
        )
        self.floor = ParkingFloor.objects.create(
            configuration=self.config,
            floor_number=1,
            total_spaces=20
        )

    def test_create_parking_space(self):
        """Test: Crear espacio de estacionamiento"""
        space = ParkingSpace.objects.create(
            floor=self.floor,
            space_number='A-01',
            space_type=VehicleType.CAR,
            is_available=True
        )

        self.assertEqual(space.floor, self.floor)
        self.assertEqual(space.space_number, 'A-01')
        self.assertEqual(space.space_type, VehicleType.CAR)
        self.assertTrue(space.is_available)
        print("Test crear espacio: PASS")

    def test_space_string_representation(self):
        """Test: Representación en string del espacio"""
        space = ParkingSpace.objects.create(
            floor=self.floor,
            space_number='B-05',
            space_type=VehicleType.MOTORCYCLE
        )

        expected = "Piso 1 - Espacio B-05 (Moto)"
        self.assertEqual(str(space), expected)
        print("Test representación string espacio: PASS")

    def test_space_availability_toggle(self):
        """Test: Cambiar disponibilidad del espacio"""
        space = ParkingSpace.objects.create(
            floor=self.floor,
            space_number='C-10',
            space_type=VehicleType.CAR,
            is_available=True
        )

        # Marcar como ocupado
        space.is_available = False
        space.save()
        self.assertFalse(space.is_available)

        # Marcar como disponible nuevamente
        space.is_available = True
        space.save()
        self.assertTrue(space.is_available)
        print("Test cambiar disponibilidad: PASS")

    def test_space_number_uniqueness_per_floor(self):
        """Test: El número de espacio debe ser único por piso"""
        ParkingSpace.objects.create(
            floor=self.floor,
            space_number='D-15',
            space_type=VehicleType.CAR
        )

        # Intentar crear otro espacio con el mismo número en el mismo piso
        with self.assertRaises(Exception):
            ParkingSpace.objects.create(
                floor=self.floor,
                space_number='D-15',
                space_type=VehicleType.TRUCK
            )
        print("Test número de espacio único por piso: PASS")


class ParkingAssignmentTestCase(TestCase):
    """Tests para el modelo ParkingAssignment"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='user_test',
            email='user@test.com',
            password='user123'
        )
        self.admin = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='admin123',
            is_staff=True
        )

        # Crear configuración y espacios
        self.config = ParkingConfiguration.objects.create(
            total_floors=1,
            spaces_per_floor=10,
            is_active=True,
            created_by=self.admin
        )
        self.floor = ParkingFloor.objects.create(
            configuration=self.config,
            floor_number=1,
            total_spaces=10
        )
        self.space = ParkingSpace.objects.create(
            floor=self.floor,
            space_number='A-01',
            space_type=VehicleType.CAR,
            is_available=True
        )

        # Crear vehículo
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            vehicle_type=VehicleType.CAR,
            brand='Toyota',
            model='Corolla',
            year=2020,
            color='Rojo',
            license_plate='ABC-123',
            registered_by=self.admin
        )

        # Crear tarifa
        self.tariff = VehicleTariff.objects.create(
            vehicle_type=VehicleType.CAR,
            hourly_rate=Decimal('3.00'),
            daily_rate=Decimal('20.00'),
            monthly_rate=Decimal('400.00')
        )

    def test_create_parking_assignment(self):
        """Test: Crear asignación de estacionamiento"""
        assignment = ParkingAssignment.objects.create(
            vehicle=self.vehicle,
            assigned_space=self.space,
            entry_time=timezone.now(),
            assigned_by=self.admin
        )

        self.assertEqual(assignment.vehicle, self.vehicle)
        self.assertEqual(assignment.assigned_space, self.space)
        self.assertIsNotNone(assignment.entry_time)
        self.assertIsNone(assignment.exit_time)
        print("Test crear asignación: PASS")

    def test_assignment_string_representation(self):
        """Test: Representación en string de la asignación"""
        assignment = ParkingAssignment.objects.create(
            vehicle=self.vehicle,
            assigned_space=self.space,
            entry_time=timezone.now(),
            assigned_by=self.admin
        )

        self.assertIn('ABC-123', str(assignment))
        self.assertIn('A-01', str(assignment))
        print("Test representación string asignación: PASS")

    def test_calculate_duration(self):
        """Test: Calcular duración de estacionamiento"""
        entry = timezone.now()
        exit_time = entry + timedelta(hours=3)

        assignment = ParkingAssignment.objects.create(
            vehicle=self.vehicle,
            assigned_space=self.space,
            entry_time=entry,
            exit_time=exit_time,
            assigned_by=self.admin
        )

        duration = assignment.calculate_duration()
        self.assertIsNotNone(duration)
        self.assertGreaterEqual(duration.total_seconds(), 10800)  # 3 horas en segundos
        print("Test calcular duración: PASS")

    def test_calculate_cost(self):
        """Test: Calcular costo de estacionamiento"""
        entry = timezone.now()
        exit_time = entry + timedelta(hours=2)

        assignment = ParkingAssignment.objects.create(
            vehicle=self.vehicle,
            assigned_space=self.space,
            entry_time=entry,
            exit_time=exit_time,
            assigned_by=self.admin
        )

        cost = assignment.calculate_cost()
        # 2 horas * $3.00/hora = $6.00
        expected_cost = Decimal('6.00')
        self.assertEqual(cost, expected_cost)
        print("Test calcular costo: PASS")

    def test_assignment_without_exit(self):
        """Test: Asignación activa sin salida"""
        assignment = ParkingAssignment.objects.create(
            vehicle=self.vehicle,
            assigned_space=self.space,
            entry_time=timezone.now(),
            assigned_by=self.admin
        )

        self.assertIsNone(assignment.exit_time)
        self.assertIsNone(assignment.total_cost)
        print("Test asignación sin salida: PASS")


class ParkingReservationTestCase(TestCase):
    """Tests para el modelo ParkingReservation"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='user_test',
            email='user@test.com',
            password='user123'
        )
        self.admin = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='admin123',
            is_staff=True
        )

        # Crear configuración y espacios
        self.config = ParkingConfiguration.objects.create(
            total_floors=1,
            spaces_per_floor=10,
            is_active=True,
            created_by=self.admin
        )
        self.floor = ParkingFloor.objects.create(
            configuration=self.config,
            floor_number=1,
            total_spaces=10
        )
        self.space = ParkingSpace.objects.create(
            floor=self.floor,
            space_number='A-01',
            space_type=VehicleType.CAR,
            is_available=True
        )

        # Crear vehículo
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            vehicle_type=VehicleType.CAR,
            brand='Toyota',
            model='Corolla',
            year=2020,
            color='Rojo',
            license_plate='ABC-123',
            registered_by=self.admin
        )

    def test_create_normal_reservation(self):
        """Test: Crear reserva normal"""
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=3)

        reservation = ParkingReservation.objects.create(
            vehicle=self.vehicle,
            reserved_space=self.space,
            start_datetime=start,
            end_datetime=end,
            is_quick_reservation=False,
            created_by=self.admin
        )

        self.assertEqual(reservation.vehicle, self.vehicle)
        self.assertEqual(reservation.reserved_space, self.space)
        self.assertFalse(reservation.is_quick_reservation)
        self.assertFalse(reservation.is_cancelled)
        print("Test crear reserva normal: PASS")

    def test_create_quick_reservation(self):
        """Test: Crear reserva rápida"""
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)

        reservation = ParkingReservation.objects.create(
            reserved_space=self.space,
            start_datetime=start,
            end_datetime=end,
            customer_name='Juan Pérez',
            customer_phone='+51999999999',
            customer_email='juan@ejemplo.com',
            vehicle_plate='XYZ-789',
            vehicle_type_temp=VehicleType.MOTORCYCLE,
            is_quick_reservation=True,
            created_by=self.admin
        )

        self.assertIsNone(reservation.vehicle)
        self.assertEqual(reservation.customer_name, 'Juan Pérez')
        self.assertEqual(reservation.vehicle_plate, 'XYZ-789')
        self.assertTrue(reservation.is_quick_reservation)
        print("Test crear reserva rápida: PASS")

    def test_reservation_string_representation(self):
        """Test: Representación en string de la reserva"""
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=3)

        reservation = ParkingReservation.objects.create(
            vehicle=self.vehicle,
            reserved_space=self.space,
            start_datetime=start,
            end_datetime=end,
            created_by=self.admin
        )

        self.assertIn('ABC-123', str(reservation))
        self.assertIn('A-01', str(reservation))
        print("Test representación string reserva: PASS")

    def test_cancel_reservation(self):
        """Test: Cancelar reserva"""
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=3)

        reservation = ParkingReservation.objects.create(
            vehicle=self.vehicle,
            reserved_space=self.space,
            start_datetime=start,
            end_datetime=end,
            created_by=self.admin
        )

        # Cancelar reserva
        reservation.is_cancelled = True
        reservation.save()

        self.assertTrue(reservation.is_cancelled)
        print("Test cancelar reserva: PASS")

    def test_reservation_with_notes(self):
        """Test: Reserva con notas"""
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=3)

        reservation = ParkingReservation.objects.create(
            vehicle=self.vehicle,
            reserved_space=self.space,
            start_datetime=start,
            end_datetime=end,
            notes='Cliente VIP - requiere atención especial',
            created_by=self.admin
        )

        self.assertIsNotNone(reservation.notes)
        self.assertIn('VIP', reservation.notes)
        print("Test reserva con notas: PASS")


# Función para ejecutar todos los tests
def run_all_tests():
    """Ejecuta todos los tests y muestra un resumen"""
    import unittest

    print("\n" + "="*80)
    print("EJECUTANDO TESTS DEL SISTEMA DE ESTACIONAMIENTO")
    print("="*80 + "\n")

    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar todos los test cases
    suite.addTests(loader.loadTestsFromTestCase(ParkingConfigurationTestCase))
    suite.addTests(loader.loadTestsFromTestCase(VehicleTariffTestCase))
    suite.addTests(loader.loadTestsFromTestCase(VehicleTestCase))
    suite.addTests(loader.loadTestsFromTestCase(ParkingFloorTestCase))
    suite.addTests(loader.loadTestsFromTestCase(ParkingSpaceTestCase))
    suite.addTests(loader.loadTestsFromTestCase(ParkingAssignmentTestCase))
    suite.addTests(loader.loadTestsFromTestCase(ParkingReservationTestCase))

    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Mostrar resumen
    print("\n" + "="*80)
    print("RESUMEN DE TESTS")
    print("="*80)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*80 + "\n")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
