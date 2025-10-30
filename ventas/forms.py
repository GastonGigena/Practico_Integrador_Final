from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Venta, ItemVenta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit','Crear Venta'))

class ItemVentaForm(forms.ModelForm):
    class Meta:
        model = ItemVenta
        fields = ['producto','cantidad','precio_unitario']

ItemVentaFormSet = inlineformset_factory(
    Venta, ItemVenta, form=ItemVentaForm, extra=1, can_delete=True
)

class CSVUploadForm(forms.Form):
    archivo = forms.FileField(label="Seleccionar archivo CSV")