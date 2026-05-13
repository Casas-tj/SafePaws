from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .services.inventario_services import ProductService, MovementService


# =========================
# SUMINISTROS (menú)
# =========================
@login_required
def suministros(request):

    summary = MovementService.get_stock_summary()

    return render(request, 'inventario/suministros.html', {
        'headertitle': 'Gestión de Suministros',
        'headersubtitle': 'Control de Inventario',
        'btn_back': 'Volver',
        'back_url': 'home',
        'summary': summary,
    })


# =========================
# PRODUCTOS
# =========================
@login_required
def inventario(request):

    products = ProductService.list_products()

    return render(request, 'inventario/inventario.html', {
        'products': products,
        'headertitle': 'Gestión de Inventario',
        'headersubtitle': 'Listado de Productos',
        'btn_nuevo': 'Nuevo Producto',
        'form_url': 'inventario_form',
        'btn_back': 'Volver',
        'back_url': 'suministros',
    })


@login_required
def inventario_delete(request, product_id):
    if request.method == "POST":
        ProductService.delete_product(product_id)
    return redirect('inventario')


@login_required
def inventario_form(request, product_id=None):

    if request.method == "GET":

        product = None

        if product_id:
            product = ProductService.get_product_by_id(product_id)

        return render(request, 'inventario/inventario_form.html', {
            'product': product,
            'headertitle': 'Gestión de Inventario',
            'headersubtitle': 'Editar Producto' if product else 'Registrar Producto',
            'btn_back': 'Cancelar',
            'back_url': 'inventario',
        })

    if request.method == "POST":
        data = {
            'name':        request.POST.get('name', ''),
            'description': request.POST.get('description', ''),
            'unit':        request.POST.get('unit', ''),
        }

        if product_id:
            ProductService.update_product(product_id, **data)
        else:
            ProductService.create_product(**data)

        return redirect('inventario')


# =========================
# MOVIMIENTOS (stock)
# =========================
@login_required
def stock(request):

    movements = MovementService.list_movements()

    # Filtro por tipo si viene en GET
    tipo_filtro = request.GET.get('tipo', '')
    if tipo_filtro in ('Entrada', 'Salida'):
        movements = [m for m in movements if m.type == tipo_filtro]

    return render(request, 'inventario/stock.html', {
        'movements': movements,
        'tipo_filtro': tipo_filtro,
        'headertitle': 'Gestión de Stock',
        'headersubtitle': 'Historial de Movimientos',
        'btn_nuevo': 'Registrar Movimiento',
        'form_url': 'stock_form',
        'btn_back': 'Volver',
        'back_url': 'suministros',
    })


@login_required
def stock_delete(request, movement_id):
    if request.method == "POST":
        MovementService.delete_movement(movement_id)
    return redirect('stock')


@login_required
def stock_form(request, movement_id=None):

    if request.method == "GET":

        movement = None
        if movement_id:
            movement = MovementService.get_movement_by_id(movement_id)

        products = ProductService.list_products()

        return render(request, 'inventario/stock_form.html', {
            'movement': movement,
            'products': products,
            'headertitle': 'Gestión de Stock',
            'headersubtitle': 'Editar Movimiento' if movement else 'Registrar Movimiento',
            'btn_back': 'Cancelar',
            'back_url': 'stock',
        })

    if request.method == "POST":
        data = {
            'product_id':    request.POST.get('product_id'),
            'movement_date': request.POST.get('movement_date'),
            'quantity':      request.POST.get('quantity', 1),
            'type':          request.POST.get('type', 'Entrada'),
            'reason':        request.POST.get('reason', ''),
        }

        if movement_id:
            MovementService.update_movement(movement_id, **data)
        else:
            MovementService.create_movement(**data)

        return redirect('stock')


@login_required
def inventario_details(request, product_id):
    product = ProductService.get_product_by_id(product_id)
    product.movements_list = product.movements.filter(is_active=True).order_by('-movement_date')[:10]
    return render(request, 'inventario/inventario_details.html', {
        'product': product,
        'headertitle': 'Producto',
        'headersubtitle': 'Detalles del producto',
        'btn_back': 'Volver',
        'back_url': 'inventario',
    })


@login_required
def stock_details(request, movement_id):
    movement = MovementService.get_movement_by_id(movement_id)
    return render(request, 'inventario/stock_details.html', {
        'movement': movement,
        'headertitle': 'Movimiento',
        'headersubtitle': 'Detalles del movimiento',
        'btn_back': 'Volver',
        'back_url': 'stock',
    })
