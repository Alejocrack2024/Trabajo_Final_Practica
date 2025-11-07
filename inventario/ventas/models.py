from django.db import models
from django.urls import reverse
# Asumo que Cliente y Producto están en sus respectivas apps
from clientes.models import Cliente 
from productos.models import Producto
from decimal import Decimal

class Venta(models.Model):
    """Modelo para representar la cabecera de una venta o comprobante."""
    CODIGO_PREFIJO = 'VNT-'

    codigo_venta = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Código de Venta",
    ) 
    
    # ESTA LÍNEA ES LA QUE PROTEGE AL CLIENTE. ESTÁ BIEN.
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas', verbose_name="Cliente")
    
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Venta")
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        verbose_name="Total Comprobante"
    )
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.codigo_venta} - {self.cliente.nombre} {self.cliente.apellido}"

    def get_absolute_url(self):
        return reverse('ventas:venta_detail', args=[str(self.pk)])

class ItemVenta(models.Model):
    """Modelo para representar un ítem o línea dentro de una venta."""

    
    venta = models.ForeignKey(
        Venta, 
        on_delete=models.CASCADE, # Correcto: si se borra la Venta, se borran sus items
        related_name='items', 
        verbose_name="Venta Relacionada"
    )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.PROTECT, # Correcto: protege a los productos
        verbose_name="Producto"
    )
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Precio Unitario"
    )
    subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Subtotal de Línea"
    )

    class Meta:
        verbose_name = "Item de Venta"
        verbose_name_plural = "Items de Venta"
        unique_together = ('venta', 'producto') 

    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad} unidades)"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)