from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ItemVenta
from productos.models import Producto
from django.db.models import Sum
from django.core.exceptions import ValidationError

@receiver(post_save, sender=ItemVenta)
def descontar_stock_y_actualizar_total(sender, instance, created, **kwargs):
    if created:
        producto = instance.producto
        if instance.cantidad > producto.stock:
            # En lugar de ValueError, lanzamos ValidationError
            raise ValidationError(f"Stock insuficiente para {producto.nombre}")
        producto.stock -= instance.cantidad
        producto.save()
        venta = instance.venta
        total = venta.items.aggregate(s=Sum('subtotal'))['s'] or 0
        venta.total = total
        venta.save()
