from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','stock']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit','Guardar'))
