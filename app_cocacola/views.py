from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *

def seleccionar_rol(request):
    """Vista para seleccionar entre modo Administrador y Cliente"""
    return render(request, 'seleccion_rol.html')

def inicio(request):
    """Página principal con selección de rol"""
    if request.user.is_authenticated:
        # Si ya está autenticado, redirigir según su rol
        if request.user.is_staff:
            return redirect('dashboard')
        else:
            return redirect('cliente_inicio')  # Esta vista la crearás después
    return render(request, 'inicio.html')

# ==============================
# VISTAS DE AUTENTICACIÓN
# ==============================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            
            # Redirigir según el tipo de usuario
            if user.is_staff:
                return redirect('dashboard')  # Administrador
            else:
                return redirect('cliente_inicio')  # Cliente normal
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'autenticacion/login.html')

def registro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
        else:
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # Crear cliente
            Cliente.objects.create(
                usuario=user,
                telefono=telefono,
                direccion=direccion
            )
            messages.success(request, 'Cuenta creada exitosamente. Puede iniciar sesión.')
            return redirect('login')
    
    return render(request, 'autenticacion/registro.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')

# ==============================
# DASHBOARD
# ==============================
@login_required
def dashboard(request):
    # Estadísticas para el dashboard
    total_clientes = Cliente.objects.count()
    total_pedidos = Pedido.objects.count()
    total_refrescos = Refresco.objects.count()
    total_aguas = Agua.objects.count()
    total_jugos = Jugo.objects.count()
    total_energizantes = Energizante.objects.count()
    
    context = {
        'total_clientes': total_clientes,
        'total_pedidos': total_pedidos,
        'total_refrescos': total_refrescos,
        'total_aguas': total_aguas,
        'total_jugos': total_jugos,
        'total_energizantes': total_energizantes,
    }
    return render(request, 'administrador/dashboard.html', context)

# ==============================
# CRUD CLIENTES
# ==============================
@login_required
def clientes_list(request):
    clientes = Cliente.objects.all().order_by('-fecha_registro')
    return render(request, 'administrador/clientes/list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            Cliente.objects.create(
                usuario=user,
                telefono=telefono,
                direccion=direccion
            )
            messages.success(request, 'Cliente creado exitosamente')
            return redirect('clientes_list')
    
    return render(request, 'administrador/clientes/create.html')

