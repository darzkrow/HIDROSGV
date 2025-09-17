import pytest
from dashboard.models import Empresa, UnidadOrganizativa, Departamento, Cargo, User
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_empresa_unica():
    Empresa.objects.create(nombre='Empresa1', razon_social='RS', rif='J-123', titulo='Sistema', email='test@mail.com')
    with pytest.raises(Exception):
        Empresa.objects.create(nombre='Empresa2', razon_social='RS2', rif='J-456', titulo='Sistema2', email='test2@mail.com')

@pytest.mark.django_db
def test_unidad_organizativa():
    empresa = Empresa.objects.create(nombre='Empresa1', razon_social='RS', rif='J-123', titulo='Sistema', email='test@mail.com')
    unidad = UnidadOrganizativa.objects.create(empresa=empresa, prefijo='U1', nombre='Unidad1')
    assert unidad.empresa == empresa
    assert unidad.prefijo == 'U1'

@pytest.mark.django_db
def test_departamento():
    empresa = Empresa.objects.create(nombre='Empresa1', razon_social='RS', rif='J-123', titulo='Sistema', email='test@mail.com')
    unidad = UnidadOrganizativa.objects.create(empresa=empresa, prefijo='U1', nombre='Unidad1')
    departamento = Departamento.objects.create(unidad=unidad, nombre='Depto1')
    assert departamento.unidad == unidad
    assert departamento.nombre == 'Depto1'

@pytest.mark.django_db
def test_cargo():
    empresa = Empresa.objects.create(nombre='Empresa1', razon_social='RS', rif='J-123', titulo='Sistema', email='test@mail.com')
    unidad = UnidadOrganizativa.objects.create(empresa=empresa, prefijo='U1', nombre='Unidad1')
    departamento = Departamento.objects.create(unidad=unidad, nombre='Depto1')
    cargo = Cargo.objects.create(departamento=departamento, nombre='Cargo1')
    assert cargo.departamento == departamento
    assert cargo.nombre == 'Cargo1'

@pytest.mark.django_db
def test_usuario_creacion():
    user = User.objects.create_user(username='testuser', password='123456', email='test@mail.com')
    assert user.username == 'testuser'
    assert user.check_password('123456')
