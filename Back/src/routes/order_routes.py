# src/modules/order/order_routes.py

from flask import Blueprint
from src.controllers.order_controller import OrderController

order_bp = Blueprint('orders', __name__)
order_controller = OrderController()

# Obtener todos los pedidos
@order_bp.route('/orders', methods=['GET'])
def get_orders():
    return order_controller.get_all_orders()

# Crear un nuevo pedido
@order_bp.route('/orders', methods=['POST'])
def create_order():
    return order_controller.create_order()

# Obtener un pedido específico
@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    return order_controller.get_order(order_id)