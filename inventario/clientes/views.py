from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Cliente
from .forms import ClienteForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import ProtectedError

class ClienteList(ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'

class ClienteCreate(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:cliente_list')

class ClienteUpdate(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:cliente_list')


# --- VISTA DE BORRADO (AQUÍ ESTÁ LA CORRECCIÓN) ---
class ClienteDelete(DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    
    # URL a la que redirigir si el borrado es exitoso
    # (También la usamos si falla, para mostrar el mensaje de error)
    success_url = reverse_lazy('clientes:cliente_list') 

    def post(self, request, *args, **kwargs):
        """
        Sobrescribimos el método post para capturar el ProtectedError.
        """
        self.object = self.get_object()
        
        try:
            # Intenta borrar el objeto
            response = super().delete(request, *args, **kwargs)
            
            # Si tiene éxito, muestra un mensaje de éxito
            messages.success(request, f"Cliente '{self.object}' eliminado con éxito.")
            return response

        except ProtectedError:
            # Si falla por ProtectedError, muestra un mensaje de error
            messages.error(
                request, 
                f"No se puede borrar el cliente '{self.object}' porque tiene "
                f"una o más ventas asociadas."
            )
            # Redirige de vuelta a la lista (donde se mostrará el mensaje)
            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'eliminar'
        return context

class ClienteDetail(DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
