from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import User, Profile
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import timedelta

class UserSecurityTests(TestCase):
    def setUp(self):
        self.admin_group = Group.objects.create(name='Administrador-IT')
        self.admin = User.objects.create_user(username='admin', email='admin@test.com', password='admin123', is_superuser=True)
        self.admin.groups.add(self.admin_group)
        self.user = User.objects.create_user(username='user1', email='user1@test.com', password='user123')
        profile, _ = Profile.objects.get_or_create(user=self.user)
        profile.dni = 12345678
        profile.nac = 'V'
        profile.save()
        self.client = Client()

    def test_register_user_generates_random_password(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('register'), {
            'username': 'nuevo',
            'dni': 87654321,
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'email': 'nuevo@test.com',
            'telefono': '123456789',
            'nac': 'V',
            'groups': self.admin_group.id
        })
        self.assertRedirects(response, reverse('users_list'))
        nuevo = User.objects.get(username='nuevo')
        # Verificar que el perfil se creó
        self.assertTrue(Profile.objects.filter(user=nuevo).exists())
        # Verificar que la contraseña no es la default
        self.assertFalse(nuevo.check_password('nuevo'))

    def test_login_forces_password_change(self):
        profile = Profile.objects.get(user=self.user)
        profile.must_change_password = True
        profile.save()
        response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user123'})
        self.assertRedirects(response, reverse('change_password'))

    def test_password_expiration(self):
        profile = Profile.objects.get(user=self.user)
        profile.password_expires_at = timezone.now() - timedelta(days=1)
        profile.save()
        response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user123'})
        self.assertRedirects(response, reverse('change_password'))

    def test_block_user_after_failed_attempts(self):
        for _ in range(5):
            self.client.post(reverse('login'), {'username': 'user1', 'password': 'wrongpass'})
        user = User.objects.get(username='user1')
        self.assertFalse(user.is_active)

    def test_unique_email_and_dni(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('register'), {
            'username': 'user2',
            'dni': 12345678,  # Duplicado
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'user1@test.com',  # Duplicado
            'telefono': '123456789',
            'nac': 'V',
            'groups': self.admin_group.id
        })
        self.assertContains(response, 'Ya existe un usuario con esa cédula')
        self.assertContains(response, 'Ya existe un usuario con ese correo electrónico')

    def test_disable_enable_user(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('toggle_active', args=[self.user.id]))
        user = User.objects.get(id=self.user.id)
        self.assertFalse(user.is_active)
        response = self.client.post(reverse('toggle_active', args=[self.user.id]))
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_reset_password_sets_must_change(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('reset_password', args=[self.user.id]))
        profile = Profile.objects.get(user=self.user)
        self.assertTrue(profile.must_change_password)

    def test_blocked_user_login(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(reverse('login'), {'username': 'user1', 'password': 'user123'})
        self.assertContains(response, 'bloqueado')

    def test_single_session_enforcement(self):
        # Simula dos sesiones para el mismo usuario
        self.client.force_login(self.user)
        client2 = Client()
        client2.force_login(self.user)
        response = client2.get(reverse('dashboard'))
        self.assertIn('session_blocked', client2.session)

# Pentesting básico
class UserPentestTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='pentest', email='pentest@test.com', password='pentest123')
        profile, _ = Profile.objects.get_or_create(user=self.user)
        profile.dni = 99999999
        profile.nac = 'V'
        profile.save()
        self.client = Client()

    def test_sql_injection_login(self):
        response = self.client.post(reverse('login'), {'username': "' OR 1=1 --", 'password': 'anything'})
        self.assertContains(response, 'Por favor, introduzca un nombre de usuario y clave correctos')

    def test_xss_in_register(self):
        self.client.force_login(User.objects.create_superuser('adminxss', 'adminxss@test.com', 'adminxss123'))
        response = self.client.post(reverse('register'), {
            'username': '<script>alert(1)</script>',
            'dni': 88888888,
            'first_name': '<img src=x onerror=alert(1)>',
            'last_name': 'User',
            'email': 'xss@test.com',
            'telefono': '123456789',
            'nac': 'V',
            'groups': Group.objects.create(name='Test').id
        })
        self.assertNotIn('<script>', response.content.decode())
        self.assertNotIn('<img', response.content.decode())

    def test_brute_force_block(self):
        for _ in range(6):
            self.client.post(reverse('login'), {'username': 'pentest', 'password': 'wrong'})
        user = User.objects.get(username='pentest')
        self.assertFalse(user.is_active)

    def test_csrf_protection(self):
        # Enviar sin token CSRF
        response = self.client.post(reverse('register'), {
            'username': 'csrfuser',
            'dni': 77777777,
            'first_name': 'CSRF',
            'last_name': 'User',
            'email': 'csrf@test.com',
            'telefono': '123456789',
            'nac': 'V',
            'groups': Group.objects.create(name='CSRF').id
        })
        self.assertEqual(response.status_code, 403)

    def test_direct_profile_access(self):
        # Intentar acceder al perfil de otro usuario
        other = User.objects.create_user(username='other', email='other@test.com', password='other123')
        profile, _ = Profile.objects.get_or_create(user=other)
        profile.dni = 11111111
        profile.nac = 'V'
        profile.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse('detalle_user_id', args=[other.id]))
        self.assertNotEqual(response.status_code, 200)

from django.test import TestCase
from dashboard.models import User
from .models import Profile

class ProfileSignalTest(TestCase):
	def test_profile_created_on_user_creation(self):
		user = User.objects.create_user(username='testuser', password='testpass', first_name='Test', last_name='User', email='test@example.com')
		# El perfil debe existir automáticamente
		self.assertTrue(Profile.objects.filter(user=user).exists())
		profile = Profile.objects.get(user=user)
		self.assertEqual(profile.user.username, 'testuser')
		self.assertEqual(profile.user.email, 'test@example.com')
