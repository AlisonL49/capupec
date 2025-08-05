"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from sistema.views import principal, login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login1/', lambda request: redirect('login')),
    path('login/', login_view, name='login'), 
    
    path('', principal, name='principal'),

    path('', include('sistema.urls')),
    path('administracion/', include('administracion.urls')),
    path('contabilidad/', include('contabilidad.urls')),
    path('operativo/', include('operativo.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('socios/', include('socios.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
