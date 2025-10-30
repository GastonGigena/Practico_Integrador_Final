from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from .forms import VentaForm, ItemVentaFormSet
from .models import Venta, ItemVenta, Producto


class VentaListView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas/venta_list.html'
    paginate_by = 10


class VentaDetailView(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = 'ventas/venta_detail.html'


class VentaCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
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
                    it.save()  # Aquí puede lanzar ValidationError desde signals.py
            except ValidationError as e:
                # Si hay stock insuficiente, eliminamos la venta incompleta
                venta.delete()
                messages.error(request, e.message)
                return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset})

            messages.success(request, 'Venta creada correctamente.')
            return redirect('ventas:detail', pk=venta.pk)

        return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset})


def dashboard(request):
    # Ventas totales por día
    ventas = Venta.objects.order_by('fecha').values('fecha').annotate(total_dia=Sum('total'))
    fechas = [v['fecha'].strftime('%Y-%m-%d') for v in ventas]
    totales = [float(v['total_dia']) for v in ventas]

    # Productos más vendidos
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
    venta = get_object_or_404(Venta, id=venta_id)
    html_string = render_to_string('ventas/comprobante.html', {'venta': venta})

    # Generar el PDF con ruta absoluta para que WeasyPrint encuentre el logo
    pdf_file = HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')  # importante para imágenes en PDF
    ).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="comprobante_{venta.id}.pdf"'
    return response



