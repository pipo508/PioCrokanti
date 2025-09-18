# src/modules/order/order_repository.py

from src.config.database import db
from src.models import Order, OrderDetail

class OrderRepository:
    def get_all(self):
        return Order.query.order_by(Order.created_at.desc()).all()
    
    def get_by_id(self, order_id):
        return Order.query.get(order_id)
    
    def create(self, order_data, details_data):
        """
        Crea un pedido y sus detalles en una sola transacción.
        """
        new_order = Order(**order_data)
        db.session.add(new_order)
        # Hacemos un 'flush' para obtener el ID del nuevo pedido antes del commit final
        db.session.flush()

        for detail_data in details_data:
            detail_data['order_id'] = new_order.id
            new_detail = OrderDetail(**detail_data)
            db.session.add(new_detail)
            
        db.session.commit()
        return new_order