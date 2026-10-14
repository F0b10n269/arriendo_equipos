from django.db import models


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio (CLP)",
    )
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class Arriendo(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cliente = models.CharField(max_length=100)
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Monto (CLP)",
    )

    def __str__(self):
        return f'Arriendo de {self.equipo.nombre} para {self.cliente}'
    