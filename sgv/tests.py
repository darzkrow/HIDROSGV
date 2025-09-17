
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Visitante, Carnet, Visita, Empleado, Oficina, Piso
from django.contrib.auth.models import User, Group, Permission

def create_user_with_perms(username, password, perms=None, groups=None):
    user = User.objects.create_user(username=username, password=password)
    if perms:
        for perm in perms:
            user.user_permissions.add(Permission.objects.get(codename=perm, content_type__app_label='sgv'))
    if groups:
        for group in groups:
            g, _ = Group.objects.get_or_create(name=group)
            user.groups.add(g)
    user.save()
    return user

class VisitanteAPITests(APITestCase):
    def setUp(self):
        self.admin = create_user_with_perms(
            'admin123', 'admin123',
            perms=[
                'add_visitante', 'change_visitante', 'delete_visitante', 'view_visitante',
                'add_visita', 'change_visita', 'delete_visita', 'view_visita',
                'add_carnet', 'change_carnet', 'delete_carnet', 'view_carnet',
                'add_empleado', 'change_empleado', 'delete_empleado', 'view_empleado',
                'add_oficina', 'change_oficina', 'delete_oficina', 'view_oficina',
                'add_piso', 'change_piso', 'delete_piso', 'view_piso',
            ]
        )
        self.client = APIClient()
        response = self.client.post('/api/v1/token/', {'username': 'admin123', 'password': 'admin123'}, format='json')
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.visitante_data = {
            'nombre_completo': 'Juan Pérez',
            'identificacion': '12345678',
            'telefono': '04141234567',
            'correo': 'juan@example.com',
        }
        self.visitante = Visitante.objects.create(**self.visitante_data)

    def test_listar_visitantes(self):
        url = reverse('visitante-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_crear_visitante(self):
        url = reverse('visitante-list')
        data = {
            'nombre_completo': 'Ana Gómez',
            'identificacion': '87654321',
            'telefono': '04149876543',
            'correo': 'ana@example.com',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre_completo'], 'Ana Gómez')

    def test_detalle_visitante(self):
        url = reverse('visitante-detail', args=[self.visitante.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['identificacion'], self.visitante.identificacion)

    def test_editar_visitante(self):
        url = reverse('visitante-detail', args=[self.visitante.id])
        response = self.client.patch(url, {'telefono': '04140000000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['telefono'], '04140000000')

    def test_eliminar_visitante(self):
        url = reverse('visitante-detail', args=[self.visitante.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class CarnetAPITests(APITestCase):
    def setUp(self):
        self.recepcionista = create_user_with_perms(
            'recepcionista', 'recep123',
            perms=['add_carnet', 'change_carnet', 'delete_carnet', 'view_carnet'],
            groups=['Recepcionista']
        )
        self.client = APIClient()
        response = self.client.post('/api/v1/token/', {'username': 'recepcionista', 'password': 'recep123'}, format='json')
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.carnet = Carnet.objects.create(numero='C001', estado='disponible')

    def test_listar_carnets(self):
        url = reverse('carnet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_detalle_carnet(self):
        url = reverse('carnet-detail', args=[self.carnet.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['numero'], 'C001')

class VisitaAPITests(APITestCase):
    def setUp(self):
        self.visitante_user = create_user_with_perms(
            'visitante', 'visitante123',
            perms=['add_visita', 'change_visita', 'delete_visita', 'view_visita'],
            groups=['Visitante']
        )
        self.client = APIClient()
        response = self.client.post('/api/v1/token/', {'username': 'visitante', 'password': 'visitante123'}, format='json')
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.piso = Piso.objects.create(nombre='Piso 1')
        self.oficina = Oficina.objects.create(nombre='Oficina 101', piso=self.piso)
        self.anfitrion = Empleado.objects.create(nombre_completo='Carlos Ruiz', identificacion='11122233', activo=True)
        self.visitante = Visitante.objects.create(nombre_completo='Juan Pérez', identificacion='12345678')
        self.carnet = Carnet.objects.create(numero='C002', estado='disponible')
        self.visita_data = {
            'visitante': self.visitante,
            'motivo': 'Reunión',
            'anfitrion': self.anfitrion,
            'oficina': self.oficina,
        }
        self.visita = Visita.objects.create(**self.visita_data)

    def test_listar_visitas(self):
        url = reverse('visita-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_crear_visita(self):
        url = reverse('visita-list')
        data = {
            'visitante': self.visitante.id,
            'motivo': 'Entrega',
            'anfitrion': self.anfitrion.id,
            'oficina': self.oficina.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['motivo'], 'Entrega')

    def test_detalle_visita(self):
        url = reverse('visita-detail', args=[self.visita.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['motivo'], self.visita.motivo)

    def test_editar_visita(self):
        url = reverse('visita-detail', args=[self.visita.id])
        response = self.client.patch(url, {'motivo': 'Cambio'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['motivo'], 'Cambio')

    def test_eliminar_visita(self):
        url = reverse('visita-detail', args=[self.visita.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
