from django.urls import path
from contabilidad import views

urlpatterns = [
    path('plan-cuentas/', views.plan_cuentas, name='plan-cuentas'),
    path('planilla-contable/',views.planilla_contable, name='planilla-contable'),
    path('mayor-auxiliar/', views.mayor_auxiliar, name='mayor-auxiliar'),
    path('libro-diario/', views.libro_diario, name='libro-diario'),
    path('balance-comprobacion/', views.balance_comprobacion, name='balance-comprobacion'),
    path('balance-general/',views.balance_general, name='balance-general'),
    path('estado-perdidas-ganancias/', views.estado_perdidas_ganancias, name='estado-perdidas-ganancias'),
    path('revision-crecimiento/', views.revision_crecimiento, name='revision-crecimiento'),
    path('cierre-dia/', views.cierre_dia, name='cierre-dia'),
]