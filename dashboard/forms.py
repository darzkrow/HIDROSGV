from django import forms
from django.contrib.auth.forms import UserCreationForm
from dashboard.models import User
from .models import Profile
from django.db import transaction, IntegrityError

class CustomUserCreationForm(forms.ModelForm):
    dni = forms.IntegerField(label='Cédula', required=True)
    first_name = forms.CharField(label='Nombre', max_length=30, required=True)
    last_name = forms.CharField(label='Apellido', max_length=30, required=True)
    email = forms.EmailField(label='Correo electrónico', required=True)
    telefono = forms.CharField(label='Teléfono', max_length=15, required=False)
    nac = forms.ChoiceField(label='Nacionalidad', choices=Profile.NAC_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'dni', 'first_name', 'last_name', 'email')


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con ese correo electrónico.')
        return email

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Profile.objects.filter(dni=dni).exists():
            raise forms.ValidationError('Ya existe un usuario con esa cédula.')
        if dni <= 0:
            raise forms.ValidationError('La cédula debe ser un número positivo.')
        return dni

    def save(self, commit=True):

        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
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
                user.delete()
                return None
        return user
