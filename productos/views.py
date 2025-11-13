from django.views.generic import (
    ListView, 
    CreateView, 
    # Nuevas importaciones para CRUD completo
    DetailView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Producto
from .forms import ProductoForm
# Importación necesaria para el buscador: Q objects
from django.db.models import Q 

# --- VISTAS EXISTENTES (Listar y Crear) ---

class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    paginate_by = 10
    
    # Método modificado para añadir la lógica de búsqueda
    def get_queryset(self):
        # 1. Obtener el queryset base
        queryset = super().get_queryset()
        
        # 2. Obtener el término de búsqueda (query) de la URL (?q=...)
        query = self.request.GET.get('q')
        
        # 3. Aplicar filtro si existe el término
        if query:
            # Filtramos por nombre, descripción o SKU. El icontains es case-insensitive.
            queryset = queryset.filter(
                Q(nombre__icontains=query) | 
                Q(descripcion__icontains=query) |
                Q(sku__icontains=query)
            ).distinct()
            
        return queryset

class ProductoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'productos.add_producto'
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('productos:list')

# -------------------------------------------
# --- VISTAS FALTANTES (Detalle, Actualizar, Eliminar) ---
# -------------------------------------------

# R: Detalle (Retrieve)
class ProductoDetailView(LoginRequiredMixin, DetailView):
    """Muestra la información detallada de un producto."""
    model = Producto
    template_name = 'productos/producto_detail.html'
    context_object_name = 'producto' # Define el nombre de la variable en el template

# U: Actualizar (Update)
class ProductoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Permite modificar los datos de un producto existente."""
    # Requiere el permiso de cambio/modificación
    permission_required = 'productos.change_producto' 
    model = Producto
    form_class = ProductoForm
    # Reutiliza el template de creación (producto_form.html)
    template_name = 'productos/producto_form.html' 
    
    # Redirige a la lista después de actualizar
    success_url = reverse_lazy('productos:list') 

# D: Eliminar (Delete)
class ProductoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Permite eliminar un producto."""
    # Requiere el permiso de eliminación
    permission_required = 'productos.delete_producto' 
    model = Producto
    # Template para confirmar la eliminación
    template_name = 'productos/producto_confirm_delete.html' 
    # Redirige a la lista después de eliminar
    success_url = reverse_lazy('productos:list')