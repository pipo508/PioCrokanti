# src/services/mercadopago_service.py

import mercadopago
from flask import current_app

class MercadoPagoService:
    def __init__(self):
        self.sdk = None

    def _get_sdk(self):
        if self.sdk is None:
            access_token = current_app.config.get('MP_ACCESS_TOKEN')
            if not access_token:
                raise ValueError("MP_ACCESS_TOKEN no está configurado en la aplicación.")
            self.sdk = mercadopago.SDK(access_token)
        return self.sdk

    def create_preference(self, order):
        sdk = self._get_sdk()

        items_for_mp = []
        for detail in order.details:
            items_for_mp.append({
                "title": detail.product.nombre,
                "quantity": detail.cantidad,
                "unit_price": float(detail.precio_unitario),
                "currency_id": "ARS"
            })
            
        # --- URL DE NGROK INSERTADA AQUÍ ---
        public_base_url = "https://a6950b9a4104.ngrok-free.app"

        preference_data = {
            "items": items_for_mp,
            "back_urls": {
                "success": f"{public_base_url}/order/success",
                "failure": f"{public_base_url}/order/failure",
            },
            "auto_return": "approved",
            "notification_url": f"{public_base_url}/api/payments/webhook",
            "external_reference": str(order.id)
        }

        try:
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]
            return preference
        except Exception as e:
            print(f"Error al crear la preferencia de pago en Mercado Pago: {e}")
            raise