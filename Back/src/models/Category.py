# /models/category.py (archivo modificado)

from src.config.database import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- RELACIÓN ACTIVADA ---
    # Al descomentar esta línea, ahora puedes hacer `mi_categoria.products`
    # y te devolverá una lista con todos los productos de esa categoría.
    products = db.relationship('Product', backref='category', lazy=True)

    def __init__(self, nombre, descripcion=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.activo = True

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }