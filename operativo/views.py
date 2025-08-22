import os
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Q
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from administracion.models import FormasPago, Representantes, TiposCredito, Parametros
from usuarios.models import Roles, EstadoCivil, PerfilUsuario
from .models import CreditosAprobados, CuentasAhorros, HistorialTransacciones, SolicitudesCredito, PagosCredito, estadosSolicitud
from sistema.views import resultados_busqueda, admin_required
from weasyprint import HTML
import base64

from .validaciones import (validar_solicitud_credito_completa, mostrar_errores_validacion, validar_monto_y_cuotas_segun_tipo_credito)

# Helper function to get the base64 encoded logo

def get_logo_base64():
    logo_base64 = ""
    try:
        # Possible paths for the logo
        possible_paths = [
            os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.png'),
            os.path.join(settings.BASE_DIR, 'staticfiles', 'img', 'logo.png'),
        ]

        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            possible_paths.insert(0, os.path.join(
                settings.STATIC_ROOT, 'img', 'logo.png'))

        if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
            for static_dir in settings.STATICFILES_DIRS:
                possible_paths.insert(0, os.path.join(
                    static_dir, 'img', 'logo.png'))

        for logo_path in possible_paths:
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as logo_file:
                    logo_base64 = base64.b64encode(
                        logo_file.read()).decode('utf-8')
                break
    except Exception as e:
        pass # Continue without logo if loading fails

    return logo_base64

@csrf_exempt
@admin_required
def get_credit_details(request):
    if request.method == "GET":
        tipo_credito_id = request.GET.get("tipo_credito_id")
        tipo_credito = get_object_or_404(TiposCredito, pk=tipo_credito_id)
        response_data = {
            "interes": tipo_credito.tcredito_tasa_interes,
            "gracia": tipo_credito.tcredito_gracia,
            "min_aporte": tipo_credito.tcredito_aporte_minimo,
        }
        return JsonResponse(response_data)


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



