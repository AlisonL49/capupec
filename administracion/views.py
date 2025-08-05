from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from sistema.views import admin_required
from .forms import DestinosCreditoForm, FormasPagoForm, InteresAFuturosForm, InteresAhorrosForm, ParametrosForm, PeriodosForm, RepresentantesForm,  TiposAFuturosForm, TiposAhorrosForm, TiposCreditoForm, PlazoFijoForm
from .models import Capitalizaciones, DestinosCredito,  FormasPago, InteresAFuturo, InteresAhorros, Parametros, PeriodoContable, Representantes, TiposAFuturos, TiposAhorros, TiposCredito,  PlazoFijo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@admin_required
def representantes(request):
    representante = Representantes.objects.first()  
    if request.method == 'POST':
        form = RepresentantesForm(request.POST, instance=representante)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados correctamente.")
            return redirect('representantes')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, field, f" {error}")
    else:
        form = RepresentantesForm(instance=representante)

    return render(request, 'administracion/representantes.html', {'titulo': 'Administración', 'categoria_actual': 'administracion','form': form, 'representante': representante})

@admin_required
def parametros(request):
    if request.method == "POST":
        form = ParametrosForm(request.POST)
        if form.is_valid():
            
                form.save()
                messages.success(request, "Parámetro registrado correctamente.")
                return redirect("parametros")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f" {error}")
    else:
        form = ParametrosForm()

    parametros = Parametros.objects.all()
    return render(request, 'administracion/parametros.html', {'titulo': 'Administración', 'categoria_actual': 'administracion',"form": form, 'parametros': parametros})

@login_required
@admin_required
@csrf_exempt
def parametro_eliminar(request, pk):
    if request.method == 'POST':
        parametro = get_object_or_404(Parametros, pk=pk)
        parametro.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
@admin_required
@csrf_exempt
def parametro_editar(request, pk):
    if request.method == 'POST':
        parametro = get_object_or_404(Parametros, pk=pk)
        parametro.parm_abreviatura = request.POST.get('parm_abreviatura')
        parametro.parm_descripcion = request.POST.get('parm_descripcion')
        parametro.parm_valor = request.POST.get('parm_valor')
        parametro.parm_estado = bool(request.POST.get('parm_estado'))
        parametro.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@admin_required
def formas_pago(request):
    formas_pago = FormasPago.objects.all()

    if request.method == 'POST':
        form = FormasPagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Forma de Pago registrada correctamente.")
            return redirect('formas-pago')  
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = FormasPagoForm()
    return render(request, 'administracion/formas_pago.html', {'titulo': 'Administración', 'categoria_actual': 'administracion', 'form': form, 'formas_pago': formas_pago})

@login_required
@csrf_exempt
def forma_pago_editar(request, pk):
    if request.method == 'POST':
        pago = get_object_or_404(FormasPago, pk=pk)
        pago.fpago_codigo = request.POST.get('fpago_codigo')
        pago.fpago_descripcion = request.POST.get('fpago_descripcion')
        pago.fpago_estado = bool(request.POST.get('fpago_estado'))
        pago.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
@csrf_exempt
def forma_pago_eliminar(request, pk):
    if request.method == 'POST':
        pago = get_object_or_404(FormasPago, pk=pk)
        pago.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@admin_required
def destinos(request):
    destinos_credito = DestinosCredito.objects.all()

    if request.method == 'POST':
        form = DestinosCreditoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Destino registrado correctamente.")
            return redirect('destinos') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}") 
    else:
        form = DestinosCreditoForm()
    return render(request, 'administracion/destinos.html', {'titulo': 'Administración', 'categoria_actual': 'administracion', 'form': form, 'destinos_credito': destinos_credito})

@admin_required
def tipos_ahorros(request):
    tipos_ahorros = TiposAhorros.objects.all()
    capitalizaciones = Capitalizaciones.objects.all()

    if request.method == "POST":
        form = TiposAhorrosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de ahorro registrado exitosamente.")
            return redirect("tipos-ahorros")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f" {error}")

    else:
        form = TiposAhorrosForm()
    return render(request, 'administracion/tipos_ahorros.html', {'titulo': 'Administración', 'categoria_actual': 'administracion',"form": form, "tipos_ahorros": tipos_ahorros, "capitalizaciones": capitalizaciones})

