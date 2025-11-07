from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView , DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Venta, ItemVenta, Producto, Cliente
from .forms import VentaForm, ItemVentaFormSet

class VentaCreateView(View):
    def get(self, request, *args, **kwargs):
        """
        Maneja las solicitudes GET y muestra el formulario de venta.
        """
        form = VentaForm()
        formset = ItemVentaFormSet()
        
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, 'ventas/venta_form.html', context)


    def post(self, request, *args, **kwargs):
        """Procesa el formulario y el formset."""
        form = VentaForm(request.POST)
        formset = ItemVentaFormSet(request.POST, prefix='items')

        if form.is_valid() and formset.is_valid():
            try:
                # Usamos una transacción atómica para asegurar que si falla el stock, 
                # la venta completa se revierte.
                with transaction.atomic():
                    # 1. GUARDAR LA VENTA (Cabecera)
                    nueva_venta = form.save(commit=False)
                    
                    # Generar código de venta simple (ej. VNT-000001)
                    # Esto es un ejemplo, se puede mejorar usando secuencias de DB
                    last_id = Venta.objects.all().order_by('-pk').first().pk if Venta.objects.exists() else 0
                    nueva_venta.codigo_venta = f"{Venta.CODIGO_PREFIJO}{(last_id + 1):07d}"
                    
                    # Guarda el objeto Venta
                    nueva_venta.save()
                    
                    total_venta = 0
                    
                    # 2. PROCESAR LOS ÍTEMS DEL FORMSET
                    for item_form in formset:
                        if item_form.cleaned_data.get('DELETE'):
                            continue # Si la línea está marcada para borrar, la ignoramos

                        producto = item_form.cleaned_data.get('producto')
                        cantidad = item_form.cleaned_data.get('cantidad')
                        
                        if not producto or not cantidad:
                            continue

                        # 2.1. Validar Stock
                        if producto.stock < cantidad:
                            raise Exception(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}, Pedido: {cantidad}.")

                        # 2.2. Descontar Stock y Registrar Subtotal
                        
                        # Precio unitario actual del producto
                        precio_unitario = producto.precio_venta 
                        subtotal = precio_unitario * cantidad
                        
                        # Descontar stock (IMPORTANTE)
                        producto.stock -= cantidad
                        producto.save() # Guarda el producto con el stock actualizado
                        
                        # Guardar el ItemVenta (relacionado a la nueva_venta)
                        item_venta = item_form.save(commit=False)
                        item_venta.venta = nueva_venta
                        item_venta.precio_unitario = precio_unitario
                        item_venta.subtotal = subtotal
                        item_venta.save()
                        
                        total_venta += subtotal

                    # 3. REGISTRAR EL TOTAL DE LA VENTA
                    if total_venta == 0 and not formset.cleaned_data:
                        # Si no hay ítems, borramos la cabecera de la venta.
                        nueva_venta.delete()
                        messages.warning(request, "La venta no puede estar vacía.")
                        return render(request, self.template_name, {'form': form, 'formset': formset})
                    
                    nueva_venta.total = total_venta
                    nueva_venta.save()
                    
                    messages.success(request, f"Venta {nueva_venta.codigo_venta} creada con éxito y stock actualizado.")
                    return redirect('ventas:venta_list')

            except Exception as e:
                # Si algo falla (ej. stock insuficiente), se revierte la transacción
                messages.error(request, f"Error al procesar la venta: {e}")
                
        # Si la validación falla (del form o formset)
        return render(request, self.template_name, {'form': form, 'formset': formset})

# ==============================================================================
# Vistas de Listado y Detalle
# ==============================================================================

class VentaListView(ListView):
    """Muestra el listado de todas las ventas."""
    model = Venta
    template_name = 'ventas/venta_list.html'
    context_object_name = 'ventas'
    paginate_by = 10

class VentaDetailView(DetailView):
    """Muestra el detalle de una venta y sus ítems."""
    model = Venta
    template_name = 'ventas/venta_detail.html'
    context_object_name = 'venta'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Asegura que los ítems estén disponibles en el contexto
        context['items'] = self.object.items.all()
        return context
    

# --- AÑADE ESTA CLASE ---
class VentaDelete(DeleteView):
    model = Venta
    template_name = 'ventas/venta_confirm_delete.html'
    
    # URL a la que ir después de borrar (ej. la lista de ventas)
    success_url = reverse_lazy('ventas:venta_list') 

    def form_valid(self, form):
        # Opcional: Añadir un mensaje de éxito
        messages.success(self.request, f"Venta '{self.object.codigo_venta}' eliminada con éxito.")
        return super().form_valid(form)
