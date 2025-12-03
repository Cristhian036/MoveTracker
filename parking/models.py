from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import User


class VehicleType(models.TextChoices):
    # Tipos de vehiculos soportados
    CAR = 'CAR', 'Auto'
    TRUCK = 'TRUCK', 'Camioneta'
    MOTORCYCLE = 'MOTORCYCLE', 'Moto'


class ParkingConfiguration(models.Model):
    # Configuracion dinamica del estacionamiento
    total_floors = models.PositiveIntegerField(
        verbose_name='Total de Pisos',
        validators=[MinValueValidator(1)],
        help_text='Número total de pisos en el estacionamiento'
    )
    spaces_per_floor = models.PositiveIntegerField(
        verbose_name='Espacios por Piso',
        validators=[MinValueValidator(1)],
        help_text='Cantidad de espacios de estacionamiento por piso'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Configuración Activa',
        help_text='Solo puede haber una configuración activa'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='parking_configurations',
        verbose_name='Creado por'
    )

    class Meta:
        verbose_name = 'Configuración de Estacionamiento'
        verbose_name_plural = 'Configuraciones de Estacionamiento'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.total_floors} pisos - {self.spaces_per_floor} espacios/piso"

    def save(self, *args, **kwargs):
        # Asegura que solo haya una configuracion activa
        if self.is_active:
            ParkingConfiguration.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    @property
    def total_capacity(self):
        # Capacidad total del estacionamiento
        return self.total_floors * self.spaces_per_floor


class VehicleTariff(models.Model):
    # Tarifas por tipo de vehiculo
    vehicle_type = models.CharField(
        max_length=20,
        choices=VehicleType.choices,
        unique=True,
        verbose_name='Tipo de Vehículo'
    )
    rate_per_hour = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Tarifa por Hora (S/)',
        help_text='Costo por hora de estacionamiento en Soles'
    )
    custom_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Nombre Personalizado',
        help_text='Nombre para mostrar en lugar del tipo por defecto (ej: "Sedan" en vez de "Auto")'
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Descripción',
        help_text='Nombre personalizado para mostrar en la tarifa (opcional)'
    )
    is_active = models.BooleanField(default=True, verbose_name='Tarifa Activa')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        verbose_name = 'Tarifa de Vehículo'
        verbose_name_plural = 'Tarifas de Vehículos'
        ordering = ['vehicle_type']

    def __str__(self):
        return f"{self.get_vehicle_type_display()} - ${self.rate_per_hour}/hora"


class Vehicle(models.Model):
    # Vehiculos registrados en el sistema
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vehicles',
        verbose_name='Propietario',
        null=True,
        blank=True
    )
    vehicle_type = models.CharField(
        max_length=20,
        choices=VehicleType.choices,
        verbose_name='Tipo de Vehículo'
    )
    brand = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Marca',
        help_text='Marca del vehículo (opcional)'
    )
    model = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Modelo',
        help_text='Modelo del vehículo (opcional)'
    )
    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Año',
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        help_text='Año de fabricación (opcional)'
    )
    color = models.CharField(max_length=30, verbose_name='Color')
    license_plate = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Placa',
        help_text='Número de placa del vehículo'
    )
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    registered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='registered_vehicles',
        verbose_name='Registrado por'
    )

    class Meta:
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['license_plate']),
            models.Index(fields=['owner', 'is_active']),
        ]

    def __str__(self):
        return f"{self.license_plate} - {self.brand} {self.model} ({self.get_vehicle_type_display()})"

    @property
    def full_description(self):
        # Descripcion completa del vehiculo
        return f"{self.year} {self.brand} {self.model} {self.color}"