@login_required
@admin_required
@csrf_exempt
def tipo_ahorro_editar(request, pk):
    if request.method == 'POST':
        tipo = get_object_or_404(TiposAhorros, pk=pk)
        tipo.tahorro_abreviatura = request.POST.get('tahorro_abreviatura')
        tipo.tahorro_tipo = request.POST.get('tahorro_tipo')
        tipo.tahorro_dia_aporte = request.POST.get('tahorro_dia_aporte')
        tipo.tahorro_meses_minimo = request.POST.get('tahorro_meses_minimo')
        tipo.tahorro_porcent_aporte = request.POST.get('tahorro_porcent_aporte')
        tipo.tahorro_capitalizacion_id = request.POST.get('tahorro_capitalizacion')
        tipo.tahorro_estado = bool(request.POST.get('tahorro_estado'))
        tipo.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
@admin_required
@csrf_exempt
def tipo_ahorro_eliminar(request, pk):
    if request.method == 'POST':
        tipo = get_object_or_404(TiposAhorros, pk=pk)
        tipo.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@admin_required
def tipos_credito(request):
    tipos_creditos = TiposCredito.objects.all()

    if request.method == "POST":
        form = TiposCreditoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de crédito guardado exitosamente.")
            return redirect("tipos-credito")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f" {error}")

    else:
        form = TiposCreditoForm()    
    return render(request, 'administracion/tipos_credito.html', {'titulo': 'Administración', 'categoria_actual': 'administracion',"form": form, "tipos_creditos": tipos_creditos})

@login_required
@admin_required
@csrf_exempt
def tipo_credito_editar(request, pk):
    if request.method == 'POST':
        credito = get_object_or_404(TiposCredito, pk=pk)
        credito.tcredito_tipo = request.POST.get('tcredito_tipo')
        credito.tcredito_descripcion = request.POST.get('tcredito_descripcion')
        credito.tcredito_monto_maximo = request.POST.get('tcredito_monto_maximo')
        credito.tcredito_num_cuotas = request.POST.get('tcredito_num_cuotas')
        credito.tcredito_tasa_interes = request.POST.get('tcredito_tasa_interes')
        credito.tcredito_aporte_minimo = request.POST.get('tcredito_aporte_minimo')
        credito.tcredito_porcentaje_encaje = request.POST.get('tcredito_porcentaje_encaje')
        credito.tcredito_gracia = request.POST.get('tcredito_gracia')
        credito.tcredito_porcentaje_mora = request.POST.get('tcredito_porcentaje_mora')
        credito.tcredito_estado = bool(request.POST.get('tcredito_estado'))
        credito.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
@admin_required
@csrf_exempt
def tipo_credito_eliminar(request, pk):
    if request.method == 'POST':
        credito = get_object_or_404(TiposCredito, pk=pk)
        credito.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@admin_required
def tipos_ahorrofuturo(request):
    tipos_afuturos = TiposAFuturos.objects.all()

    if request.method == "POST":
        form = TiposAFuturosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de ahorro futuro registrado exitosamente.")
            return redirect("tipos-ahorrofuturo")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f" {error}")

    else:
        form = TiposAFuturosForm()
    return render(request, 'administracion/tipos_ahorro_futuro.html', {'titulo': 'Administración', 'categoria_actual': 'administracion', "form": form, "tipos_afuturos": tipos_afuturos,})

@login_required
@admin_required
@csrf_exempt
def tipo_ahorrofuturo_editar(request, pk):
    if request.method == 'POST':
        afuturo = get_object_or_404(TiposAFuturos, pk=pk)
        afuturo.tafuturo_abreviatura = request.POST.get('tafuturo_abreviatura')
        afuturo.tafuturo_tipo = request.POST.get('tafuturo_tipo')
        afuturo.tafuturo_v_inicial = request.POST.get('tafuturo_v_inicial')
        afuturo.tafuturo_v_periodico = request.POST.get('tafuturo_v_periodico')
        afuturo.tafuturo_plazo = request.POST.get('tafuturo_plazo')
        afuturo.tafuturo_penalizacion = request.POST.get('tafuturo_penalizacion')
        afuturo.tafuturo_estado = bool(request.POST.get('tafuturo_estado'))
        afuturo.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
@admin_required
@csrf_exempt
def tipo_ahorrofuturo_eliminar(request, pk):
    if request.method == 'POST':
        afuturo = get_object_or_404(TiposAFuturos, pk=pk)
        afuturo.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@admin_required
def plazo_fijo(request):
    plazos = PlazoFijo.objects.all()

    if request.method == 'POST':
        form = PlazoFijoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Plazo fijo registrado correctamente.")
            return redirect('plazo-fijo') 
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = PlazoFijoForm()
    
    return render(request, 'administracion/plazo_fijo.html', {
        'form': form,
        'plazos': plazos,
        'titulo': 'Administracion',
        'categoria_actual': 'administracion'
    })

