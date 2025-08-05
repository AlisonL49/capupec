from django.urls import path
from sistema import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('logout/', views.signout, name='logout'),
    path('acceso-denegado/', views.acceso_denegado, name='acceso-denegado'),
] 
