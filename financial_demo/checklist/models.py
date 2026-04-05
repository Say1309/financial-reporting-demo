from django.db import models
from django.contrib.auth.models import User
from reporteo.models import ProcesoEjecucion

class ChecklistBase(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_REVISION', 'En revisión'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    proceso = models.OneToOneField(ProcesoEjecucion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    solicitado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    revisado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        abstract = True

class ChecklistCuentas(ChecklistBase):
    conciliacion_bancaria = models.BooleanField(default=False)
    saldos_validados = models.BooleanField(default=False)
    movimientos_revisados = models.BooleanField(default=False)
    diferencias_justificadas = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Checklist Cuentas"
        verbose_name_plural = "Checklists Cuentas"

    def completado(self):
        return all([self.conciliacion_bancaria, self.saldos_validados,
                    self.movimientos_revisados, self.diferencias_justificadas])

class ChecklistData(ChecklistBase):
    datos_fuente_cargados = models.BooleanField(default=False)
    formatos_validados = models.BooleanField(default=False)
    campos_obligatorios = models.BooleanField(default=False)
    integridad_verificada = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Checklist Data"
        verbose_name_plural = "Checklists Data"

    def completado(self):
        return all([self.datos_fuente_cargados, self.formatos_validados,
                    self.campos_obligatorios, self.integridad_verificada])

class ChecklistExpedientes(ChecklistBase):
    documentos_completos = models.BooleanField(default=False)
    firmas_vigentes = models.BooleanField(default=False)
    poderes_validados = models.BooleanField(default=False)
    dictamen_anexo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Checklist Expedientes"
        verbose_name_plural = "Checklists Expedientes"

    def completado(self):
        return all([self.documentos_completos, self.firmas_vigentes,
                    self.poderes_validados, self.dictamen_anexo])
