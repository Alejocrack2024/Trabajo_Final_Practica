from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Div, Row, Column
from .models import Venta, ItemVenta, Producto

# ==============================================================================
# 1. Formulario para la Cabecera de la Venta (Venta)
# ==============================================================================

class VentaForm(forms.ModelForm):
    """Formulario para los datos principales (cabecera) de la Venta."""
    class Meta:
        model = Venta
        fields = ['cliente']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML('<h3 class="mt-4 mb-3 text-primary">Datos del Comprobante</h3>'),
                'cliente',
            ),
        )
        self.fields['cliente'].label = "Cliente"

# ==============================================================================
# 2. Formulario para los Ítems (ItemVenta)
# ==============================================================================

class ItemVentaForm(forms.ModelForm):
    """Formulario para una sola línea de ItemVenta."""
    
    precio_actual = forms.DecimalField(
        label='Precio Actual',
        required=False,
        max_digits=10, 
        decimal_places=2,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}) 
    )
    
    class Meta:
        model = ItemVenta
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control select-producto'}),
            'cantidad': forms.NumberInput(attrs={'min': 1, 'class': 'form-control input-cantidad'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 1. Obtenemos la instancia si existe
        instance = kwargs.get('instance')
        
        # 2. Corregido: Verificamos si existe la instancia y si tiene un producto antes de acceder.
        # Esto evita el error en el formulario vacío.
        if instance and hasattr(instance, 'producto') and instance.producto:
            self.fields['precio_actual'].initial = instance.producto.precio_venta
        
        # 3. Mantenemos la lógica para la inicialización con datos
        elif self.initial.get('producto'):
            try:
                producto = Producto.objects.get(pk=self.initial['producto'])
                self.fields['precio_actual'].initial = producto.precio_venta
            except (Producto.DoesNotExist, ValueError):
                pass
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Column('producto', css_class='form-group col-md-5 mb-0'),
                Column('cantidad', css_class='form-group col-md-2 mb-0'),
                Column('precio_actual', css_class='form-group col-md-3 mb-0'),
                Column(HTML('<div class="form-group pt-4 delete-button-container"></div>'), css_class='form-group col-md-2 mb-0'),
            ),
        )

# ==============================================================================
# 3. Formset Factory para Ítems
# ==============================================================================

ItemVentaFormSet = inlineformset_factory(
    Venta, 
    ItemVenta, 
    form=ItemVentaForm, 
    extra=1, 
    can_delete=True, 
    fields=('producto', 'cantidad'),
)
