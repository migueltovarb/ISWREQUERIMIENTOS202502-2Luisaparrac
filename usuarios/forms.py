from django import forms
from django.contrib.auth import authenticate
from .models import Usuario


class LoginForm(forms.Form):

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "placeholder": "nombre@correo.com",
            "class": "form-control"
        })
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Contraseña",
            "class": "form-control"
        }),
        min_length=8
    )

    def clean(self):
        cleaned_data = super().clean()
        correo = cleaned_data.get("correo")
        password = cleaned_data.get("password")

        if not correo or not password:
            return cleaned_data

        try:
            usuario = Usuario.objects.get(email=correo)
        except Usuario.DoesNotExist:
            raise forms.ValidationError("Correo o contraseña incorrectos")

        if usuario.esta_bloqueado():
            raise forms.ValidationError(
                "Tu cuenta está bloqueada temporalmente por múltiples intentos fallidos."
            )

        user = authenticate(
            request=self.request,
            email=correo,
            password=password
        )

        if user is None:
            usuario.registrar_fallo_login()
            raise forms.ValidationError("Correo o contraseña incorrectos")

        usuario.resetear_intentos()
        cleaned_data["user"] = user
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get("user")



#  Crear usuarios

class UsuarioCreateForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña provisional",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Mínimo 8 caracteres",
            "class": "form-control"
        }),
        min_length=8
    )

    class Meta:
        model = Usuario
        fields = ["nombre_completo", "email", "password", "rol", "is_active"]

        widgets = {
            "nombre_completo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre completo"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "correo@empresa.com"
            }),
            "rol": forms.Select(attrs={
                "class": "form-control"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "checkbox-active"
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        # Asegurar que nombre_completo se asigne explícitamente
        nc = self.cleaned_data.get("nombre_completo")
        if nc is not None:
            user.nombre_completo = nc

        pwd = self.cleaned_data.get("password")
        if not pwd:
            raise forms.ValidationError("La contraseña es obligatoria.")
        user.set_password(pwd)
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con ese correo.')
        return email


#  Edicion de usuarios


class UsuarioEditForm(forms.ModelForm):
    password = forms.CharField(
        label="Nueva contraseña (opcional)",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Déjalo vacío si no deseas cambiarla"
        }),
        required=False,
        min_length=8
    )

    class Meta:
        model = Usuario
        fields = ["nombre_completo", "email", "rol", "is_active"]

        widgets = {
            "nombre_completo": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),
            "rol": forms.Select(attrs={
                "class": "form-control"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "checkbox-active"
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Usuario.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe otro usuario con ese correo.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Asegurar que nombre_completo se actualice desde el formulario
        nc = self.cleaned_data.get('nombre_completo')
        if nc is not None:
            user.nombre_completo = nc
        pwd = self.cleaned_data.get("password")
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user
    
