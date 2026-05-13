from apps.inventario.models import Product, Movement
from django.db.models import Sum
from django.db import transaction

STOCK_BAJO_UMBRAL = 5


class ProductService:

    # =========================
    # 🟢 CREATE
    # =========================
    @staticmethod
    @transaction.atomic
    def create_product(name, description='', unit=''):
        # El quantity empieza en 0 y solo se modifica via movimientos
        product = Product.objects.create(
            name=name,
            description=description,
            quantity=0,
            unit=unit,
        )
        return product

    # =========================
    # 🔵 READ (uno)
    # =========================
    @staticmethod
    def get_product_by_id(product_id):
        product = Product.objects.filter(id=product_id).first()
        if product:
            ProductService._add_labels(product)
        return product

    # =========================
    # 🔵 READ (lista)
    # =========================
    @staticmethod
    def list_products():
        products = Product.objects.filter(is_active=True).order_by('name')
        for p in products:
            ProductService._add_labels(p)
        return products

    # =========================
    # 🟡 UPDATE
    # =========================
    @staticmethod
    @transaction.atomic
    def update_product(product_id, **kwargs):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return None
        allowed = ['name', 'description', 'unit']
        for key, value in kwargs.items():
            if key in allowed:
                setattr(product, key, value)
        product.save()
        return product

    # =========================
    # 🔴 DELETE
    # =========================
    @staticmethod
    @transaction.atomic
    def delete_product(product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return False
        product.is_active = False
        product.save(update_fields=['is_active'])
        return True

    # =============================
    # 🏷️ LABELS — helper interno
    # =============================
    @staticmethod
    def _add_labels(product):
        """Añade atributos de presentación a un producto."""

        product.stock_bajo = product.quantity <= STOCK_BAJO_UMBRAL and product.quantity > 0

        product.sin_stock = product.quantity == 0

        if product.quantity == 0:
            product.stock_label = "Sin stock"
        elif product.quantity <= STOCK_BAJO_UMBRAL:
            product.stock_label = "Stock bajo"
        else:
            product.stock_label = "Stock OK"


class MovementService:

    @staticmethod
    def recalculate_stock(product_id):
        """
        Recalcula el stock sumando todas las entradas y restando
        todas las salidas. Siempre consistente, nunca negativo.
        """
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return

        entradas = Movement.objects.filter(
            product_id=product_id, type='Entrada'
        ).aggregate(total=Sum('quantity'))['total'] or 0

        salidas = Movement.objects.filter(
            product_id=product_id, type='Salida'
        ).aggregate(total=Sum('quantity'))['total'] or 0

        product.quantity = max(0, entradas - salidas)
        product.save(update_fields=['quantity'])

    # =========================
    # 🟢 CREATE
    # =========================
    @staticmethod
    @transaction.atomic
    def create_movement(product_id, movement_date, quantity, type, reason=''):
        movement = Movement.objects.create(
            product_id=product_id,
            movement_date=movement_date,
            quantity=int(quantity),
            type=type,
            reason=reason,
        )

        # ✅ Recalcular stock automáticamente tras crear
        MovementService.recalculate_stock(product_id)
        return movement

    # =========================
    # 🔵 READ (uno)
    # =========================
    @staticmethod
    def get_movement_by_id(movement_id):
        return Movement.objects.select_related('product').filter(id=movement_id).first()

    # =========================
    # 🔵 READ (lista)
    # =========================
    @staticmethod
    def list_movements():
        movements = list(
            Movement.objects.select_related('product').order_by(
                '-movement_date', '-created_at')
        )

        for m in movements:
            MovementService._add_labels(m)
        return movements

    # =========================
    # 🟡 UPDATE
    # =========================
    @staticmethod
    @transaction.atomic
    def update_movement(movement_id, **kwargs):
        movement = Movement.objects.filter(id=movement_id).first()
        if not movement:
            return None

        old_product_id = movement.product_id

        allowed = ['product_id', 'movement_date', 'quantity', 'type', 'reason']
        for key, value in kwargs.items():
            if key in allowed:
                if key == 'quantity':
                    value = int(value)
                setattr(movement, key, value)
        movement.save()

        # ✅ Recalcular stock del producto anterior y del nuevo (si cambió)
        MovementService.recalculate_stock(old_product_id)
        if str(movement.product_id) != str(old_product_id):
            MovementService.recalculate_stock(movement.product_id)

        return movement

    # =========================
    # 🔴 DELETE
    # =========================
    @staticmethod
    @transaction.atomic
    def delete_movement(movement_id):
        movement = Movement.objects.filter(id=movement_id).first()
        if not movement:
            return False
        product_id = movement.product_id
        movement.delete()

        # ✅ Recalcular stock tras eliminar
        MovementService.recalculate_stock(product_id)
        return True

    # =========================
    # 📊 RESUMEN de stock
    # =========================
    @staticmethod
    def get_stock_summary():
        """
        Devuelve un resumen del estado del inventario para el dashboard/suministros.
        """
        from django.db.models import Count, Q

        total = Product.objects.filter(is_active=True).count()
        stock_bajo = Product.objects.filter(
            is_active=True, quantity__lte=STOCK_BAJO_UMBRAL
        ).count()
        sin_stock = Product.objects.filter(
            is_active=True, quantity=0
        ).count()

        return {
            'total_productos': total,
            'stock_bajo': stock_bajo,
            'sin_stock': sin_stock,
            'ok': total - stock_bajo,
        }

    # =============================
    # 🏷️ LABELS — helper interno
    # =============================
    @staticmethod
    def _add_labels(movement):
        movement.type_label = '📥 Entrada' if movement.type == 'Entrada' else '📤 Salida'
        movement.type_class = 'badge-success' if movement.type == 'Entrada' else 'badge-danger'
