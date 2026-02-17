from django.db import models


class Ambiente(models.Model):
    NombreAmbiente = models.CharField(max_length=100)
    TipoAmbiente = models.CharField(max_length=100)
    Observacion = models.CharField(max_length=250)

    class Meta:
        db_table = 'ambientes'
