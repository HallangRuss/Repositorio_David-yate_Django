from django.db import models

class Cuentadante(models.Model):
    instructor = models.ForeignKey('AmbienteSena.Instructor', on_delete=models.RESTRICT)
    ambiente = models.ForeignKey('AmbienteSena.Ambiente', on_delete=models.RESTRICT)
    observacion = models.TextField(blank=True)
    fechaasignacion = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'cuentadante'
        managed = True  # <-- Asegúrate de que esté en True
        # unique_together = ('instructor', 'ambiente') # Déjalo comentado por ahora