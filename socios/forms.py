from django import forms
from .models import SimulacionCredito


class SimulacionCreditoForm(forms.ModelForm):
    class Meta:
        model = SimulacionCredito
        fields = ['simu_nombre', 'simu_tipo_credito', 'simu_monto', 'simu_meses']
        widgets = {
            'tipo_credito': forms.Select(choices=SimulacionCredito.TIPOS_CREDITO),
            'monto': forms.NumberInput(attrs={'step': '0.01'}),
            'meses': forms.NumberInput(attrs={'min': '1'}),
        }
