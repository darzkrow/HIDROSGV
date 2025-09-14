from django.urls import path
from . import views
from .views import session_blocked_view
from .views import (
    EmpresaListView, EmpresaCreateView, EmpresaUpdateView,
    UnidadListView, UnidadCreateView, UnidadUpdateView, UnidadDeleteView,
    DepartamentoListView, DepartamentoCreateView, DepartamentoUpdateView, DepartamentoDeleteView,
    CargoListView, CargoCreateView, CargoUpdateView, CargoDeleteView
)

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('roles/', views.roles_permissions_view, name='roles_permissions'),
    path('create-group/', views.create_group_view, name='create_group'),
    path('session-blocked/', session_blocked_view, name='session_blocked'),
    path('bloquear-sesion/', views.session_blocked_view, name='bloquear_sesion'),
    path('desconectar-usuario/', views.desconectar_usuario_view, name='desconectar_usuario'),
    path('users-connected/', views.connected_users_view, name='users_connected'),
    path('detalle-user/', views.detalle_user_view, name='detalle_user'),
    path('detalle-user/<int:user_id>/', views.detalle_user_view, name='detalle_user_id'),
    path('users-list/', views.users_list_view, name='users_list'),
    path('reset-password/<int:user_id>/', views.reset_password_view, name='reset_password'),
    path('toggle-active/<int:user_id>/', views.toggle_active_view, name='toggle_active'),

    path('empresas/', EmpresaListView.as_view(), name='empresa_list'),
    path('empresas/nueva/', EmpresaCreateView.as_view(), name='empresa_create'),
    path('empresas/<int:pk>/editar/', EmpresaUpdateView.as_view(), name='empresa_update'),

    path('unidades/', UnidadListView.as_view(), name='unidad_list'),
    path('unidades/nueva/', UnidadCreateView.as_view(), name='unidad_create'),
    path('unidades/<int:pk>/editar/', UnidadUpdateView.as_view(), name='unidad_update'),
    path('unidades/<int:pk>/eliminar/', UnidadDeleteView.as_view(), name='unidad_delete'),

    path('departamentos/', DepartamentoListView.as_view(), name='departamento_list'),
    path('departamentos/nuevo/', DepartamentoCreateView.as_view(), name='departamento_create'),
    path('departamentos/<int:pk>/editar/', DepartamentoUpdateView.as_view(), name='departamento_update'),
    path('departamentos/<int:pk>/eliminar/', DepartamentoDeleteView.as_view(), name='departamento_delete'),

    path('cargos/', CargoListView.as_view(), name='cargo_list'),
    path('cargos/nuevo/', CargoCreateView.as_view(), name='cargo_create'),
    path('cargos/<int:pk>/editar/', CargoUpdateView.as_view(), name='cargo_update'),
    path('cargos/<int:pk>/eliminar/', CargoDeleteView.as_view(), name='cargo_delete'),
]
