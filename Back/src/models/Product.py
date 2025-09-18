# /models/product.py

from src.config.database import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    precio = db.Column(db.Float, nullable=False)
    
    # Este campo es clave para tu lógica de negocio.
    cantidad_personas = db.Column(db.Integer, nullable=False, default=1)
    
    imagen_url = db.Column(db.String(255), nullable=True)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- El Conector ---
    # Esta línea crea la columna que guardará el ID de la categoría.
    # Es el enlace físico entre un producto y su categoría.
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __init__(self, nombre, precio, category_id, cantidad_personas, descripcion=None, imagen_url=None):
        self.nombre = nombre
        self.precio = precio
        self.category_id = category_id
        self.cantidad_personas = cantidad_personas
        self.descripcion = descripcion
        self.imagen_url = imagen_url
        self.activo = True

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'cantidad_personas': self.cantidad_personas,
            'activo': self.activo,
            'imagen_url': self.imagen_url,
            'category_id': self.category_id
        }