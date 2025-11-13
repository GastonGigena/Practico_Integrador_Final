from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView # <--- Importar DeleteView
from django.urls import reverse_lazy # <--- Importar reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from .forms import VentaForm, ItemVentaFormSet
from .models import Venta, ItemVenta, Producto

# --- VISTAS EXISTENTES (Listar y Detalle) ---

class VentaListView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas/venta_list.html'
    context_object_name = 'ventas'
    paginate_by = 10
    
    def get_queryset(self):
        return Venta.objects.all().order_by('-fecha')


class VentaDetailView(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = 'ventas/venta_detail.html'

# --- VISTA EXISTENTE (Crear) ---

class VentaCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    # ... (El contenido de esta vista no se modifica) ...
    permission_required = 'ventas.add_venta'

    def get(self, request):
        form = VentaForm()
        formset = ItemVentaFormSet()
        return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset})

    def post(self, request):
        form = VentaForm(request.POST)
        formset = ItemVentaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            venta = form.save(commit=False)
            venta.total = 0
            venta.save()
            items = formset.save(commit=False)
            try:
                for it in items:
                    it.venta = venta
                    if not it.precio_unitario:
                        it.precio_unitario = it.producto.precio
                    it.save()
            except ValidationError as e:
                venta.delete()
                messages.error(request, e.message)
                return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset})

            messages.success(request, 'Venta creada correctamente.')
            return redirect('ventas:detail', pk=venta.pk)

        return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset})


# -------------------------------------------
# --- VISTAS FALTANTES (Actualizar y Eliminar) ---
# -------------------------------------------

# U: Actualizar (Update) - Se mantiene como View para manejar el FormSet
class VentaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'ventas.change_venta'

    def get_object(self):
        return get_object_or_404(Venta, pk=self.kwargs['pk'])

    def get(self, request, pk):
        venta = self.get_object()
        form = VentaForm(instance=venta)
        # Inicializa el formset con los ítems existentes de la venta
        formset = ItemVentaFormSet(instance=venta) 
        return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset, 'venta': venta})

    def post(self, request, pk):
        venta = self.get_object()
        form = VentaForm(request.POST, instance=venta)
        # Pasa la instancia para que el formset sepa qué ítems actualizar/eliminar
        formset = ItemVentaFormSet(request.POST, instance=venta) 
        
        if form.is_valid() and formset.is_valid():
            # 1. Guardar Venta (el total se recalculará en señales)
            venta = form.save()

            # 2. Guardar Ítems (esto debe manejar la lógica de stock en signals.py)
            try:
                formset.save(commit=False) # Guarda los ítems con commit=False para permitir ajustes

                # Recorremos los ítems que NO están marcados para eliminación
                for it in formset.new_objects + formset.changed_objects:
                    if not it.precio_unitario:
                        it.precio_unitario = it.producto.precio
                    it.venta = venta # Asignar la venta por si es un nuevo ítem
                    it.save()
                
                # Eliminar los ítems marcados para eliminación
                for it in formset.deleted_objects:
                    it.delete() # Esto debe disparar la señal para devolver el stock

            except ValidationError as e:
                messages.error(request, e.message)
                return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset, 'venta': venta})


            messages.success(request, 'Venta actualizada correctamente.')
            return redirect('ventas:detail', pk=venta.pk)

        return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset, 'venta': venta})

# D: Eliminar (Delete) - Se usa DeleteView estándar
class VentaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Permite eliminar una venta. La eliminación debe disparar la señal para devolver todo el stock."""
    permission_required = 'ventas.delete_venta'
    model = Venta
    template_name = 'ventas/venta_confirm_delete.html'
    success_url = reverse_lazy('ventas:list') 


# --- FUNCIONES EXISTENTES (Dashboard y PDF) ---

def dashboard(request):
    # ... (El contenido de esta función no se modifica) ...
    ventas = Venta.objects.order_by('fecha').values('fecha').annotate(total_dia=Sum('total'))
    fechas = [v['fecha'].strftime('%Y-%m-%d') for v in ventas]
    totales = [float(v['total_dia']) for v in ventas]

    productos = ItemVenta.objects.values('producto__nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido')
    nombres_productos = [p['producto__nombre'] for p in productos]
    cantidades_vendidas = [p['total_vendido'] for p in productos]

    context = {
        'fechas': fechas,
        'totales': totales,
        'nombres_productos': nombres_productos,
        'cantidades_vendidas': cantidades_vendidas
    }
    return render(request, 'ventas/dashboard.html', context)


def comprobante_pdf(request, venta_id):
    # ... (El contenido de esta función no se modifica) ...
    venta = get_object_or_404(Venta, id=venta_id)
    html_string = render_to_string('ventas/comprobante.html', {'venta': venta})

    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="comprobante_{venta.id}.pdf"'
    return response