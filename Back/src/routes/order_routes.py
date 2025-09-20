# src/routes/order_routes.py

from flask import Blueprint
from src.controllers.order_controller import OrderController

order_bp = Blueprint('orders', __name__)
order_controller = OrderController()

# Obtener todos los pedidos
@order_bp.route('/', methods=['GET'])
def get_orders():
    return order_controller.get_all_orders()

# Obtener un pedido específico
@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    return order_controller.get_order(order_id)

# Iniciar un pago y crear una preferencia de Mercado Pago
@order_bp.route('/initiate-payment', methods=['POST'])
def initiate_payment():
    return order_controller.initiate_payment()

# Actualizar el estado de un pedido
@order_bp.route('/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    return order_controller.update_order_status(order_id)

@order_bp.route('/cash-order', methods=['POST'])
def create_cash_order():
    return order_controller.create_cash_order()