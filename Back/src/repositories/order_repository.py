from src.config.database import db
from src.models.order import Order

class OrderRepository:
    def get_all(self):
        return Order.query.all()
    
    def get_by_id(self, order_id):
        return Order.query.get(order_id)
    
    def create(self, order_data):
        order = Order(**order_data)
        db.session.add(order)
        db.session.commit()
        return order
    
    def update(self, order_id, order_data):
        order = self.get_by_id(order_id)
        if order:
            for key, value in order_data.items():
                setattr(order, key, value)
            db.session.commit()
        return order
    
    def delete(self, order_id):
        order = self.get_by_id(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
        return order
