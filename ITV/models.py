from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Usuario (AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    TRABAJADOR = 3
    ROLES = (
        (ADMINISTRADOR,"administrador"),
        (CLIENTE,"cliente"),
        (TRABAJADOR,"trabajador")
    )
    rol = models.PositiveBigIntegerField(choices=ROLES,default=1)