@login_required
def cliente_update(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        cliente.usuario.first_name = request.POST.get('first_name', cliente.usuario.first_name)
        cliente.usuario.last_name = request.POST.get('last_name', cliente.usuario.last_name)
        cliente.usuario.email = request.POST.get('email', cliente.usuario.email)
        cliente.telefono = request.POST.get('telefono', cliente.telefono)
        cliente.direccion = request.POST.get('direccion', cliente.direccion)
        
        cliente.usuario.save()
        cliente.save()
        
        messages.success(request, 'Cliente actualizado exitosamente')
        return redirect('clientes_list')
    
    return render(request, 'administrador/clientes/update.html', {'cliente': cliente})

@login_required
def cliente_delete(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        usuario = cliente.usuario
        cliente.delete()
        usuario.delete()
        
        messages.success(request, 'Cliente eliminado exitosamente')
        return redirect('clientes_list')
    
    return render(request, 'administrador/clientes/delete.html', {'cliente': cliente})

# ==============================
# CRUD REFRESCOS
# ==============================
@login_required
def refrescos_list(request):
    refrescos = Refresco.objects.all().order_by('-fecha_creacion')
    return render(request, 'administrador/bebidas/refrescos/list.html', {'refrescos': refrescos})
@login_required
def refresco_create(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        sabor = request.POST.get('sabor')
        tamaño = request.POST.get('tamaño')
        
        # Manejar la imagen - NUEVO CÓDIGO
        imagen = request.FILES.get('imagen')  # ← request.FILES en lugar de request.POST
        
        # Crear el objeto
        refresco = Refresco(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            sabor=sabor,
            tamaño=tamaño
        )
        
        # Asignar imagen si se subió - NUEVO CÓDIGO
        if imagen:
            refresco.imagen = imagen
            
        refresco.save()  # ← Guardar después de asignar la imagen
        
        messages.success(request, 'Refresco creado exitosamente')
        return redirect('refrescos_list')
    
    return render(request, 'administrador/bebidas/refrescos/create.html')
@login_required
def refresco_update(request, id):
    refresco = get_object_or_404(Refresco, id=id)
    
    if request.method == 'POST':
        refresco.nombre = request.POST.get('nombre', refresco.nombre)
        refresco.descripcion = request.POST.get('descripcion', refresco.descripcion)
        refresco.precio = request.POST.get('precio', refresco.precio)
        refresco.stock = request.POST.get('stock', refresco.stock)
        refresco.sabor = request.POST.get('sabor', refresco.sabor)
        refresco.tamaño = request.POST.get('tamaño', refresco.tamaño)
        refresco.activo = request.POST.get('activo') == 'on'
        
        # Manejar nueva imagen - NUEVO CÓDIGO
        nueva_imagen = request.FILES.get('imagen')  # ← request.FILES en lugar de request.POST
        if nueva_imagen:
            refresco.imagen = nueva_imagen  # ← Solo actualizar si se subió nueva imagen
            
        refresco.save()
        
        messages.success(request, 'Refresco actualizado exitosamente')
        return redirect('refrescos_list')
    
    return render(request, 'administrador/bebidas/refrescos/update.html', {'refresco': refresco})


@login_required  # ← AGREGAR ESTA LÍNEA
def refresco_delete(request, id):
    refresco = get_object_or_404(Refresco, id=id)
    
    if request.method == 'POST':
        refresco.delete()
        messages.success(request, 'Refresco eliminado exitosamente')
        return redirect('refrescos_list')
    
    return render(request, 'administrador/bebidas/refrescos/delete.html', {'refresco': refresco})

# ==============================
# CRUD AGUAS
# ==============================
@login_required
def aguas_list(request):
    aguas = Agua.objects.all().order_by('-fecha_creacion')
    return render(request, 'administrador/bebidas/aguas/list.html', {'aguas': aguas})

@login_required
def agua_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        tipo = request.POST.get('tipo')
        tamaño = request.POST.get('tamaño')
        
        # Manejar la imagen
        imagen = request.FILES.get('imagen')
        
        agua = Agua(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            tipo=tipo,
            tamaño=tamaño
        )
        
        if imagen:
            agua.imagen = imagen
            
        agua.save()
        
        messages.success(request, 'Agua creada exitosamente')
        return redirect('aguas_list')
    
    return render(request, 'administrador/bebidas/aguas/create.html')


@login_required
def agua_update(request, id):
    agua = get_object_or_404(Agua, id=id)
    
    if request.method == 'POST':
        agua.nombre = request.POST.get('nombre', agua.nombre)
        agua.descripcion = request.POST.get('descripcion', agua.descripcion)
        agua.precio = request.POST.get('precio', agua.precio)
        agua.stock = request.POST.get('stock', agua.stock)
        agua.tipo = request.POST.get('tipo', agua.tipo)
        agua.tamaño = request.POST.get('tamaño', agua.tamaño)
        agua.activo = request.POST.get('activo') == 'on'
        
        # Manejar nueva imagen
        nueva_imagen = request.FILES.get('imagen')
        if nueva_imagen:
            agua.imagen = nueva_imagen
            
        agua.save()
        
        messages.success(request, 'Agua actualizada exitosamente')
        return redirect('aguas_list')
    
    return render(request, 'administrador/bebidas/aguas/update.html', {'agua': agua})

@login_required
def agua_delete(request, id):
    agua = get_object_or_404(Agua, id=id)
    
    if request.method == 'POST':
        agua.delete()
        messages.success(request, 'Agua eliminada exitosamente')
        return redirect('aguas_list')
    
    return render(request, 'administrador/bebidas/aguas/delete.html', {'agua': agua})

# ==============================
# CRUD JUGOS
# ==============================
@login_required
def jugos_list(request):
    jugos = Jugo.objects.all().order_by('-fecha_creacion')
    return render(request, 'administrador/bebidas/jugos/list.html', {'jugos': jugos})

@login_required
def jugo_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        sabor = request.POST.get('sabor')
        natural = request.POST.get('natural') == 'on'
        tamaño = request.POST.get('tamaño')
        
        # Manejar la imagen
        imagen = request.FILES.get('imagen')
        
        jugo = Jugo(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            sabor=sabor,
            natural=natural,
            tamaño=tamaño
        )
        
        if imagen:
            jugo.imagen = imagen
            
        jugo.save()
        
        messages.success(request, 'Jugo creado exitosamente')
        return redirect('jugos_list')
    
    return render(request, 'administrador/bebidas/jugos/create.html')

@login_required
def jugo_update(request, id):
    jugo = get_object_or_404(Jugo, id=id)
    
    if request.method == 'POST':
        jugo.nombre = request.POST.get('nombre', jugo.nombre)
        jugo.descripcion = request.POST.get('descripcion', jugo.descripcion)
        jugo.precio = request.POST.get('precio', jugo.precio)
        jugo.stock = request.POST.get('stock', jugo.stock)
        jugo.sabor = request.POST.get('sabor', jugo.sabor)
        jugo.natural = request.POST.get('natural') == 'on'
        jugo.tamaño = request.POST.get('tamaño', jugo.tamaño)
        jugo.activo = request.POST.get('activo') == 'on'
        
        # Manejar nueva imagen
        nueva_imagen = request.FILES.get('imagen')
        if nueva_imagen:
            jugo.imagen = nueva_imagen
            
        jugo.save()
        
        messages.success(request, 'Jugo actualizado exitosamente')
        return redirect('jugos_list')
    
    return render(request, 'administrador/bebidas/jugos/update.html', {'jugo': jugo})

@login_required
def jugo_delete(request, id):
    jugo = get_object_or_404(Jugo, id=id)
    
    if request.method == 'POST':
        jugo.delete()
        messages.success(request, 'Jugo eliminado exitosamente')
        return redirect('jugos_list')
    
    return render(request, 'administrador/bebidas/jugos/delete.html', {'jugo': jugo})

# ==============================
# CRUD ENERGIZANTES
# ==============================
@login_required
def energizantes_list(request):
    energizantes = Energizante.objects.all().order_by('-fecha_creacion')
    return render(request, 'administrador/bebidas/energizantes/list.html', {'energizantes': energizantes})

@login_required
def energizante_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        sabor = request.POST.get('sabor')
        contenido_cafeina = request.POST.get('contenido_cafeina')
        tamaño = request.POST.get('tamaño')
        
        # Manejar la imagen
        imagen = request.FILES.get('imagen')
        
        energizante = Energizante(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            sabor=sabor,
            contenido_cafeina=contenido_cafeina,
            tamaño=tamaño
        )
        
        if imagen:
            energizante.imagen = imagen
            
        energizante.save()
        
        messages.success(request, 'Energizante creado exitosamente')
        return redirect('energizantes_list')
    
    return render(request, 'administrador/bebidas/energizantes/create.html')

@login_required
def energizante_update(request, id):
    energizante = get_object_or_404(Energizante, id=id)
    
    if request.method == 'POST':
        energizante.nombre = request.POST.get('nombre', energizante.nombre)
        energizante.descripcion = request.POST.get('descripcion', energizante.descripcion)
        energizante.precio = request.POST.get('precio', energizante.precio)
        energizante.stock = request.POST.get('stock', energizante.stock)
        energizante.sabor = request.POST.get('sabor', energizante.sabor)
        energizante.contenido_cafeina = request.POST.get('contenido_cafeina', energizante.contenido_cafeina)
        energizante.tamaño = request.POST.get('tamaño', energizante.tamaño)
        energizante.activo = request.POST.get('activo') == 'on'
        
        # Manejar nueva imagen
        nueva_imagen = request.FILES.get('imagen')
        if nueva_imagen:
            energizante.imagen = nueva_imagen
            
        energizante.save()
        
        messages.success(request, 'Energizante actualizado exitosamente')
        return redirect('energizantes_list')
    
    return render(request, 'administrador/bebidas/energizantes/update.html', {'energizante': energizante})

@login_required
def energizante_delete(request, id):
    energizante = get_object_or_404(Energizante, id=id)
    
    if request.method == 'POST':
        energizante.delete()
        messages.success(request, 'Energizante eliminado exitosamente')
        return redirect('energizantes_list')
    
    return render(request, 'administrador/bebidas/energizantes/delete.html', {'energizante': energizante})

# ==============================
# CRUD PEDIDOS COMPLETO
# ==============================
@login_required
def pedidos_list(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    return render(request, 'administrador/pedidos/list.html', {'pedidos': pedidos})

@login_required
def pedido_create(request):
    clientes = Cliente.objects.all()
    
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        direccion_envio = request.POST.get('direccion_envio')
        metodo_pago = request.POST.get('metodo_pago')
        total = request.POST.get('total', 0)
        estado = request.POST.get('estado', 'PENDIENTE')
        
        Pedido.objects.create(
            cliente_id=cliente_id,
            direccion_envio=direccion_envio,
            metodo_pago=metodo_pago,
            total=total,
            estado=estado
        )
        
        messages.success(request, 'Pedido creado exitosamente')
        return redirect('pedidos_list')
    
    return render(request, 'administrador/pedidos/create.html', {'clientes': clientes})

@login_required
def pedido_detail(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    return render(request, 'administrador/pedidos/detail.html', {'pedido': pedido})

@login_required
def pedido_update(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    
    if request.method == 'POST':
        pedido.estado = request.POST.get('estado', pedido.estado)
        pedido.direccion_envio = request.POST.get('direccion_envio', pedido.direccion_envio)
        pedido.metodo_pago = request.POST.get('metodo_pago', pedido.metodo_pago)
        pedido.save()
        
        messages.success(request, 'Pedido actualizado exitosamente')
        return redirect('pedidos_list')
    
    return render(request, 'administrador/pedidos/update.html', {'pedido': pedido})

@login_required
def pedido_delete(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido eliminado exitosamente')
        return redirect('pedidos_list')
    
    return render(request, 'administrador/pedidos/delete.html', {'pedido': pedido})

# ==============================
# CRUD OFERTAS
# ==============================
@login_required
def ofertas_list(request):
    ofertas = Oferta.objects.all().order_by('-fecha_inicio')
    return render(request, 'administrador/ofertas/list.html', {'ofertas': ofertas})

@login_required
def oferta_create(request):
    if request.method == 'POST':
        Oferta.objects.create(
            producto_tipo=request.POST.get('producto_tipo'),
            producto_id=request.POST.get('producto_id'),
            descuento=request.POST.get('descuento'),
            fecha_inicio=request.POST.get('fecha_inicio'),
            fecha_fin=request.POST.get('fecha_fin')
        )
        messages.success(request, 'Oferta creada exitosamente')
        return redirect('ofertas_list')
    
    return render(request, 'administrador/ofertas/create.html')

@login_required
def oferta_update(request, id):
    oferta = get_object_or_404(Oferta, id=id)
    
    if request.method == 'POST':
        oferta.producto_tipo = request.POST.get('producto_tipo', oferta.producto_tipo)
        oferta.producto_id = request.POST.get('producto_id', oferta.producto_id)
        oferta.descuento = request.POST.get('descuento', oferta.descuento)
        oferta.fecha_inicio = request.POST.get('fecha_inicio', oferta.fecha_inicio)
        oferta.fecha_fin = request.POST.get('fecha_fin', oferta.fecha_fin)
        oferta.activa = request.POST.get('activa') == 'on'
        oferta.save()
        
        messages.success(request, 'Oferta actualizada exitosamente')
        return redirect('ofertas_list')
    
    return render(request, 'administrador/ofertas/update.html', {'oferta': oferta})

@login_required
def oferta_delete(request, id):
    oferta = get_object_or_404(Oferta, id=id)
    
    if request.method == 'POST':
        oferta.delete()
        messages.success(request, 'Oferta eliminada exitosamente')
        return redirect('ofertas_list')
    
    return render(request, 'administrador/ofertas/delete.html', {'oferta': oferta})

# ==============================
# CRUD RESEÑAS COMPLETO
# ==============================
@login_required
def resenas_list(request):
    resenas = Resena.objects.all().order_by('-fecha_creacion')
    return render(request, 'administrador/resenas/list.html', {'resenas': resenas})

@login_required
def resena_create(request):
    clientes = Cliente.objects.all()
    
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        producto_tipo = request.POST.get('producto_tipo')
        producto_id = request.POST.get('producto_id')
        calificacion = request.POST.get('calificacion')
        comentario = request.POST.get('comentario')
        aprobada = request.POST.get('aprobada') == 'on'
        
        Resena.objects.create(
            cliente_id=cliente_id,
            producto_tipo=producto_tipo,
            producto_id=producto_id,
            calificacion=calificacion,
            comentario=comentario,
            aprobada=aprobada
        )
        
        messages.success(request, 'Reseña creada exitosamente')
        return redirect('resenas_list')
    
    return render(request, 'administrador/resenas/create.html', {'clientes': clientes})

@login_required
def resena_detail(request, id):
    resena = get_object_or_404(Resena, id=id)
    return render(request, 'administrador/resenas/detail.html', {'resena': resena})

@login_required
def resena_update(request, id):
    resena = get_object_or_404(Resena, id=id)
    
    if request.method == 'POST':
        resena.calificacion = request.POST.get('calificacion', resena.calificacion)
        resena.comentario = request.POST.get('comentario', resena.comentario)
        resena.aprobada = request.POST.get('aprobada') == 'on'
        resena.save()
        
        messages.success(request, 'Reseña actualizada exitosamente')
        return redirect('resenas_list')
    
    return render(request, 'administrador/resenas/update.html', {'resena': resena})

@login_required
def resena_delete(request, id):
    resena = get_object_or_404(Resena, id=id)
    
    if request.method == 'POST':
        resena.delete()
        messages.success(request, 'Reseña eliminada exitosamente')
        return redirect('resenas_list')
    
    return render(request, 'administrador/resenas/delete.html', {'resena': resena})




def cliente_inicio(request):
    """Vista temporal para la sección cliente"""
    return render(request, 'cliente/temporal.html')