from django.test import TestCase
from django.contrib.auth import get_user_model
from parking.models import (
    ParkingConfiguration,
    VehicleTariff,
    Vehicle,
    VehicleType,
    ParkingFloor,
    ParkingSpace,
    ParkingAssignment
)
from django.utils import timezone

User = get_user_model()


class ParkingConfigurationTestCase(TestCase):
    """Tests para el modelo ParkingConfiguration"""
    
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
    
    def test_create_parking_configuration(self):
        """Crear una configuración de estacionamiento"""
        config = ParkingConfiguration.objects.create(
            total_floors=3,
            spaces_per_floor=20,
            created_by=self.admin
        )
        
        self.assertEqual(config.total_floors, 3)
        self.assertEqual(config.spaces_per_floor, 20)
        self.assertEqual(config.total_capacity, 60)
        self.assertTrue(config.is_active)
    
    def test_only_one_active_configuration(self):
        """Solo puede haber una configuración activa"""
        config1 = ParkingConfiguration.objects.create(
            total_floors=2,
            spaces_per_floor=10,
            created_by=self.admin,
            is_active=True
        )
        
        config2 = ParkingConfiguration.objects.create(
            total_floors=3,
            spaces_per_floor=15,
            created_by=self.admin,
            is_active=True
        )
        
        config1.refresh_from_db()
        self.assertFalse(config1.is_active)
        self.assertTrue(config2.is_active)


class VehicleTariffTestCase(TestCase):
    """Tests para el modelo VehicleTariff"""
    
    def test_create_tariff(self):
        """Crear una tarifa para vehículos"""
        tariff = VehicleTariff.objects.create(
            vehicle_type=VehicleType.CAR,
            hourly_rate=3.00,
            daily_rate=25.00,
            monthly_rate=500.00
        )
        
        self.assertEqual(tariff.vehicle_type, VehicleType.CAR)
        self.assertEqual(tariff.hourly_rate, 3.00)
        self.assertTrue(tariff.is_active)
    
    def test_unique_vehicle_type(self):
        """El tipo de vehículo debe ser único"""
        VehicleTariff.objects.create(
            vehicle_type=VehicleType.CAR,
            hourly_rate=3.00,
            daily_rate=25.00,
            monthly_rate=500.00
        )
        
        with self.assertRaises(Exception):
            VehicleTariff.objects.create(
                vehicle_type=VehicleType.CAR,
                hourly_rate=4.00,
                daily_rate=30.00,
                monthly_rate=600.00
            )


class VehicleTestCase(TestCase):
    """Tests para el modelo Vehicle"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='testpass123'
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
    
    def test_create_vehicle(self):
        """Crear un vehículo"""
        vehicle = Vehicle.objects.create(
            owner=self.user,
            vehicle_type=VehicleType.CAR,
            brand='Toyota',
            model='Corolla',
            year=2020,
            color='Rojo',
            license_plate='ABC-123',
            registered_by=self.admin
        )
        
        self.assertEqual(vehicle.license_plate, 'ABC-123')
        self.assertEqual(vehicle.owner, self.user)
        self.assertTrue(vehicle.is_active)
    
    def test_unique_license_plate(self):
        """La placa debe ser única"""
        Vehicle.objects.create(
            owner=self.user,
            vehicle_type=VehicleType.CAR,
            brand='Toyota',
            model='Corolla',
            year=2020,
            color='Rojo',
            license_plate='ABC-123',
            registered_by=self.admin
        )
        
        with self.assertRaises(Exception):
            Vehicle.objects.create(
                owner=self.user,
                vehicle_type=VehicleType.MOTORCYCLE,
                brand='Honda',
                model='CBR',
                year=2021,
                color='Negro',
                license_plate='ABC-123',
                registered_by=self.admin
            )


class ParkingSpaceTestCase(TestCase):
    """Tests para espacios de estacionamiento"""
    
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        
        # Crear configuración (automáticamente crea pisos y espacios)
        self.config = ParkingConfiguration.objects.create(
            total_floors=2,
            spaces_per_floor=10,
            created_by=self.admin
        )
    
    def test_spaces_created_automatically(self):
        """Los espacios se crean automáticamente con la configuración"""
        total_floors = ParkingFloor.objects.filter(configuration=self.config).count()
        total_spaces = ParkingSpace.objects.filter(floor__configuration=self.config).count()
        
        self.assertEqual(total_floors, 2)
        self.assertEqual(total_spaces, 20)
    
    def test_space_full_code(self):
        """Verificar el código completo del espacio"""
        floor = ParkingFloor.objects.filter(configuration=self.config).first()
        space = ParkingSpace.objects.filter(floor=floor).first()
        
        expected_code = f"P{floor.floor_number}-001"
        self.assertEqual(space.full_code, expected_code)


class ParkingAssignmentTestCase(TestCase):
    """Tests para asignaciones de estacionamiento"""
    
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
        
        self.user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='testpass123'
        )
        
        # Configuración
        self.config = ParkingConfiguration.objects.create(
            total_floors=2,
            spaces_per_floor=10,
            created_by=self.admin
        )
        
        # Tarifa
        self.tariff = VehicleTariff.objects.create(
            vehicle_type=VehicleType.CAR,
            hourly_rate=3.00,
            daily_rate=25.00,
            monthly_rate=500.00
        )
        
        # Vehículo
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
        
        # Espacio
        self.space = ParkingSpace.objects.filter(
            floor__configuration=self.config,
            status='AVAILABLE'
        ).first()
    
    def test_create_assignment(self):
        """Crear una asignación de estacionamiento"""
        assignment = ParkingAssignment.objects.create(
            vehicle=self.vehicle,
            parking_space=self.space,
            assigned_by=self.admin
        )
        
        self.assertEqual(assignment.status, 'ACTIVE')
        self.assertIsNotNone(assignment.entry_time)
        self.assertIsNone(assignment.exit_time)
    
    def test_complete_assignment(self):
        """Completar una asignación y calcular costo"""
        assignment = ParkingAssignment.objects.create(
            vehicle=self.vehicle,
            parking_space=self.space,
            assigned_by=self.admin
        )
        
        # Marcar espacio como ocupado
        self.space.status = 'OCCUPIED'
        self.space.save()
        
        # Completar asignación
        assignment.complete_assignment(completed_by=self.admin)
        
        self.assertEqual(assignment.status, 'COMPLETED')
        self.assertIsNotNone(assignment.exit_time)
        self.assertIsNotNone(assignment.total_cost)
        
        # Verificar que el espacio está disponible
        self.space.refresh_from_db()
        self.assertEqual(self.space.status, 'AVAILABLE')
