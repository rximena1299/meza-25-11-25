from django.urls import path
from . import views

urlpatterns = [
    # Páginas principales (DEBEN IR PRIMERO)
    path('', views.inicio, name='inicio'),
    path('seleccionar-rol/', views.seleccionar_rol, name='seleccionar_rol'),
    path('cliente/', views.cliente_inicio, name='cliente_inicio'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard Administrador
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # CRUD Clientes
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/agregar/', views.cliente_create, name='cliente_create'),
    path('clientes/editar/<int:id>/', views.cliente_update, name='cliente_update'),
    path('clientes/eliminar/<int:id>/', views.cliente_delete, name='cliente_delete'),
    
    # SECCIÓN BEBIDAS
    path('bebidas/refrescos/', views.refrescos_list, name='refrescos_list'),
    path('bebidas/refrescos/agregar/', views.refresco_create, name='refresco_create'),
    path('bebidas/refrescos/editar/<int:id>/', views.refresco_update, name='refresco_update'),
    path('bebidas/refrescos/eliminar/<int:id>/', views.refresco_delete, name='refresco_delete'),
    
    path('bebidas/aguas/', views.aguas_list, name='aguas_list'),
    path('bebidas/aguas/agregar/', views.agua_create, name='agua_create'),
    path('bebidas/aguas/editar/<int:id>/', views.agua_update, name='agua_update'),
    path('bebidas/aguas/eliminar/<int:id>/', views.agua_delete, name='agua_delete'),
    
    path('bebidas/jugos/', views.jugos_list, name='jugos_list'),
    path('bebidas/jugos/agregar/', views.jugo_create, name='jugo_create'),
    path('bebidas/jugos/editar/<int:id>/', views.jugo_update, name='jugo_update'),
    path('bebidas/jugos/eliminar/<int:id>/', views.jugo_delete, name='jugo_delete'),
    
    path('bebidas/energizantes/', views.energizantes_list, name='energizantes_list'),
    path('bebidas/energizantes/agregar/', views.energizante_create, name='energizante_create'),
    path('bebidas/energizantes/editar/<int:id>/', views.energizante_update, name='energizante_update'),
    path('bebidas/energizantes/eliminar/<int:id>/', views.energizante_delete, name='energizante_delete'),
    
    # CRUD Pedidos
    path('pedidos/', views.pedidos_list, name='pedidos_list'),
    path('pedidos/agregar/', views.pedido_create, name='pedido_create'),
    path('pedidos/detalle/<int:id>/', views.pedido_detail, name='pedido_detail'),
    path('pedidos/editar/<int:id>/', views.pedido_update, name='pedido_update'),
    path('pedidos/eliminar/<int:id>/', views.pedido_delete, name='pedido_delete'),
    
    # CRUD Ofertas
    path('ofertas/', views.ofertas_list, name='ofertas_list'),
    path('ofertas/agregar/', views.oferta_create, name='oferta_create'),
    path('ofertas/editar/<int:id>/', views.oferta_update, name='oferta_update'),
    path('ofertas/eliminar/<int:id>/', views.oferta_delete, name='oferta_delete'),
    
    # CRUD Reseñas
    path('resenas/', views.resenas_list, name='resenas_list'),
    path('resenas/agregar/', views.resena_create, name='resena_create'),
    path('resenas/detalle/<int:id>/', views.resena_detail, name='resena_detail'),
    path('resenas/editar/<int:id>/', views.resena_update, name='resena_update'),
    path('resenas/eliminar/<int:id>/', views.resena_delete, name='resena_delete'),
]