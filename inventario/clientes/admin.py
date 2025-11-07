# clientes/admin.py
from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'numero_documento', 'e_mail', 'telefono', 'direccion']
    list_filter = ['nombre']
    search_fields = ['nombre', 'apellido', 'numero_documento', 'e_mail', 'telefono', 'direccion']
