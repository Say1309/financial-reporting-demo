from django.db import models
from django.contrib.auth.models import User
from core.models import Fideicomiso

PASOS = [
    (1, 'Verificación de datos fuente'),
    (2, 'Carga de información'),
    (3, 'Validación de saldos'),
    (4, 'Cálculo de rendimientos'),
    (5, 'Generación de reportes'),
    (6, 'Revisión supervisor'),
    (7, 'Autorización'),
    (8, 'Cierre de proceso'),
]

class ProcesoEjecucion(models.Model):
    ESTADOS = [
        ('ABIERTO',  'Abierto'),
        ('EN_PROCESO', 'En proceso'),
        ('CERRADO',  'Cerrado'),
        ('CANCELADO', 'Cancelado'),
    ]
    fideicomiso = models.ForeignKey(Fideicomiso, on_delete=models.CASCADE, related_name='procesos')
    periodo = models.CharField(max_length=7, help_text='YYYY-MM')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ABIERTO')
    paso_actual = models.IntegerField(default=1)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='procesos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('fideicomiso', 'periodo')
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.fideicomiso} | {self.periodo} | {self.get_estado_display()}"

    def porcentaje_avance(self):
        return int((self.paso_actual - 1) / 8 * 100)

    def paso_nombre(self):
        return dict(PASOS).get(self.paso_actual, '')

class PasoLog(models.Model):
    proceso = models.ForeignKey(ProcesoEjecucion, on_delete=models.CASCADE, related_name='logs')
    paso = models.IntegerField(choices=PASOS)
    completado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return f"Paso {self.paso} - {self.proceso}"

class DatoFideicomiso(models.Model):
    proceso = models.OneToOneField(ProcesoEjecucion, on_delete=models.CASCADE, related_name='datos')
    saldo_inicial = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    aportaciones = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    retiros = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    rendimientos = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    comisiones = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    tasa_referencia = models.DecimalField(max_digits=8, decimal_places=4, default=0, help_text='TIIE o tasa aplicable')
    fecha_captura = models.DateTimeField(auto_now=True)
    capturado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    @property
    def saldo_final(self):
        return self.saldo_inicial + self.aportaciones - self.retiros + self.rendimientos - self.comisiones

    def __str__(self):
        return f"Datos {self.proceso}"
