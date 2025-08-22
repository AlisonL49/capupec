from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.shortcuts import get_object_or_404
import re

from django.db.models import Sum, Count

def validar_datos_entrada_credito(request):
    """
    Valida todos los datos de entrada para la solicitud de crédito
    Retorna: (es_valido, datos_limpios, errores)
    """
    errores = []
    datos_limpios = {}
    
    try:
        # Validar socio seleccionado
        socio_id = request.POST.get("sol_socio", "").strip()
        if not socio_id:
            errores.append("Debe seleccionar un socio")
        else:
            try:
                socio_id = int(socio_id)
                datos_limpios['socio_id'] = socio_id
            except (ValueError, TypeError):
                errores.append("ID de socio inválido")
        
        # Validar tipo de crédito
        tipo_credito_id = request.POST.get("sol_tipo_credito", "").strip()
        if not tipo_credito_id:
            errores.append("Debe seleccionar un tipo de crédito")
        else:
            try:
                tipo_credito_id = int(tipo_credito_id)
                datos_limpios['tipo_credito_id'] = tipo_credito_id
            except (ValueError, TypeError):
                errores.append("Tipo de crédito inválido")
        
        # Validar forma de pago
        forma_pago_id = request.POST.get("sol_forma_pago", "").strip()
        if not forma_pago_id:
            errores.append("Debe seleccionar una forma de pago")
        else:
            try:
                forma_pago_id = int(forma_pago_id)
                datos_limpios['forma_pago_id'] = forma_pago_id
            except (ValueError, TypeError):
                errores.append("Forma de pago inválida")
        
        # Validar monto
        monto_str = request.POST.get("sol_monto", "").strip()
        if not monto_str:
            errores.append("El monto es obligatorio")
        else:
            try:
                # Limpiar el monto de caracteres no numéricos (excepto punto y coma)
                monto_limpio = re.sub(r'[^\d.,]', '', monto_str)
                monto_limpio = monto_limpio.replace(',', '.')
                
                monto = Decimal(monto_limpio)
                
                # Validaciones básicas de rango
                if monto <= 0:
                    errores.append("El monto debe ser mayor a cero")
                elif monto < Decimal('100'):  # Mínimo 100
                    errores.append("El monto mínimo es de 100")
                else:
                    datos_limpios['monto'] = monto
                    
            except (InvalidOperation, ValueError, TypeError):
                errores.append("El monto debe ser un número válido")
        
        # Validar cuotas
        cuotas_str = request.POST.get("sol_cuotas", "").strip()
        if not cuotas_str:
            errores.append("El número de cuotas es obligatorio")
        else:
            try:
                cuotas = int(cuotas_str)
                
                if cuotas <= 0:
                    errores.append("El número de cuotas debe ser mayor a cero")
                else:
                    datos_limpios['cuotas'] = cuotas
                    
            except (ValueError, TypeError):
                errores.append("El número de cuotas debe ser un número entero válido")
        
        # Validar forma de pago (opcional)
        forma_pago_id = request.POST.get("sol_forma_pago", "").strip()
        if forma_pago_id:
            try:
                forma_pago_id = int(forma_pago_id)
                datos_limpios['forma_pago_id'] = forma_pago_id
            except (ValueError, TypeError):
                errores.append("Forma de pago inválida")
        
        # Validar garante (opcional)
        garante_id = request.POST.get("sol_nro_garante", "").strip()
        if garante_id:
            try:
                garante_id = int(garante_id)
                datos_limpios['garante_id'] = garante_id
            except (ValueError, TypeError):
                errores.append("ID de garante inválido")
        
    
    except Exception as e:
        errores.append(f"Error inesperado en la validación: {str(e)}")
    
    return len(errores) == 0, datos_limpios, errores


