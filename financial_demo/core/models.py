from django.db import models
from django.contrib.auth.models import User

class Fideicomiso(models.Model):
    numero = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=200)
    fiduciaria = models.CharField(max_length=200)
    fideicomitente = models.CharField(max_length=200)
    monto_inicial = models.DecimalField(max_digits=18, decimal_places=2)
    fecha_constitucion = models.DateField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Fideicomisos"
        ordering = ['numero']

    def __str__(self):
        return f"{self.numero} - {self.nombre}"

class Rol(models.Model):
    ROLES = [
        (10, 'Capturista'),
        (20, 'Ejecutivo Mesa'),
        (30, 'Supervisor'),
        (40, 'Administrador'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rol')
    nivel = models.IntegerField(choices=ROLES, default=10)
    fideicomisos = models.ManyToManyField(Fideicomiso, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_nivel_display()}"

    def es_ejecutivo_mesa(self):
        return self.nivel >= 20

    def es_supervisor(self):
        return self.nivel >= 30
