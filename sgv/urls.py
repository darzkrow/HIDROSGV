from .views import estadisticas_acceso
from django.urls import path
from . import views

urlpatterns = [
    path('estadisticas/', estadisticas_acceso, name='estadisticas-acceso'),

    path('visitante/<int:visitante_id>/', views.detalle_visitante, name='detalle-visitante'),
    # Unificada:
    path('buscar/', views.buscar_visitante, name='buscar'),
    path('registrar-visitante-nuevo/<str:identificacion>/', views.registrar_visitante, name='registro-visitante-nuevo'),
    path('registrar-visita-directo/<int:visitante_id>/', views.registrar_visita, name='registro-visita-directo'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('registrar-salida/<int:visita_id>/', views.registrar_salida, name='registrar-salida'),
    path('visitante/', views.registrar_visitante, name='registro-visitante'),
    path('visita/', views.registrar_visita, name='registro-visita'),
    path('lista/', views.ListaVisitasView.as_view(), name='lista-visitas'),
]
