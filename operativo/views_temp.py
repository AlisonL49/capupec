import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from administracion.models import DestinosCredito,  FormasPago, Representantes, TiposCredito, Parametros
from usuarios.models import Roles, EstadoCivil, PerfilUsuario
from .models import CuentasAhorros
from .forms import SolicitudesCreditoForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime, timedelta
from decimal import Decimal
from sistema.views import resultados_busqueda, admin_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import base64



@admin_required
def consulta_garantias(request):
    usuarios = User.objects.all().order_by('last_name', 'first_name')
    socio_seleccionado = None

    # Aplicar búsqueda si existe
    usuarios, search_query, category = resultados_busqueda(
        request,
        usuarios,
        search_fields=['first_name', 'last_name']
    )

    if 'seleccionar' in request.GET:
        usuario_id = request.GET.get('seleccionar')
        socio_seleccionado = User.objects.filter(id=usuario_id).first()

    return render(request, 'operativo/consulta_garantias.html', {'titulo': 'Operativo', 'categoria_actual': 'operativo',
                                                                 'usuarios': usuarios,
                                                                 'socio_seleccionado': socio_seleccionado,
                                                                 'search_query': search_query,
                                                                 'selected_category': category,
                                                                 'search_categories': [
                                                                     {'value': 'activo',
                                                                         'label': 'Activos'},
                                                                     {'value': 'inactivo',
                                                                         'label': 'Inactivos'},
                                                                     ],
    })

@admin_required
def solicitud(request):
    tipos_credito = TiposCredito.objects.all()
    formas_pago = FormasPago.objects.all()
    usuarios = PerfilUsuario.objects.all().order_by('user__last_name', 'user__first_name')
    solicitud_form = SolicitudesCreditoForm()
    seguro = Parametros.objects.get(parm_nombre='SEGUROGRAV')
    comision = Parametros.objects.get(parm_nombre='COMISION')

    accion = ''
    socio_seleccionado = None
    condicion_socio = ''
    nombre_garante = ''
    num_garante = ''
    s_creditos = ''
    tipo_credito_id = ''
    comision_valor = 0
    encaje_valor = 0
    monto_total = 0
    tabla_amortizacion = []
    interes = gracia = nro_aportes = valor_aportes = ''

    valores_ingresados = {
        'num_solicitud': '',
        'nombre_garante': '',
        'num_garante': '',
        's_creditos': '',
        'tipo_credito_id': '',
        'forma_pago': '',
        'tipo_tabla': '',
        'condicion': '',
        'disponible': '',
        'monto': '',
        'cuotas': '',
        'tipos_credito': '',
        'seguro_valor': seguro.parm_valor,
        'comision_valor': comision.parm_valor,
       
    }
    # Aplicar búsqueda
    usuarios, search_query, category = resultados_busqueda(
        request,
        usuarios,
        search_fields=['first_name', 'last_name']
    )

    # Obtener socio seleccionado por búsqueda
    if 'seleccionar' in request.GET:
        usuario_id = request.GET.get('seleccionar')
        socio_seleccionado = PerfilUsuario.objects.filter(id=usuario_id).first()
        condicion_socio = socio_seleccionado.nombramiento if socio_seleccionado else ''

    # POST para cambio de tipo de crédito o guardar solicitud
    if request.method == 'POST':
        accion = request.POST.get('accion', '')

        # Recoger campos del formulario
        valores_ingresados['num_solicitud'] = request.POST.get(
            'sol_nro_solicitud', '')
        valores_ingresados['nombre_garante'] = request.POST.get(
            'sol_nombres_garante', '')
        valores_ingresados['num_garante'] = request.POST.get(
            'sol_nro_garante', '')
        valores_ingresados['s_creditos'] = request.POST.get(
            'sol_s_creditos', '')
        valores_ingresados['tipo_credito_id'] = request.POST.get(
            'sol_tipo_credito', '')
        valores_ingresados['forma_pago'] = request.POST.get(
            'sol_forma_pago', '')
        valores_ingresados['tipo_tabla'] = request.POST.get(
            'sol_tipo_tabla', '')
        valores_ingresados['condicion'] = request.POST.get('sol_condicion', '')
        valores_ingresados['disponible'] = request.POST.get(
            'sol_disponible', '')
        valores_ingresados['monto'] = request.POST.get('sol_monto', '')
        valores_ingresados['cuotas'] = request.POST.get('sol_cuotas', '')

    # Recuperar datos si se recarga por selección de tipo de crédito
    socio_id = request.GET.get('sol_socio')
    if socio_id and not socio_seleccionado:
        socio_seleccionado = PerfilUsuario.objects.filter(id=socio_id).first()
        condicion_socio = socio_seleccionado.nombramiento if socio_seleccionado else ''

    # Obtener datos del garante si existen
    num_garante = valores_ingresados['num_garante']
    if num_garante:
        garante = PerfilUsuario.objects.filter(id=num_garante).first()
        if garante:
            nombre_garante = f"{garante.first_name} {garante.last_name}"
            # Aquí podrías calcular `s_creditos` si tienes lógica
            s_creditos = '0'  # reemplaza con cálculo real si aplica

  
    # Capturar selección de tipo de crédito
    tipo_credito_id = valores_ingresados['tipo_credito_id']
    if tipo_credito_id and accion == "cambio_tipo_credito":
       try:
           tipo = TiposCredito.objects.get(id=tipo_credito_id)
           interes = tipo.tcredito_tasa_interes
           gracia = tipo.tcredito_gracia
           encaje = tipo.tcredito_porcentaje_encaje
           nro_aportes = tipo.tcredito_num_cuotas
           valor_aportes = tipo.tcredito_aporte_minimo
       except TiposCredito.DoesNotExist:
           pass
       
    # Guardar solicitud de crédito
    elif accion == "guardar_solicitud":
        solicitud_form = SolicitudesCreditoForm(request.POST)
        if solicitud_form.is_valid() and socio_seleccionado:
            solicitud = solicitud_form.save(commit=False)
            solicitud.socio = socio_seleccionado
            solicitud.save()
            messages.success(request, "Solicitud de crédito registrada exitosamente.")
            return redirect('solicitud')
        else:
            messages.error(request, "Por favor revise los datos ingresados.")


    return render(request, 'operativo/solicitud.html', {
        'titulo': 'Operativo',
        'categoria_actual': 'operativo',
        'tipos_credito': tipos_credito,
        'formas_pago': formas_pago,
        'usuarios': usuarios,
        'socio_seleccionado': socio_seleccionado,
        'condicion': condicion_socio,
        'tipo_credito_id': tipo_credito_id,
        'interes': interes,
        'gracia': gracia,
        'nro_aportes': nro_aportes,
        'valor_aportes': valor_aportes,
        'solicitud_form': solicitud_form,
        'search_query': search_query,
        'selected_category': category,
        'nombre_garante': nombre_garante,
        'num_garante': num_garante,
        's_creditos': s_creditos,
        'valores_ingresados': valores_ingresados,
        'search_categories': [
            {'value': 'activo', 'label': 'Activos'},
            {'value': 'inactivo', 'label': 'Inactivos'},
        ],
    })

