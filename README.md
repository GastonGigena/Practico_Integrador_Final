# Simulador Ventas Docker (v2)

## Levantar
1. Descargar y descomprimir.
2. Desde la carpeta del proyecto:
   docker-compose up --build
3. Abrir: http://localhost:8000

Superusuario por defecto:
  user: admin
  pass: admin123

## Notas
- Entrada automática crea superuser y grupos al arrancar (entrypoint.sh).
- Para crear superuser con otros datos, exportar variables DJANGO_SUPERUSER_* en environment.
