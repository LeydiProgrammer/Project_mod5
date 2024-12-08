from django.db import models
from django.core.exceptions import ValidationError

# Validación personalizada para precios
def validar_positivo(valor):
    if valor <= 0:
        raise ValidationError("El valor debe ser positivo.")

# Validación personalizada para teléfonos
def validate_celular(value):
    if not value.isdigit() or len(value) != 8:
        raise ValidationError("El numero de celuar debe contener exactamente 8 dígitos.")

# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_positivo])
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

# Modelo de Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    celular = models.CharField(max_length=8, validators=[validate_celular])

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

# Modelo de Pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(detalle.precio_subtotal for detalle in self.detalles.all())

    def __str__(self):
        return f"Pedido #{self.id} de {self.cliente.nombre}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

# Modelo de Detalle PedidoS

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[validar_positivo])

    @property
    def precio_subtotal(self):
        return self.cantidad * self.producto.precio

    def clean(self):
               # Validar que la cantidad no exceda el stock del producto
        if self.cantidad > self.producto.stock:
            raise ValidationError(f"Stock insuficiente para el producto '{self.producto.nombre}'. Disponible: {self.producto.stock} unidades.")


    def save(self, *args, **kwargs):
        # Llama al método clean antes de guardar
        self.clean()

        # Actualiza el stock al guardar
        if self.pk:  # Si ya existe el detalle (update)
            detalle_anterior = DetallePedido.objects.get(pk=self.pk)
            cantidad_diferencia = self.cantidad - detalle_anterior.cantidad
        else:  # Si es un nuevo detalle
            cantidad_diferencia = self.cantidad

        # Verificar y actualizar el stock del producto
        if self.producto.stock >= cantidad_diferencia:
            self.producto.stock -= cantidad_diferencia
            self.producto.save()
        else:
            raise ValidationError(f"Stock insuficiente para el producto '{self.producto.nombre}'.")

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Revertir el stock al eliminar un detalle
        self.producto.stock += self.cantidad
        self.producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Se quiere registrar {self.cantidad}  {self.producto.nombre} "

    class Meta:
        verbose_name = "Detalle de Pedido"
        verbose_name_plural = "Detalles de Pedido"