@admin_required
def calcular_amortizacion_francesa(monto, interes, cuotas, seguro, comision, encaje):
    amortizacion = []
    monto_total = Decimal(monto) + (Decimal(monto) * Decimal(comision) / Decimal(100))  # Agregar comisión al monto inicial
    saldo = monto_total
    interes_mensual = Decimal(interes) / Decimal(100) / 12
    
    # Calcular cuota base sin seguros/encaje
    cuota_base = saldo * (interes_mensual / (1 - (1 + interes_mensual) ** -int(cuotas)))
    
    # Valor fijo de comisión para mostrar en la tabla
    comision_valor = Decimal(monto) * Decimal(comision) / Decimal(100)
    
    for i in range(0, int(cuotas) + 1):
        interes_mensual_valor = saldo * interes_mensual
        capital = cuota_base - interes_mensual_valor
        
        # Calcular valores dinámicos cada mes
        seguro_mensual = saldo * Decimal(seguro) / Decimal(100)
        
        saldo -= capital
        
        amortizacion.append({
            'numero': i,
            'fecha_pago': (datetime.today() + timedelta(days=30 * i)).strftime('%Y-%m-%d'),
            'capital': round(capital, 2),
            'interes': round(interes_mensual_valor, 2),
            'seguro': round(seguro_mensual, 2),
            'comision': round(comision_valor, 2) if i == 1 else Decimal('0.00'),  # Solo mostrar en primera cuota
            'cuota_total': round(cuota_base + seguro_mensual, 2),
            'saldo': round(saldo if saldo > 0 else Decimal('0.00'), 2),
        })
    return amortizacion

