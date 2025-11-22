from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuario personalizado que extiende AbstractUser
    Añade campos adicionales: dni y phone
    """
    dni = models.CharField(max_length=10, blank=True, null=True, verbose_name='DNI')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'auth_user'
    
    def __str__(self):
        return self.username
