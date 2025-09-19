# /models/order.py

from src.config.database import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default='Recibido', nullable=False)
    direccion_entrega = db.Column(db.String(255), nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    details = db.relationship('OrderDetail', backref='order', lazy=True, cascade="all, delete-orphan")

    def __init__(self, user_id, total, direccion_entrega, metodo_pago=None):
        self.user_id = user_id
        self.total = total
        self.direccion_entrega = direccion_entrega
        self.metodo_pago = metodo_pago

    def to_dict(self):
        """Convierte el objeto Order a diccionario para JSON"""
        return {
            'id': self.id,
            'total': self.total,
            'estado': self.estado,
            'direccion_entrega': self.direccion_entrega,
            'metodo_pago': self.metodo_pago,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id,
            # --- CORRECCIÓN 1: AÑADIR DATOS DEL USUARIO ---
            'user': self.user.to_dict() if self.user else None,
            'details': [detail.to_dict() for detail in self.details] if self.details else []
        }


class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False) 

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref='order_details', lazy=True)

    def to_dict(self):
        """Convierte el objeto OrderDetail a diccionario para JSON"""
        return {
            'id': self.id,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            # --- CORRECCIÓN 2: CALCULAR SUBTOTAL ---
            'subtotal': self.cantidad * self.precio_unitario,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product': {
                'id': self.product.id,
                'nombre': self.product.nombre,
                'precio': self.product.precio
            } if self.product else None
        }