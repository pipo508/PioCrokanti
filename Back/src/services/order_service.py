# src/modules/order/order_service.py

from src.repositories.order_repository import OrderRepository
from src.repositories.user_repository import UserRepository
from src.repositories.product_repository import ProductRepository
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
        if not data:
            raise ValidationError("No se recibieron datos")
            
        user_data = data.get('user')
        items_data = data.get('items')
        
        if not user_data:
            raise ValidationError("El campo 'user' es requerido")
        if not items_data:
            raise ValidationError("El campo 'items' es requerido")
        if not isinstance(items_data, list) or len(items_data) == 0:
            raise ValidationError("El campo 'items' debe ser una lista no vacía")
        
        # 2. Buscar o crear el usuario
        try:
            user = self.user_repository.get_by_telefono(user_data['telefono'])
            if not user:
                user = self.user_repository.create(user_data)
        except KeyError as e:
            raise ValidationError(f"Campo requerido en user: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Error al procesar usuario: {str(e)}")
            
        # 3. Validar productos y calcular el total
        total = 0
        details_to_create = []
        
        for i, item in enumerate(items_data):
            try:
                product_id = item.get('product_id')
                cantidad = item.get('cantidad')
                
                if not product_id:
                    raise ValidationError(f"product_id requerido en item {i+1}")
                if not cantidad or cantidad <= 0:
                    raise ValidationError(f"cantidad debe ser mayor a 0 en item {i+1}")
                
                product = self.product_repository.get_by_id(product_id)
                if not product:
                    raise ValidationError(f"Producto con ID {product_id} no encontrado")
                if not product.activo:
                    raise ValidationError(f"Producto con ID {product_id} está inactivo")
                
                subtotal = product.precio * cantidad
                total += subtotal
                
                details_to_create.append({
                    'product_id': product.id,
                    'cantidad': cantidad,
                    'precio_unitario': product.precio
                })
                
            except ValidationError:
                raise
            except Exception as e:
                raise ValidationError(f"Error procesando item {i+1}: {str(e)}")

        # 4. Preparar datos y llamar al repositorio para crear la orden
        order_data = {
            'user_id': user.id,
            'total': total,
            'direccion_entrega': user.direccion,  # Usamos la dirección del usuario
            'metodo_pago': data.get('payment_method') # <-- AÑADIR MÉTODO DE PAGO
        }
        
        try:
            return self.order_repository.create(order_data, details_to_create)
        except Exception as e:
            raise ValidationError(f"Error al crear el pedido: {str(e)}")