from django import forms 
from App.models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields='__all__'
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
            'Representante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Representante'}),
            'Contacto':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contacto'})}