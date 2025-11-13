from django.urls import path
from . import views
app_name = 'productos'

urlpatterns = [
    # R: Listar
    path('', views.ProductoListView.as_view(), name='list'),
    
    # C: Crear
    path('create/', views.ProductoCreateView.as_view(), name='create'),
    
    # --- RUTAS AÑADIDAS PARA EL CRUD ---
    
    # R: Detalle (Retrieve)
    path('<int:pk>/', views.ProductoDetailView.as_view(), name='detail'),
    
    # U: Actualizar (Update)
    path('<int:pk>/update/', views.ProductoUpdateView.as_view(), name='update'),
    
    # D: Eliminar (Delete)
    path('<int:pk>/delete/', views.ProductoDeleteView.as_view(), name='delete'),
]