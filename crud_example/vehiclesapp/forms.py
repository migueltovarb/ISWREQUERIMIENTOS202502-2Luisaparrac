from django import forms
from .models import vehiculo   

class VehicleForm(forms.ModelForm):

    class Meta:
        model = vehiculo   

        fields = [
            "placa",
            "marca",
            "modelo",
            "color",   
        ]

        labels = {
            'placa': 'Número de placa',
            'marca': 'Marca del vehículo',
            'modelo': 'Modelo del vehículo',
            'color': 'Color del vehículo',   
        }

        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
        }