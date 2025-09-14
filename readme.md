
# HIDROSGV - Dashboard Empresarial

Sistema avanzado para la gestión de usuarios, empresas y administración con seguridad y roles personalizados.

---

## Workflow recomendado

### 1. Instalación y entorno

```bash
git clone <repo-url>
cd HIDROSGV
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Configuración inicial

Ejecuta los siguientes comandos para crear roles, permisos y poblar el dashboard:

```bash
python manage.py create_roles_permissions
python manage.py populate_dashboard
```
O ejecuta ambos en un solo paso:
```bash
python manage.py setup_dashboard
```

### 4. Crear superusuario

```bash
python manage.py createsuperuser
```

### 5. Ejecutar pruebas

```bash
pytest
```

### 6. Iniciar el servidor

```bash
python manage.py runserver
```

### 7. Acceso y login

Accede a la página principal. Si no estás logueado, verás el index moderno. Inicia sesión para acceder al dashboard y funcionalidades avanzadas.

---

## Recomendaciones
- Ejecuta `setup_dashboard` después de migrar para tener roles y datos iniciales.
- Revisa los mensajes en consola para confirmar la correcta ejecución.
- Si necesitas reiniciar la configuración, puedes volver a ejecutar `setup_dashboard`.

---

## Otros comandos útiles
- Para ejecutar las pruebas:
  ```bash
  pytest
  ```
- Para crear un superusuario:
  ```bash
  python manage.py createsuperuser
  ```

---

## Contacto y soporte
Para dudas o soporte, contacta al equipo de desarrollo.
