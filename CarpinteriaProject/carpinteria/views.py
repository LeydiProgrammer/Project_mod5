

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Producto, Cliente, Pedido, DetallePedido
from .serializers import ProductoSerializer, ClienteSerializer, PedidoSerializer, DetallePedidoSerializer
from .serializers import ProductoSerializer
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

#Custom API 
class ProductosPrecioMayorView(APIView):
    def get(self, request, precio_minimo):
        # Filtra los productos cuyo precio sea mayor o igual al precio mínimo
        productos = Producto.objects.filter(precio__gte=precio_minimo)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)