class ParkingFloor(models.Model):
    # Representa un piso del estacionamiento
    configuration = models.ForeignKey(
        ParkingConfiguration,
        on_delete=models.CASCADE,
        related_name='floors',
        verbose_name='Configuración'
    )
    floor_number = models.PositiveIntegerField(
        verbose_name='Número de Piso',
        validators=[MinValueValidator(1)]
    )
    floor_name = models.CharField(
        max_length=50,
        verbose_name='Nombre del Piso',
        blank=True,
        help_text='Ej: Piso 1, Sótano 1, etc.'
    )
    is_active = models.BooleanField(default=True, verbose_name='Piso Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')

    class Meta:
        verbose_name = 'Piso de Estacionamiento'
        verbose_name_plural = 'Pisos de Estacionamiento'
        ordering = ['floor_number']
        unique_together = [['configuration', 'floor_number']]

    def __str__(self):
        return self.floor_name or f"Piso {self.floor_number}"

    def save(self, *args, **kwargs):
        if not self.floor_name:
            self.floor_name = f"Piso {self.floor_number}"
        super().save(*args, **kwargs)


class ParkingSpace(models.Model):
    # Representa un espacio individual de estacionamiento
    class SpaceStatus(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Disponible'
        OCCUPIED = 'OCCUPIED', 'Ocupado'
        RESERVED = 'RESERVED', 'Reservado'
        MAINTENANCE = 'MAINTENANCE', 'En Mantenimiento'

    floor = models.ForeignKey(
        ParkingFloor,
        on_delete=models.CASCADE,
        related_name='spaces',
        verbose_name='Piso'
    )
    space_number = models.PositiveIntegerField(
        verbose_name='Número de Espacio',
        validators=[MinValueValidator(1)]
    )
    status = models.CharField(
        max_length=20,
        choices=SpaceStatus.choices,
        default=SpaceStatus.AVAILABLE,
        verbose_name='Estado'
    )
    is_active = models.BooleanField(default=True, verbose_name='Espacio Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        verbose_name = 'Espacio de Estacionamiento'
        verbose_name_plural = 'Espacios de Estacionamiento'
        ordering = ['floor__floor_number', 'space_number']
        unique_together = [['floor', 'space_number']]
        indexes = [
            models.Index(fields=['status', 'is_active']),
        ]

    def __str__(self):
        return f"{self.floor.floor_name} - Espacio {self.space_number}"

    @property
    def full_code(self):
        # Codigo completo del espacio
        return f"P{self.floor.floor_number}-{str(self.space_number).zfill(3)}"


class ParkingAssignment(models.Model):
    # Asignacion de un vehiculo a un espacio
    class AssignmentStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Activo'
        COMPLETED = 'COMPLETED', 'Completado'
        CANCELLED = 'CANCELLED', 'Cancelado'

    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Efectivo'
        CARD = 'CARD', 'Tarjeta'
        YAPE = 'YAPE', 'Yape'
        PLIN = 'PLIN', 'Plin'

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='parking_assignments',
        verbose_name='Vehículo'
    )
    parking_space = models.ForeignKey(
        ParkingSpace,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='Espacio de Estacionamiento'
    )
    status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.ACTIVE,
        verbose_name='Estado'
    )
    entry_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Hora de Entrada'
    )
    exit_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Hora de Salida'
    )
    planned_exit_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Hora de Salida Planificada',
        help_text='Hora estimada de salida'
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Costo Total'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        null=True,
        blank=True,
        verbose_name='Método de Pago'
    )
    receipt_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        unique=True,
        verbose_name='Número de Boleta'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='parking_assignments_created',
        verbose_name='Asignado por'
    )
    completed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parking_assignments_completed',
        verbose_name='Completado por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        verbose_name = 'Asignación de Estacionamiento'
        verbose_name_plural = 'Asignaciones de Estacionamiento'
        ordering = ['-entry_time']
        indexes = [
            models.Index(fields=['status', 'entry_time']),
            models.Index(fields=['vehicle', 'status']),
        ]

    def __str__(self):
        return f"{self.vehicle.license_plate} en {self.parking_space.full_code}"

    def calculate_cost(self):
        # Calcula el costo segun el tiempo de estacionamiento
        if not self.exit_time:
            return None
        
        from decimal import Decimal
        import math
        
        duration = self.exit_time - self.entry_time
        total_minutes = duration.total_seconds() / 60
        
        # Redondear hacia arriba cada hora (fracción se cobra como hora completa)
        hours = math.ceil(total_minutes / 60)
        
        try:
            tariff = VehicleTariff.objects.get(
                vehicle_type=self.vehicle.vehicle_type,
                is_active=True
            )
            
            # Calcular costo basado en horas completas
            return Decimal(str(hours)) * tariff.rate_per_hour
        except VehicleTariff.DoesNotExist:
            return None

    def generate_receipt_number(self):
        # Genera un numero unico de boleta
        from django.utils import timezone
        import random
        
        # Formato: B-YYYYMMDD-XXXXX (B de Boleta)
        now = timezone.now()
        date_part = now.strftime('%Y%m%d')
        random_part = str(random.randint(10000, 99999))
        
        receipt_num = f"B-{date_part}-{random_part}"
        
        # Verificar que no exista
        while ParkingAssignment.objects.filter(receipt_number=receipt_num).exists():
            random_part = str(random.randint(10000, 99999))
            receipt_num = f"B-{date_part}-{random_part}"
        
        return receipt_num
    
    def complete_assignment(self, completed_by=None, payment_method=None):
        # Marca la asignacion como completada y genera boleta
        from django.utils import timezone
        
        self.exit_time = timezone.now()
        self.status = self.AssignmentStatus.COMPLETED
        self.total_cost = self.calculate_cost()
        self.completed_by = completed_by
        self.payment_method = payment_method or self.PaymentMethod.CASH
        
        # Generar número de boleta
        if not self.receipt_number:
            self.receipt_number = self.generate_receipt_number()
        
        # Liberar el espacio
        self.parking_space.status = ParkingSpace.SpaceStatus.AVAILABLE
        self.parking_space.save()
        
        self.save()


