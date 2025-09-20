# src/routes/payment_routes.py

from flask import Blueprint
from src.controllers.payment_controller import PaymentController

payment_bp = Blueprint('payments', __name__)
payment_controller = PaymentController()

@payment_bp.route('/webhook', methods=['POST'])
def receive_webhook():
    return payment_controller.receive_webhook()