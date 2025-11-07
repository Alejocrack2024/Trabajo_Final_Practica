from django.urls import path
from .views import VentaCreateView, VentaListView, VentaDetailView, VentaDelete

app_name = 'ventas'

urlpatterns = [
    path('', VentaListView.as_view(), name='venta_list'),
    path('crear/', VentaCreateView.as_view(), name='venta_create'),  # Nombre correcto: venta_create
    path('<int:pk>/', VentaDetailView.as_view(), name='venta_detail'),
    path('<int:pk>/eliminar/', VentaDelete.as_view(), name='cliente_delete')

]
