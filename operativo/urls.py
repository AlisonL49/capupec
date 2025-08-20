from django.urls import path
from operativo import views

urlpatterns = [    
    path('consulta-garantias/', views.consulta_garantias, name='consulta-garantias'),
    path('solicitud/', views.solicitud, name='solicitud'),
    path('get_credit_details/', views.get_credit_details, name='get_credit_details'),
    
    #path('obtener-datos-credito/', views.obtener_datos_credito, name='obtener_datos_credito'),
    path('solicitud-credito/imprimir/', views.imprimir_solicitud_credito, name='imprimir_solicitud_credito'),
    path('pdf-amortizacion/', views.generar_pdf_amortizacion, name='pdf_amortizacion'),
    path('consulta-aprobacion/', views.consulta_aprobacion, name='consulta-aprobacion'),
    path('ahorros/', views.ahorros, name='ahorros'),
    path('registrar-aporte/', views.registrar_aporte, name='registrar_aporte'),
    path('ahorros/recibo-pdf/<int:usuario_id>/<str:aporte>/', views.generar_recibo_pdf, name='generar_recibo_pdf'),

    path('ahorro-futuro/',views.ahorro_futuro, name='ahorro-futuro'),
    path('debitos-cetificados/', views.deb_cetificados, name='debitos-cetificados'),
    path('pagos-por-rol/', views.pagos_rol, name='pagos-por-rol'),
    path('caja/', views.caja, name='caja'),
    path('reportes/', views.reportes, name='reportes'),
    path('cierre-diario/', views.cierre_diario, name='cierre-diario'),
    path('distribucion-excedente/', views.distrib_excedente, name='distribucion-excedente'),    
    path('reporte-socios-pdf/', views.reporte_socios_pdf, name='reporte_socios_pdf'),
    path('obtener-saldo-usuario/', views.obtener_saldo_usuario, name='obtener_saldo_usuario'),
]