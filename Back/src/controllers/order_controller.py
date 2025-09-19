# src/modules/order/order_controller.py

from flask import jsonify, request
from src.services.order_service import OrderService
from src.utils.exceptions import ValidationError, NotFoundError
import json

class OrderController:
    def __init__(self):
        self.order_service = OrderService()

    def get_all_orders(self):
        try:
            print("=== GET ALL ORDERS ===")
            orders = self.order_service.get_all_orders()
            print(f"Se encontraron {len(orders)} pedidos")
            
            orders_dict = []
            for order in orders:
                if hasattr(order, 'to_dict'):
                    orders_dict.append(order.to_dict())
                else:
                    orders_dict.append(self._order_to_dict(order))
            
            return jsonify(orders_dict), 200
        except Exception as e:
            print(f"Error en get_all_orders: {str(e)}")
            return jsonify({'error': str(e)}), 500

    def get_order(self, order_id):
        try:
            print(f"=== GET ORDER {order_id} ===")
            order = self.order_service.get_order_by_id(order_id)
            
            if hasattr(order, 'to_dict'):
                return jsonify(order.to_dict()), 200
            else:
                return jsonify(self._order_to_dict(order)), 200
                
        except NotFoundError as e:
            print(f"Pedido no encontrado: {str(e)}")
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            print(f"Error en get_order: {str(e)}")
            return jsonify({'error': str(e)}), 500

    def create_order(self):
        try:
            print("=== CREATE ORDER ===")
            
            # 1. Verificar Content-Type
            print(f"Content-Type: {request.content_type}")
            
            # 2. Obtener datos raw
            raw_data = request.get_data(as_text=True)
            print(f"Raw data: {raw_data}")
            
            # 3. Intentar obtener JSON
            data = request.get_json()
            print(f"Parsed JSON: {data}")
            print(f"Tipo de data: {type(data)}")
            
            # 4. Verificar si data es None o vacío
            if data is None:
                print("ERROR: data es None")
                return jsonify({
                    'error': 'No se recibieron datos JSON válidos',
                    'content_type': request.content_type,
                    'raw_data': raw_data[:200] if raw_data else None
                }), 400
            
            # 5. Verificar estructura del JSON
            if not isinstance(data, dict):
                print(f"ERROR: data no es dict, es {type(data)}")
                return jsonify({'error': 'Los datos deben ser un objeto JSON'}), 400
            
            # 6. Imprimir claves disponibles
            print(f"Claves en data: {list(data.keys())}")
            
            # 7. Manejar estructura anidada si es necesario
            if 'json' in data and 'user' not in data:
                print("Detectada estructura anidada, extrayendo datos...")
                data = data['json']
                print(f"Nuevas claves después de extraer: {list(data.keys())}")
            
            # 8. Verificar campo user específicamente
            user_data = data.get('user')
            items_data = data.get('items')
            
            print(f"Campo 'user': {user_data}")
            print(f"Campo 'items': {items_data}")
            
            # 9. Crear el pedido
            order = self.order_service.create_order(data)
            print(f"Pedido creado exitosamente: {order.id}")
            
            if hasattr(order, 'to_dict'):
                return jsonify(order.to_dict()), 201
            else:
                return jsonify(self._order_to_dict(order)), 201
                
        except ValidationError as e:
            print(f"Error de validación: {str(e)}")
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            print(f"Error interno en create_order: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': "Error interno del servidor"}), 500

    def _order_to_dict(self, order):
        """Método auxiliar para convertir Order a diccionario si no tiene to_dict()"""
        return {
            'id': order.id,
            'total': order.total,
            'estado': order.estado,
            'direccion_entrega': order.direccion_entrega,
            'metodo_pago': order.metodo_pago,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'updated_at': order.updated_at.isoformat() if order.updated_at else None,
            'user_id': order.user_id,
            'details': [self._detail_to_dict(detail) for detail in order.details] if hasattr(order, 'details') else []
        }

    def _detail_to_dict(self, detail):
        """Método auxiliar para convertir OrderDetail a diccionario"""
        return {
            'id': detail.id,
            'cantidad': detail.cantidad,
            'precio_unitario': detail.precio_unitario,
            'product_id': detail.product_id,
            'product_name': detail.product.nombre if hasattr(detail, 'product') and detail.product else None
        }