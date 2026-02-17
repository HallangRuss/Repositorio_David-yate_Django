from django.db import models
from AmbienteSena.Models.ambiente import Ambiente

class Elemento(models.Model):
    Nombre = models.CharField(max_length=100)
    Tipo = models.CharField(max_length=100)
    Observacion = models.CharField(max_length=255)
    Foto = models.CharField(max_length=255)
    ambiente = models.ForeignKey(Ambiente,on_delete=models.RESTRICT)

    class Meta:
        db_table = 'elemento'