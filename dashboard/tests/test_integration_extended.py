from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()

class DashboardIntegrationExtendedTests(TestCase):
    def setUp(self):
        # Crear superusuario y usuario normal
        self.admin = User.objects.create_superuser(username='admin_int', email='admin_int@test.local', password='pass12345')
        self.user = User.objects.create_user(username='normal', email='normal@test.local', password='userpass')
        self.client = Client()

    def test_sidebar_and_pages_render(self):
        # Login admin
        self.client.login(username='admin_int', password='pass12345')

        # Dashboard
        resp = self.client.get(reverse('dashboard'))
        self.assertIn(resp.status_code, (200,302))

        # Sidebar should include 'Gestión de Roles' link
        resp = self.client.get(reverse('group_list'))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertIn('Gestión de Roles', content)
        self.assertIn('Crear nuevo grupo', content)

        # Create a group via form and ensure card layout present
        resp = self.client.post(reverse('group_create'), {'name': 'extended_group'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Group.objects.filter(name='extended_group').exists())
        resp = self.client.get(reverse('group_list'))
        self.assertIn('list-group-item', resp.content.decode())

    def test_permissions_assignment_and_access_control(self):
        # Login admin and create a group
        self.client.login(username='admin_int', password='pass12345')
        resp = self.client.post(reverse('group_create'), {'name': 'perm_group'}, follow=True)
        grp = Group.objects.get(name='perm_group')

        # Assign a permission if any exists
        perms = Permission.objects.filter(codename__icontains='change')
        if perms.exists():
            perm = perms.first()
            resp = self.client.post(reverse('group_update', kwargs={'pk': grp.pk}), {'name': grp.name, 'permissions': [perm.pk]}, follow=True)
            self.assertEqual(resp.status_code, 200)
            grp.refresh_from_db()
            self.assertIn(perm, grp.permissions.all())

        # Ensure non-admin cannot access group_create
        self.client.logout()
        self.client.login(username='normal', password='userpass')
        resp = self.client.get(reverse('group_create'))
        # Non-superuser should be redirected or forbidden
        self.assertIn(resp.status_code, (302, 403))

    def test_full_crud_flow_with_content_checks(self):
        self.client.login(username='admin_int', password='pass12345')
        # Create
        resp = self.client.post(reverse('group_create'), {'name': 'crud_group'}, follow=True)
        self.assertTrue(Group.objects.filter(name='crud_group').exists())
        grp = Group.objects.get(name='crud_group')
        # Update and check flash message content
        resp = self.client.post(reverse('group_update', kwargs={'pk': grp.pk}), {'name': 'crud_group_new'}, follow=True)
        self.assertContains(resp, 'actualizado correctamente')
        grp.refresh_from_db()
        self.assertEqual(grp.name, 'crud_group_new')
        # Delete
        resp = self.client.post(reverse('group_delete', kwargs={'pk': grp.pk}), follow=True)
        self.assertContains(resp, 'eliminado correctamente')
        self.assertFalse(Group.objects.filter(name='crud_group_new').exists())
