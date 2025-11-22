import os
import sys
import django

# Agregar el directorio raíz del proyecto al path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from user.forms import UserRegisterForm
from user.models import User

# Simular datos de registro
form_data = {
    'username': 'test_user_dni',
    'email': 'test@example.com',
    'first_name': 'Juan',
    'last_name': 'Pérez',
    'dni': '12345678',
    'phone': '987654321',
    'password1': 'TestPassword123!',
    'password2': 'TestPassword123!',
}


# Limpiar usuarios de prueba anteriores
User.objects.filter(username='test_user_dni').delete()
print("Usuarios de prueba anteriores eliminados\n")

print(f"Datos de prueba:")
for key, value in form_data.items():
    if 'password' not in key:
        print(f"  {key:12} : {value}")

form = UserRegisterForm(data=form_data)

print(f"\nCampos del formulario:")
print(f"  {', '.join(form.fields.keys())}")
print(f"\n¿Formulario válido?: {form.is_valid()}")

if form.is_valid():
    user = form.save()
    
    print(f"\n{'=' * 70}")
    print("USUARIO CREADO EXITOSAMENTE")
    print("=" * 70)
    print(f"  Username  : {user.username}")
    print(f"  Email     : {user.email}")
    print(f"  Nombre    : {user.first_name}")
    print(f"  Apellido  : {user.last_name}")
    print(f"  DNI       : {user.dni}")
    print(f"  Teléfono  : {user.phone}")
   
    # Limpiar - eliminar el usuario de prueba
    user.delete()
    print("\nUsuario de prueba eliminado correctamente")
else:
    print(f"\nErrores del formulario:")
    for field, errors in form.errors.items():
        print(f"   {field}: {errors}")


