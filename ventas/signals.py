from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.db import transaction 

# Importamos los modelos (para usarlos en el cuerpo de las funciones)
from .models import ItemVenta, Venta
from productos.models import Producto 


def actualizar_total_venta(venta):
    """Calcula y guarda el total de la venta."""
    # Suma los subtotales de todos los items relacionados a esta venta
    total = venta.items.aggregate(s=Sum('subtotal'))['s'] or 0
    venta.total = total
    venta.save()


# ----------------------------------------------------------------------
# 1. GESTIÓN DE STOCK AL CREAR/ACTUALIZAR ÍTEM (post_save)
# ----------------------------------------------------------------------

# **IMPORTANTE:** Usamos la referencia de string 'ventas.ItemVenta' para evitar errores de AppRegistryNotReady
@receiver(post_save, sender='ventas.ItemVenta')
def gestionar_stock_y_total(sender, instance, created, **kwargs):
    producto = instance.producto
    
    # Aseguramos que las operaciones de stock sean atómicas
    with transaction.atomic():
        if created:
            # ESCENARIO 1: CREACIÓN
            if instance.cantidad > producto.stock:
                 raise ValidationError(f"Stock insuficiente para {producto.nombre} durante la creación.")
                 
            producto.stock -= instance.cantidad
            producto.save()
            
        else:
            # ESCENARIO 2: ACTUALIZACIÓN (Lógica de diferencia neta)
            try:
                # Usamos ItemVenta.objects.get() para obtener la instancia antigua
                old_instance = ItemVenta.objects.get(pk=instance.pk)
                
                # Diferencia: (Cantidad antigua) - (Cantidad nueva)
                diferencia_stock = old_instance.cantidad - instance.cantidad
                
                # Devolver stock (la cantidad disminuyó)
                if diferencia_stock > 0:
                    producto.stock += diferencia_stock
                
                # Descontar más stock (la cantidad aumentó)
                elif diferencia_stock < 0:
                    stock_a_descontar = abs(diferencia_stock)
                    if stock_a_descontar > producto.stock:
                         raise ValidationError(f"Stock insuficiente para actualizar el producto {producto.nombre}.")
                    producto.stock -= stock_a_descontar
                
                producto.save()

            except ItemVenta.DoesNotExist:
                pass
                
    # Actualizamos el total de la venta
    actualizar_total_venta(instance.venta)


# ----------------------------------------------------------------------
# 2. GESTIÓN DE STOCK AL ELIMINAR ÍTEM (pre_delete)
# ----------------------------------------------------------------------

# **IMPORTANTE:** Usamos la referencia de string para evitar errores de AppRegistryNotReady
@receiver(pre_delete, sender='ventas.ItemVenta')
def devolver_stock_por_eliminacion(sender, instance, **kwargs):
    """Devuelve el stock al producto cuando un ItemVenta es eliminado. 
    Esto soluciona el problema de la restitución al eliminar una Venta completa."""
    
    # ESCENARIO 3: ELIMINACIÓN
    with transaction.atomic():
        producto = instance.producto
        
        # Devolver la cantidad completa del ítem al stock
        producto.stock += instance.cantidad
        producto.save()
        
    # Recálculo preventivo del total si es el último ítem
    try:
        if instance.venta and instance.venta.items.count() == 1:
            instance.venta.total = 0 
            instance.venta.save()
    except Venta.DoesNotExist:
        pass