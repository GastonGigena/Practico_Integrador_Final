from django.urls import path
from . import views
app_name = 'clientes'
urlpatterns = [
    path('', views.ClienteListView.as_view(), name='list'),
    path('create/', views.ClienteCreateView.as_view(), name='create'),
]