@admin_required
def generar_pdf_amortizacion(request):
    if request.method == 'POST':
        monto = Decimal(request.POST.get('monto'))
        cuotas = int(request.POST.get('cuotas'))
        interes = Decimal(request.POST.get('interes'))
        tipo_credito_id = request.POST.get('tipo_credito')

        try:
            tipo_credito = TiposCredito.objects.get(id=tipo_credito_id)
            encaje = tipo_credito.tcredito_porcentaje_encaje
        except TiposCredito.DoesNotExist:
            encaje = Decimal(0)

        comision = Parametros.objects.filter(parm_nombre__iexact='COMISION').first()
        comision_valor = Decimal(comision.parm_valor) if comision else Decimal(0)

        seguro = Parametros.objects.filter(parm_nombre__iexact='SEGUROGRAV').first()
        seguro_valor = Decimal(seguro.parm_valor) if seguro else Decimal(0)

        tabla_amortizacion = calcular_amortizacion_francesa(monto, interes, cuotas, seguro_valor, comision_valor, encaje)

        # Calcular totales para el resumen
        total_capital = sum(cuota['capital'] for cuota in tabla_amortizacion)
        total_interes = sum(cuota['interes'] for cuota in tabla_amortizacion)
        total_seguro = sum(cuota['seguro'] for cuota in tabla_amortizacion)
        total_encaje = sum(cuota['encaje'] for cuota in tabla_amortizacion)
        total_comision = sum(cuota['comision'] for cuota in tabla_amortizacion)
        total_cuotas = sum(cuota['cuota_total'] for cuota in tabla_amortizacion)

        html_string = render_to_string('pdf_amortizacion.html', {
            'tabla_amortizacion': tabla_amortizacion,
            'fecha': datetime.today().strftime('%d-%m-%Y'),
            'monto_solicitado': monto,
            'plazo_meses': cuotas,
            'tasa_interes': interes,
            'total_capital': round(total_capital, 2),
            'total_interes': round(total_interes, 2),
            'total_seguro': round(total_seguro, 2),
            'total_encaje': round(total_encaje, 2),
            'total_comision': round(total_comision, 2),
            'total_cuotas': round(total_cuotas, 2),
        })
        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="amortizacion.pdf"'
        return response

@admin_required
def consulta_aprobacion(request):
    return render(request, 'operativo/consulta_aprobacion.html', {'titulo': 'Operativo', 'categoria_actual': 'operativo'})

@admin_required
def ahorros(request):
    if request.method == 'POST':
        # Procesar los datos enviados por el formulario
        accion = request.POST.get('accion', '')
        ah_no_socio = request.POST.get('ah_no_socio', '')
        valor_aporte = request.POST.get('ah_saldo', '')

        # Validar y procesar el aporte
        if accion == 'guardar' and ah_no_socio and valor_aporte:
            try:
                # Validar que el valor del aporte sea positivo
                valor_aporte_decimal = Decimal(valor_aporte)
                if valor_aporte_decimal <= 0:
                    messages.error(request, "El valor del aporte debe ser mayor a cero.")
                    return redirect('ahorros')

                # Obtener el socio
                socio = PerfilUsuario.objects.get(user__id=ah_no_socio)
                
                # Obtener o crear la cuenta de ahorros
                cuenta, created = CuentasAhorros.objects.get_or_create(
                    ah_no_socio=socio,
                    defaults={'ah_saldo': Decimal('0.00')}
                )
                
                # Sumar el aporte al saldo actual
                saldo_anterior = cuenta.ah_saldo
                cuenta.ah_saldo += valor_aporte_decimal
                cuenta.save()

                # Generar el PDF del recibo
                return generar_recibo_aporte_pdf(request, socio, valor_aporte_decimal, saldo_anterior, cuenta.ah_saldo)

            except PerfilUsuario.DoesNotExist:
                messages.error(request, "El socio seleccionado no existe.")
            except ValueError:
                messages.error(request, "El valor del aporte debe ser un número válido.")
            except Exception as e:
                messages.error(request, f"Error al procesar el aporte: {str(e)}")

    # Renderizar la plantilla de ahorros
    return render(request, 'operativo/ahorros.html', {
        'titulo': 'Operativo',
        'categoria_actual': 'operativo',
        'valores_ingresados': {
            'buscar': '',
            'ah_saldo': '',
        },
    })

@admin_required
def generar_recibo_aporte_pdf(request, socio, valor_aporte, saldo_anterior, saldo_actual):
    """Genera un PDF con el recibo del aporte realizado"""
    try:
        # Obtener representantes para el encabezado
        representantes = Representantes.objects.first()
        
        # Convertir logo a base64 para incluir en PDF
        logo_base64 = ""
        try:
            possible_paths = [
                os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png'),
                os.path.join(settings.BASE_DIR, 'staticfiles', 'img', 'logo.png'),
            ]
            
            if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
                possible_paths.insert(0, os.path.join(settings.STATIC_ROOT, 'img', 'logo.png'))
            
            if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
                for static_dir in settings.STATICFILES_DIRS:
                    possible_paths.insert(0, os.path.join(static_dir, 'img', 'logo.png'))
            
            for logo_path in possible_paths:
                if os.path.exists(logo_path):
                    with open(logo_path, 'rb') as logo_file:
                        logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
                    break
        except Exception as e:
            pass

        # Renderizar template HTML para el recibo
        html_string = render_to_string('pdf/recibo_aporte.html', {
            'socio': socio,
            'valor_aporte': valor_aporte,
            'saldo_anterior': saldo_anterior,
            'saldo_actual': saldo_actual,
            'fecha_aporte': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'representantes': representantes,
            'logo_base64': logo_base64,
        })
        
        # Generar PDF
        pdf_file = HTML(string=html_string).write_pdf()
        
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="recibo_aporte_{socio.user.id}_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
        return response
        
    except Exception as e:
        messages.error(request, f"Error al generar el recibo: {str(e)}")
        return redirect('ahorros')

