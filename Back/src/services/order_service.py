# src/modules/order/order_service.py

from ..repositories.order_repository import OrderRepository
from ..repositories.user_repository import UserRepository
from ..repositories.product_repository import ProductRepository
from src.utils.exceptions import ValidationError, NotFoundError

class OrderService:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.user_repository = UserRepository()
        self.product_repository = ProductRepository()
    
    def get_all_orders(self):
        return self.order_repository.get_all()
    
    def get_order_by_id(self, order_id):
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundError(f'Pedido con ID {order_id} no encontrado')
        return order
    
    def create_order(self, data):
        # 1. Validar datos de entrada
        user_data = data.get('user')
        items_data = data.get('items')
        if not user_data or not items_data:
            raise ValidationError("Los campos 'user' e 'items' son requeridos.")
        
        # 2. Buscar o crear el usuario
        user = self.user_repository.get_by_telefono(user_data['telefono'])
        if not user:
            user = self.user_repository.create(user_data)
            
        # 3. Validar productos y calcular el total
        total = 0
        details_to_create = []
        for item in items_data:
            product = self.product_repository.get_by_id(item['product_id'])
            if not product or not product.activo:
                raise ValidationError(f"Producto con ID {item['product_id']} no es válido o está inactivo.")
            
            cantidad = item['cantidad']
            total += product.precio * cantidad
            details_to_create.append({
                'product_id': product.id,
                'cantidad': cantidad,
                'precio_unitario': product.precio
            })

        # 4. Preparar datos y llamar al repositorio para crear la orden
        order_data = {
            'user_id': user.id,
            'total': total,
            'direccion_entrega': user.direccion # Usamos la dirección del usuario
        }
        
        return self.order_repository.create(order_data, details_to_create)