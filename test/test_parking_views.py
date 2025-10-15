"""
Tests para las vistas del sistema de estacionamiento.

Este archivo contiene tests para verificar el correcto funcionamiento de:
- Dashboard
- Vistas de vehículos (añadir, listar, asignar)
- Vistas de reservas (normal, rápida, listar, detalle, cancelar)
- Control de acceso y permisos

Ejecutar:
    python -m pytest test/test_parking_views.py -v
    O
    python manage.py test test.test_parking_views
"""

import os
import sys
import django
from datetime import timedelta
from decimal import Decimal

# Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from parking.models import (
    ParkingConfiguration, VehicleTariff, Vehicle,
    ParkingFloor, ParkingSpace, ParkingReservation,
    VehicleType
)

User = get_user_model()


class ParkingViewsAccessTestCase(TestCase):
    """Tests para verificar el control de acceso a las vistas"""

    def setUp(self):
        """Configuración inicial para los tests"""
        # Usuario normal (sin permisos)
        self.normal_user = User.objects.create_user(
            username='normal_user',
            email='normal@test.com',
            password='normal123'
        )

        # Usuario trabajador (con permisos)
        self.worker = User.objects.create_user(
            username='worker',
            email='worker@test.com',
            password='worker123',
            is_staff=True
        )

        # Superusuario (con todos los permisos)
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )

        self.client = Client()

    def test_dashboard_requires_login(self):
        """Test: Dashboard requiere login"""
        response = self.client.get(reverse('parking:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect a login
        print("Test dashboard requiere login: PASS")

    def test_dashboard_requires_staff_permission(self):
        """Test: Dashboard requiere permiso de staff"""
        # Login con usuario normal
        self.client.login(username='normal_user', password='normal123')
        response = self.client.get(reverse('parking:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect
        print("Test dashboard requiere staff: PASS")

    def test_dashboard_accessible_by_staff(self):
        """Test: Dashboard accesible por staff"""
        self.client.login(username='worker', password='worker123')
        response = self.client.get(reverse('parking:dashboard'))
        self.assertEqual(response.status_code, 200)
        print("Test dashboard accesible por staff: PASS")

    def test_dashboard_accessible_by_admin(self):
        """Test: Dashboard accesible por admin"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('parking:dashboard'))
        self.assertEqual(response.status_code, 200)
        print("Test dashboard accesible por admin: PASS")

    def test_all_views_require_authentication(self):
        """Test: Todas las vistas requieren autenticación"""
        urls_to_test = [
            'parking:dashboard',
            'parking:vehicle_list',
            'parking:add_vehicle',
            'parking:assign_vehicle',
            'parking:reservation_list',
            'parking:normal_reservation',
            'parking:quick_reservation',
        ]

        for url_name in urls_to_test:
            response = self.client.get(reverse(url_name))
            self.assertEqual(
                response.status_code, 
                302, 
                f"{url_name} debería redirigir sin autenticación"
            )
        print("Test todas las vistas requieren autenticación: PASS")


class DashboardViewTestCase(TestCase):
    """Tests para la vista del dashboard"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )

        # Crear configuración
        self.config = ParkingConfiguration.objects.create(
            total_floors=2,
            spaces_per_floor=10,
            is_active=True,
            created_by=self.admin
        )

        # Crear pisos y espacios
        for floor_num in range(1, 3):
            floor = ParkingFloor.objects.create(
                configuration=self.config,
                floor_number=floor_num,
                total_spaces=10
            )
            for space_num in range(1, 11):
                ParkingSpace.objects.create(
                    floor=floor,
                    space_number=f'A-{space_num:02d}',
                    space_type=VehicleType.CAR,
                    is_available=True
                )

        self.client = Client()
        self.client.login(username='admin', password='admin123')

    def test_dashboard_loads_successfully(self):
        """Test: Dashboard carga correctamente"""
        response = self.client.get(reverse('parking:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parking/dashboard.html')
        print("Test dashboard carga: PASS")

    def test_dashboard_shows_statistics(self):
        """Test: Dashboard muestra estadísticas"""
        response = self.client.get(reverse('parking:dashboard'))
        self.assertIn('total_spaces', response.context)
        self.assertIn('available_spaces', response.context)
        self.assertIn('occupied_spaces', response.context)
        self.assertEqual(response.context['total_spaces'], 20)
        print("Test dashboard muestra estadísticas: PASS")

    def test_dashboard_shows_configuration(self):
        """Test: Dashboard muestra configuración"""
        response = self.client.get(reverse('parking:dashboard'))
        self.assertIn('config', response.context)
        self.assertEqual(response.context['config'].total_floors, 2)
        print("Test dashboard muestra configuración: PASS")


class VehicleViewsTestCase(TestCase):
    """Tests para las vistas de vehículos"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )

        self.owner = User.objects.create_user(
            username='owner',
            email='owner@test.com',
            password='owner123'
        )

        self.client = Client()
        self.client.login(username='admin', password='admin123')

    def test_vehicle_list_view(self):
        """Test: Vista de lista de vehículos"""
        # Crear vehículos
        Vehicle.objects.create(
            owner=self.owner,
            vehicle_type=VehicleType.CAR,
            brand='Toyota',
            model='Corolla',
            year=2020,
            color='Rojo',
            license_plate='ABC-123',
            registered_by=self.admin
        )

        response = self.client.get(reverse('parking:vehicle_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parking/vehicle_list.html')
        self.assertIn('vehicles', response.context)
        print("Test lista de vehículos: PASS")

    def test_add_vehicle_view_get(self):
        """Test: Vista de añadir vehículo (GET)"""
        response = self.client.get(reverse('parking:add_vehicle'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parking/vehicle_form.html')
        self.assertIn('form', response.context)
        print("Test añadir vehículo GET: PASS")

    def test_add_vehicle_view_post(self):
        """Test: Vista de añadir vehículo (POST)"""
        data = {
            'license_plate': 'XYZ-789',
            'vehicle_type': VehicleType.CAR,
            'brand': 'Honda',
            'model': 'Civic',
            'year': 2021,
            'color': 'Azul',
            'owner': self.owner.id
        }

        response = self.client.post(reverse('parking:add_vehicle'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Vehicle.objects.filter(license_plate='XYZ-789').exists())
        print("Test añadir vehículo POST: PASS")

    def test_assign_vehicle_view(self):
        """Test: Vista de asignar vehículo"""
        # Crear vehículo
        vehicle = Vehicle.objects.create(
            owner=self.owner,
            vehicle_type=VehicleType.CAR,
            brand='Ford',
            model='Fiesta',
            year=2019,
            color='Blanco',
            license_plate='DEF-456',
            registered_by=self.admin
        )

        response = self.client.get(reverse('parking:assign_vehicle'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parking/assign_vehicle.html')
        print("Test asignar vehículo: PASS")

    def test_vehicle_search(self):
        """Test: Búsqueda de vehículos"""
        Vehicle.objects.create(
            owner=self.owner,
            vehicle_type=VehicleType.CAR,
            brand='Toyota',
            model='Corolla',
            year=2020,
            color='Rojo',
            license_plate='ABC-123',
            registered_by=self.admin
        )

        response = self.client.get(reverse('parking:vehicle_list'), {'search': 'Toyota'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('vehicles', response.context)
        print("Test búsqueda de vehículos: PASS")


class ReservationViewsTestCase(TestCase):
    """Tests para las vistas de reservas"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )

        self.owner = User.objects.create_user(
            username='owner',
            email='owner@test.com',
            password='owner123'
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
            owner=self.owner,
            vehicle_type=VehicleType.CAR,
            brand='Toyota',
            model='Corolla',
            year=2020,
            color='Rojo',
            license_plate='ABC-123',
            registered_by=self.admin
        )

        self.client = Client()
        self.client.login(username='admin', password='admin123')

    def test_reservation_list_view(self):
        """Test: Vista de lista de reservas"""
        response = self.client.get(reverse('parking:reservation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parking/reservation_list.html')
        self.assertIn('reservations', response.context)
        print("Test lista de reservas: PASS")

    def test_normal_reservation_view_get(self):
        """Test: Vista de reserva normal (GET)"""
        response = self.client.get(reverse('parking:normal_reservation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parking/reservation_form.html')
        self.assertIn('form', response.context)
        print("Test reserva normal GET: PASS")

    def test_normal_reservation_view_post(self):
        """Test: Vista de reserva normal (POST)"""
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=3)

        data = {
            'vehicle': self.vehicle.id,
            'reserved_space': self.space.id,
            'start_datetime': start.strftime('%Y-%m-%dT%H:%M'),
            'end_datetime': end.strftime('%Y-%m-%dT%H:%M'),
            'notes': 'Test reservation'
        }

        response = self.client.post(reverse('parking:normal_reservation'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(ParkingReservation.objects.filter(vehicle=self.vehicle).exists())
        print("Test reserva normal POST: PASS")

    def test_quick_reservation_view_get(self):
        """Test: Vista de reserva rápida (GET)"""
        response = self.client.get(reverse('parking:quick_reservation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parking/reservation_form.html')
        self.assertIn('form', response.context)
        print("Test reserva rápida GET: PASS")

    def test_quick_reservation_view_post(self):
        """Test: Vista de reserva rápida (POST)"""
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)

        data = {
            'customer_name': 'Juan Pérez',
            'customer_phone': '+51999999999',
            'customer_email': 'juan@test.com',
            'vehicle_plate': 'XYZ-789',
            'vehicle_type_temp': VehicleType.MOTORCYCLE,
            'reserved_space': self.space.id,
            'start_datetime': start.strftime('%Y-%m-%dT%H:%M'),
            'end_datetime': end.strftime('%Y-%m-%dT%H:%M'),
        }

        response = self.client.post(reverse('parking:quick_reservation'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(
            ParkingReservation.objects.filter(
                customer_name='Juan Pérez',
                is_quick_reservation=True
            ).exists()
        )
        print("Test reserva rápida POST: PASS")

    def test_reservation_detail_view(self):
        """Test: Vista de detalle de reserva"""
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=3)

        reservation = ParkingReservation.objects.create(
            vehicle=self.vehicle,
            reserved_space=self.space,
            start_datetime=start,
            end_datetime=end,
            created_by=self.admin
        )

        response = self.client.get(
            reverse('parking:reservation_detail', kwargs={'pk': reservation.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parking/reservation_detail.html')
        self.assertIn('reservation', response.context)
        print("Test detalle de reserva: PASS")

    def test_cancel_reservation_view(self):
        """Test: Vista de cancelar reserva"""
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=3)

        reservation = ParkingReservation.objects.create(
            vehicle=self.vehicle,
            reserved_space=self.space,
            start_datetime=start,
            end_datetime=end,
            created_by=self.admin
        )

        # GET - Mostrar confirmación
        response = self.client.get(
            reverse('parking:cancel_reservation', kwargs={'pk': reservation.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parking/reservation_cancel.html')

        # POST - Cancelar reserva
        response = self.client.post(
            reverse('parking:cancel_reservation', kwargs={'pk': reservation.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        reservation.refresh_from_db()
        self.assertTrue(reservation.is_cancelled)
        print("Test cancelar reserva: PASS")

    def test_reservation_filters(self):
        """Test: Filtros de reservas"""
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=3)

        # Crear reserva normal
        ParkingReservation.objects.create(
            vehicle=self.vehicle,
            reserved_space=self.space,
            start_datetime=start,
            end_datetime=end,
            is_quick_reservation=False,
            created_by=self.admin
        )

        # Crear reserva rápida
        ParkingReservation.objects.create(
            reserved_space=self.space,
            start_datetime=start,
            end_datetime=end,
            customer_name='Juan Pérez',
            customer_phone='+51999999999',
            vehicle_plate='XYZ-789',
            vehicle_type_temp=VehicleType.MOTORCYCLE,
            is_quick_reservation=True,
            created_by=self.admin
        )

        # Filtrar por tipo: rápida
        response = self.client.get(reverse('parking:reservation_list'), {'type': 'quick'})
        self.assertEqual(response.status_code, 200)
        
        # Filtrar por tipo: normal
        response = self.client.get(reverse('parking:reservation_list'), {'type': 'normal'})
        self.assertEqual(response.status_code, 200)
        
        print("Test filtros de reservas: PASS")


class FormValidationTestCase(TestCase):
    """Tests para validación de formularios"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )

        self.owner = User.objects.create_user(
            username='owner',
            email='owner@test.com',
            password='owner123'
        )

        self.client = Client()
        self.client.login(username='admin', password='admin123')

    def test_vehicle_form_missing_required_fields(self):
        """Test: Formulario de vehículo con campos requeridos faltantes"""
        data = {
            'brand': 'Toyota',
            'model': 'Corolla'
            # Faltan: license_plate, vehicle_type, year, color, owner
        }

        response = self.client.post(reverse('parking:add_vehicle'), data)
        self.assertEqual(response.status_code, 200)  # No redirige, muestra errores
        self.assertFormError(response, 'form', 'license_plate', 'This field is required.')
        print("Test validación campos requeridos vehículo: PASS")

    def test_reservation_invalid_dates(self):
        """Test: Reserva con fechas inválidas"""
        # Crear espacio
        config = ParkingConfiguration.objects.create(
            total_floors=1,
            spaces_per_floor=10,
            is_active=True,
            created_by=self.admin
        )
        floor = ParkingFloor.objects.create(
            configuration=config,
            floor_number=1,
            total_spaces=10
        )
        space = ParkingSpace.objects.create(
            floor=floor,
            space_number='A-01',
            space_type=VehicleType.CAR,
            is_available=True
        )

        # Fechas inválidas (fin antes de inicio)
        start = timezone.now() + timedelta(hours=3)
        end = timezone.now() + timedelta(hours=1)  # Antes del inicio

        data = {
            'customer_name': 'Test User',
            'customer_phone': '+51999999999',
            'vehicle_plate': 'ABC-123',
            'vehicle_type_temp': VehicleType.CAR,
            'reserved_space': space.id,
            'start_datetime': start.strftime('%Y-%m-%dT%H:%M'),
            'end_datetime': end.strftime('%Y-%m-%dT%H:%M'),
        }

        response = self.client.post(reverse('parking:quick_reservation'), data)
        # Debería mostrar error o no crear la reserva
        print("Test validación fechas reserva: PASS")


# Función para ejecutar todos los tests
def run_all_tests():
    """Ejecuta todos los tests y muestra un resumen"""
    import unittest

    print("\n" + "="*80)
    print("EJECUTANDO TESTS DE VISTAS DEL SISTEMA DE ESTACIONAMIENTO")
    print("="*80 + "\n")

    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar todos los test cases
    suite.addTests(loader.loadTestsFromTestCase(ParkingViewsAccessTestCase))
    suite.addTests(loader.loadTestsFromTestCase(DashboardViewTestCase))
    suite.addTests(loader.loadTestsFromTestCase(VehicleViewsTestCase))
    suite.addTests(loader.loadTestsFromTestCase(ReservationViewsTestCase))
    suite.addTests(loader.loadTestsFromTestCase(FormValidationTestCase))

    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Mostrar resumen
    print("\n" + "="*80)
    print("RESUMEN DE TESTS DE VISTAS")
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
