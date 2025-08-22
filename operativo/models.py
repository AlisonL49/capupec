from django.db import models
from datetime import datetime
from django.utils import timezone
from administracion.models import DestinosCredito, FormasPago, TiposCredito
from usuarios.models import PerfilUsuario
from django.contrib.auth.models import User

class CuentasAhorros(models.Model):
    ah_no_socio = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    #ah_fecha_apertura = models.DateField(default=timezone.now)
    ah_saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.ah_no_socio
    
    class Meta:
        verbose_name = 'CuentaAhorro'
        verbose_name_plural = 'CuentasAhorros'
        db_table = 'cuentasAhorros'


class HistorialTransacciones(models.Model):
    trans_usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    trans_tipo = models.CharField(max_length=10)
    trans_valor = models.DecimalField(max_digits=10, decimal_places=2)
    trans_saldo = models.DecimalField(max_digits=10, decimal_places=2)
    trans_fecha = models.DateTimeField()

    def __str__(self):
        return f"{self.trans_usuario} - {self.trans_tipo} - {self.trans_valor}"

    class Meta:
        ordering = ['-trans_fecha']
        verbose_name = 'Transaccion'
        verbose_name_plural = 'Transacciones'
        db_table = 'transacciones'

class TablasAmortizacion (models.Model):
    tabla_nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tabla_nombre
    
    class Meta: 
        verbose_name= 'TablaAmortizacion'
        verbose_name_plural= 'TablasAmortizaciones'
        db_table = 'tablasAmortizaciones'

class estadosSolicitud(models.Model):
    estado_nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.estado_nombre
    
    class Meta:
        verbose_name = 'EstadoSolicitud'
        verbose_name_plural = 'EstadosSolicitudes'
        db_table = 'estadosSolicitudes'

class SolicitudesCredito(models.Model):
    sol_nombre = models.CharField(max_length=100, null=True, blank=True)
    sol_socio = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    sol_tipo_credito = models.ForeignKey(TiposCredito, on_delete=models.CASCADE)
    sol_forma_pago = models.ForeignKey(FormasPago, on_delete=models.CASCADE)
    sol_tipo_tabla = models.ForeignKey(TablasAmortizacion, on_delete=models.CASCADE, default=1)
    sol_nro_solicitud = models.CharField(max_length=10, unique=True)
    sol_monto = models.DecimalField(max_digits=10, decimal_places=2)
    sol_cuotas = models.IntegerField()
    sol_comision = models.DecimalField(max_digits=10, decimal_places=2)
    sol_valor_encaje = models.DecimalField(max_digits=10, decimal_places=2)
    sol_monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    sol_garante = models.BooleanField(default=False)
    sol_nro_garante = models.IntegerField(null=True, blank=True)
    sol_fecha_solicitud = models.DateField(default=timezone.now)
    sol_estado = models.ForeignKey(estadosSolicitud, on_delete=models.CASCADE)
    sol_observacion = models.TextField(null=True, blank=True, default=" ")



    def __str__(self):
        return f"Solicitud {self.sol_nro_solicitud} - Socio: {self.sol_socio}"

    @property
    def sol_tasa_interes(self):
        return self.sol_tipo_credito.tcredito_tasa_interes

    @property
    def sol_gracia(self):
        return self.sol_tipo_credito.tcredito_gracia
    @property
    def sol_nro_aportes(self):
        return self.sol_tipo_credito.tcredito_num_cuotas

    @property
    def sol_valor_aportes(self):
        return self.sol_tipo_credito.tcredito_aporte_minimo
    
    @property
    def sol_condicion(self):
        return self.sol_socio.nombramiento
    
    class Meta:
                verbose_name= 'SolicitudCredito'
                verbose_name_plural= 'SolicitudesCreditos'
                db_table= 'solicitudesCreditos'


class CreditosAprobados(models.Model):
    credito_solicitud = models.ForeignKey(SolicitudesCredito, on_delete=models.CASCADE)
    credito_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    credito_fecha_aprobacion = models.DateField(default=timezone.now)
    credito_saldo = models.DecimalField(max_digits=10, decimal_places=2)
    credito_estado = models.BooleanField(default=True)

    def __str__(self):
        return f"Credito {self.credito_solicitud.sol_nro_solicitud} "

    class Meta:
        verbose_name = 'CreditoAprobado'
        verbose_name_plural = 'CreditosAprobados'
        db_table = 'creditosAprobados'

class PagosCredito(models.Model):
    pago_credito = models.ForeignKey(CreditosAprobados, on_delete=models.CASCADE)
    pago_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pago_fecha = models.DateField(default=timezone.now)
    pago_monto_capital = models.DecimalField(max_digits=10, decimal_places=2)
    pago_monto_interes = models.DecimalField(max_digits=10, decimal_places=2)
    pago_monto_comision = models.DecimalField(max_digits=10, decimal_places=2)
    pago_monto_seguro = models.DecimalField(max_digits=10, decimal_places=2)
    pago_monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    pago_numero_cuota = models.IntegerField()
    pago_fecha_vencimiento = models.DateField()
    pago_estado = models.BooleanField(default=True)
    pago_saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pago {self.pago_credito.credito_solicitud.sol_nro_solicitud}"

    class Meta:
        verbose_name = 'PagoCredito'
        verbose_name_plural = 'PagosCreditos'
        db_table = 'pagosCreditos'