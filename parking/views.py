from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Vehicle, ParkingReservation, ParkingSpace, VehicleType, ParkingConfiguration, ParkingFloor, ParkingAssignment, VehicleTariff
from .forms import (
    VehicleForm, AssignVehicleForm, 
    NormalReservationForm, QuickReservationForm,
    ParkingConfigurationForm, CheckoutForm
)
import math


def is_admin_or_worker(user):
    """Verifica si el usuario es administrador o trabajador"""
    if not user.is_authenticated:
        return False
    # Si el usuario es superusuario, tiene acceso
    if user.is_superuser:
        return True
    # Verificar si tiene el atributo role (cuando se implemente)
    if hasattr(user, 'role'):
        return user.role in ['ADMIN', 'WORKER']
    # Por ahora, permitir a usuarios staff
    return user.is_staff


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def add_vehicle(request):
    """Vista para añadir un nuevo vehículo"""
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.registered_by = request.user
            vehicle.save()
            messages.success(
                request, 
                f'Vehículo {vehicle.license_plate} añadido exitosamente.'
            )
            return redirect('parking:vehicle_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = VehicleForm()
    
    context = {
        'form': form,
        'title': 'Añadir Vehículo',
        'submit_text': 'Guardar Vehículo'
    }
    return render(request, 'parking/vehicle_form.html', context)


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def vehicle_list(request):
    """Vista para listar todos los vehículos"""
    vehicles = Vehicle.objects.select_related('owner', 'registered_by').all()
    
    # Filtros
    search = request.GET.get('search', '')
    vehicle_type = request.GET.get('type', '')
    
    if search:
        vehicles = vehicles.filter(
            Q(license_plate__icontains=search) |
            Q(brand__icontains=search) |
            Q(model__icontains=search) |
            Q(owner__username__icontains=search) |
            Q(owner__first_name__icontains=search) |
            Q(owner__last_name__icontains=search)
        )
    
    if vehicle_type:
        vehicles = vehicles.filter(vehicle_type=vehicle_type)
    
    context = {
        'vehicles': vehicles,
        'title': 'Lista de Vehículos',
        'search': search,
        'vehicle_type': vehicle_type,
        'vehicle_types': VehicleType.choices
    }
    return render(request, 'parking/vehicle_list.html', context)


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def assign_vehicle(request):
    """Vista para asignar un vehículo a un usuario"""
    if request.method == 'POST':
        form = AssignVehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.cleaned_data['vehicle']
            user = form.cleaned_data['user']
            
            # Cambiar el propietario
            old_owner = vehicle.owner
            vehicle.owner = user
            vehicle.save()
            
            old_owner_name = (old_owner.get_full_name() or old_owner.username) if old_owner else "Sin propietario"
            
            messages.success(
                request,
                f'Vehículo {vehicle.license_plate} reasignado de {old_owner_name} a {user.get_full_name() or user.username}.'
            )
            return redirect('parking:vehicle_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = AssignVehicleForm()
    
    # Obtener vehículos asignados para mostrar en la tabla
    assigned_vehicles = Vehicle.objects.filter(owner__isnull=False).select_related('owner').order_by('-updated_at')
    
    context = {
        'form': form,
        'title': 'Asignar Vehículo a Usuario',
        'submit_text': 'Asignar Vehículo',
        'assigned_vehicles': assigned_vehicles
    }
    return render(request, 'parking/assign_vehicle.html', context)


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def normal_reservation(request):
    """Vista para crear reservas normales (usuarios registrados)"""
    if request.method == 'POST':
        form = NormalReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.created_by = request.user
            
            # Asignar el usuario propietario del vehículo a la reserva
            if reservation.vehicle and reservation.vehicle.owner:
                reservation.user = reservation.vehicle.owner
                
            reservation.save()
            
            # CREAR ASIGNACIÓN AUTOMÁTICA (ENTRADA)
            from .models import ParkingAssignment, ParkingSpace
            
            # Crear asignación usando la fecha de reserva como hora de entrada
            assignment = ParkingAssignment(
                vehicle=reservation.vehicle,
                parking_space=reservation.parking_space,
                status=ParkingAssignment.AssignmentStatus.ACTIVE,
                assigned_by=request.user
            )
            # Guardar primero para obtener el ID
            assignment.save()
            # Actualizar entry_time con la fecha de reserva
            ParkingAssignment.objects.filter(id=assignment.id).update(
                entry_time=reservation.reservation_date
            )
            
            # Actualizar estado del espacio
            reservation.parking_space.status = ParkingSpace.SpaceStatus.OCCUPIED
            reservation.parking_space.save()
            
            # Actualizar estado de la reserva
            reservation.status = ParkingReservation.ReservationStatus.CONFIRMED
            reservation.save()
            
            messages.success(
                request,
                f'Reserva y entrada registradas exitosamente para el vehículo {reservation.vehicle.license_plate}.'
            )
            return redirect('parking:reservation_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = NormalReservationForm()
    
    context = {
        'form': form,
        'title': 'Nueva Reserva Normal',
        'submit_text': 'Registrar Entrada',
        'reservation_type': 'normal'
    }
    return render(request, 'parking/reservation_form.html', context)


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def quick_reservation(request):
    """Vista para crear reservas rápidas (sin usuario registrado)"""
    if request.method == 'POST':
        form = QuickReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.is_quick_reservation = True
            reservation.created_by = request.user
            reservation.save()
            
            # CREAR ASIGNACIÓN AUTOMÁTICA (ENTRADA)
            from .models import ParkingAssignment, ParkingSpace, Vehicle
            
            # 1. Buscar o crear vehículo temporal
            vehicle, created = Vehicle.objects.get_or_create(
                license_plate=reservation.vehicle_plate,
                defaults={
                    'vehicle_type': reservation.vehicle_type_temp,
                    'color': 'Desconocido', # Valor por defecto
                    'owner': None # Sin propietario registrado
                }
            )
            
            # Si el vehículo ya existía pero no tenía tipo, actualizarlo
            if not created and not vehicle.vehicle_type:
                vehicle.vehicle_type = reservation.vehicle_type_temp
                vehicle.save()
            
            # 2. Crear asignación usando la fecha de reserva como hora de entrada
            assignment = ParkingAssignment(
                vehicle=vehicle,
                parking_space=reservation.parking_space,
                status=ParkingAssignment.AssignmentStatus.ACTIVE,
                assigned_by=request.user
            )
            # Guardar primero para obtener el ID
            assignment.save()
            # Actualizar entry_time con la fecha de reserva
            ParkingAssignment.objects.filter(id=assignment.id).update(
                entry_time=reservation.reservation_date
            )
            
            # 3. Actualizar estado del espacio
            reservation.parking_space.status = ParkingSpace.SpaceStatus.OCCUPIED
            reservation.parking_space.save()
            
            # 4. Actualizar estado de la reserva
            reservation.status = ParkingReservation.ReservationStatus.CONFIRMED
            reservation.save()
            
            messages.success(
                request,
                f'Entrada rápida registrada exitosamente para {reservation.customer_name or "Cliente"} - Vehículo {reservation.vehicle_plate}.'
            )
            return redirect('parking:reservation_list')
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = QuickReservationForm()
    
    context = {
        'form': form,
        'title': 'Nueva Reserva Rápida',
        'submit_text': 'Registrar Entrada Rápida',
        'reservation_type': 'quick'
    }
    return render(request, 'parking/reservation_form.html', context)


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def reservation_list(request):
    """Vista para listar todas las reservas"""
    # Actualizar duración de reservas activas/pendientes
    now = timezone.now()
    active_reservations = ParkingReservation.objects.filter(
        status__in=[
            ParkingReservation.ReservationStatus.PENDING,
            ParkingReservation.ReservationStatus.CONFIRMED
        ]
    )
    
    for reservation in active_reservations:
        # Calcular minutos transcurridos desde la fecha de reserva hasta ahora
        # Si la fecha de reserva es futura, la duración será 0 o negativa (lo manejamos como 0)
        if reservation.reservation_date <= now:
            delta = now - reservation.reservation_date
            minutes = int(delta.total_seconds() / 60)
            if minutes != reservation.duration_minutes:
                reservation.duration_minutes = minutes
                reservation.save(update_fields=['duration_minutes'])

    reservations = ParkingReservation.objects.select_related(
        'vehicle', 'vehicle__owner', 'parking_space', 'parking_space__floor', 'created_by'
    ).all().order_by('-created_at')
    
    # Filtros
    search = request.GET.get('search', '')
    reservation_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    
    if search:
        reservations = reservations.filter(
            Q(customer_name__icontains=search) |
            Q(customer_phone__icontains=search) |
            Q(vehicle_plate__icontains=search) |
            Q(vehicle__license_plate__icontains=search) |
            Q(vehicle__owner__username__icontains=search)
        )
    
    if reservation_type == 'quick':
        reservations = reservations.filter(is_quick_reservation=True)
    elif reservation_type == 'normal':
        reservations = reservations.filter(is_quick_reservation=False)
    
    if status:
        if status == 'active':
            reservations = reservations.filter(
                status=ParkingReservation.ReservationStatus.CONFIRMED
            )
        elif status == 'pending':
            reservations = reservations.filter(
                status=ParkingReservation.ReservationStatus.PENDING
            )
        elif status == 'completed':
            reservations = reservations.filter(
                status=ParkingReservation.ReservationStatus.COMPLETED
            )
        elif status == 'cancelled':
            reservations = reservations.filter(
                status=ParkingReservation.ReservationStatus.CANCELLED
            )
    
    context = {
        'reservations': reservations,
        'title': 'Lista de Reservas',
        'search': search,
        'reservation_type': reservation_type,
        'status': status,
        'now': timezone.now()
    }
    return render(request, 'parking/reservation_list.html', context)


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def reservation_detail(request, pk):
    """Vista para ver el detalle de una reserva"""
    reservation = get_object_or_404(
        ParkingReservation.objects.select_related(
            'vehicle', 'vehicle__owner', 'parking_space', 
            'parking_space__floor', 'created_by'
        ),
        pk=pk
    )
    
    context = {
        'reservation': reservation,
        'title': f'Detalle de Reserva #{reservation.id}',
        'now': timezone.now()
    }
    return render(request, 'parking/reservation_detail.html', context)


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def cancel_reservation(request, pk):
    """Vista para cancelar una reserva"""
    reservation = get_object_or_404(ParkingReservation, pk=pk)
    
    if request.method == 'POST':
        reservation.status = ParkingReservation.ReservationStatus.CANCELLED
        reservation.save()
        
        messages.success(request, f'Reserva #{reservation.id} cancelada exitosamente.')
        return redirect('parking:reservation_list')
    
    context = {
        'reservation': reservation,
        'title': f'Cancelar Reserva #{reservation.id}'
    }
    return render(request, 'parking/reservation_cancel.html', context)


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def dashboard(request):
    """Dashboard principal del sistema de estacionamiento"""
    from .models import ParkingConfiguration, ParkingFloor
    
    # Obtener configuración activa
    config = ParkingConfiguration.objects.filter(is_active=True).first()
    
    # Estadísticas
    total_spaces = ParkingSpace.objects.filter(is_active=True).count()
    available_spaces = ParkingSpace.objects.filter(
        status=ParkingSpace.SpaceStatus.AVAILABLE,
        is_active=True
    ).count()
    occupied_spaces = ParkingSpace.objects.filter(
        status=ParkingSpace.SpaceStatus.OCCUPIED,
        is_active=True
    ).count()
    reserved_spaces = ParkingSpace.objects.filter(
        status=ParkingSpace.SpaceStatus.RESERVED,
        is_active=True
    ).count()
    
    total_vehicles = Vehicle.objects.filter(is_active=True).count()
    
    now = timezone.now()
    active_reservations = ParkingReservation.objects.filter(
        reservation_date__lte=now,
        status__in=[
            ParkingReservation.ReservationStatus.PENDING,
            ParkingReservation.ReservationStatus.CONFIRMED
        ]
    ).count()
    
    pending_reservations = ParkingReservation.objects.filter(
        reservation_date__gt=now,
        status=ParkingReservation.ReservationStatus.PENDING
    ).count()
    
    # Reservas recientes
    recent_reservations = ParkingReservation.objects.select_related(
        'vehicle', 'vehicle__owner', 'parking_space', 'created_by'
    ).exclude(
        status=ParkingReservation.ReservationStatus.CANCELLED
    ).order_by('-created_at')[:5]
    
    context = {
        'title': 'Dashboard - Sistema de Estacionamiento',
        'config': config,
        'total_spaces': total_spaces,
        'available_spaces': available_spaces,
        'occupied_spaces': occupied_spaces,
        'reserved_spaces': reserved_spaces,
        'total_vehicles': total_vehicles,
        'active_reservations': active_reservations,
        'pending_reservations': pending_reservations,
        'recent_reservations': recent_reservations,
        'occupancy_percentage': (occupied_spaces / total_spaces * 100) if total_spaces > 0 else 0,
    }
    return render(request, 'parking/dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser or (u.groups.filter(name='admin').exists()), login_url='user:login')
def space_configuration(request):
    """Vista para configurar los espacios del estacionamiento"""
    # Obtener configuración actual para pre-llenar (si existe)
    current_config = ParkingConfiguration.objects.filter(is_active=True).first()
    
    if request.method == 'POST':
        # Creamos una nueva instancia siempre, no editamos la anterior
        form = ParkingConfigurationForm(request.POST)
        if form.is_valid():
            # 1. Desactivar espacios y pisos antiguos
            ParkingSpace.objects.filter(is_active=True).update(is_active=False)
            ParkingFloor.objects.filter(is_active=True).update(is_active=False)
            
            # 2. Guardar nueva configuración
            new_config = form.save(commit=False)
            new_config.created_by = request.user
            new_config.is_active = True
            new_config.save() # Esto desactivará la configuración anterior automáticamente y disparará los signals para crear pisos/espacios
            
            # Nota: La creación de pisos y espacios se maneja automáticamente mediante signals
            # en parking/signals.py (create_parking_structure y create_floor_spaces)
            
            total_spaces = new_config.total_floors * new_config.spaces_per_floor
            
            messages.success(
                request, 
                f'Configuración actualizada. Se generaron {new_config.total_floors} pisos y {total_spaces} espacios nuevos.'
            )
            return redirect('parking:space_configuration')
    else:
        # Pre-llenar formulario con valores actuales pero sin vincular a la instancia
        initial_data = {}
        if current_config:
            initial_data = {
                'total_floors': current_config.total_floors,
                'spaces_per_floor': current_config.spaces_per_floor
            }
        form = ParkingConfigurationForm(initial=initial_data)
    
    context = {
        'form': form,
        'title': 'Configuración de Espacios',
        'submit_text': 'Actualizar Configuración'
    }
    return render(request, 'parking/space_configuration.html', context)


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def assignment_list(request):
    """Vista para listar todas las asignaciones de estacionamiento"""
    assignments = ParkingAssignment.objects.select_related(
        'vehicle', 'parking_space', 'parking_space__floor', 'assigned_by', 'completed_by'
    ).all().order_by('-entry_time')
    
    # Filtros
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    if search:
        assignments = assignments.filter(
            Q(vehicle__license_plate__icontains=search) |
            Q(parking_space__space_number__icontains=search) |
            Q(receipt_number__icontains=search)
        )
    
    if status == 'active':
        assignments = assignments.filter(status=ParkingAssignment.AssignmentStatus.ACTIVE)
    elif status == 'completed':
        assignments = assignments.filter(status=ParkingAssignment.AssignmentStatus.COMPLETED)
    
    context = {
        'assignments': assignments,
        'title': 'Gestión de Asignaciones',
        'search': search,
        'status': status,
        'now': timezone.now()
    }
    return render(request, 'parking/assignment_list.html', context)


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def checkout(request, pk):
    """Vista para registrar la salida de un vehículo y procesar el pago"""
    assignment = get_object_or_404(
        ParkingAssignment.objects.select_related('vehicle', 'parking_space', 'parking_space__floor'),
        pk=pk
    )
    
    # Verificar que la asignación esté activa
    if assignment.status != ParkingAssignment.AssignmentStatus.ACTIVE:
        messages.error(request, 'Esta asignación ya fue completada o cancelada.')
        return redirect('parking:assignment_list')
    
    # Calcular el costo actual
    now = timezone.now()
    duration = now - assignment.entry_time
    total_minutes = duration.total_seconds() / 60
    hours_parked = math.ceil(total_minutes / 60)
    
    # Obtener tarifa
    try:
        tariff = VehicleTariff.objects.get(
            vehicle_type=assignment.vehicle.vehicle_type,
            is_active=True
        )
    except VehicleTariff.DoesNotExist:
        messages.error(request, f'No se encontró tarifa para el tipo de vehículo {assignment.vehicle.get_vehicle_type_display()}.')
        return redirect('parking:assignment_list')
    
    from decimal import Decimal
    total_cost = Decimal(str(hours_parked)) * tariff.rate_per_hour
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST, instance=assignment)
        if form.is_valid():
            # Completar asignación
            payment_method = form.cleaned_data['payment_method']
            assignment.complete_assignment(
                completed_by=request.user,
                payment_method=payment_method
            )
            
            messages.success(
                request,
                f'Salida registrada exitosamente. Total: S/ {assignment.total_cost:.2f}. Boleta: {assignment.receipt_number}'
            )
            return redirect('parking:print_receipt', pk=assignment.id)
        else:
            messages.error(request, 'Por favor corrija los errores del formulario.')
    else:
        form = CheckoutForm(instance=assignment)
    
    context = {
        'form': form,
        'assignment': assignment,
        'title': f'Salida - {assignment.vehicle.license_plate}',
        'now': now,
        'hours_parked': hours_parked,
        'tariff': tariff,
        'total_cost': total_cost
    }
    return render(request, 'parking/checkout.html', context)


@login_required
@user_passes_test(is_admin_or_worker, login_url='user:login')
def print_receipt(request, pk):
    """Vista para imprimir/visualizar la boleta de pago"""
    assignment = get_object_or_404(
        ParkingAssignment.objects.select_related('vehicle', 'parking_space', 'parking_space__floor', 'completed_by'),
        pk=pk
    )
    
    if not assignment.receipt_number:
        messages.error(request, 'Esta asignación no tiene boleta generada.')
        return redirect('parking:assignment_list')
    
    # Calcular horas
    if assignment.exit_time and assignment.entry_time:
        duration = assignment.exit_time - assignment.entry_time
        total_minutes = duration.total_seconds() / 60
        hours_parked = math.ceil(total_minutes / 60)
    else:
        hours_parked = 0
    
    # Obtener tarifa
    try:
        tariff = VehicleTariff.objects.get(
            vehicle_type=assignment.vehicle.vehicle_type,
            is_active=True
        )
        tariff_amount = f"{tariff.rate_per_hour:.2f}"
    except VehicleTariff.DoesNotExist:
        tariff_amount = "0.00"
    
    context = {
        'assignment': assignment,
        'hours_parked': hours_parked,
        'tariff_amount': tariff_amount,
        'now': timezone.now()
    }
    return render(request, 'parking/receipt.html', context)
