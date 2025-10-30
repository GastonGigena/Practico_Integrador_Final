from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Cliente
from .forms import ClienteForm

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
