from django import forms
from App.models import Proveedor, Empleado, Compra, Producto

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields='__all__'
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
            'Representante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Representante'}),
            'Contacto':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contacto'})}
        

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__' 
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email ID'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'genero': forms.Select(attrs={'class': 'form-control'}, choices=[('M', 'Masculino'), ('F', 'Femenino')]),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edad'}),
            'tipo': forms.RadioSelect(attrs={'class': 'form-check-input'},choices=[('Manager', 'Manager'), ('Empleado', 'Empleado')]),
        }

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'producto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'})
        }

class ProductoForm (forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'})


        }