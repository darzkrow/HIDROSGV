# HIDROSGV Dashboard

## Español

### Descripción
Sistema de gestión de usuarios avanzado en Django, con roles, seguridad, administración y control de sesiones. Incluye:
- Registro y autenticación de usuarios
- Edición de perfil y cambio de contraseña
- Restablecimiento de contraseña con expiración cada 30 días
- Asignación de roles y bloqueo/desbloqueo de usuarios
- Seguridad avanzada: bloqueo tras 5 intentos fallidos, sesión única, alertas, y protección contra ataques comunes
- Tests unitarios y de pentesting incluidos

### Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/darzkrow/HIDROSGV.git
   cd HIDROSGV
   ```
2. Instala dependencias:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configura variables en `.env` y ejecuta migraciones:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```
4. Crea un superusuario:
   ```bash
   python3 manage.py createsuperuser
   ```

### Uso
- Accede al panel de administración en `/admin`
- El administrador puede registrar usuarios, asignar roles y bloquear/desbloquear cuentas
- Los usuarios deben cambiar la contraseña al iniciar sesión si fue restablecida o expiró

### Seguridad
- Contraseña expira cada 30 días
- Bloqueo tras 5 intentos fallidos
- Un solo inicio de sesión por usuario
- Alertas para usuarios bloqueados y acciones administrativas
- Tests de pentesting incluidos

### Tests
Ejecuta todos los tests:
```bash
python3 manage.py test dashboard
```

---

## English

### Description
Advanced user management system in Django, with roles, security, admin controls, and session management. Features:
- User registration and authentication
- Profile editing and password change
- Password reset with expiration every 30 days
- Role assignment and user blocking/unblocking
- Advanced security: block after 5 failed attempts, single session, alerts, and protection against common attacks
- Includes unit and pentesting tests

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/darzkrow/HIDROSGV.git
   cd HIDROSGV
   ```
2. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configure variables in `.env` and run migrations:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python3 manage.py createsuperuser
   ```

### Usage
- Access the admin panel at `/admin`
- Admin can register users, assign roles, and block/unblock accounts
- Users must change their password on login if it was reset or expired

### Security
- Password expires every 30 days
- Block after 5 failed login attempts
- Single session per user
- Alerts for blocked users and admin actions
- Pentesting tests included

### Tests
Run all tests:
```bash
python3 manage.py test dashboard
```
