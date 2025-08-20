from django.contrib import admin
from administracion.models import  Capitalizaciones
from usuarios.models import Roles, EstadoCivil, PerfilUsuario, Carreras

# Register your models here.
admin.site.register(Roles)
admin.site.register(Capitalizaciones)
admin.site.register(EstadoCivil)
admin.site.register(PerfilUsuario)
admin.site.register(Carreras)