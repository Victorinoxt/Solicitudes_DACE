from django.db import models

class Estudiante(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado')
    ]
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    ano_ingreso = models.IntegerField()
    carrera = models.CharField(max_length=100)
    estado_solicitud = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    es_egresado = models.BooleanField(default=False)  # False para admisión, True para egresados

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cedula}"
