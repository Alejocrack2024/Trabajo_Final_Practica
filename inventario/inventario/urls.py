"""
URL configuration for inventario project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. URL de la administración (SOLO UNA VEZ)
    path('admin/', admin.site.urls),
    
    # 2. URLs para el módulo de CLIENTES
    # Asignamos un prefijo claro: /clientes/
    path('clientes/', include("clientes.urls")),
    
    # 3. URLs para el módulo de PRODUCTOS
    # La dejamos en la raíz si es la aplicación principal.
    path("", include("productos.urls")),

    path('ventas/', include("ventas.urls")),
]

# Configuración de archivos media (imágenes, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)