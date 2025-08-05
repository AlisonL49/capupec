from django.shortcuts import render
from sistema.views import admin_required

@admin_required
def plan_cuentas(request):
    return render(request, 'contabilidad/plan_cuentas.html', {'titulo': 'Contabilidad' , 'categoria_actual': 'contabilidad'})

@admin_required
def planilla_contable(request):
    return render(request, 'contabilidad/planilla_contable.html', {'titulo': 'Contabilidad' , 'categoria_actual': 'contabilidad'})

@admin_required
def mayor_auxiliar(request):
    return render(request, 'contabilidad/mayor_auxiliar.html', {'titulo': 'Contabilidad' , 'categoria_actual': 'contabilidad'})

@admin_required
def libro_diario(request):
    return render(request, 'contabilidad/libro_diario.html', {'titulo': 'Contabilidad' , 'categoria_actual': 'contabilidad'})

@admin_required
def balance_comprobacion(request):
    return render(request, 'contabilidad/balance_comprobacion.html', {'titulo': 'Contabilidad' , 'categoria_actual': 'contabilidad'})

@admin_required
def balance_general(request):
    return render(request, 'contabilidad/balance_general.html', {'titulo': 'Contabilidad' , 'categoria_actual': 'contabilidad'})

@admin_required
def estado_perdidas_ganancias(request):
    return render(request, 'contabilidad/estado_perdidas_ganancias.html', {'titulo': 'Contabilidad' , 'categoria_actual': 'contabilidad'})

@admin_required
def revision_crecimiento(request):
    return render(request, 'contabilidad/revision_crecimiento.html', {'titulo': 'Contabilidad' , 'categoria_actual': 'contabilidad'})

@admin_required
def cierre_dia(request):
    return render(request, 'contabilidad/cierre_dia.html', {'titulo': 'Contabilidad' , 'categoria_actual': 'contabilidad'})
