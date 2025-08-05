from django.urls import path
from administracion import views


urlpatterns = [
    
    path('representantes/', views.representantes, name='representantes'),
    path('parametros/', views.parametros, name='parametros'),
    path('parametros/editar/<int:pk>/', views.parametro_editar, name='parametros_editar'),
    path('parametros/eliminar/<int:pk>/', views.parametro_eliminar, name='parametros_eliminar'),
    path('formas-pago/',views.formas_pago, name='formas-pago'),
    path('formas-pago/editar/<int:pk>/', views.forma_pago_editar, name='forma_pago_editar'),
    path('formas-pago/eliminar/<int:pk>/', views.forma_pago_eliminar, name='forma_pago_eliminar'),
    path('destinos/', views.destinos, name='destinos'),
    path('tipos-ahorros/', views.tipos_ahorros, name='tipos-ahorros'),
    path('tipos-ahorros/editar/<int:pk>/', views.tipo_ahorro_editar, name='tipo_ahorro_editar'),
    path('tipos-ahorros/eliminar/<int:pk>/', views.tipo_ahorro_eliminar, name='tipo_ahorro_eliminar'),
    path('tipos-credito/', views.tipos_credito, name='tipos-credito'),
    path('tipos-credito/editar/<int:pk>/', views.tipo_credito_editar, name='tipo_credito_editar'),
    path('tipos-credito/eliminar/<int:pk>/', views.tipo_credito_eliminar, name='tipo_credito_eliminar'),
    path('tipos-ahorrofuturo/', views.tipos_ahorrofuturo, name='tipos-ahorrofuturo'),
    path('tipos-ahorrofuturo/editar/<int:pk>/', views.tipo_ahorrofuturo_editar, name='tipo_ahorrofuturo_editar'),
    path('tipos-ahorrofuturo/eliminar/<int:pk>/', views.tipo_ahorrofuturo_eliminar, name='tipo_ahorrofuturo_eliminar'),
    path('plazo-fijo/', views.plazo_fijo, name='plazo-fijo'),
    path('plazo-fijo/editar/<int:pk>/', views.plazo_editar, name='editar_plazo'),
    path('plazo-fijo/eliminar/<int:pk>/', views.plazo_eliminar, name='eliminar_plazo'),
    path('interes-ahorros/', views.interes_ahorros, name='interes-ahorros'),
    path('interes-ahorros/editar/<int:pk>/', views.interes_ahorros_editar, name='interes_ahorros_editar'),
    path('interes-ahorros/eliminar/<int:pk>/', views.interes_ahorros_eliminar, name='interes_ahorros_eliminar'),
    path('interes-ahorrofuturo/', views.interes_afuturo, name='interes-ahorrofuturo'),
    path('interes-ahorrofuturo/editar/<int:pk>/', views.interes_afuturo_editar, name='interes_afuturo_editar'),
    path('interes-ahorrofuturo/eliminar/<int:pk>/', views.interes_afuturo_eliminar, name='interes_afuturo_eliminar'),
    path('periodos-contables/', views.periodos_contables, name='periodos-contables'),
]