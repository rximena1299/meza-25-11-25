from django.contrib import admin
from .models import *

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'fecha_registro')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'telefono')

# Tablas de Bebidas
@admin.register(Refresco)
class RefrescoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sabor', 'precio', 'stock', 'activo')
    list_filter = ('sabor', 'activo')
    search_fields = ('nombre', 'descripcion')

@admin.register(Agua)
class AguaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'precio', 'stock', 'activo')
    list_filter = ('tipo', 'activo')
    search_fields = ('nombre', 'descripcion')

@admin.register(Jugo)
class JugoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sabor', 'natural', 'precio', 'stock', 'activo')
    list_filter = ('sabor', 'natural', 'activo')
    search_fields = ('nombre', 'descripcion')

@admin.register(Energizante)
class EnergizanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sabor', 'precio', 'stock', 'activo')
    list_filter = ('sabor', 'activo')
    search_fields = ('nombre', 'descripcion')

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ('producto_tipo', 'descuento', 'fecha_inicio', 'fecha_fin', 'activa')
    list_filter = ('activa', 'producto_tipo')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado', 'total')
    list_filter = ('estado', 'fecha_pedido')

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'producto_tipo', 'calificacion', 'fecha_creacion', 'aprobada')
    list_filter = ('calificacion', 'aprobada', 'producto_tipo')