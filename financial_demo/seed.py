import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_demo.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Fideicomiso, Rol
from reporteo.models import ProcesoEjecucion, PasoLog, DatoFideicomiso
from checklist.models import ChecklistCuentas, ChecklistData, ChecklistExpedientes
from django.utils import timezone
from datetime import date

print("Creando fideicomisos demo...")
fideicomisos = [
    Fideicomiso.objects.get_or_create(numero=1001, defaults=dict(nombre="Fideicomiso Alfa SA de CV", fiduciaria="BBVA Mexico SA", fideicomitente="Grupo Alfa Industrial", monto_inicial=50_000_000, fecha_constitucion=date(2020,3,15)))[0],
    Fideicomiso.objects.get_or_create(numero=1002, defaults=dict(nombre="Fondo Beta Inmobiliario", fiduciaria="Banorte SA", fideicomitente="Desarrolladora Beta", monto_inicial=120_000_000, fecha_constitucion=date(2019,7,1)))[0],
    Fideicomiso.objects.get_or_create(numero=1003, defaults=dict(nombre="Trust Gamma Agropecuario", fiduciaria="Scotiabank Mexico", fideicomitente="Gamma Agro SA", monto_inicial=30_000_000, fecha_constitucion=date(2021,1,20)))[0],
]

print("Creando usuarios demo...")
users = {}
for username, fname, lname, nivel in [
    ('capturista', 'Ana', 'García', 10),
    ('ejecutivo',  'Carlos', 'Mendoza', 20),
    ('supervisor', 'Sayuri', 'Mota', 30),
]:
    u, created = User.objects.get_or_create(username=username, defaults=dict(first_name=fname, last_name=lname, email=f'{username}@demo.com'))
    if created:
        u.set_password('demo123')
        u.save()
    rol, _ = Rol.objects.get_or_create(usuario=u, defaults={'nivel': nivel})
    rol.fideicomisos.set(fideicomisos)
    users[username] = u

print("Creando procesos demo...")
cap = users['capturista']
sup = users['supervisor']

# Proceso 1: en progreso paso 3
p1, _ = ProcesoEjecucion.objects.get_or_create(fideicomiso=fideicomisos[0], periodo='2026-03', defaults=dict(estado='EN_PROCESO', paso_actual=3, creado_por=cap))
for paso in [1, 2]:
    PasoLog.objects.get_or_create(proceso=p1, paso=paso, defaults=dict(completado_por=cap, notas=f'Paso {paso} completado sin incidencias.'))
DatoFideicomiso.objects.get_or_create(proceso=p1, defaults=dict(saldo_inicial=48_500_000, aportaciones=2_000_000, retiros=500_000, rendimientos=285_000, comisiones=12_500, tasa_referencia=11.25, capturado_por=cap))
ChecklistCuentas.objects.get_or_create(proceso=p1, defaults=dict(solicitado_por=cap, conciliacion_bancaria=True, saldos_validados=True, movimientos_revisados=False, diferencias_justificadas=False))
ChecklistData.objects.get_or_create(proceso=p1, defaults=dict(solicitado_por=cap, datos_fuente_cargados=True, formatos_validados=True, campos_obligatorios=True, integridad_verificada=False))
ChecklistExpedientes.objects.get_or_create(proceso=p1, defaults=dict(solicitado_por=cap))

# Proceso 2: recién abierto
p2, _ = ProcesoEjecucion.objects.get_or_create(fideicomiso=fideicomisos[1], periodo='2026-03', defaults=dict(estado='ABIERTO', paso_actual=1, creado_por=cap))
ChecklistCuentas.objects.get_or_create(proceso=p2, defaults=dict(solicitado_por=cap))
ChecklistData.objects.get_or_create(proceso=p2, defaults=dict(solicitado_por=cap))
ChecklistExpedientes.objects.get_or_create(proceso=p2, defaults=dict(solicitado_por=cap))

# Proceso 3: cerrado (histórico)
p3, _ = ProcesoEjecucion.objects.get_or_create(fideicomiso=fideicomisos[0], periodo='2026-02', defaults=dict(estado='CERRADO', paso_actual=8, creado_por=cap, fecha_cierre=timezone.now()))
for paso in range(1, 9):
    PasoLog.objects.get_or_create(proceso=p3, paso=paso, defaults=dict(completado_por=cap if paso < 6 else sup, notas='OK'))
DatoFideicomiso.objects.get_or_create(proceso=p3, defaults=dict(saldo_inicial=46_000_000, aportaciones=3_000_000, retiros=800_000, rendimientos=260_000, comisiones=11_000, tasa_referencia=11.00, capturado_por=cap))
ChecklistCuentas.objects.get_or_create(proceso=p3, defaults=dict(solicitado_por=cap, estado='APROBADO', revisado_por=sup, conciliacion_bancaria=True, saldos_validados=True, movimientos_revisados=True, diferencias_justificadas=True))
ChecklistData.objects.get_or_create(proceso=p3, defaults=dict(solicitado_por=cap, estado='APROBADO', revisado_por=sup, datos_fuente_cargados=True, formatos_validados=True, campos_obligatorios=True, integridad_verificada=True))
ChecklistExpedientes.objects.get_or_create(proceso=p3, defaults=dict(solicitado_por=cap, estado='APROBADO', revisado_por=sup, documentos_completos=True, firmas_vigentes=True, poderes_validados=True, dictamen_anexo=True))

print("✓ Seed completado. Usuarios: capturista/ejecutivo/supervisor · Password: demo123")
