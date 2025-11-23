from django.db import models
from usuarios.models import Usuario

class Proyecto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    jefe = models.ForeignKey(
        'usuarios.Usuario',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='proyectos_jefe'
    )

    def __str__(self):
        return self.nombre

class Tarea(models.Model):

    class Prioridad(models.TextChoices):
        BAJA = "BAJA", "Baja"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"
        URGENTE = "URGENTE", "Urgente"

    class Estado(models.TextChoices):
        PENDIENTE = "P", "Pendiente"
        EN_PROGRESO = "E", "En progreso"
        EN_REVISION = "R", "En revisión"
        COMPLETADA = "C", "Completada"

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_limite = models.DateField()

    prioridad = models.CharField(
        max_length=10,
        choices=Prioridad.choices,
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )

    proyecto = models.ForeignKey(
        "Proyecto",
        on_delete=models.CASCADE,
        related_name="tareas"
    )

    asignados = models.ManyToManyField(
        "usuarios.Usuario",
        related_name="tareas_asignadas",
        blank=True,
    )

    def __str__(self):
        return self.nombre