from django.urls import path
from . import views
app_name = 'productos'
urlpatterns = [
    path('', views.ProductoListView.as_view(), name='list'),
    path('create/', views.ProductoCreateView.as_view(), name='create'),
]
