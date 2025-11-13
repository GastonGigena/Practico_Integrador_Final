from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    # R: Listar
    path('', views.VentaListView.as_view(), name='list'),
    
    # C: Crear
    path('create/', views.VentaCreateView.as_view(), name='create'),
    
    # R: Detalle
    path('<int:pk>/', views.VentaDetailView.as_view(), name='detail'),
    
    # --- RUTAS AÑADIDAS PARA EL CRUD ---
    
    # U: Actualizar (usa PK)
    path('<int:pk>/update/', views.VentaUpdateView.as_view(), name='update'),
    
    # D: Eliminar (usa PK)
    path('<int:pk>/delete/', views.VentaDeleteView.as_view(), name='delete'),
    
    # --- RUTAS FUNCIONALES ---
    
    # R: Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # R: PDF (usa venta_id)
    path('<int:venta_id>/pdf/', views.comprobante_pdf, name='comprobante_pdf'),
]