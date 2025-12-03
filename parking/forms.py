from django import forms
from django.contrib.auth import get_user_model
from .models import Vehicle, ParkingReservation, VehicleType, ParkingConfiguration, ParkingAssignment

User = get_user_model()


class ParkingConfigurationForm(forms.ModelForm):
    """Formulario para configurar el estacionamiento"""
    class Meta:
        model = ParkingConfiguration
        fields = ['total_floors', 'spaces_per_floor']
        widgets = {
            'total_floors': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Ej: 3'
            }),
            'spaces_per_floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Ej: 20'
            }),
        }
        labels = {
            'total_floors': 'Número de Pisos',
            'spaces_per_floor': 'Espacios por Piso',
        }
        help_texts = {
            'total_floors': 'Cantidad total de niveles del estacionamiento',
            'spaces_per_floor': 'Cantidad de espacios disponibles en cada nivel',
        }


class VehicleForm(forms.ModelForm):
    """Formulario para añadir vehículos"""
    
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'vehicle_type', 'brand', 'model', 'year', 'color', 'owner']
        widgets = {
            'license_plate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-123',
                'required': True
            }),
            'vehicle_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Toyota, Honda, etc. (opcional)',
                'required': False
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Corolla, Civic, etc. (opcional)',
                'required': False
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2020 (opcional)',
                'min': 1900,
                'max': 2100,
                'required': False
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rojo, Azul, etc.'
            }),
            'owner': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }
        labels = {
            'license_plate': 'Placa del Vehículo',
            'vehicle_type': 'Tipo de Vehículo',
            'brand': 'Marca (opcional)',
            'model': 'Modelo (opcional)',
            'year': 'Año (opcional)',
            'color': 'Color',
            'owner': 'Propietario',
        }
        help_texts = {
            'license_plate': 'Ingrese la placa en formato válido (ej: ABC-123)',
            'brand': 'Marca del vehículo (campo opcional)',
            'model': 'Modelo del vehículo (campo opcional)',
            'year': 'Año de fabricación (campo opcional)',
            'owner': 'Seleccione el usuario propietario del vehículo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar usuarios activos
        self.fields['owner'].queryset = User.objects.filter(is_active=True)


class AssignVehicleForm(forms.Form):
    """Formulario para asignar un vehículo existente a un usuario"""
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        label='Vehículo',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        help_text='Seleccione el vehículo a asignar'
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        label='Usuario',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        help_text='Seleccione el usuario al que se asignará el vehículo'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar vehiculos con propietario
        self.fields['vehicle'].queryset = Vehicle.objects.select_related('owner').all()
        self.fields['vehicle'].label_from_instance = lambda obj: f"{obj.license_plate} - {obj.get_vehicle_type_display()} ({obj.owner.get_full_name() if obj.owner else 'Sin propietario'})"


class NormalReservationForm(forms.ModelForm):
    """Formulario para reservas normales (usuarios registrados)"""
    
    class Meta:
        model = ParkingReservation
        fields = ['vehicle', 'parking_space', 'reservation_date', 'notes']
        widgets = {
            'vehicle': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'parking_space': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'reservation_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales (opcional)'
            }),
        }
        labels = {
            'vehicle': 'Vehículo',
            'parking_space': 'Espacio de Estacionamiento',
            'reservation_date': 'Fecha/Hora de Reserva',
            'notes': 'Notas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar vehiculos registrados
        self.fields['vehicle'].queryset = Vehicle.objects.select_related('owner').all()
        self.fields['vehicle'].label_from_instance = lambda obj: f"{obj.license_plate} - {obj.get_vehicle_type_display()}"
        
        # Mostrar espacios disponibles
        from .models import ParkingSpace
        self.fields['parking_space'].queryset = ParkingSpace.objects.filter(
            status=ParkingSpace.SpaceStatus.AVAILABLE,
            is_active=True
        ).select_related('floor')
        self.fields['parking_space'].label_from_instance = lambda obj: f"Piso {obj.floor.floor_number} - Espacio {obj.space_number}"


class QuickReservationForm(forms.ModelForm):
    """Formulario para reservas rápidas (sin usuario registrado)"""
    
    class Meta:
        model = ParkingReservation
        fields = [
            'customer_name', 'customer_phone', 'customer_email',
            'vehicle_plate', 'vehicle_type_temp',
            'parking_space', 'reservation_date', 'notes'
        ]
        widgets = {
            'customer_name': forms.HiddenInput(),
            'customer_phone': forms.HiddenInput(),
            'customer_email': forms.HiddenInput(),
            'vehicle_plate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-123'
            }),
            'vehicle_type_temp': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'parking_space': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'reservation_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales (opcional)'
            }),
        }
        labels = {
            'vehicle_plate': 'Placa del Vehículo',
            'vehicle_type_temp': 'Tipo de Vehículo',
            'parking_space': 'Espacio de Estacionamiento',
            'reservation_date': 'Fecha/Hora de Reserva',
            'notes': 'Notas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar como reserva rapida
        self.instance.is_quick_reservation = True
        
        # Campos obligatorios
        self.fields['vehicle_type_temp'].required = True
        self.fields['parking_space'].required = True
        self.fields['reservation_date'].required = True
        
        # Campos opcionales
        self.fields['customer_name'].required = False
        self.fields['customer_phone'].required = False
        self.fields['customer_email'].required = False
        self.fields['vehicle_plate'].required = False
        self.fields['notes'].required = False

        # Mostrar espacios disponibles
        from .models import ParkingSpace
        self.fields['parking_space'].queryset = ParkingSpace.objects.filter(
            status=ParkingSpace.SpaceStatus.AVAILABLE,
            is_active=True
        ).select_related('floor')
        self.fields['parking_space'].label_from_instance = lambda obj: f"Piso {obj.floor.floor_number} - Espacio {obj.space_number}"


class CheckoutForm(forms.ModelForm):
    """Formulario para registrar la salida y pago de un vehículo"""
    
    class Meta:
        model = ParkingAssignment
        fields = ['payment_method', 'notes']
        widgets = {
            'payment_method': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            }),
        }
        labels = {
            'payment_method': 'Método de Pago',
            'notes': 'Observaciones',
        }
        help_texts = {
            'notes': 'Información adicional sobre el pago o la salida'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].required = True
        self.fields['notes'].required = False
