from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()

class DashboardIntegrationTests(TestCase):
    def setUp(self):
        # Crear superusuario de prueba
        self.admin = User.objects.create_superuser(username='admin_test', email='admin@test.local', password='pass12345')
        self.client = Client()
        self.client.login(username='admin_test', password='pass12345')

    def test_full_basic_flow(self):
        # 1) Acceder al dashboard
        url_dashboard = reverse('dashboard')
        resp = self.client.get(url_dashboard)
        self.assertIn(resp.status_code, (200, 302))

        # 2) Listar grupos (existirá al menos el grupo admin)
        url_groups = reverse('group_list')
        resp = self.client.get(url_groups)
        self.assertEqual(resp.status_code, 200)

        # 3) Crear un nuevo grupo
        url_create = reverse('group_create')
        resp = self.client.post(url_create, {'name': 'integ_test_group'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Group.objects.filter(name='integ_test_group').exists())

        group = Group.objects.get(name='integ_test_group')

        # 4) Actualizar el grupo (cambiar nombre)
        url_update = reverse('group_update', kwargs={'pk': group.pk})
        resp = self.client.post(url_update, {'name': 'integ_test_group_renamed'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Group.objects.filter(name='integ_test_group_renamed').exists())

        group = Group.objects.get(name='integ_test_group_renamed')

        # 5) Asignar un permiso al grupo (si existe alguno)
        perms = Permission.objects.all()
        if perms.exists():
            perm = perms.first()
            resp = self.client.post(url_update, {'name': group.name, 'permissions': [perm.pk]}, follow=True)
            self.assertEqual(resp.status_code, 200)
            group.refresh_from_db()
            self.assertIn(perm, group.permissions.all())

        # 6) Eliminar el grupo
        url_delete = reverse('group_delete', kwargs={'pk': group.pk})
        resp = self.client.post(url_delete, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Group.objects.filter(name='integ_test_group_renamed').exists())

        # 7) Probar páginas críticas (roles_permissions)
        url_roles = reverse('roles_permissions')
        resp = self.client.get(url_roles)
        self.assertEqual(resp.status_code, 200)

        # 8) Probar lista de usuarios
        url_users = reverse('users_list')
        resp = self.client.get(url_users)
        self.assertEqual(resp.status_code, 200)
