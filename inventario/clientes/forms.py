# clientes/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # Nombres de campos corregidos
        fields = ['nombre', 'apellido', 'numero_documento', 'e_mail', 'telefono', 'direccion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Nombres de campos corregidos
            Field('nombre'),
            Field('apellido'),
            Field('numero_documento'),
            Field('e_mail'),
            Field('telefono'),
            Field('direccion'),
            Submit('submit', 'Guardar', css_class='btn-success mt-3')
        )
