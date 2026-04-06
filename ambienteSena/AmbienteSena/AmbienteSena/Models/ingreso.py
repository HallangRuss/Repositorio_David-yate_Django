from django.db import models
from django.utils import timezone

class Ingreso(models.Model):
    instructor = models.ForeignKey('AmbienteSena.Instructor', on_delete=models.RESTRICT)
    ambiente = models.ForeignKey('AmbienteSena.Ambiente', on_delete=models.RESTRICT)  
    observacion = models.TextField()
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'ingreso'
