# /models/order.py

from src.config.database import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default='Recibido', nullable=False) # Ej: Recibido, En preparación, Entregado, etc.
    direccion_entrega = db.Column(db.String(255), nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # --- Conectores ---
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # --- Relación ---
    # Un pedido (Order) tiene muchos detalles (OrderDetail)
    # cascade="all, delete-orphan" significa que si borras un pedido, se borran sus detalles automáticamente.
    details = db.relationship('OrderDetail', backref='order', lazy=True, cascade="all, delete-orphan")

    def __init__(self, user_id, total, direccion_entrega, metodo_pago=None):
        self.user_id = user_id
        self.total = total
        self.direccion_entrega = direccion_entrega
        self.metodo_pago = metodo_pago


class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    
    # Guardamos el precio del producto al momento de la compra.
    # Es importante por si en el futuro cambias los precios de los productos.
    precio_unitario = db.Column(db.Float, nullable=False) 

    # --- Conectores ---
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref='order_details', lazy=True)
