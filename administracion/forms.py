# REGISTRO DE USUARIOS

from django import forms
from administracion.models import DestinosCredito, FormasPago, InteresAFuturo, InteresAhorros, Parametros, PeriodoContable, Representantes, TiposAFuturos, TiposAhorros, TiposCredito, PlazoFijo



#REGISTRO DE REPRESENTANTES
class RepresentantesForm(forms.ModelForm):
    class Meta:
        model = Representantes
        fields = ['presidente', 'administrador', 'secretario', 'tesorero_aso', 'tesorero']



# REGISTRO DE PARAMETROS
class ParametrosForm(forms.ModelForm):
    class Meta:
        model = Parametros
        fields = [ 'parm_abreviatura', 'parm_descripcion', 'parm_valor', 'parm_estado']

    def clean_parm_abreviatura(self):
        parm_abreviatura = self.cleaned_data.get("parm_abreviatura")
        if Parametros.objects.filter(parm_abreviatura=parm_abreviatura).exists():
            raise forms.ValidationError(
                "El parámetro con esta abreviatura ya existe.")
        return parm_abreviatura

#FORMAS DE PAGO
class FormasPagoForm(forms.ModelForm):
    class Meta:
        model = FormasPago
        fields = ['fpago_codigo', 'fpago_descripcion', 'fpago_estado']

    def clean_fpago_codigo(self):
        fpago_codigo = self.cleaned_data.get("fpago_codigo")
        if FormasPago.objects.filter(fpago_codigo=fpago_codigo).exists():
            raise forms.ValidationError(
                "Esta forma de pago ya existe.")
        return fpago_codigo
    
#DESTINOS DE CREDITO
class DestinosCreditoForm(forms.ModelForm):
    class Meta:
        model = DestinosCredito
        fields = ['dest_codigo', 'dest_descripcion', 'dest_estado']
        
    def clean_dest_codigo(self): 
        dest_codigo = self.cleaned_data.get("dest_codigo")
        if DestinosCredito.objects.filter(dest_codigo=dest_codigo).exists():
            raise forms.ValidationError(
                "Este destino ya está registrado.")
        return dest_codigo
#DEFINICION DE TIPOS PLAZO FIJO 
from django import forms
from administracion.models import PlazoFijo

class PlazoFijoForm(forms.ModelForm):
    class Meta:
        model = PlazoFijo
        fields = '__all__'
        widgets = {
            'pf_fecha_vencimiento': forms.DateInput(
                attrs={
                    'type': 'date',          
                    'class': 'form-control'  
                }
            ),
        }
    
    def clean_pf_descripcion(self):
        descripcion = self.cleaned_data.get("pf_descripcion")
        if PlazoFijo.objects.filter(pf_descripcion=descripcion).exists():
            raise forms.ValidationError("Ya existe un plazo fijo con esta descripción.")
        return descripcion

#DEFINICION DE TIPOS AHORRO
class TiposAhorrosForm(forms.ModelForm):
    class Meta:
        model = TiposAhorros
        fields = [
            'tahorro_tipo', 'tahorro_abreviatura', 'tahorro_dia_aporte',
            'tahorro_meses_minimo', 'tahorro_porcent_aporte', 
            'tahorro_capitalizacion', 'tahorro_estado'
        ]

    def clean_tahorro_abreviatura(self):
        abreviatura = self.cleaned_data.get("tahorro_abreviatura")
        if TiposAhorros.objects.filter(tahorro_abreviatura=abreviatura).exists():
            raise forms.ValidationError("Este tipo de ahorro ya está en uso.")
        return abreviatura


#DEFINICION DE TIPOS DE CREDITO
class TiposCreditoForm(forms.ModelForm):
    class Meta:
        model = TiposCredito
        fields = [
            "tcredito_tipo", "tcredito_abreviatura", "tcredito_monto_maximo", "tcredito_tasa_interes", "tcredito_porcentaje_mora", "tcredito_num_cuotas", 
            "tcredito_aporte_minimo", "tcredito_porcentaje_encaje", "tcredito_gracia", "tcredito_estado"
        ]

    def clean_tcredito_abreviatura(self):
        abreviatura = self.cleaned_data["tcredito_abreviatura"].upper().replace(" ", "")
        if TiposCredito.objects.filter(tcredito_abreviatura=abreviatura).exists():
            raise forms.ValidationError("Este tipo de crédito ya está registrado.")
        return abreviatura

#TIPOS DE AHORRO FUTURO
class TiposAFuturosForm(forms.ModelForm):
    class Meta:
        model = TiposAFuturos
        fields = [
            'tafuturo_tipo', 'tafuturo_abreviatura', 'tafuturo_v_inicial', 'tafuturo_v_periodico',
            'tafuturo_plazo', 'tafuturo_penalizacion',  'tafuturo_estado'
        ]

    def clean_tafuturo_abreviatura(self):
        abreviatura = self.cleaned_data.get("tafuturo_abreviatura")
        if TiposAFuturos.objects.filter(tafuturo_abreviatura=abreviatura).exists():
            raise forms.ValidationError("Este tipo de ahorro futuro ya está en uso.")
        return abreviatura


#TIPOS DE INTERESES EN AHORROS 
class InteresAhorrosForm(forms.ModelForm):
    class Meta:
        model = InteresAhorros
        fields = [
            'iahorro_tipo', 'iahorro_rendimiento',
            'iahorro_v_minimo', 'iahorro_v_maximo', 'iahorro_estado',
        ]


#TIPOS DE INTERES EN AHORROS FUTURO 
class InteresAFuturosForm(forms.ModelForm):
    class Meta:
        model = InteresAFuturo
        fields = [
            'iafuturo_tipo',  'iafuturo_rendimiento',
            'iafuturo_v_minimo', 'iafuturo_v_maximo', 'iafuturo_estado',
        ]


#PERIODOS CONTABLES
class PeriodosForm(forms.ModelForm):
    class Meta:
        model = PeriodoContable
        fields = [
            'periodo_año', 'periodo_estado',
        ]

    def clean_periodo_año(self):
        año = self.cleaned_data.get("periodo_año")
        if PeriodoContable.objects.filter(periodo_año=año).exists():
            raise forms.ValidationError("Este periodo ya registrado.")
        return año
