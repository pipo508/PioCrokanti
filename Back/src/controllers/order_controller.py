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
            print("=== CREATE ORDER (versión corregida) ===")
            
            # 1. Obtener el JSON que envía el frontend
            data = request.get_json()
            print(f"JSON recibido: {data}")

            # 2. Validar que no esté vacío
            if not data:
                return jsonify({'error': 'No se recibieron datos JSON válidos'}), 400

            # 3. Pasar los datos DIRECTAMENTE al servicio
            order = self.order_service.create_order(data)
            print(f"Pedido creado exitosamente: {order.id}")
            
            if hasattr(order, 'to_dict'):
                return jsonify(order.to_dict()), 201
            else:
                return jsonify(self._order_to_dict(order)), 201
                
        except ValidationError as e:
            print(f"Error de validación desde el servicio: {str(e)}")
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
    def update_order_status(self, order_id):
        try:
            data = request.get_json()
            new_status = data.get('estado')
            if not new_status:
                raise ValidationError("El campo 'estado' es requerido.")
            
            updated_order = self.order_service.update_order_status(order_id, new_status)
            return jsonify(updated_order.to_dict()), 200
            
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500