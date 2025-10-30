from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.VentaListView.as_view(), name='list'),
    path('create/', views.VentaCreateView.as_view(), name='create'),
    path('<int:pk>/', views.VentaDetailView.as_view(), name='detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:venta_id>/pdf/', views.comprobante_pdf, name='comprobante_pdf'),
    
]
