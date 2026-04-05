from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from core.models import Fideicomiso
from .models import ProcesoEjecucion, PasoLog, DatoFideicomiso, PASOS
from checklist.models import ChecklistCuentas, ChecklistData, ChecklistExpedientes

@login_required
def dashboard(request):
    try:
        rol = request.user.rol
        fideicomisos = rol.fideicomisos.filter(activo=True)
    except:
        fideicomisos = Fideicomiso.objects.filter(activo=True)

    procesos_activos = ProcesoEjecucion.objects.filter(
        fideicomiso__in=fideicomisos,
        estado__in=['ABIERTO', 'EN_PROCESO']
    ).select_related('fideicomiso')

    procesos_cerrados = ProcesoEjecucion.objects.filter(
        fideicomiso__in=fideicomisos,
        estado='CERRADO'
    ).select_related('fideicomiso')[:5]

    return render(request, 'reporteo/dashboard.html', {
        'fideicomisos': fideicomisos,
        'procesos_activos': procesos_activos,
        'procesos_cerrados': procesos_cerrados,
        'total_activos': procesos_activos.count(),
        'total_fideicomisos': fideicomisos.count(),
    })

@login_required
def proceso_nuevo(request):
    try:
        rol = request.user.rol
        fideicomisos = rol.fideicomisos.filter(activo=True)
    except:
        fideicomisos = Fideicomiso.objects.filter(activo=True)

    if request.method == 'POST':
        fideicomiso_id = request.POST.get('fideicomiso')
        periodo = request.POST.get('periodo')
        fideicomiso = get_object_or_404(Fideicomiso, id=fideicomiso_id)

        if ProcesoEjecucion.objects.filter(fideicomiso=fideicomiso, periodo=periodo).exists():
            messages.error(request, f'Ya existe un proceso para {fideicomiso} en el periodo {periodo}.')
            return redirect('proceso_nuevo')

        proceso = ProcesoEjecucion.objects.create(
            fideicomiso=fideicomiso,
            periodo=periodo,
            estado='ABIERTO',
            paso_actual=1,
            creado_por=request.user
        )
        ChecklistCuentas.objects.create(proceso=proceso, solicitado_por=request.user)
        ChecklistData.objects.create(proceso=proceso, solicitado_por=request.user)
        ChecklistExpedientes.objects.create(proceso=proceso, solicitado_por=request.user)

        messages.success(request, f'Proceso creado para {fideicomiso} — {periodo}')
        return redirect('proceso_detalle', pk=proceso.pk)

    return render(request, 'reporteo/proceso_nuevo.html', {'fideicomisos': fideicomisos})

@login_required
def proceso_detalle(request, pk):
    proceso = get_object_or_404(ProcesoEjecucion, pk=pk)
    logs = proceso.logs.select_related('completado_por').all()
    datos = getattr(proceso, 'datos', None)

    try:
        checklist_cuentas = proceso.checklistcuentas
        checklist_data = proceso.checklistdata
        checklist_expedientes = proceso.checklistexpedientes
    except:
        checklist_cuentas = checklist_data = checklist_expedientes = None

    pasos_info = []
    for num, nombre in PASOS:
        log = logs.filter(paso=num).first()
        pasos_info.append({
            'numero': num,
            'nombre': nombre,
            'completado': log is not None,
            'log': log,
            'es_actual': num == proceso.paso_actual,
            'es_futuro': num > proceso.paso_actual,
        })

    return render(request, 'reporteo/proceso_detalle.html', {
        'proceso': proceso,
        'pasos_info': pasos_info,
        'datos': datos,
        'checklist_cuentas': checklist_cuentas,
        'checklist_data': checklist_data,
        'checklist_expedientes': checklist_expedientes,
        'logs': logs,
    })

@login_required
def avanzar_paso(request, pk):
    if request.method != 'POST':
        return redirect('proceso_detalle', pk=pk)

    proceso = get_object_or_404(ProcesoEjecucion, pk=pk)

    if proceso.estado == 'CERRADO':
        messages.error(request, 'Este proceso ya está cerrado.')
        return redirect('proceso_detalle', pk=pk)

    notas = request.POST.get('notas', '')
    PasoLog.objects.create(
        proceso=proceso,
        paso=proceso.paso_actual,
        completado_por=request.user,
        notas=notas
    )

    if proceso.paso_actual < 8:
        proceso.paso_actual += 1
        proceso.estado = 'EN_PROCESO'
    else:
        proceso.estado = 'CERRADO'
        proceso.fecha_cierre = timezone.now()

    proceso.save()
    messages.success(request, f'Paso {proceso.paso_actual - 1 if proceso.estado != "CERRADO" else 8} completado.')
    return redirect('proceso_detalle', pk=pk)

@login_required
def captura_datos(request, pk):
    proceso = get_object_or_404(ProcesoEjecucion, pk=pk)
    datos, _ = DatoFideicomiso.objects.get_or_create(proceso=proceso, defaults={'capturado_por': request.user})

    if request.method == 'POST':
        datos.saldo_inicial    = request.POST.get('saldo_inicial', 0)
        datos.aportaciones     = request.POST.get('aportaciones', 0)
        datos.retiros          = request.POST.get('retiros', 0)
        datos.rendimientos     = request.POST.get('rendimientos', 0)
        datos.comisiones       = request.POST.get('comisiones', 0)
        datos.tasa_referencia  = request.POST.get('tasa_referencia', 0)
        datos.capturado_por    = request.user
        datos.save()
        messages.success(request, 'Datos guardados correctamente.')
        return redirect('proceso_detalle', pk=pk)

    return render(request, 'reporteo/captura_datos.html', {'proceso': proceso, 'datos': datos})

@login_required
def reporte_html(request, pk):
    proceso = get_object_or_404(ProcesoEjecucion, pk=pk)
    datos = getattr(proceso, 'datos', None)
    return render(request, 'reporteo/reporte.html', {'proceso': proceso, 'datos': datos})
