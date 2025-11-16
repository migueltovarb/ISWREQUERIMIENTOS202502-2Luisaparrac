from django.db import models 

class vehiculo(models.Model):
    COLORLIST = (
        ('ROJO', 'Rojo'),
        ('AZUL', 'Azul'),
        ('VERDE', 'Verde'),
    )

    placa = models.CharField(max_length=10)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)   # ✔ texto libre
    color = models.CharField(max_length=10, choices=COLORLIST)  # ✔ select de colores

    def __str__(self):
        return f"{self.placa} - {self.marca}"
# Create your models here.
