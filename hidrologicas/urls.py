from django.urls import path
from .views import hidrologica_list, hidrologica_create, hidrologica_update, hidrologica_delete, gerente_create, hidrologica_detail, hidrologicas_status_api

urlpatterns = [
    path('list/', hidrologica_list, name='hidrologica_list'),
    path('create/', hidrologica_create, name='hidrologica_create'),
    path('update/<int:pk>/', hidrologica_update, name='hidrologica_update'),
    path('delete/<int:pk>/', hidrologica_delete, name='hidrologica_delete'),
    path('gerente/create/', gerente_create, name='gerente_create'),
    path('detail/<int:pk>/', hidrologica_detail, name='hidrologica_detail'),
    path('api/status/', hidrologicas_status_api, name='hidrologicas_status_api'),
]
