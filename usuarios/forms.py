from django.contrib.auth.models import User
from django import forms
from .models import PerfilUsuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = [
            'rol', 'cedula', 'fecha_caducidad', 'fecha_nacimiento', 'fecha_ingreso', 'genero', 'nombramiento',
            'lugar_trabajo', 'ciudad', 'direccion', 'telefono', 'estado_civil', 'estado'
        ]

