
from django.urls import path
from . import views
from .views import session_blocked_view

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
    path('bloquear-sesion/', views.bloquear_sesion_view, name='bloquear_sesion'),
    path('detalle-user/', views.detalle_user_view, name='detalle_user'),
    path('detalle-user/<int:user_id>/', views.detalle_user_view, name='detalle_user_id'),
    path('users-list/', views.users_list_view, name='users_list'),
    path('reset-password/<int:user_id>/', views.reset_password_view, name='reset_password'),
    path('toggle-active/<int:user_id>/', views.toggle_active_view, name='toggle_active'),
]
