from rest_framework import serializers
from .models import Producto, Cliente, Pedido, DetallePedido

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    detalles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'

