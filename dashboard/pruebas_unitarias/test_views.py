import pytest
from django.urls import reverse
from dashboard.models import Empresa, UnidadOrganizativa, Departamento, Cargo, User
from django.test import Client

@pytest.mark.django_db
def test_dashboard_access():
    user = User.objects.create_user(username='admin', password='admin123', email='admin@mail.com', is_superuser=True)
    client = Client()
    client.login(username='admin', password='admin123')
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
    assert b'Bienvenido' in response.content

@pytest.mark.django_db
def test_empresa_list_view():
    Empresa.objects.create(nombre='Empresa1', razon_social='RS', rif='J-123', titulo='Sistema', email='test@mail.com')
    user = User.objects.create_user(username='admin', password='admin123', email='admin@mail.com', is_superuser=True)
    client = Client()
    client.login(username='admin', password='admin123')
    response = client.get(reverse('empresa_list'))
    assert response.status_code == 200
    assert b'Empresa1' in response.content

@pytest.mark.django_db
def test_unidad_list_view():
    empresa = Empresa.objects.create(nombre='Empresa1', razon_social='RS', rif='J-123', titulo='Sistema', email='test@mail.com')
    UnidadOrganizativa.objects.create(empresa=empresa, prefijo='U1', nombre='Unidad1')
    user = User.objects.create_user(username='admin', password='admin123', email='admin@mail.com', is_superuser=True)
    client = Client()
    client.login(username='admin', password='admin123')
    response = client.get(reverse('unidad_list'))
    assert response.status_code == 200
    assert b'Unidad1' in response.content
