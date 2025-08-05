from django.urls import path
from usuarios import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('buscar-usuarios/', views.buscar_usuarios, name='buscar_usuarios'),
    

]

