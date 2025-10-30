PRACTICO INTEGRADOR FINAL - SISTEMA DE VENTAS “MR FRÍO”

---------------------------------------------------------
DESCRIPCIÓN GENERAL
---------------------------------------------------------
Este proyecto es un Sistema de Gestión de Ventas desarrollado en Django, 
contenedorizado con Docker. Permite administrar productos, clientes y ventas, 
controlando el stock de manera automática y generando comprobantes en PDF. 
Además, incluye un dashboard interactivo con estadísticas de ventas y productos.

---------------------------------------------------------
FUNCIONALIDADES PRINCIPALES
---------------------------------------------------------
- Gestión de Productos: alta, baja y modificación con control de stock.
- Gestión de Clientes: registro y consulta de clientes.
- Gestión de Ventas: creación de ventas con actualización automática de stock.
- Generación de comprobantes en formato PDF.
- Dashboard con gráficos de ventas diarias y productos más vendidos.
- Sistema de autenticación con distintos tipos de usuarios.

---------------------------------------------------------
ROLES DE USUARIO
---------------------------------------------------------
ADMINISTRADOR:
- Accede a todos los módulos (productos, clientes, ventas, dashboard y panel admin).

VENTAS:
- Puede registrar y consultar ventas, sin acceso al dashboard ni al stock.

STOCK:
- Gestiona el inventario de productos, sin acceso a ventas ni al dashboard.

---------------------------------------------------------
TECNOLOGÍAS UTILIZADAS
---------------------------------------------------------
- Python 3 / Django 5
- SQLite3
- Bootstrap 4.5
- Chart.js
- WeasyPrint (para PDFs)
- Docker / Docker Compose

---------------------------------------------------------
EJECUCIÓN DEL PROYECTO CON DOCKER
---------------------------------------------------------
1. Construir los contenedores:
   docker compose build

2. Aplicar migraciones:
   docker compose exec web python manage.py makemigrations
   docker compose exec web python manage.py migrate

3. Crear un superusuario:
   docker compose exec web python manage.py createsuperuser

4. Iniciar la aplicación:
   docker compose up

El sistema estará disponible en: http://localhost:8000

---------------------------------------------------------
INFORMACIÓN DEL DASHBOARD
---------------------------------------------------------
El dashboard muestra:
- Ventas diarias (gráfico de líneas)
- Totales por cliente
- Productos más vendidos (gráfico de barras)
Los gráficos son generados con Chart.js y los datos provienen directamente 
de la base de datos de Django.

---------------------------------------------------------
AUTOR
---------------------------------------------------------
Proyecto desarrollado por: Gastón Gigena  
Instituto Técnico Superior Córdoba  
Materia: Práctico Integrador Final  
Año: 2025
