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
    tipo = forms.ChoiceField(
        choices=[('Manager', 'Manager'), ('Bodeguero', 'Bodeguero'), ('Vendedor', 'Vendedor')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True,
        initial='Manager'
    )
    habilitado = forms.BooleanField(
        required=False,
        initial=True,  # Marcado por defecto
        label='Habilitado en la tienda'
    )

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
            'tipo': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),        }




class ProductoForm (forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Imagen de producto'})

        }
class CompraForm(forms.ModelForm):

    class Meta:
        model = Compra
        fields = ['proveedor', 'producto', 'cantidad', 'precio']
        widgets = {
            #las ids son para correr el script de javascript de manera correcta
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad' ,'id':'id_cantidad','required': 'required'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio', 'id':'id_precio','required': 'required'}),
            'proveedor': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'producto': forms.Select(attrs={'class': 'form-select', 'required': 'required' , 'id':'id_producto'})
        }
    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(habilitado=True)
        self.fields['proveedor'].queryset = Proveedor.objects.filter(habilitado=True)