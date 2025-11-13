import uuid
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=32, unique=True, editable=False)

    # AÑADIR CLASE META PARA ORDENACIÓN
    class Meta:
        # Ordenar por el ID descendente (el último ID agregado es el más reciente)
        # Esto asegura que los productos más nuevos aparezcan primero en las listas.
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"