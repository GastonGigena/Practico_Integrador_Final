from django.urls import path
from . import views
app_name = 'clientes'

urlpatterns = [
    # R: Listar
    path('', views.ClienteListView.as_view(), name='list'),
    
    # C: Crear
    path('create/', views.ClienteCreateView.as_view(), name='create'),
    
    # --- RUTAS AÑADIDAS PARA EL CRUD ---
    
    # R: Detalle (Retrieve)
    path('<int:pk>/', views.ClienteDetailView.as_view(), name='detail'),
    
    # U: Actualizar (Update)
    path('<int:pk>/update/', views.ClienteUpdateView.as_view(), name='update'),
    
    # D: Eliminar (Delete)
    path('<int:pk>/delete/', views.ClienteDeleteView.as_view(), name='delete'),
]