def solicitud(request):
    """
    Vista completa para solicitud de crédito con validaciones integradas
    """
    # Inicializar variables
    usuarios = PerfilUsuario.objects.all().order_by('user__last_name', 'user__first_name')
    tipos_credito = TiposCredito.objects.filter(tcredito_estado=True)
    formas_pago = FormasPago.objects.filter(fpago_estado=True)
    
    socio_seleccionado = None
    v_solicitud = Decimal('0.00')
    comision = ''
    v_encaje = ''
    monto_total = ''
    suma_capital = Decimal('0.00')
    suma_interes = Decimal('0.00')
    suma_seguro = Decimal('0.00')
    valores_ingresados = {}
    tabla_amortizacion = []
    search_query = ''
    category = ''

    # Aplicar búsqueda
    usuarios, search_query, category = resultados_busqueda(
        request,
        usuarios,
        search_fields=['user__first_name', 'user__last_name']
    )

    # Obtener socio seleccionado por búsqueda
    if 'seleccionar' in request.GET:
        try:
            usuario_id = request.GET.get('seleccionar')
            if not usuario_id:
                messages.error(request, "ID de usuario no proporcionado")
                return redirect('solicitud')
            
            socio_seleccionado = get_object_or_404(PerfilUsuario, pk=usuario_id, user__is_active=True)
            
            # Validar que el socio esté activo
            if not socio_seleccionado.estado:
                messages.error(request, "El socio seleccionado no está activo.")
                return redirect('solicitud')

            # Datos aportes con annotate
            aportes_info = HistorialTransacciones.objects.filter(
                trans_usuario=socio_seleccionado, trans_tipo="ahorro"
            ).aggregate(
                nro_aportes=Count("id"),
                valor_aportes=Sum("trans_valor")
            )

            condicion = socio_seleccionado.nombramiento
            disponible = CuentasAhorros.objects.filter(ah_no_socio=socio_seleccionado).first()
            disponible_saldo = disponible.ah_saldo if disponible else Decimal("0.00")

            # Generar Nro. Solicitud
            ultimo = SolicitudesCredito.objects.order_by("-id").first()
            nro_solicitud = f"SC{(ultimo.id + 1) if ultimo else 1:03d}"

            valores_ingresados.update({
                "nro_aportes": aportes_info["nro_aportes"] or 0,
                "valor_aportes": aportes_info["valor_aportes"] or Decimal("0.00"),
                "condicion": condicion,
                "disponible": disponible_saldo,
                "nro_solicitud": nro_solicitud
            })

            request.session['valores_ingresados'] = {
                "solicitud_id": str(nro_solicitud),
            }

            # Si tiene garante, calcular S. Créditos
            garante_id = request.POST.get("sol_nro_garante") if request.method == "POST" else None
            if garante_id:
                try:
                    garante_seleccionado = get_object_or_404(PerfilUsuario, pk=garante_id)
                    s_creditos = CreditosAprobados.objects.filter(
                        socio=garante_seleccionado
                    ).aggregate(
                        total_saldo=Sum("cred_saldo")
                    )["total_saldo"] or 0
                except Exception as e:
                    messages.error(request, f"Error al validar garante: {str(e)}")

        except Exception as e:
            messages.error(request, f"Error al seleccionar socio: {str(e)}")
            return redirect('solicitud')

    # Acción calcular con validaciones completas
    if request.method == "POST" and request.POST.get("accion") == "calcular":
        selected_tipo_credito = request.POST.get("sol_tipo_credito")
        selected_forma_pago = request.POST.get("sol_forma_pago")
        try:
            # Ejecutar todas las validaciones
            es_valido, datos_limpios, errores = validar_solicitud_credito_completa(request)
            
            if not es_valido:
                # Mostrar errores y continuar para mostrar el formulario
                mostrar_errores_validacion(request, errores)
                # Mantener el socio seleccionado si existe
                socio_id = request.POST.get("sol_socio")
                if socio_id:
                    try:
                        socio_seleccionado = get_object_or_404(PerfilUsuario, pk=socio_id)
                    except:
                        pass
            else:
                # Datos validados y limpios
                socio_seleccionado = datos_limpios['socio']
                tipo_credito = datos_limpios['tipo_credito']
                forma_pago = datos_limpios['forma_pago_id']
                monto = datos_limpios['monto']
                cuotas = datos_limpios['cuotas']
                
                # Mostrar información de límites aplicados
                messages.success(
                    request,
                    f"Validación exitosa - Monto: {monto:,.2f}, Cuotas: {cuotas} "
                    f"(Límites del tipo '{tipo_credito.tcredito_tipo}': "
                    f"Monto máx: {tipo_credito.tcredito_monto_maximo:,.2f}, "
                    f"Cuotas máx: {tipo_credito.tcredito_num_cuotas})"
                )

                valores_ingresados.update({
                "selected_tipo_credito": selected_tipo_credito,
                "selected_forma_pago": selected_forma_pago,
                "monto": monto,
                "forma_pago": forma_pago,
                "cuotas": cuotas,
                })
                
                # Calcular parámetros del crédito
                tasa_mensual = Decimal(tipo_credito.tcredito_tasa_interes) / Decimal(100) / 12
                tasa_mensual = tasa_mensual.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)

                try:
                    comision_param = get_object_or_404(Parametros, parm_abreviatura="COMISION")
                    seguro_param = get_object_or_404(Parametros, parm_abreviatura="SEGRAVAMEN")
                except Exception as e:
                    messages.error(request, f"Error al obtener parámetros del sistema: {str(e)}")
                    return redirect('solicitud')

                seguro_valor = Decimal(seguro_param.parm_valor) / Decimal(100)
                v_solicitud = monto
                comision = Decimal(comision_param.parm_valor) * cuotas
                v_encaje = (Decimal(tipo_credito.tcredito_porcentaje_encaje) / 100) * monto

                
                tabla_amortizacion = []
                
                # Calcular cuota fija
                if tasa_mensual > 0:
                    cuota_fija = (monto * tasa_mensual) / (Decimal(1) - (Decimal(1) + tasa_mensual) ** (-cuotas))
                else:
                    cuota_fija = monto / cuotas  # Para créditos sin interés
                
                cuota_fija = cuota_fija.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                saldo = monto
                suma_capital = Decimal('0.00')
                suma_interes = Decimal('0.00')
                suma_seguro = Decimal('0.00')

                # Agregar fila inicial (período 0)
                tabla_amortizacion.append({
                    "numero": 0,
                    "fecha_pago": date.today(),
                    "capital": Decimal('0.00'),
                    "interes": Decimal('0.00'),
                    "seguro": Decimal('0.00'),
                    "cuota_total": Decimal('0.00'),
                    "saldo": saldo
                })

                # Calcular cada período
                for i in range(1, cuotas + 1):
                    # Calcular interés y seguro sobre saldo pendiente
                    interes = (saldo * tasa_mensual).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    seguro = (saldo * seguro_valor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    
                    # Capital es la diferencia entre cuota fija e interés
                    capital = cuota_fija - interes
                    capital = capital.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    
                    # Ajustar última cuota para que no quede saldo residual
                    if i == cuotas:
                        capital = saldo
                        cuota_total = capital + interes + seguro
                    else:
                        cuota_total = cuota_fija + seguro
                    
                    # Actualizar saldo
                    saldo -= capital
                    if saldo < 0:
                        saldo = Decimal('0.00')
                    
                    # Agregar a tabla
                    tabla_amortizacion.append({
                        "numero": i,
                        "fecha_pago": date.today() + timedelta(days=30 * i),
                        "capital": capital,
                        "interes": interes,
                        "seguro": seguro,
                        "cuota_total": cuota_total,
                        "saldo": saldo
                    })
                    
                    # Acumular totales
                    suma_capital += capital
                    suma_interes += interes
                    suma_seguro += seguro

                # Calcular monto total
                monto_total = (v_solicitud + comision + suma_interes + suma_seguro).quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP
                )

                # Guardar en sesión con validación
                try:
                    request.session['valores_credito'] = {
                        "cuotas": str(cuotas),
                        "interes": str(tipo_credito.tcredito_tasa_interes),
                        "v_solicitud": str(v_solicitud),
                        "comision": str(comision),
                        "v_encaje": str(v_encaje),
                        "suma_capital": str(suma_capital),
                        "suma_interes": str(suma_interes),
                        "suma_seguro": str(suma_seguro),
                        "monto_total": str(monto_total),
                    }
                    
                    # Convertir tabla para JSON
                    tabla_json = []
                    for fila in tabla_amortizacion:
                        tabla_json.append({
                            "numero": fila["numero"],
                            "fecha_pago": fila["fecha_pago"].isoformat(),
                            "capital": float(fila["capital"]),
                            "interes": float(fila["interes"]),
                            "seguro": float(fila["seguro"]),
                            "cuota_total": float(fila["cuota_total"]),
                            "saldo": float(fila["saldo"])
                        })
                    
                    request.session['tabla_amortizacion'] = tabla_json
                    
                except Exception as e:
                    messages.error(request, f"Error al guardar datos en sesión: {str(e)}")

        except Exception as e:
            messages.error(request, f"Error en el cálculo del crédito: {str(e)}")
            return redirect('solicitud')
        
    

    # Acción guardar (placeholder - implementar según tus necesidades)
    elif request.method == "POST" and request.POST.get("accion") == "guardar":
        try:
            # Validar que existan datos de cálculo en sesión
            if 'valores_credito' not in request.session:
                messages.error(request, "Debe calcular el crédito antes de guardarlo")
                return redirect('solicitud')
            
            valores_credito = request.session.get("valores_credito", {})
            
            comision = Decimal(valores_credito.get("comision", "0.00"))
            v_encaje = Decimal(valores_credito.get("v_encaje", "0.00"))
            monto_total = Decimal(valores_credito.get("monto_total", "0.00"))

            # Ejecutar validaciones antes de guardar
            es_valido, datos_limpios, errores = validar_solicitud_credito_completa(request)
            
            if not es_valido:
                mostrar_errores_validacion(request, errores)
                return redirect('solicitud')

            socio = datos_limpios['socio']
            tipo_credito = datos_limpios['tipo_credito']
            forma_pago = get_object_or_404(FormasPago, pk=datos_limpios['forma_pago_id'])

            SolicitudesCredito.objects.create(
                sol_nombre='',
                sol_socio=socio,
                sol_tipo_credito=tipo_credito,
                sol_forma_pago=forma_pago,
                sol_tipo_tabla_id=1,  # Ajusta según tu diseño
                sol_nro_solicitud=nro_solicitud,
                sol_monto=datos_limpios['monto'],
                sol_cuotas=datos_limpios['cuotas'],
                sol_comision=comision,
                sol_valor_encaje=v_encaje,
                sol_monto_total=monto_total,
                sol_estado=get_object_or_404(estadosSolicitud, estado_nombre='Pendiente')
            )

            messages.success(request, "Solicitud de crédito guardada exitosamente")
            
            # Limpiar sesión después de guardar
            request.session.pop('valores_credito', None)
            request.session.pop('valores_ingresados', None)
            request.session.pop('tabla_amortizacion', None)

        except Exception as e:
            messages.error(request, f"Error al guardar la solicitud: {str(e)}")


    # Recuperar datos de sesión si existen
    '''try:
        if 'valores_credito' in request.session:
            valores_sesion = request.session['valores_credito']
            v_solicitud = Decimal(valores_sesion.get('v_solicitud', '0.00'))
            comision = Decimal(valores_sesion.get('comision', '0.00'))
            v_encaje = Decimal(valores_sesion.get('v_encaje', '0.00'))
            suma_capital = Decimal(valores_sesion.get('suma_capital', '0.00'))
            suma_interes = Decimal(valores_sesion.get('suma_interes', '0.00'))
            suma_seguro = Decimal(valores_sesion.get('suma_seguro', '0.00'))
            monto_total = Decimal(valores_sesion.get('monto_total', '0.00'))
        
        if 'tabla_amortizacion' in request.session:
            tabla_sesion = request.session['tabla_amortizacion']
            tabla_amortizacion = []
            for fila in tabla_sesion:
                tabla_amortizacion.append({
                    "numero": fila["numero"],
                    "fecha_pago": date.fromisoformat(fila["fecha_pago"]) if isinstance(fila["fecha_pago"], str) else fila["fecha_pago"],
                    "capital": Decimal(str(fila["capital"])),
                    "interes": Decimal(str(fila["interes"])),
                    "seguro": Decimal(str(fila["seguro"])),
                    "cuota_total": Decimal(str(fila["cuota_total"])),
                    "saldo": Decimal(str(fila["saldo"]))
                })
    
    except Exception as e:
        messages.warning(request, f"Error al recuperar datos de sesión: {str(e)}")
        # Limpiar sesión corrupta
        if 'valores_credito' in request.session:
            del request.session['valores_credito']
        if 'tabla_amortizacion' in request.session:
            del request.session['tabla_amortizacion'] '''

    # Preparar contexto para el template
    context = {
        'titulo': 'Operativo',
        'categoria_actual': 'operativo',
        'usuarios': usuarios,
        'tipos_credito': tipos_credito,
        'formas_pago': formas_pago,
        'valores_ingresados': valores_ingresados,
        'tabla_amortizacion': tabla_amortizacion,
        'v_solicitud': v_solicitud,
        'comision': comision,
        'v_encaje': v_encaje,
        'suma_capital': suma_capital,
        'suma_interes': suma_interes,
        'suma_seguro': suma_seguro,
        'monto_total': monto_total,
        'socio_seleccionado': socio_seleccionado,
        'search_query': search_query,
        'selected_category': category,
    }

    return render(request, 'operativo/solicitud.html', context)



