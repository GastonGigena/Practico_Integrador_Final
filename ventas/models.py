import uuid
from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from productos.models import Producto

class Venta(models.Model):
    codigo_venta = models.CharField(max_length=32, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # AÑADIR CLASE META PARA ORDENACIÓN
    class Meta:
        # Ordenar por fecha descendente (el más nuevo primero)
        ordering = ['-fecha'] 

    def save(self, *args, **kwargs):
        if not self.codigo_venta:
            self.codigo_venta = f"VEN-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo_venta} - {self.cliente}"

class ItemVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # AÑADIR CLASE META PARA ORDENACIÓN
    class Meta:
        # Ordenar por el ID descendente (el último ID agregado es el más reciente)
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)