from django.contrib.auth import logout

# Bloquear manualmente la sesión
from django.contrib.auth.decorators import login_required
def bloquear_sesion_view(request):
	if request.user.is_authenticated:
		logout(request)
		request.session['session_blocked'] = True
		return redirect('session_blocked')
	return redirect('login')
import random
import string
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test
from dashboard.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import Profile
from dashboard.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Permission

from django.http import HttpResponseForbidden



from django.shortcuts import redirect

# Resetear contraseña y obligar cambio al iniciar sesión
@user_passes_test(lambda u: u.is_superuser)
def reset_password_view(request, user_id):
	user = get_object_or_404(User, id=user_id)
	if request.method == 'POST':
		new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
		user.set_password(new_password)
		user.save()
		# Marcar que debe cambiar contraseña (puedes usar un campo en Profile, ej: must_change_password)
		profile, _ = Profile.objects.get_or_create(user=user, defaults={"dni": 0})
		profile.must_change_password = True
		profile.save()
		# Mostrar la contraseña generada (puedes usar mensajes o redirigir con la info)
		messages.success(request, f'Contraseña reseteada: {new_password}')
		return HttpResponseRedirect(reverse('users_list'))
	return HttpResponseForbidden()

# Habilitar/deshabilitar usuario
@user_passes_test(lambda u: u.is_superuser)
def toggle_active_view(request, user_id):
	user = get_object_or_404(User, id=user_id)
	if request.method == 'POST':
		user.is_active = not user.is_active
		user.save()
		return HttpResponseRedirect(reverse('users_list'))
	return HttpResponseForbidden()
from django.contrib.auth.decorators import user_passes_test

# Vista solo para administradores: lista de usuarios
@user_passes_test(lambda u: u.is_superuser)
def users_list_view(request):
	from django.core.paginator import Paginator
	users = User.objects.all().order_by('username')
	grupos = Group.objects.all()
	q = request.GET.get('q', '').strip()
	group_id = request.GET.get('group')
	page_number = request.GET.get('page', 1)
	if q:
		users = users.filter(
			username__icontains=q
		) | users.filter(
			first_name__icontains=q
		) | users.filter(
			last_name__icontains=q
		) | users.filter(
			email__icontains=q
		)
	if group_id:
		users = users.filter(groups__id=group_id)
	cantidad = users.count()
	paginator = Paginator(users, 10)
	page_obj = paginator.get_page(page_number)
	return render(request, 'dashboard/admin/users_list.html', {
		'users': page_obj.object_list,
		'cantidad': cantidad,
		'grupos': grupos,
		'request': request,
		'page_obj': page_obj
	})

@login_required
def detalle_user_view(request, user_id=None):
    if user_id:
        user = get_object_or_404(User, id=user_id)
        # Solo el propio usuario o el admin pueden ver el perfil
        if request.user.id != user.id and not request.user.is_superuser:
            return HttpResponseForbidden('No tienes permiso para ver este perfil.')
    else:
        user = request.user
    profile, created = Profile.objects.get_or_create(user=user, defaults={"dni": 0})
    return render(request, 'dashboard/users/detalle_user.html', {'user': user, 'profile': profile})
from django.shortcuts import render, redirect

