# /models/user.py (archivo modificado)

from src.config.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False, unique=True)
    direccion = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- RELACIÓN AÑADIDA ---
    # Un usuario (User) puede tener muchos pedidos (Order).
    # Con esto, podrás hacer `mi_usuario.orders` para obtener su historial.
    orders = db.relationship('Order', backref='user', lazy=True)

    def __init__(self, nombre, apellido, telefono, direccion):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.direccion = direccion

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'nombre_completo': self.nombre_completo,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
            # No incluimos los pedidos aquí para no sobrecargar la respuesta por defecto
        }