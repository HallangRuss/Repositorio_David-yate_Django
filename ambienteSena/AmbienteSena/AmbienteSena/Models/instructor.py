from django.db import models

class Instructor(models.Model):
    NombreCompleto = models.CharField(max_length=255)
    Area = models.CharField(max_length=255)
    Celular = models.CharField(max_length=20)
    # Nota: IntegerField no lleva un número como 50 dentro del paréntesis para longitud.
    # Si quieres limitar dígitos usa BigIntegerField o quita el 50.
    Cedula = models.IntegerField() 
    
    # --- SE ELIMINÓ LA RELACIÓN MANY TO MANY CON ELEMENTOS ---

    class Meta:
        db_table = 'instructor'