def session_blocked_view(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	if request.method == 'POST':
		return redirect('login')
	return render(request, 'dashboard/users/session_blocked.html')

def index_view(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	return render(request, 'dashboard/index.html')

def create_group_view(request):
	groups = Group.objects.all()
	permissions = Permission.objects.all()
	message = None
	# Eliminar grupo
	if request.method == 'POST' and 'delete_group' in request.POST:
		group_id = request.POST.get('delete_group')
		Group.objects.filter(id=group_id).delete()
		message = 'Grupo eliminado correctamente.'
	# Editar permisos de grupo
	elif request.method == 'POST' and 'edit_group' in request.POST:
		group_id = request.POST.get('edit_group')
		perms_ids = request.POST.getlist(f'perms_{group_id}')
		group = Group.objects.get(id=group_id)
		group.permissions.set(perms_ids)
		message = f'Permisos actualizados para el grupo "{group.name}".'
	# Crear grupo
	elif request.method == 'POST':
		group_name = request.POST.get('group_name')
		perms_ids = request.POST.getlist('perms')
		if group_name:
			group, created = Group.objects.get_or_create(name=group_name)
			group.permissions.set(perms_ids)
			message = f'Grupo "{group_name}" creado y permisos asignados.'
	groups = Group.objects.all()  # Actualizar lista
	return render(request, 'dashboard/admin/create_group.html', {
		'groups': groups,
		'permissions': permissions,
		'message': message
	})



# Vista solo para administradores para gestión de roles y permisos
@user_passes_test(lambda u: u.is_superuser)
def roles_permissions_view(request):

	users = User.objects.all()
	grupos = Group.objects.all()
	permissions = Permission.objects.all()
	message = None
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		group_id = request.POST.get('group_id')
		if user_id and group_id:
			user = User.objects.get(id=user_id)
			group = Group.objects.get(id=group_id)
			user.groups.add(group)
			message = f'Rol "{group.name}" asignado a {user.username}.'
	return render(request, 'dashboard/admin/roles_permissions.html', {
		'users': users,
		'groups': grupos,
		'permissions': permissions,
		'message': message
	})




@login_required
def change_password_view(request):
	profile, _ = Profile.objects.get_or_create(user=request.user, defaults={"dni": 0})
	if profile.must_change_password:
		from django.contrib.auth.forms import SetPasswordForm
		FormClass = SetPasswordForm
	else:
		FormClass = PasswordChangeForm

	if request.method == 'POST':
		form = FormClass(user=request.user, data=request.POST)
		if form.is_valid():
			user = form.save()
			profile.must_change_password = False
			from django.utils import timezone
			from datetime import timedelta
			profile.password_expires_at = timezone.now() + timedelta(days=30)
			profile.save()
			messages.success(request, 'Contraseña cambiada correctamente.')
			login(request, user)
			return redirect('dashboard')
	else:
		form = FormClass(user=request.user)
	return render(request, 'dashboard/users/change_password.html', {'form': form})

def logout_view(request):
	logout(request)
	return redirect('login')

from django.db import IntegrityError

def register_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Solo los administradores pueden registrar usuarios.')
    groups = Group.objects.all()
    from django.utils import timezone
    from datetime import timedelta
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        group_id = request.POST.get('groups')
        if form.is_valid():
            user = form.save(commit=False)
            # Generar contraseña aleatoria
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user.set_password(new_password)
            user.save()
            # Asignar grupo
            if user and group_id:
                group = get_object_or_404(Group, id=group_id)
                user.groups.add(group)
            # Crear perfil y forzar cambio de contraseña
            try:
                profile, _ = Profile.objects.get_or_create(user=user, defaults={
                    "telefono": form.cleaned_data.get("telefono"),
                    "nac": form.cleaned_data.get("nac"),
                    "dni": form.cleaned_data.get("dni"),
                    "must_change_password": True,
                    "password_expires_at": timezone.now() + timedelta(days=30)
                })
                profile.must_change_password = True
                profile.password_expires_at = timezone.now() + timedelta(days=30)
                profile.save()
                # Mostrar la contraseña generada
                messages.success(request, f'Usuario registrado. Contraseña temporal: {new_password}')
                return redirect('users_list')
            except IntegrityError:
                user.delete()
                messages.error(request, 'Ya existe un usuario con esa cédula.')
        # Si no se creó el usuario, se muestran los errores en el formulario
    else:
        form = CustomUserCreationForm()
    return render(request, 'dashboard/users/register.html', {'form': form, 'groups': groups})

def login_view(request):
    from django.utils import timezone
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        user_qs = User.objects.filter(username=username)
        user = user_qs.first() if user_qs.exists() else None
        if form.is_valid():
            if user and not user.is_active:
                messages.error(request, 'Su usuario está bloqueado. Por favor, comuníquese con el administrador del sistema.')
                return render(request, 'dashboard/users/login.html', {'form': form})
            profile, _ = Profile.objects.get_or_create(user=form.get_user(), defaults={"dni": 0})
            login(request, form.get_user())
            # Resetear contador de intentos fallidos
            request.session['failed_attempts'] = 0
            expired = profile.password_expires_at and profile.password_expires_at <= timezone.now()
            if profile.must_change_password or expired:
                if expired:
                    profile.must_change_password = True
                    profile.save()
                    messages.warning(request, 'Su contraseña ha expirado. Debe cambiarla para continuar.')
                else:
                    messages.warning(request, 'Debe cambiar su contraseña antes de continuar.')
                return redirect('change_password')
            return redirect('dashboard')
        else:
            # Si el usuario existe y no está bloqueado, aumentar el contador de intentos fallidos
            if user and user.is_active:
                failed = request.session.get('failed_attempts', 0) + 1
                request.session['failed_attempts'] = failed
                if failed >= 5:
                    user.is_active = False
                    user.save()
                    messages.error(request, 'Su usuario ha sido bloqueado por exceder el número de intentos fallidos. Contacte al administrador.')
            elif user and not user.is_active:
                messages.error(request, 'Su usuario está bloqueado. Por favor, comuníquese con el administrador del sistema.')
        # ...existing code...
    else:
        form = AuthenticationForm()
    return render(request, 'dashboard/users/login.html', {'form': form})

@login_required
def dashboard_view(request):
	profile, created = Profile.objects.get_or_create(user=request.user)
	return render(request, 'dashboard/dashboard.html', {'profile': profile})

@login_required
def edit_profile_view(request):
	user_id = request.GET.get('user_id')
	groups = Group.objects.all()
	if user_id and request.user.is_superuser:
		user = get_object_or_404(User, id=user_id)
	else:
		user = request.user
	profile, created = Profile.objects.get_or_create(user=user, defaults={"dni": 0})
	if request.method == 'POST':
		email = request.POST.get('email')
		if User.objects.filter(email=email).exclude(id=user.id).exists():
			messages.error(request, 'Ya existe un usuario con ese correo electrónico.')
		else:
			user.first_name = request.POST.get('first_name')
			user.last_name = request.POST.get('last_name')
			user.email = email
			profile.telefono = request.POST.get('telefono')
			profile.nac = request.POST.get('nac')
			dni = request.POST.get('dni')
			if dni:
				profile.dni = int(dni)
			profile.bio = request.POST.get('bio')
			avatar = request.FILES.get('avatar')
			if avatar:
				profile.avatar = avatar
			user.save()
			profile.save()
			# Asignar grupo/rol si es admin
			if request.user.is_superuser:
				group_id = request.POST.get('groups')
				if group_id:
					group = get_object_or_404(Group, id=group_id)
					user.groups.clear()
					user.groups.add(group)
			if request.user.is_superuser and user_id:
				return redirect('users_list')
			return redirect('dashboard')
	return render(request, 'dashboard/users/edit_profile.html', {'profile': profile, 'user': user, 'groups': groups})

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Empresa, UnidadOrganizativa, Departamento, Cargo
from django.urls import reverse_lazy

class EmpresaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Empresa
    template_name = 'dashboard/admin/empresa/list.html'
    context_object_name = 'empresas'
    permission_required = 'dashboard.view_empresa'

class EmpresaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Empresa
    fields = ['nombre', 'razon_social', 'rif', 'titulo', 'direccion', 'telefono', 'email']
    template_name = 'dashboard/admin/empresa/create.html'
    success_url = reverse_lazy('empresa_list')
    permission_required = 'dashboard.add_empresa'

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            if str(e) == 'Solo puede existir una empresa en el sistema.':
                messages.error(self.request, 'Solo puede existir una empresa en el sistema.')
                return redirect('empresa_list')
            raise e

class EmpresaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Empresa
    fields = ['nombre', 'razon_social', 'rif', 'titulo', 'direccion', 'telefono', 'email']
    template_name = 'dashboard/admin/empresa/update.html'
    success_url = reverse_lazy('empresa_list')
    permission_required = 'dashboard.change_empresa'

class EmpresaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Empresa
    template_name = 'dashboard/admin/empresa/delete.html'
    success_url = reverse_lazy('empresa_list')
    permission_required = 'dashboard.delete_empresa'

# Repetir estructura para UnidadOrganizativa, Departamento y Cargo
class UnidadListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = UnidadOrganizativa
    template_name = 'dashboard/admin/unidad/list.html'
    context_object_name = 'unidades'
    permission_required = 'dashboard.view_unidadorganizativa'

class UnidadCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = UnidadOrganizativa
    fields = ['empresa', 'prefijo', 'nombre', 'descripcion']
    template_name = 'dashboard/admin/unidad/create.html'
    success_url = reverse_lazy('unidad_list')
    permission_required = 'dashboard.add_unidadorganizativa'

class UnidadUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = UnidadOrganizativa
    fields = ['empresa', 'prefijo', 'nombre', 'descripcion']
    template_name = 'dashboard/admin/unidad/update.html'
    success_url = reverse_lazy('unidad_list')
    permission_required = 'dashboard.change_unidadorganizativa'

class UnidadDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = UnidadOrganizativa
    template_name = 'dashboard/admin/unidad/delete.html'
    success_url = reverse_lazy('unidad_list')
    permission_required = 'dashboard.delete_unidadorganizativa'

class DepartamentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Departamento
    template_name = 'dashboard/admin/departamento/list.html'
    context_object_name = 'departamentos'
    permission_required = 'dashboard.view_departamento'

class DepartamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Departamento
    fields = ['unidad', 'nombre', 'descripcion']
    template_name = 'dashboard/admin/departamento/create.html'
    success_url = reverse_lazy('departamento_list')
    permission_required = 'dashboard.add_departamento'

class DepartamentoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Departamento
    fields = ['unidad', 'nombre', 'descripcion']
    template_name = 'dashboard/admin/departamento/update.html'
    success_url = reverse_lazy('departamento_list')
    permission_required = 'dashboard.change_departamento'

class DepartamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Departamento
    template_name = 'dashboard/admin/departamento/delete.html'
    success_url = reverse_lazy('departamento_list')
    permission_required = 'dashboard.delete_departamento'

class CargoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cargo
    template_name = 'dashboard/admin/cargo/list.html'
    context_object_name = 'cargos'
    permission_required = 'dashboard.view_cargo'

class CargoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Cargo
    fields = ['departamento', 'nombre', 'descripcion']
    template_name = 'dashboard/admin/cargo/create.html'
    success_url = reverse_lazy('cargo_list')
    permission_required = 'dashboard.add_cargo'

class CargoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cargo
    fields = ['departamento', 'nombre', 'descripcion']
    template_name = 'dashboard/admin/cargo/update.html'
    success_url = reverse_lazy('cargo_list')
    permission_required = 'dashboard.change_cargo'

class CargoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Cargo
    template_name = 'dashboard/admin/cargo/delete.html'
    success_url = reverse_lazy('cargo_list')
    permission_required = 'dashboard.delete_cargo'

from .models import Empresa

def get_empresa():
    return Empresa.objects.first()
