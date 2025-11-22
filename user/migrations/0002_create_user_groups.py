# Generated migration for creating user groups/roles

from django.db import migrations


def create_user_groups(apps, schema_editor):
    """
    Crear los grupos (roles) del sistema:
    - administrador: Acceso completo al sistema
    - trabajador: Personal operativo del estacionamiento
    - usuario: Clientes que usan el estacionamiento
    """
    Group = apps.get_model('auth', 'Group')
    
    # Crear los tres grupos
    grupos = [
        ('administrador', 'Acceso completo al sistema'),
        ('trabajador', 'Personal operativo del estacionamiento'),
        ('usuario', 'Clientes que usan el estacionamiento')
    ]
    
    for group_name, description in grupos:
        Group.objects.create(name=group_name)
        print(f"Grupo '{group_name}' creado")


def reverse_create_groups(apps, schema_editor):
    """
    Eliminar los grupos creados (para rollback)
    """
    Group = apps.get_model('auth', 'Group')
    
    grupos = ['administrador', 'trabajador', 'usuario']
    
    for group_name in grupos:
        Group.objects.filter(name=group_name).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_user_groups, reverse_create_groups),
    ]
