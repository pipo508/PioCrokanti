# src/controllers/order_controller.py

from flask import jsonify, request
from src.services.order_service import OrderService
from src.utils.exceptions import ValidationError, NotFoundError

class OrderController:
    def __init__(self):
        self.order_service = OrderService()

    def get_all_orders(self):
        try:
            orders = self.order_service.get_all_orders()
            return jsonify([order.to_dict() for order in orders]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_order(self, order_id):
        try:
            order = self.order_service.get_order_by_id(order_id)
            return jsonify(order.to_dict()), 200
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def initiate_payment(self):
        """
        Endpoint que inicia todo el flujo de pago con Mercado Pago.
        """
        try:
            raw_data = request.get_json()
            if not raw_data or 'json' not in raw_data:
                raise ValidationError("Payload inválido. Se esperaba una clave 'json'.")
            
            data_to_process = raw_data.get('json')
            
            # La variable 'base_url' se elimina, ya no es necesaria aquí.
            # La llamada al servicio ahora solo necesita los datos.
            preference = self.order_service.create_order_for_payment(data_to_process)
            
            return jsonify(preference), 200
            
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'error': "Error al crear la preferencia de pago"}), 500

    def update_order_status(self, order_id):
        try:
            data = request.get_json()
            new_status = data.get('estado')
            if not new_status:
                raise ValidationError("El campo 'estado' es requerido.")
            
            updated_order = self.order_service.update_order_status(order_id, new_status)
            return jsonify(updated_order.to_dict()), 200
        except (ValidationError, NotFoundError) as e:
            return jsonify({'error': str(e)}), 400 if isinstance(e, ValidationError) else 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

    def create_cash_order(self):
        try:
            raw_data = request.get_json()
            if not raw_data or 'json' not in raw_data:
                raise ValidationError("Payload inválido.")
            
            data_to_process = raw_data.get('json')
            order = self.order_service.create_cash_order(data_to_process)
            return jsonify(order.to_dict()), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500