from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=250, blank=True)

    # AÑADIR CLASE META PARA ORDENACIÓN
    class Meta:
        # Ordenar por el ID descendente (el último ID agregado es el más reciente)
        # Esto asegura que los clientes más nuevos aparezcan primero en las listas.
        ordering = ['-id']

    def __str__(self):
        return f"{self.apellido}, {self.nombre} - {self.dni}"