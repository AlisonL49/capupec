from django.shortcuts import render,redirect
from django.contrib import messages
from socios.forms import SimulacionCreditoForm
from socios.models import SimulacionCredito
from sistema.views import socio_required
from django.contrib.auth.decorators import login_required

def acceso_denegado(request):
    return render(request, 'socios/acceso_denegado.html', status=403)

@socio_required
def dashboard(request):
    # Datos de ejemplo (puedes reemplazarlos con datos reales de tu base de datos)
    context = {
        'user': request.user,  # Usuario logueado
        'saldo_actual': 5000.00,
        'ahorro_futuro': 2000.00,
        'credito_disponible': 3000.00,
        'transacciones': [
            {'tipo': 'deposito', 'fecha': '01/01/2024', 'valor': 1000.00, 'saldo_despues': 6000.00},
            {'tipo': 'retiro', 'fecha': '02/01/2024', 'valor': 500.00, 'saldo_despues': 5500.00},
            {'tipo': 'deposito', 'fecha': '03/01/2024', 'valor': 2000.00, 'saldo_despues': 7500.00},
            {'tipo': 'retiro', 'fecha': '04/01/2024', 'valor': 1000.00, 'saldo_despues': 6500.00},
        ],
    }
    return render(request, 'socios/dashboard.html', context )

@socio_required
def simulador(request):
    #Página inicial donde se ingresa la simulación de crédito
    if request.method == "POST":
        form = SimulacionCreditoForm(request.POST)
        if form.is_valid():
            simulacion = form.save()
            return redirect('resultado', simulacion_id=simulacion.id)
    else:
        form = SimulacionCreditoForm()
    return render(request, 'socios/simulador.html', { 'categoria_actual': 'socios','form': form})

@socio_required
def resultado_simulacion(request, simulacion_id):
    #Página donde se muestra la simulación del crédito
    simulacion = SimulacionCredito.objects.get(id=simulacion_id)
    cuota_mensual, monto_total = simulacion.calcular_amortizacion_francesa()

    return render(request, 'socios/resultado_simulacion.html', {
        'simulacion': simulacion,
        'cuota_mensual': cuota_mensual,
        'monto_total': monto_total
    })

@socio_required
def info_capupec(request):
    return render(request, 'socios/info_capupec.html',  {'categoria_actual':'socios'})


@socio_required
def perfil_usuario(request):
    #Muestra los datos del usuario logueado.
    return render(request, 'socios/perfil.html', { 'categoria_actual':'socios', 'usuario': request.user})

