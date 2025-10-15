from django import forms
from django.contrib.auth import get_user_model
from .models import Vehicle, ParkingReservation, VehicleType

User = get_user_model()


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
                'placeholder': 'Toyota, Honda, etc.'
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Corolla, Civic, etc.'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2020',
                'min': 1900,
                'max': 2100
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
            'brand': 'Marca',
            'model': 'Modelo',
            'year': 'Año',
            'color': 'Color',
            'owner': 'Propietario',
        }
        help_texts = {
            'license_plate': 'Ingrese la placa en formato válido (ej: ABC-123)',
            'owner': 'Seleccione el usuario propietario del vehículo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo usuarios activos
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
        # Mostrar solo vehículos con propietario
        self.fields['vehicle'].queryset = Vehicle.objects.select_related('owner').all()
        self.fields['vehicle'].label_from_instance = lambda obj: f"{obj.license_plate} - {obj.get_vehicle_type_display()} ({obj.owner.get_full_name() or obj.owner.username})"


class NormalReservationForm(forms.ModelForm):
    """Formulario para reservas normales (usuarios registrados)"""
    
    class Meta:
        model = ParkingReservation
        fields = ['vehicle', 'parking_space', 'reservation_date', 'duration_hours', 'notes']
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
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1',
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
            'duration_hours': 'Duración (horas)',
            'notes': 'Notas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar vehículos registrados
        self.fields['vehicle'].queryset = Vehicle.objects.select_related('owner').all()
        self.fields['vehicle'].label_from_instance = lambda obj: f"{obj.license_plate} - {obj.get_vehicle_type_display()}"
        
        # Solo mostrar espacios disponibles
        from .models import ParkingSpace
        self.fields['parking_space'].queryset = ParkingSpace.objects.filter(
            is_available=True
        ).select_related('floor')
        self.fields['parking_space'].label_from_instance = lambda obj: f"Piso {obj.floor.floor_number} - Espacio {obj.space_number}"


class QuickReservationForm(forms.ModelForm):
    """Formulario para reservas rápidas (sin usuario registrado)"""
    
    class Meta:
        model = ParkingReservation
        fields = [
            'customer_name', 'customer_phone', 'customer_email',
            'vehicle_plate', 'vehicle_type_temp',
            'parking_space', 'reservation_date', 'duration_hours', 'notes'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cliente',
                'required': True
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+51 999 999 999',
                'required': True
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'cliente@ejemplo.com'
            }),
            'vehicle_plate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-123',
                'required': True
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
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales (opcional)'
            }),
        }
        labels = {
            'customer_name': 'Nombre del Cliente',
            'customer_phone': 'Teléfono',
            'customer_email': 'Email',
            'vehicle_plate': 'Placa del Vehículo',
            'vehicle_type_temp': 'Tipo de Vehículo',
            'parking_space': 'Espacio de Estacionamiento',
            'reservation_date': 'Fecha/Hora de Reserva',
            'duration_hours': 'Duración (horas)',
            'notes': 'Notas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar espacios disponibles
        from .models import ParkingSpace
        self.fields['parking_space'].queryset = ParkingSpace.objects.filter(
            is_available=True
        ).select_related('floor')
        self.fields['parking_space'].label_from_instance = lambda obj: f"Piso {obj.floor.floor_number} - Espacio {obj.space_number}"
