from django.db import models


class Instructor(models.Model):
    NombreCompleto = models.CharField(max_length=255)
    Area = models.CharField(max_length=255)
    Celular = models.CharField(max_length=20)
    Cedula = models.IntegerField(50)
    
    elementos = models.ManyToManyField(
        'AmbienteSena.ELemento',
        through= 'AmbienteSena.Cuentadante',
        related_name='instructores'
    )

    class Meta:
        db_table = 'instructor'
