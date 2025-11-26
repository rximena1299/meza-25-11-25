from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"

# Tablas dentro de la sección Bebidas
class Refresco(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='bebidas/refrescos/', default='bebidas/default.jpg') # Para desarrollo
    sabor = models.CharField(max_length=100)
    tamaño = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class Agua(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='bebidas/aguas/', default='bebidas/default.jpg')
    tipo = models.CharField(max_length=100, choices=[
        ('NATURAL', 'Natural'),
        ('SABORIZADA', 'Saborizada'),
        ('MINERAL', 'Mineral')
    ])
    tamaño = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class Jugo(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='bebidas/jugos/', default='bebidas/default.jpg')
    sabor = models.CharField(max_length=100)
    natural = models.BooleanField(default=False)
    tamaño = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class Energizante(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='bebidas/energizantes/', default='bebidas/default.jpg')
    sabor = models.CharField(max_length=100)
    contenido_cafeina = models.CharField(max_length=50)
    tamaño = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class Oferta(models.Model):
    producto_tipo = models.CharField(max_length=20, choices=[
        ('REFRESCO', 'Refresco'),
        ('AGUA', 'Agua'),
        ('JUGO', 'Jugo'),
        ('ENERGIZANTE', 'Energizante'),
    ])
    producto_id = models.IntegerField()
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Oferta - {self.descuento}%"

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    direccion_envio = models.TextField()
    metodo_pago = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto_tipo = models.CharField(max_length=20)
    producto_id = models.IntegerField()
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def subtotal(self):
        return self.cantidad * self.precio_unitario

class Resena(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto_tipo = models.CharField(max_length=20)
    producto_id = models.IntegerField()
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobada = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reseña de {self.cliente}"