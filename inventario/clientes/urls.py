from django.urls import path
from .views import ClienteList, ClienteCreate, ClienteUpdate, ClienteDelete, ClienteDetail

app_name = 'clientes'

urlpatterns = [
    # URL para la lista de clientes
    path('', ClienteList.as_view(), name='cliente_list'),
    
    # URL para crear un nuevo cliente
    path('crear/', ClienteCreate.as_view(), name='cliente_create'),
    
    # URL para ver los detalles de un cliente
    path('<int:pk>/', ClienteDetail.as_view(), name='cliente_detail'),
    
    # URL para actualizar un cliente existente
    path('<int:pk>/editar/', ClienteUpdate.as_view(), name='cliente_update'),
    
    # URL para eliminar un cliente
    path('<int:pk>/eliminar/', ClienteDelete.as_view(), name='cliente_delete'),
]
