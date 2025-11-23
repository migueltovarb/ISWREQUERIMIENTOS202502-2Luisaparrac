from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta


class UsuarioManager(BaseUserManager):
    """Manager para manejar usuarios usando email como identificador."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):

    nombre_completo = models.CharField(max_length=150, blank=True)

    username = models.CharField(
        max_length=150,
        unique=False,
        blank=True,
        null=True,
        help_text="Ignorado, usamos email para login."
    )

    email = models.EmailField(unique=True)

    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        JEFE = 'JEFE', 'Jefe de proyecto'
        USUARIO = 'USUARIO', 'Usuario'

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.USUARIO)

    intentos_fallidos = models.PositiveIntegerField(default=0)
    bloqueado_hasta = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    def esta_bloqueado(self):
        if not self.bloqueado_hasta:
            return False
        return timezone.now() < self.bloqueado_hasta

    def registrar_fallo_login(self, limite=5, minutos_bloqueo=15):
        self.intentos_fallidos += 1
        if self.intentos_fallidos >= limite:
            self.bloqueado_hasta = timezone.now() + timedelta(minutes=minutos_bloqueo)
        self.save()

    def resetear_intentos(self):
        self.intentos_fallidos = 0
        self.bloqueado_hasta = None
        self.save()