class ParkingReservation(models.Model):
    # Reservas de espacios de estacionamiento
    class ReservationStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        CONFIRMED = 'CONFIRMED', 'Confirmado'
        CANCELLED = 'CANCELLED', 'Cancelado'
        COMPLETED = 'COMPLETED', 'Completado'

    # Usuario registrado (opcional para reservas rápidas)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='parking_reservations',
        verbose_name='Usuario',
        null=True,
        blank=True,
        help_text='Usuario registrado. Dejar en blanco para reserva rápida/manual'
    )
    
    # Vehículo registrado (opcional para reservas rápidas)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Vehículo',
        null=True,
        blank=True,
        help_text='Vehículo registrado. Dejar en blanco para reserva rápida/manual'
    )
    
    # Datos para reserva rápida/manual (cuando no hay usuario/vehículo registrado)
    customer_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Nombre del Cliente',
        help_text='Para reservas rápidas sin usuario registrado'
    )
    customer_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono del Cliente',
        help_text='Para reservas rápidas sin usuario registrado'
    )
    customer_email = models.EmailField(
        blank=True,
        verbose_name='Email del Cliente',
        help_text='Para reservas rápidas sin usuario registrado'
    )
    vehicle_plate = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Placa del Vehículo',
        help_text='Para reservas rápidas sin vehículo registrado'
    )
    vehicle_type_temp = models.CharField(
        max_length=20,
        choices=VehicleType.choices,
        blank=True,
        verbose_name='Tipo de Vehículo (Temporal)',
        help_text='Para reservas rápidas sin vehículo registrado'
    )
    
    # Espacio asignado
    parking_space = models.ForeignKey(
        ParkingSpace,
        on_delete=models.CASCADE,
        related_name='reservations',
        null=True,
        blank=True,
        verbose_name='Espacio Asignado'
    )
    
    # Estado y fechas
    status = models.CharField(
        max_length=20,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING,
        verbose_name='Estado'
    )
    reservation_date = models.DateTimeField(
        verbose_name='Fecha de Reserva',
        help_text='Fecha y hora para la cual se reserva'
    )
    duration_minutes = models.PositiveIntegerField(
        verbose_name='Duración (minutos)',
        validators=[MinValueValidator(1)],
        default=60,
        help_text='Duración de la reserva en minutos'
    )
    
    # Información adicional
    is_quick_reservation = models.BooleanField(
        default=False,
        verbose_name='Reserva Rápida',
        help_text='Indica si es una reserva rápida/manual sin usuario registrado'
    )
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservations_created',
        verbose_name='Creado por',
        help_text='Trabajador o admin que creó la reserva'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        verbose_name = 'Reserva de Estacionamiento'
        verbose_name_plural = 'Reservas de Estacionamiento'
        ordering = ['-reservation_date']
        indexes = [
            models.Index(fields=['status', 'reservation_date']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['is_quick_reservation', 'status']),
        ]

    def __str__(self):
        if self.is_quick_reservation:
            identifier = self.customer_name or self.vehicle_plate or f"Reserva #{self.pk}"
            return f"Reserva Rápida: {identifier} - {self.reservation_date}"
        else:
            user_name = self.user.username if self.user else "Sin usuario"
            return f"Reserva {user_name} - {self.reservation_date}"
    
    def clean(self):
        # Validacion: debe tener usuario/vehiculo O datos de reserva rapida
        from django.core.exceptions import ValidationError
        
        # Si no es reserva rápida, debe tener usuario y vehículo
        if not self.is_quick_reservation:
            # Si tiene vehículo pero no usuario, intentamos obtener el dueño del vehículo
            if self.vehicle and not self.user:
                if self.vehicle.owner:
                    self.user = self.vehicle.owner
                else:
                    # Si el vehículo no tiene dueño, permitimos la reserva pero advertimos o manejamos
                    # En este caso, permitimos que se guarde sin usuario si hay vehículo
                    pass

            if not self.vehicle:
                 raise ValidationError(
                    'Para reservas normales se requiere un vehículo registrado. '
                    'Marque como "Reserva Rápida" si desea crear una reserva manual.'
                )
        else:
            # Si es reserva rápida, debe tener al menos nombre o placa
            if not self.customer_name and not self.vehicle_plate:
                raise ValidationError(
                    'Para reservas rápidas debe proporcionar al menos el nombre del cliente '
                    'o la placa del vehículo.'
                )
    
    def save(self, *args, **kwargs):
        # Auto-detectar si es reserva rapida
        # Si no tiene usuario ni vehículo, marcar como reserva rápida
        if not self.user and not self.vehicle:
            self.is_quick_reservation = True
            
        # Si es reserva normal y tiene vehículo pero no usuario, asignar el dueño del vehículo
        if not self.is_quick_reservation and self.vehicle and not self.user:
            self.user = self.vehicle.owner
        
        # Validar antes de guardar
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def customer_info(self):
        # Retorna informacion del cliente
        if self.is_quick_reservation:
            info = []
            if self.customer_name:
                info.append(f"Nombre: {self.customer_name}")
            if self.customer_phone:
                info.append(f"Tel: {self.customer_phone}")
            if self.customer_email:
                info.append(f"Email: {self.customer_email}")
            return " | ".join(info) if info else "Sin información de cliente"
        else:
            if self.user:
                return f"{self.user.get_full_name() or self.user.username} ({self.user.email})"
            return "Sin usuario"
    
    @property
    def vehicle_info(self):
        # Retorna informacion del vehiculo
        if self.is_quick_reservation:
            parts = []
            if self.vehicle_plate:
                parts.append(f"Placa: {self.vehicle_plate}")
            if self.vehicle_type_temp:
                parts.append(f"Tipo: {self.get_vehicle_type_temp_display()}")
            return " | ".join(parts) if parts else "Sin información de vehículo"
        else:
            if self.vehicle:
                return f"{self.vehicle.license_plate} - {self.vehicle.full_description}"
            return "Sin vehículo"
    
    @property
    def duration_formatted(self):
        # Retorna la duracion en formato Xh Ym
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
