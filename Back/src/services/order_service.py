# src/services/order_service.py

from src.repositories.order_repository import OrderRepository
from src.repositories.user_repository import UserRepository
from src.repositories.product_repository import ProductRepository
from src.utils.exceptions import ValidationError, NotFoundError
from src.services.mercadopago_service import MercadoPagoService # <-- Se importa el nuevo servicio

class OrderService:
    def __init__(self):
        self.order_repository = OrderRepository()
        self.user_repository = UserRepository()
        self.product_repository = ProductRepository()
        self.mp_service = MercadoPagoService() # <-- Se instancia el nuevo servicio

    def get_all_orders(self):
        return self.order_repository.get_all()
    
    def get_order_by_id(self, order_id):
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundError(f'Pedido con ID {order_id} no encontrado')
        return order
        
    def create_order_for_payment(self, data):
        """
        Orquesta la creación de una orden y su preferencia de pago.
        """
        # 1. Crea la orden internamente con la lógica de negocio
        order = self._create_order_logic(data)
        
        # 2. Actualiza el estado y método de pago
        order.estado = 'Pendiente de pago'
        order.metodo_pago = 'Mercado Pago'
        self.order_repository.update(order)

        # 3. Delega la creación de la preferencia de pago al servicio especializado
        return self.mp_service.create_preference(order)

    def _create_order_logic(self, data):
        """
        Lógica interna para crear un pedido, reutilizable.
        """
        if not data: raise ValidationError("No se recibieron datos")
        user_data = data.get('user')
        items_data = data.get('items')
        if not user_data: raise ValidationError("El campo 'user' es requerido")
        if not items_data: raise ValidationError("El campo 'items' es requerido")

        user = self.user_repository.get_by_telefono(user_data.get('telefono'))
        if not user:
            user = self.user_repository.create(user_data)
        
        total = 0
        details_to_create = []
        for item in items_data:
            product = self.product_repository.get_by_id(item.get('product_id'))
            if not product: raise ValidationError(f"Producto con ID {item.get('product_id')} no encontrado")
            total += product.precio * item.get('cantidad')
            details_to_create.append({
                'product_id': product.id,
                'cantidad': item.get('cantidad'),
                'precio_unitario': product.precio
            })
            
        order_data = {
            'user_id': user.id,
            'total': total,
            'direccion_entrega': user.direccion
        }
        
        return self.order_repository.create(order_data, details_to_create)

    def update_order_status(self, order_id, new_status):
        # Añadimos 'Pagado' a los estados permitidos
        allowed_statuses = ['Recibido', 'Pagado', 'Pendiente de pago', 'En preparación', 'Entregado', 'Cancelado']
        if new_status not in allowed_statuses:
            raise ValidationError(f"Estado '{new_status}' no es válido.")
        
        order = self.get_order_by_id(order_id)
        order.estado = new_status
        return self.order_repository.update(order)
    
    def create_cash_order(self, data):
        """
        Crea una orden simple para pago en efectivo.
        """
        order = self._create_order_logic(data)
        order.estado = 'Recibido'
        order.metodo_pago = 'Efectivo'
        return self.order_repository.update(order)