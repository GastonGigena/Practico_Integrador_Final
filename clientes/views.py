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
from .models import Cliente
from .forms import ClienteForm

# --- VISTAS EXISTENTES (Listar y Crear) ---

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    paginate_by = 10
    

class ClienteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'clientes.add_cliente'
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:list')

# -------------------------------------------
# --- VISTAS FALTANTES (Detalle, Actualizar, Eliminar) ---
# -------------------------------------------

# R: Detalle (Retrieve)
class ClienteDetailView(LoginRequiredMixin, DetailView):
    """Muestra la información detallada de un cliente."""
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente' # Define el nombre de la variable en el template

# U: Actualizar (Update)
class ClienteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Permite modificar los datos de un cliente existente."""
    # Requiere el permiso de cambio/modificación
    permission_required = 'clientes.change_cliente' 
    model = Cliente
    form_class = ClienteForm
    # Reutiliza el template de creación (cliente_form.html)
    template_name = 'clientes/cliente_form.html' 
    
    # Redirige a la lista después de actualizar
    success_url = reverse_lazy('clientes:list') 

# D: Eliminar (Delete)
class ClienteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Permite eliminar un cliente."""
    # Requiere el permiso de eliminación
    permission_required = 'clientes.delete_cliente' 
    model = Cliente
    # Template para confirmar la eliminación
    template_name = 'clientes/cliente_confirm_delete.html' 
    # Redirige a la lista después de eliminar
    success_url = reverse_lazy('clientes:list')