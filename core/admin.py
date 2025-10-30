from django.contrib import admin
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from allauth.account.models import EmailAddress  # <- Falta esta línea
from django.contrib.auth.models import Group

# Desregistrar los modelos que no queremos mostrar
admin.site.unregister(Site)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(EmailAddress)

# Registrar solo tus modelos
from productos.models import Producto
from clientes.models import Cliente
from ventas.models import Venta

admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Venta)
