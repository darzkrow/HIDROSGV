import pytest
from dashboard.forms import CustomUserCreationForm
from dashboard.models import User, Profile

@pytest.fixture(autouse=True)
def limpiar_db(db):
    User.objects.all().delete()
    Profile.objects.all().delete()
@pytest.mark.django_db
def test_user_creation_form_valid():
    import random
    unique_id = str(random.randint(10000000, 99999999))
    form_data = {
        'username': f'user{unique_id}',
        'email': f'user{unique_id}@mail.com',
        'password1': 'ClaveSegura123',
        'password2': 'ClaveSegura123',
        'dni': unique_id,
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'telefono': '04141234567',
        'nac': 'V',
    }
    form = CustomUserCreationForm(data=form_data)
    if not form.is_valid():
        print('Errores:', form.errors)
    assert form.is_valid(), f"Errores de validación: {form.errors}"
    user = form.save()
    if user is None:
        print('Error al crear usuario, errores:', form.errors)
    assert user is not None, "El usuario no se creó correctamente."
    assert user.username == f'user{unique_id}'
    assert user.email == f'user{unique_id}@mail.com'
    assert user.check_password('ClaveSegura123')

@pytest.mark.django_db
def test_user_creation_form_password_mismatch():
    form_data = {
        'username': 'user02',
        'email': 'user02@mail.com',
        'password1': 'ClaveSegura123',
        'password2': 'ClaveDistinta456',
        'dni': '3000002',
        'first_name': 'Ana',
        'last_name': 'Gómez',
        'telefono': '04149876543',
        'nac': 'V',
    }
    form = CustomUserCreationForm(data=form_data)
    assert not form.is_valid()
    assert 'password2' in form.errors

@pytest.mark.django_db
def test_user_creation_form_sql_injection():
    form_data = {
        'username': "admin'; DROP TABLE users;--",
        'email': "sql@injection.com",
        'password1': 'ClaveSegura123',
        'password2': 'ClaveSegura123',
        'dni': '3000003',
        'first_name': "Robert'); DROP TABLE users;--",
        'last_name': 'Injection',
        'telefono': '04140000000',
        'nac': 'V',
    }
    form = CustomUserCreationForm(data=form_data)
    assert not form.is_valid() or 'username' in form.errors

@pytest.mark.django_db
def test_user_creation_form_missing_fields():
    form_data = {
        'username': 'user03',
        'email': 'user03@mail.com',
        'password1': 'ClaveSegura123',
        'password2': 'ClaveSegura123',
        # Falta el campo dni
        'first_name': 'Carlos',
        'last_name': 'Ramírez',
        'telefono': '04141231231',
        'nac': 'V',
    }
    form = CustomUserCreationForm(data=form_data)
    assert not form.is_valid()
    assert 'dni' in form.errors

@pytest.mark.django_db
def test_user_creation_form_invalid_email():
    form_data = {
        'username': 'user04',
        'email': 'noesunemail',
        'password1': 'ClaveSegura123',
        'password2': 'ClaveSegura123',
        'dni': '3000004',
        'first_name': 'Luis',
        'last_name': 'Martínez',
        'telefono': '04141231231',
        'nac': 'V',
    }
    form = CustomUserCreationForm(data=form_data)
    assert not form.is_valid()
    assert 'email' in form.errors

@pytest.mark.django_db
def test_user_creation_form_duplicate_dni():
    import random
    unique_dni = str(random.randint(10000000, 99999999))
    # Primer usuario y perfil
    user1 = User.objects.create_user(
        username=f'user{unique_dni}',
        email=f'user{unique_dni}@mail.com',
        password='ClaveSegura123',
        first_name='Pedro',
        last_name='López',
    )
    from dashboard.models import Profile
    Profile.objects.create(
        user=user1,
        dni=unique_dni,
        telefono='04145555555',
        nac='V',
    )
    # Segundo usuario y perfil con mismo DNI
    user2 = User.objects.create_user(
        username=f'user{unique_dni}b',
        email=f'user{unique_dni}b@mail.com',
        password='ClaveSegura123',
        first_name='Ana',
        last_name='Martínez',
    )
    with pytest.raises(Exception) as excinfo2:
        Profile.objects.create(
            user=user2,
            dni=unique_dni,  # DNI duplicado
            telefono='04146666666',
            nac='V',
        )
    print('Error esperado al crear perfil con DNI duplicado:', excinfo2.value)

@pytest.mark.django_db
def test_user_creation_form_duplicate_username_email():
    import random
    unique_id = str(random.randint(10000000, 99999999))
    # Primer usuario
    user1 = User.objects.create_user(
        username=f'user{unique_id}',
        email=f'user{unique_id}@mail.com',
        password='ClaveSegura123',
        first_name='Pedro',
        last_name='López',
    )
    # Intentar crear usuario con mismo username
    with pytest.raises(Exception) as excinfo:
        User.objects.create_user(
            username=f'user{unique_id}',  # Username duplicado
            email=f'user{unique_id}x@mail.com',
            password='ClaveSegura123',
            first_name='Ana',
            last_name='Martínez',
        )
    print('Error esperado al crear usuario con username duplicado:', excinfo.value)
    # Intentar crear usuario con mismo email
    with pytest.raises(Exception) as excinfo2:
        User.objects.create_user(
            username=f'user{unique_id}y',
            email=f'user{unique_id}@mail.com',  # Email duplicado
            password='ClaveSegura123',
            first_name='Ana',
            last_name='Martínez',
        )
    print('Error esperado al crear usuario con email duplicado:', excinfo2.value)
