from django import forms
from .models import Tarea, Proyecto
from usuarios.models import Usuario


class TareaForm(forms.ModelForm):

    fecha_limite = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = Tarea
        fields = ["nombre", "descripcion", "fecha_limite", "prioridad", "proyecto", "asignados"]

        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ejemplo: Re-branding"}),
            "descripcion": forms.Textarea(attrs={"rows": 4}),
            "prioridad": forms.Select(),
            "proyecto": forms.Select(),
            "asignados": forms.CheckboxSelectMultiple(),
        }


class ProyectoForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)

    class Meta:
        model = Proyecto
        fields = ["nombre", "descripcion", "fecha_inicio", "fecha_fin", "jefe"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # jefe debe ser un usuario con rol JEFE
        self.fields['jefe'].queryset = Usuario.objects.filter(rol=Usuario.Rol.JEFE)


class ProyectoEditForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}), required=False)
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}), required=False)

    class Meta:
        model = Proyecto
        fields = ["nombre", "descripcion", "fecha_inicio", "fecha_fin", "jefe"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del proyecto"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "jefe": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # jefe debe ser un usuario con rol JEFE
        self.fields['jefe'].queryset = Usuario.objects.filter(rol=Usuario.Rol.JEFE)