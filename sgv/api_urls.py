from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'visitantes', views.VisitanteViewSet, basename='visitante')
router.register(r'visitas', views.VisitaViewSet, basename='visita')
router.register(r'carnets', views.CarnetViewSet, basename='carnet')
router.register(r'empleados', views.EmpleadoViewSet, basename='empleado')
router.register(r'pisos', views.PisoViewSet, basename='piso')
router.register(r'oficinas', views.OficinaViewSet, basename='oficina')

urlpatterns = [
    path('', include(router.urls)),
    path('visitantes/<int:pk>/historial/', views.VisitanteHistorialView.as_view(), name='visitante-historial'),
    path('carnets/disponibles/', views.CarnetDisponiblesView.as_view(), name='carnet-disponibles'),
    path('carnets/<str:numero_carnet>/', views.CarnetDetalleView.as_view(), name='carnet-detalle'),
]
