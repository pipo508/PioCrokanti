from flask import jsonify
from src.services.order_service import OrderService
from src.utils.exceptions import ValidationError

class OrderController:
    def __init__(self):
        self.order_service = OrderService()
    
    def get_all_orders(self):
        try:
            orders = self.order_service.get_all_orders()
            return jsonify([order.to_dict() for order in orders]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def create_order(self, data):
        try:
            order = self.order_service.create_order(data)
            return jsonify(order.to_dict()), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