@login_required
@admin_required
@csrf_exempt
def plazo_eliminar(request, pk):
    if request.method == 'POST':
        plazo = get_object_or_404(PlazoFijo, pk=pk)
        plazo.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
@admin_required
@csrf_exempt
def plazo_editar(request, pk):
    if request.method == 'POST':
        plazo = get_object_or_404(PlazoFijo, pk=pk)
        plazo.pf_descripcion = request.POST.get('pf_descripcion')
        plazo.pf_monto = request.POST.get('pf_monto')
        plazo.pf_plazo = request.POST.get('pf_plazo')
        plazo.pf_tasa_interes = request.POST.get('pf_tasa_interes')
        plazo.pf_fecha_vencimiento = request.POST.get('pf_fecha_vencimiento')
        plazo.pf_estado = bool(request.POST.get('pf_estado'))
        plazo.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@admin_required
def interes_ahorros(request):
    interes_ahorros = InteresAhorros.objects.all()
    tipos_ahorros = TiposAhorros.objects.all()
    
    if request.method == "POST":
        form = InteresAhorrosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de interes de ahorro registrado exitosamente.")
            return redirect("interes-ahorros")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f" {error}")
   
    else:
        form = InteresAhorrosForm()
    return render(request, 'administracion/interes_ahorros.html', {'titulo': 'Administración', 'categoria_actual': 'administracion', "form": form, "interes_ahorros": interes_ahorros, "tipos_ahorros": tipos_ahorros})

@login_required
@admin_required
@csrf_exempt
def interes_ahorros_eliminar(request, pk):
    if request.method == 'POST':
        interes = get_object_or_404(InteresAhorros, pk=pk)
        interes.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
@admin_required
@csrf_exempt
def interes_ahorros_editar(request, pk):
    if request.method == 'POST':
        interes = get_object_or_404(InteresAhorros, pk=pk)
        tipo_id = request.POST.get('iahorro_tipo')
        if tipo_id:
            interes.iahorro_tipo_id = tipo_id
        interes.iahorro_rendimiento = request.POST.get('iahorro_rendimiento')
        interes.iahorro_v_minimo = request.POST.get('iahorro_v_minimo')
        interes.iahorro_v_maximo = request.POST.get('iahorro_v_maximo')
        interes.iahorro_estado = bool(request.POST.get('iahorro_estado'))
        interes.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
@admin_required
def interes_afuturo(request):
    interes_afuturo = InteresAFuturo.objects.all()
    tipos_afuturos = TiposAFuturos.objects.all()

    if request.method == "POST":
        form = InteresAFuturosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de interes registrado exitosamente.")
            return redirect("interes-ahorrofuturo")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f" {error}")

    else:
        form = InteresAFuturosForm()
    return render(request, 'administracion/interes_ahorro_futuro.html', {'titulo': 'Administración', 'categoria_actual': 'administracion', "form": form, "interes_afuturo": interes_afuturo, "tipos_afuturos": tipos_afuturos})

@login_required
@admin_required
@csrf_exempt
def interes_afuturo_eliminar(request, pk):
    if request.method == 'POST':
        interes = get_object_or_404(InteresAFuturo, pk=pk)
        interes.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
@admin_required
@csrf_exempt
def interes_afuturo_editar(request, pk):
    if request.method == 'POST':
        interes = get_object_or_404(InteresAFuturo, pk=pk)
        tipo_id = request.POST.get('iafuturo_tipo')
        if tipo_id:
            interes.iafuturo_tipo_id = tipo_id
        interes.iafuturo_rendimiento = request.POST.get('iafuturo_rendimiento')
        interes.iafuturo_v_minimo = request.POST.get('iafuturo_v_minimo')
        interes.iafuturo_v_maximo = request.POST.get('iafuturo_v_maximo')
        interes.iafuturo_estado = bool(request.POST.get('iafuturo_estado'))
        interes.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@admin_required
def periodos_contables(request):
    periodos_contables = PeriodoContable.objects.all()

    if request.method == 'POST':
        form = PeriodosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Periodo registrado correctamente.")
            return redirect('periodos-contables') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}") 
    else:
        form = PeriodosForm()
    return render(request, 'administracion/ad_periodos_contables.html', {'titulo': 'Administración', 'categoria_actual': 'administracion', 'form' : form, 'periodos_contables' : periodos_contables})