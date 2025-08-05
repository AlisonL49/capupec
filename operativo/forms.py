# SOLICITUDES DE CREDITO
from django import forms
from operativo.models import SolicitudesCredito, CuentasAhorros

class CuentasAhorrosForm(forms.ModelForm):
    class Meta:
        model = CuentasAhorros
        fields = [
            'ah_no_socio', 'ah_saldo'
        ]

class SolicitudesCreditoForm(forms.ModelForm):
    class Meta:
        model = SolicitudesCredito
        fields = [
            'sol_socio', 'sol_tipo_credito', 'sol_forma_pago','sol_tipo_tabla',
            'sol_nro_solicitud', 'sol_monto', 'sol_cuotas', 'sol_disponible', 'sol_comision',
            'sol_valor_encaje', 'sol_monto_total', 'sol_valor_cuota', 'sol_garante', 'sol_nombres_garante',
            'sol_nro_garante', 'sol_s_creditos'
        ]

    def clean_nro_solicitu(self):
        nro_solicitud = self.cleaned_data.get("nro_solicitud")
        if SolicitudesCredito.objects.filter(nro_solicitud=nro_solicitud).exists():
            raise forms.ValidationError("Ya se ha registrado una solicitud con este número.")
        return nro_solicitud


