from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Configura los roles del sistema: admin, usuario y trabajador'

    def handle(self, *args, **kwargs):
        # Definir los roles permitidos
        roles_permitidos = ['admin', 'usuario', 'trabajador']
        
        # Eliminar todos los grupos existentes
        grupos_eliminados = Group.objects.exclude(name__in=roles_permitidos).count()
        Group.objects.exclude(name__in=roles_permitidos).delete()
        
        self.stdout.write(
            self.style.WARNING(f'Se eliminaron {grupos_eliminados} roles/grupos no permitidos')
        )
        
        # Crear los tres roles si no existen
        roles_creados = 0
        for rol_nombre in roles_permitidos:
            grupo, created = Group.objects.get_or_create(name=rol_nombre)
            if created:
                roles_creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Rol "{rol_nombre}" creado')
                )
            else:
                self.stdout.write(
                    self.style.NOTICE(f'Rol "{rol_nombre}" ya existe')
                )
        
        # Mostrar resumen
        total_roles = Group.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'\nConfiguración completada!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total de roles en el sistema: {total_roles}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Roles activos: {", ".join(roles_permitidos)}')
        )