# Función auxiliar para limpiar sesión
def limpiar_sesion_credito(request):
    """
    Limpia los datos de sesión relacionados con el cálculo de crédito
    """
    keys_to_remove = ['valores_credito', 'tabla_amortizacion', 'valores_ingresados']
    for key in keys_to_remove:
        if key in request.session:
            del request.session[key]


# Decorador para manejo de errores
from functools import wraps

def handle_credito_errors(view_func):
    """
    Decorador para manejo centralizado de errores en vistas de crédito
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f"Error inesperado: {str(e)}")
            # Log del error para debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en {view_func.__name__}: {str(e)}", exc_info=True)
            return redirect('solicitud')
    return wrapper


# Vista con decorador de manejo de errores
@handle_credito_errors
def solicitud_segura(request):
    """
    Versión de la vista con decorador de manejo de errores
    """
    return solicitud(request)



def imprimir_solicitud_credito(request, socio_id):
    socio = get_object_or_404(PerfilUsuario, pk=socio_id)
    tabla_amortizacion = request.session.get("tabla_amortizacion", [])
    valores_credito = request.session.get("valores_credito", {})

    solicitud_id = request.session.get("valores_ingresados", {}).get("solicitud_id")

    logo_base64 = get_logo_base64()

    html_string = render_to_string("pdf/solicitud_credito.html", {
        "socio": socio,
        "fecha": date.today(),
        "solicitud_id": solicitud_id,
        "tabla_amortizacion": tabla_amortizacion,
        **valores_credito,
        'logo_base64': logo_base64,
        'fecha_generacion': datetime.now().strftime('%d/%m/%Y %H:%M'),        
        'titulo_reporte': 'SOLICITUD DE CRÉDITO',
        'titulo_documento': 'Reporte de Solicitud - CAPUPEC',
        
    })
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = f'inline; filename="solicitud_credito_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
    return response



@admin_required
def consulta_aprobacion(request):
    q = request.GET.get("q", "")
    solicitudes = SolicitudesCredito.objects.select_related("sol_socio__user", "sol_estado")

    if q:
        solicitudes = solicitudes.filter(
            Q(sol_socio__user__username__icontains=q) | 
            Q(sol_socio__user__first_name__icontains=q) | 
            Q(sol_socio__user__last_name__icontains=q)
        )
    
    solicitudes = solicitudes.order_by("-id")

    # Paginación
    paginator = Paginator(solicitudes, 10)  # 10 por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'titulo': 'Operativo',
        'categoria_actual': 'operativo',        
        "page_obj": page_obj,
    }
    return render(request, 'operativo/consulta_aprobacion.html', context)



# Vista detalle para cargar en modal

def solicitud_detalle(request, solicitud_id):
    """ Devuelve el HTML del modal de detalle """
    
    solicitud = get_object_or_404(SolicitudesCredito, id=solicitud_id)
    socio = solicitud.sol_socio

    # Aportes en ahorros (cantidad y valor total)
    aportes_info = HistorialTransacciones.objects.filter(
        trans_usuario=socio,
        trans_tipo="ahorro"
    ).aggregate(
        cantidad_aportes=Count("id"),
        total_aportes=Sum("trans_valor")
    )

    # Créditos activos y saldo total
    '''creditos_info = CreditosAprobados.objects.filter(
        credito_usuario=socio,
        credito_estado=True  
    ).aggregate(
        cantidad_creditos=Count("id"),
        saldo_creditos=Sum("credito_saldo")
    )'''

    # Saldo disponible en cuenta de ahorros
    cuenta = CuentasAhorros.objects.filter(ah_no_socio=socio).first()
    saldo_disponible = cuenta.ah_saldo if cuenta else 0

    context = {
        "solicitud": solicitud,
        "cantidad_aportes": aportes_info["cantidad_aportes"] or 0,
        "aportes_total": aportes_info["total_aportes"] or 0,
        #"creditos_activos": creditos_info["cantidad_creditos"] or 0,
        #"saldo_creditos": creditos_info["saldo_creditos"] or 0,
        "saldo_disponible": saldo_disponible,
        "nombramiento": socio.nombramiento,
    }
    return render(request, "operativo/includes/detalle_solicitud.html", context)

# Aprobar/Rechazar solicitud
@require_POST
def actualizar_estado_solicitud(request, solicitud_id, accion):
    solicitud = get_object_or_404(SolicitudesCredito, id=solicitud_id)
    try:
        if accion == "aprobar":
            solicitud.sol_estado = get_object_or_404(estadosSolicitud, estado_nombre="Aprobado")
            solicitud.sol_observacion = "Solicitud aprobada"
            solicitud.save()
            return JsonResponse({"success": True, "estado": "Aprobada"})

        elif accion == "preaprobar":
            observacion = request.POST.get("observacion", "").strip()
            if not observacion:
                return JsonResponse({"success": False, "error": "Debe ingresar una observación para preapobar"})
            solicitud.sol_estado = get_object_or_404(estadosSolicitud, estado_nombre="Preaprobado")
            solicitud.sol_observacion = observacion
            solicitud.save()
            return JsonResponse({"success": True, "estado": "Preaprobada"})
       
        elif accion == "rechazar":
            observacion = request.POST.get("observacion", "").strip()
            if not observacion:
                return JsonResponse({"success": False, "error": "Debe ingresar una observación para rechazar"})

            solicitud.sol_estado = get_object_or_404(estadosSolicitud, estado_nombre="Rechazado")
            solicitud.sol_observacion = observacion
            solicitud.save()
            return JsonResponse({"success": True, "estado": "Rechazada"})

        else:
            return JsonResponse({"success": False, "error": "Acción no válida"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

@admin_required
def ahorros(request):
    if request.method == 'POST':
        accion = request.POST.get('accion')
        socio_id = request.POST.get('ah_no_socio')

        if not socio_id:
            messages.error(request, 'Debe seleccionar un socio válido.')
            return redirect('ahorros')

        usuario = get_object_or_404(PerfilUsuario, user__id=socio_id)

        if accion == 'crear_cuenta':
            if CuentasAhorros.objects.filter(ah_no_socio=usuario).exists():
                messages.warning(
                    request, 'El socio ya tiene una cuenta de ahorros.')
            else:
                CuentasAhorros.objects.create(ah_no_socio=usuario, ah_saldo=0)
                messages.success(
                    request, 'Cuenta de ahorros creada correctamente.')

            return redirect('ahorros')

    return render(request, 'operativo/ahorros.html', {
        'titulo': 'Operativo',
        'categoria_actual': 'operativo',

    })


def obtener_saldo_usuario_por_id(user_id):
    """Obtiene el saldo actual de un socio por su user_id"""
    try:
        socio = PerfilUsuario.objects.get(user__id=user_id)
        cuenta = CuentasAhorros.objects.filter(ah_no_socio=socio).first()
        saldo = cuenta.ah_saldo if cuenta else Decimal('0.00')
        return saldo
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


def registrar_aporte(request):
    if request.method == 'POST':
        socio_id = request.POST.get('ah_no_socio')
        valor_aporte = request.POST.get('ah_saldo')

        if not socio_id or not valor_aporte:
            return JsonResponse({'success': False, 'error': 'Datos incompletos'}, status=400)

        try:
            usuario = get_object_or_404(PerfilUsuario, user__id=socio_id)
            cuenta = get_object_or_404(CuentasAhorros, ah_no_socio=usuario)
            aporte_decimal = Decimal(valor_aporte)
            cuenta.ah_saldo += aporte_decimal
            cuenta.save()

            HistorialTransacciones.objects.create(
                trans_usuario=usuario,
                trans_tipo='ahorro',
                trans_valor=aporte_decimal,
                trans_saldo=cuenta.ah_saldo,
                trans_fecha=datetime.now()
            )

            pdf_url = reverse('generar_recibo_pdf', args=[
                              socio_id, valor_aporte])

            return JsonResponse({
                "success": True,
                "usuario_id": socio_id,
                "aporte": valor_aporte,
                "pdf_url": pdf_url,
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)


@xframe_options_exempt
def generar_recibo_pdf(request, usuario_id, aporte):
    usuario = get_object_or_404(PerfilUsuario, user__id=usuario_id)
    cuenta = get_object_or_404(CuentasAhorros, ah_no_socio=usuario)
    ultima_transaccion = HistorialTransacciones.objects.order_by('-id').first()
    numero_recibo = ultima_transaccion.id

    context = {
        'fecha': datetime.now(),
        'id': usuario.user.id,
        'nombres': f'{usuario.user.first_name} {usuario.user.last_name}',
        'valor_aporte': aporte,
        'saldo': cuenta.ah_saldo,
        'numero_recibo': numero_recibo,
        'nombre_empresa': "Caja de Ahorro y Crédito CAPUPEC",
        'logo_url': request.build_absolute_uri('/static/img/logo.png'),
    }

    html_string = render_to_string('pdf/recibo_aporte.html', context)
    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="recibo_aporte.pdf"'
    return response


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

    socios = PerfilUsuario.objects.filter(rol__rol_nombre__iexact='Socio').order_by(
        'user__last_name', 'user__first_name')
    representantes = Representantes.objects.first()

    total_socios = socios.count()
    socios_activos = socios.filter(estado=True).count()
    socios_inactivos = socios.filter(estado=False).count()

    logo_base64 = get_logo_base64()

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
