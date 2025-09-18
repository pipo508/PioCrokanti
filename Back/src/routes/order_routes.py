from flask import Blueprint, jsonify, request
from src.controllers.order_controller import OrderController
from src.utils.auth import require_auth

order_bp = Blueprint('orders', __name__)
order_controller = OrderController()

@order_bp.route('/', methods=['GET'])
@require_auth
def get_orders():
    return order_controller.get_all_orders()

@order_bp.route('/', methods=['POST'])
@require_auth
def create_order():
    data = request.get_json()
    return order_controller.create_order(data)