def validar_monto_y_cuotas_segun_tipo_credito(monto, cuotas, tipo_credito):
    """
    Valida que el monto y cuotas cumplan con los límites del tipo de crédito
    """
    errores = []
    
    try:
        # Validar monto máximo según tipo de crédito
        if tipo_credito.tcredito_monto_maximo:
            if monto > tipo_credito.tcredito_monto_maximo:
                errores.append(
                    f"El monto solicitado ({monto:,.2f}) excede el límite máximo de "
                    f"{tipo_credito.tcredito_monto_maximo:,.2f} para el tipo de crédito '{tipo_credito.tcredito_tipo}'"
                )
        
        # Validar número máximo de cuotas según tipo de crédito
        if tipo_credito.tcredito_num_cuotas:
            if cuotas > tipo_credito.tcredito_num_cuotas:
                errores.append(
                    f"El número de cuotas solicitado ({cuotas}) excede el máximo permitido de "
                    f"{tipo_credito.tcredito_num_cuotas} cuotas para el tipo de crédito '{tipo_credito.tcredito_tipo}'"
                )
        
        # Validar que el tipo de crédito esté activo
        if not tipo_credito.tcredito_estado:
            errores.append(f"El tipo de crédito '{tipo_credito.tcredito_tipo}' no está disponible actualmente")
    
    except Exception as e:
        errores.append(f"Error al validar límites del tipo de crédito: {str(e)}")
    
    return len(errores) == 0, errores


def validar_socio_credito(socio, tipo_credito, monto_solicitado):
    """
    Valida que el socio cumpla con los requisitos para el crédito
    """
    errores = []
    
    try:
        # Validar que el socio esté activo
        if not socio.estado:
            errores.append("El socio seleccionado no está activo")
        
        if not socio.user.is_active:
            errores.append("El usuario del socio no está activo")
        
        # Validar aportes mínimos
        from .models import HistorialTransacciones
        aportes_info = HistorialTransacciones.objects.filter(
            trans_usuario=socio, 
            trans_tipo="ahorro"
        ).aggregate(
            nro_aportes=Count("id"),
            valor_aportes=Sum("trans_valor")
        )
        
        nro_aportes = aportes_info["nro_aportes"] or 0
        if nro_aportes < tipo_credito.tcredito_aporte_minimo:
            errores.append(
                f"El socio debe tener al menos {tipo_credito.tcredito_aporte_minimo} aportes. "
                f"Actualmente tiene {nro_aportes}"
            )
        
        

        # Validar que no tenga créditos en mora
        '''from .models import CreditosAprobados
        creditos_mora = CreditosAprobados.objects.filter(
            socio=socio,
            cred_estado_mora=True
        ).exists()
        
        if creditos_mora:
            errores.append("El socio tiene créditos en mora y no puede solicitar nuevos créditos")
        '''
        # Validar capacidad de pago (ejemplo básico) o encaje 
        from .models import CuentasAhorros
        cuenta_ahorros = CuentasAhorros.objects.filter(ah_no_socio=socio).first()
        if cuenta_ahorros:
            saldo_disponible = cuenta_ahorros.ah_saldo
            # Regla básica: el saldo debe ser al menos el 10% del monto solicitado
            minimo_requerido = monto_solicitado * Decimal('0.15')
            if saldo_disponible < minimo_requerido:
                errores.append(
                    f"Saldo insuficiente. Se requiere al menos "
                    f"{minimo_requerido:,.2f} en ahorros (15% del monto solicitado)"
                )
        else:
            errores.append("El socio no tiene cuenta de ahorros activa")
    
    except Exception as e:
        errores.append(f"Error al validar el socio: {str(e)}")
    
    return len(errores) == 0, errores


def validar_garante(garante_id, monto_solicitado):
    """
    Valida que el garante cumpla con los requisitos
    """
    errores = []
    
    try:
        from .models import PerfilUsuario, CreditosAprobados
        
        garante = get_object_or_404(PerfilUsuario, pk=garante_id)
        
        # Validar que el garante esté activo
        if not garante.estado:
            errores.append("El garante seleccionado no está activo")
        
        if not garante.user.is_active:
            errores.append("El usuario del garante no está activo")
        
        # Validar capacidad de garantía
        creditos_como_garante = CreditosAprobados.objects.filter(
            garante=garante,
            cred_saldo__gt=0
        ).aggregate(
            total_garantizado=Sum("cred_saldo")
        )["total_garantizado"] or Decimal('0.00')
        
        # Límite máximo de garantía (ejemplo: 5 veces sus ahorros)
        from .models import CuentasAhorros
        cuenta_garante = CuentasAhorros.objects.filter(ah_no_socio=garante).first()
        if cuenta_garante:
            limite_garantia = cuenta_garante.ah_saldo * 5
            total_con_nuevo = creditos_como_garante + monto_solicitado
            
            if total_con_nuevo > limite_garantia:
                errores.append(
                    f"El garante no puede garantizar más créditos. "
                    f"Límite disponible: {limite_garantia - creditos_como_garante}"
                )
        else:
            errores.append("El garante no tiene cuenta de ahorros")
    
    except Exception as e:
        errores.append(f"Error al validar el garante: {str(e)}")
    
    return len(errores) == 0, errores


