from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from carpinteria.views import ProductoViewSet, ClienteViewSet, PedidoViewSet, DetallePedidoViewSet, ProductosPrecioMayorView


router = DefaultRouter()
router.register('productos', ProductoViewSet)
router.register('clientes', ClienteViewSet)
router.register('pedidos', PedidoViewSet)
router.register('detalles-pedido', DetallePedidoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
     path('productos/precio_mayor/<str:precio_minimo>/', ProductosPrecioMayorView.as_view()),
]
