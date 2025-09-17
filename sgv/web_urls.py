from django.urls import path
from . import views

app_name = 'sgv'

urlpatterns = [
    # Rutas web (sin prefijo api)

    path('visitante/<int:visitante_id>/', views.detalle_visitante, name='detalle-visitante'),
    path('buscar-visitante/', views.buscar_visitante, name='buscar-visitante'),
    path('registrar-visitante-nuevo/<str:identificacion>/', views.registrar_visitante, name='registro-visitante-nuevo'),
    path('registrar-visita-directo/<int:visitante_id>/', views.registrar_visita, name='registro-visita-directo'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('buscar/', views.buscar_visita, name='buscar-visita'),
    path('registrar-salida/<int:visita_id>/', views.registrar_salida, name='registrar-salida'),
    path('visitante/', views.registrar_visitante, name='registro-visitante'),
    path('visita/', views.registrar_visita, name='registro-visita'),
    path('lista/', views.ListaVisitasView.as_view(), name='lista-visitas'),
]