def validar_parametros_sistema():
    """
    Valida que los parámetros del sistema estén configurados correctamente
    """
    errores = []
    
    try:
        from administracion.models import Parametros
        
        # Validar que existan los parámetros necesarios
        parametros_requeridos = ['COMISION', 'SEGRAVAMEN']
        
        for param in parametros_requeridos:
            try:
                parametro = Parametros.objects.get(parm_abreviatura=param)
                if not parametro.parm_valor:
                    errores.append(f"El parámetro {param} no tiene valor configurado")
                else:
                    try:
                        Decimal(parametro.parm_valor)
                    except (InvalidOperation, ValueError):
                        errores.append(f"El parámetro {param} tiene un valor no numérico")
            except Parametros.DoesNotExist:
                errores.append(f"El parámetro {param} no está configurado en el sistema")
    
    except Exception as e:
        errores.append(f"Error al validar parámetros del sistema: {str(e)}")
    
    return len(errores) == 0, errores


def mostrar_errores_validacion(request, errores):
    """
    Muestra los errores de validación al usuario
    """
    for error in errores:
        messages.error(request, error)


# Función principal de validación que integra todas las validaciones
def validar_solicitud_credito_completa(request):
    """
    Función principal que ejecuta todas las validaciones necesarias
    Retorna: (es_valido, datos_limpios, todos_los_errores)
    """
    todos_los_errores = []
    datos_limpios = {}
    
    # 1. Validar parámetros del sistema
    params_validos, errores_params = validar_parametros_sistema()
    if not params_validos:
        todos_los_errores.extend(errores_params)
        return False, {}, todos_los_errores
    
    # 2. Validar datos de entrada
    entrada_valida, datos_limpios, errores_entrada = validar_datos_entrada_credito(request)
    if not entrada_valida:
        todos_los_errores.extend(errores_entrada)
        return False, {}, todos_los_errores
    
    # 3. Validar socio, tipo de crédito y límites específicos
    try:
        from .models import PerfilUsuario, TiposCredito
        
        socio = get_object_or_404(PerfilUsuario, pk=datos_limpios['socio_id'])
        tipo_credito = get_object_or_404(TiposCredito, pk=datos_limpios['tipo_credito_id'])
        
        # Validar monto y cuotas según el tipo de crédito específico
        limites_validos, errores_limites = validar_monto_y_cuotas_segun_tipo_credito(
            datos_limpios['monto'], datos_limpios['cuotas'], tipo_credito
        )
        if not limites_validos:
            todos_los_errores.extend(errores_limites)
        
        # Validar reglas específicas del socio
        socio_valido, errores_socio = validar_socio_credito(
            socio, tipo_credito, datos_limpios['monto']
        )
        if not socio_valido:
            todos_los_errores.extend(errores_socio)
        
        # Agregar objetos validados a datos_limpios para uso posterior
        datos_limpios['socio'] = socio
        datos_limpios['tipo_credito'] = tipo_credito
        
        
        # 4. Validar garante si está presente
        if 'garante_id' in datos_limpios:
            garante_valido, errores_garante = validar_garante(
                datos_limpios['garante_id'], datos_limpios['monto']
            )
            if not garante_valido:
                todos_los_errores.extend(errores_garante)
    
    except Exception as e:
        todos_los_errores.append(f"Error al validar objetos relacionados: {str(e)}")
    
    es_valido = len(todos_los_errores) == 0
    return es_valido, datos_limpios, todos_los_errores