def obtener_saldo_usuario_por_id(user_id):
    """Obtiene el saldo actual de un socio por su user_id"""
    try:
        socio = PerfilUsuario.objects.get(user__id=user_id)
        cuenta = CuentasAhorros.objects.filter(ah_no_socio=socio).first()
        saldo = cuenta.ah_saldo if cuenta else Decimal('0.00')
        return saldo
    except PerfilUsuario.DoesNotExist:
        return Decimal('0.00')
    except Exception as e:
        return Decimal('0.00')

@admin_required
def obtener_saldo_usuario(request):
    """Obtiene el saldo actual de un socio"""
    socio_id = request.GET.get('socio_id')
    if socio_id:
        try:
            socio = PerfilUsuario.objects.get(id=socio_id)
            cuenta = CuentasAhorros.objects.filter(ah_no_socio=socio).first()
            saldo = cuenta.ah_saldo if cuenta else Decimal('0.00')
            return JsonResponse({'saldo': str(saldo)})
        except PerfilUsuario.DoesNotExist:
            return JsonResponse({'saldo': '0.00'})
        except Exception as e:
            return JsonResponse({'saldo': '0.00'})
    return JsonResponse({'saldo': '0.00'})



@admin_required
def ahorro_futuro(request):
    return render(request, 'operativo/ahorro_futuro.html', {'titulo': 'Operativo', 'categoria_actual': 'operativo'})

@admin_required
def deb_cetificados(request):
    return render(request, 'operativo/deb_cetificados.html', {'titulo': 'Operativo', 'categoria_actual': 'operativo'})

@admin_required
def pagos_rol(request):
    return render(request, 'operativo/pagos_rol.html', {'titulo': 'Operativo', 'categoria_actual': 'operativo'})

@admin_required
def caja(request):
    return render(request, 'operativo/caja.html', {'titulo': 'Operativo', 'categoria_actual': 'operativo'})

@admin_required
def reportes(request):
    return render(request, 'operativo/reportes.html', {'titulo': 'Operativo', 'categoria_actual': 'operativo'})

@admin_required
def cierre_diario(request):
    return render(request, 'operativo/cierre_diario.html', {'titulo': 'Operativo', 'categoria_actual': 'operativo'})

@admin_required
def distrib_excedente(request):
    return render(request, 'operativo/distrib_excedente.html', {'titulo': 'Operativo', 'categoria_actual': 'operativo'})


@admin_required
def reporte_socios_pdf(request):    
    
    socios = PerfilUsuario.objects.filter(rol__rol_nombre__iexact='Socio').order_by('user__last_name', 'user__first_name')    
    representantes = Representantes.objects.first()
    
    total_socios = socios.count()
    socios_activos = socios.filter(estado=True).count()
    socios_inactivos = socios.filter(estado=False).count()
    
    # Convertir logo a base64 para incluir en PDF
    logo_base64 = ""
    try:
        # Intentar diferentes rutas para el logo
        possible_paths = [
            os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png'),
            os.path.join(settings.BASE_DIR, 'staticfiles', 'img', 'logo.png'),
        ]
        
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            possible_paths.insert(0, os.path.join(settings.STATIC_ROOT, 'img', 'logo.png'))
        
        if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
            for static_dir in settings.STATICFILES_DIRS:
                possible_paths.insert(0, os.path.join(static_dir, 'img', 'logo.png'))
        
        for logo_path in possible_paths:
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as logo_file:
                    logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
                break
    except Exception as e:
        # Si no se puede cargar el logo, continuar sin él
        pass
    
    # Renderizar template HTML
    html_string = render_to_string('pdf/reporte_socios.html', {
        'socios': socios,
        'representantes': representantes,
        'fecha_generacion': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'total_socios': total_socios,
        'socios_activos': socios_activos,
        'socios_inactivos': socios_inactivos,
        'logo_base64': logo_base64,
        'titulo_reporte': 'REPORTE GENERAL DE SOCIOS',
        'titulo_documento': 'Reporte de Socios - CAPUPEC',
        'info_adicional': f'Total de registros: {total_socios}',
    })
    
    # Generar PDF
    pdf_file = HTML(string=html_string).write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reporte_socios_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
    return response