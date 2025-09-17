from django import forms
from django.contrib.auth.forms import UserCreationForm
from dashboard.models import User
from .models import Profile
from django.db import transaction, IntegrityError
from django.contrib.auth.models import Group, Permission
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div




class CustomUserCreationForm(forms.ModelForm):
    dni = forms.CharField(label='Cédula', max_length=12, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'dni'}))
    first_name = forms.CharField(label='Nombre', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name'}))
    last_name = forms.CharField(label='Apellido', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name'}))
    email = forms.EmailField(label='Correo electrónico', required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}))
    telefono = forms.CharField(label='Teléfono', max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'telefono'}))
    nac = forms.ChoiceField(label='Nacionalidad', choices=Profile.NAC_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control', 'id': 'nac'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'}), required=True)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'}), required=True)



    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'id': 'dni'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'id': 'telefono'}),
            'nac': forms.Select(attrs={'class': 'form-control', 'id': 'nac'}),

        }
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned_data


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con ese correo electrónico.')
        return email

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni.isdigit():
            raise forms.ValidationError('La cédula debe contener solo números.')
        if Profile.objects.filter(dni=dni).exists():
            raise forms.ValidationError('Ya existe un usuario con esa cédula.')
        if int(dni) <= 0:
            raise forms.ValidationError('La cédula debe ser un número positivo.')
        return dni

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            try:
                with transaction.atomic():
                    user.save()
                    profile = Profile.objects.create(
                        user=user,
                        telefono=self.cleaned_data['telefono'],
                        nac=self.cleaned_data['nac'],
                        dni=self.cleaned_data['dni']
                    )
            except IntegrityError:
                self.add_error('dni', 'Ya existe un usuario con esa cédula.')
                self.add_error(None, 'Ya existe un usuario con esa cédula.')
                user.delete()
                return None
        return user


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if FormHelper:
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Guardar'))


class GroupPermissionsForm(forms.Form):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all().order_by('content_type__app_label', 'codename'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Permisos'
    )

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', None) or {}
        super().__init__(*args, **kwargs)
        if 'permissions' in initial:
            self.fields['permissions'].initial = initial['permissions']
        if FormHelper:
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Field('permissions')
            )
            self.helper.add_input(Submit('submit', 'Guardar permisos'))


class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name', 'placeholder': 'Nombre'}))
    last_name = forms.CharField(label='Apellido', max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name', 'placeholder': 'Apellido'}))
    email = forms.EmailField(label='Correo electrónico', required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Correo electrónico'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1', 'placeholder': 'Contraseña'}), required=True)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2', 'placeholder': 'Confirmar contraseña'}), required=True)
    dni = forms.CharField(label='Cédula', max_length=12, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'dni', 'placeholder': 'Cédula'}))
    telefono = forms.CharField(label='Teléfono', max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'telefono', 'placeholder': 'Teléfono'}))
    nac = forms.ChoiceField(label='Nacionalidad', choices=Profile.NAC_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control', 'id': 'nac', 'placeholder': 'Nacionalidad'}))
    avatar = forms.ImageField(label='Avatar', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'avatar', 'accept': 'image/*'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if FormHelper:
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.form_enctype = 'multipart/form-data'
            self.helper.layout = Layout(
                Div(
                    Div(Field('first_name'), css_class='col-md-6'),
                    Div(Field('last_name'), css_class='col-md-6'),
                    css_class='row'
                ),
                Div(
                    Div(Field('email'), css_class='col-md-6'),
                    Div(Field('dni'), css_class='col-md-6'),
                    css_class='row'
                ),
                Div(
                    Div(Field('telefono'), css_class='col-md-6'),
                    Div(Field('nac'), css_class='col-md-6'),
                    css_class='row'
                ),
                Div(
                    Div(Field('password1'), css_class='col-md-6'),
                    Div(Field('password2'), css_class='col-md-6'),
                    css_class='row'
                ),
                Div(Field('avatar'), css_class='mb-3'),
                Submit('submit', 'Guardar', css_class='btn btn-primary mt-3')
            )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'dni', 'telefono', 'nac', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if FormHelper:
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Guardar'))




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telefono', 'nac', 'dni', 'bio', 'avatar']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'id': 'telefono'}),
            'nac': forms.Select(attrs={'class': 'form-control', 'id': 'nac'}), 
            'dni': forms.TextInput(attrs={'class': 'form-control', 'id': 'dni'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'avatar', 'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'id': 'bio', 'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'  # Importante para subir archivos
        self.helper.layout = Layout(
            Field('telefono'),
            Field('nac'),
            Field('dni'),
            Field('bio'),
            Field('avatar'),
            Submit('submit', 'Guardar cambios', css_class='btn btn-primary mt-3')
        )

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if not avatar:
            return avatar
        # Validate content type
        content_type = avatar.content_type
        if not content_type.startswith('image/'):
            raise forms.ValidationError('El archivo debe ser una imagen (jpg, png, gif).')
        # Validate file size (max 2MB)
        max_size = 2 * 1024 * 1024
        if avatar.size > max_size:
            raise forms.ValidationError('El tamaño máximo permitido es 2MB.')
        return avatar