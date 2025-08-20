from datetime import datetime, timedelta
from decimal import Decimal



def generar_amortizacion_francesa(monto, cuotas, interes_anual):
    interes_mensual = Decimal(interes_anual) / 12 / 100
    cuota = monto * (interes_mensual * (1 + interes_mensual)**cuotas) / ((1 + interes_mensual)**cuotas - 1)
    saldo = monto
    tabla = []
    total_interes = Decimal('0.00')
    total_seguro = Decimal('0.00')
    fecha_inicio = datetime.today()

    for i in range(1, cuotas + 1):
        interes = saldo * interes_mensual
        capital = cuota - interes
        saldo -= capital
        seguro = saldo * Decimal('0.04')
        total_interes += interes
        total_seguro += seguro

        tabla.append({
            'numero': i,
            'fecha_pago': (fecha_inicio + timedelta(days=30 * i)).strftime('%d/%m/%Y'),
            'capital': round(capital, 2),
            'interes': round(interes, 2),
            'seguro': round(seguro, 2),
            'cuota_total': round(cuota + seguro, 2),
            'saldo': round(max(saldo, 0), 2)
        })

    return tabla, total_interes, total_seguro
