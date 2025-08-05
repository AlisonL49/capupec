from django.urls import path
from socios import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('perfil/', views.perfil_usuario, name='perfil-usuario'),
    path('cambiar-contrasena/', auth_views.PasswordChangeView.as_view(
        template_name='cambiar_contrasena.html',
        success_url='/perfil/'
    ), name='cambiar_contrasena'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('simulador/', views.simulador, name='simulador'),
    path('resultado/<int:simulacion_id>/', views.resultado_simulacion, name='resultado'),
    path('info-capupec/', views.info_capupec, name='info-capupec'),
    
]

