# src/controllers/payment_controller.py

from flask import request, jsonify, current_app
import mercadopago
from src.services.order_service import OrderService

class PaymentController:
    def __init__(self):
        self.order_service = OrderService()

    def receive_webhook(self):
        # Recibimos la notificación de Mercado Pago
        query_params = request.args
        if query_params.get("topic") == "payment":
            payment_id = query_params.get("id") or query_params.get("data.id")
            
            try:
                # Obtenemos la información completa del pago desde Mercado Pago
                sdk = mercadopago.SDK(current_app.config['MP_ACCESS_TOKEN'])
                payment_info = sdk.payment().get(payment_id)
                
                if payment_info["status"] == 200:
                    payment = payment_info["response"]
                    order_id = payment.get("external_reference")
                    status = payment.get("status")
                    
                    if status == "approved":
                        # Si el pago está aprobado, actualizamos nuestra orden a "Pagado"
                        print(f"Webhook recibido: Pago aprobado para la orden {order_id}.")
                        self.order_service.update_order_status(int(order_id), "Pagado")
                    else:
                        print(f"Webhook recibido: Estado del pago '{status}' para la orden {order_id}.")
                else:
                    print(f"Error al obtener info del pago {payment_id} desde MP.")

            except Exception as e:
                print(f"Error al procesar webhook: {e}")
                return jsonify({'status': 'error'}), 500

        return jsonify({'status': 'received'}), 200