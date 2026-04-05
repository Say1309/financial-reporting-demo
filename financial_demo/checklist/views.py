from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from reporteo.models import ProcesoEjecucion
from .models import ChecklistCuentas, ChecklistData, ChecklistExpedientes

def _actualizar_checklist(request, checklist, campos_bool, model_name):
    for campo in campos_bool:
        setattr(checklist, campo, campo in request.POST)
    if 'observaciones' in request.POST:
        checklist.observaciones = request.POST['observaciones']

    try:
        rol = request.user.rol
        es_ejecutivo = rol.es_ejecutivo_mesa()
    except:
        es_ejecutivo = False

    if es_ejecutivo and 'accion' in request.POST:
        checklist.revisado_por = request.user
        checklist.fecha_revision = timezone.now()
        checklist.estado = 'APROBADO' if request.POST['accion'] == 'aprobar' else 'RECHAZADO'

    checklist.save()
    messages.success(request, f'{model_name} actualizado.')

@login_required
def checklist_cuentas(request, pk):
    proceso = get_object_or_404(ProcesoEjecucion, pk=pk)
    obj, _ = ChecklistCuentas.objects.get_or_create(proceso=proceso, defaults={'solicitado_por': request.user})
    if request.method == 'POST':
        _actualizar_checklist(request, obj,
            ['conciliacion_bancaria','saldos_validados','movimientos_revisados','diferencias_justificadas'],
            'Checklist Cuentas')
        return redirect('proceso_detalle', pk=pk)
    return render(request, 'checklist/checklist_form.html', {'proceso': proceso, 'checklist': obj, 'tipo': 'Cuentas'})

@login_required
def checklist_data(request, pk):
    proceso = get_object_or_404(ProcesoEjecucion, pk=pk)
    obj, _ = ChecklistData.objects.get_or_create(proceso=proceso, defaults={'solicitado_por': request.user})
    if request.method == 'POST':
        _actualizar_checklist(request, obj,
            ['datos_fuente_cargados','formatos_validados','campos_obligatorios','integridad_verificada'],
            'Checklist Data')
        return redirect('proceso_detalle', pk=pk)
    return render(request, 'checklist/checklist_form.html', {'proceso': proceso, 'checklist': obj, 'tipo': 'Data'})

@login_required
def checklist_expedientes(request, pk):
    proceso = get_object_or_404(ProcesoEjecucion, pk=pk)
    obj, _ = ChecklistExpedientes.objects.get_or_create(proceso=proceso, defaults={'solicitado_por': request.user})
    if request.method == 'POST':
        _actualizar_checklist(request, obj,
            ['documentos_completos','firmas_vigentes','poderes_validados','dictamen_anexo'],
            'Checklist Expedientes')
        return redirect('proceso_detalle', pk=pk)
    return render(request, 'checklist/checklist_form.html', {'proceso': proceso, 'checklist': obj, 'tipo': 'Expedientes'})
