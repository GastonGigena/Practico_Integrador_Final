from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from productos.models import Producto
from clientes.models import Cliente
from ventas.models import Venta

class Command(BaseCommand):
    help = "Crear grupos iniciales"

    def handle(self, *args, **options):
        admins, _ = Group.objects.get_or_create(name='administradores')
        stock_group, _ = Group.objects.get_or_create(name='stock')
        ventas_group, _ = Group.objects.get_or_create(name='ventas')

        prod_ct = ContentType.objects.get_for_model(Producto)
        cliente_ct = ContentType.objects.get_for_model(Cliente)
        venta_ct = ContentType.objects.get_for_model(Venta)

        perms_prod = Permission.objects.filter(content_type=prod_ct)
        perms_cli = Permission.objects.filter(content_type=cliente_ct)
        perms_venta = Permission.objects.filter(content_type=venta_ct)

        stock_group.permissions.set(perms_prod)
        ventas_group.permissions.set(list(perms_cli) + list(perms_venta))
        admins.permissions.set(list(perms_prod) + list(perms_cli) + list(perms_venta))

        self.stdout.write(self.style.SUCCESS('Grupos creados y permisos asignados'))
