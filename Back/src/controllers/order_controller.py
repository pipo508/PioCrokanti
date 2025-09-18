# src/modules/order/order_controller.py

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

    def create_order(self):
        try:
            data = request.get_json()
            order = self.order_service.create_order(data)
            return jsonify(order.to_dict()), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            # En un caso real, aquí deberías loggear el error.
            return jsonify({'error': "Error interno del servidor"}), 500