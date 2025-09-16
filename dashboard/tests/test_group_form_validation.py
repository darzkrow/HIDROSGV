from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()

class GroupFormValidationTests(TestCase):
    def setUp(self):
        # Superuser para acceder a vistas
        self.admin = User.objects.create_superuser(username='gadmin', email='gadmin@test.local', password='adminpass')
        self.client = Client()
        self.client.login(username='gadmin', password='adminpass')

    def test_create_group_without_name_fails(self):
        resp = self.client.post(reverse('group_create'), {'name': ''}, follow=True)
        # Debe devolver 200 y el formulario debe mostrar error
        self.assertEqual(resp.status_code, 200)
        # Comprobar errores del formulario en contexto si está disponible
        form = resp.context.get('form') if hasattr(resp, 'context') else None
        if form is not None:
            self.assertIn('name', form.errors)
        else:
            # Fallback al HTML
            content = resp.content.decode()
            self.assertTrue('This field is required' in content or 'Este campo es obligatorio' in content)
        # No crear grupo
        self.assertFalse(Group.objects.filter(name='').exists())

    def test_create_group_with_invalid_permissions(self):
        # Enviar permisos no existentes
        resp = self.client.post(reverse('group_create'), {'name': 'invalid_perm_group', 'permissions': [99999]}, follow=True)
        # La vista debería responder 200 y no crear el grupo
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Group.objects.filter(name='invalid_perm_group').exists())
        # Comprobar errores del formulario en contexto si está disponible
        form = resp.context.get('form') if hasattr(resp, 'context') else None
        if form is not None:
            self.assertIn('permissions', form.errors)
        else:
            self.assertIn('Select a valid choice', resp.content.decode() or '')
