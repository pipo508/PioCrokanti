# src/modules/product/product_repository.py

from src.config.database import db
from src.models import Product

class ProductRepository:
    def get_all(self):
        """Devuelve todos los productos que están activos."""
        return Product.query.filter_by(activo=True).all()
    
    def get_by_id(self, product_id):
        """Busca un producto por su ID, sin importar si está activo o no."""
        return Product.query.get(product_id)
    
    def create(self, product_data):
        """Crea un nuevo producto en la base de datos."""
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()
        return product
    
    def update(self, product_id, product_data):
        """Actualiza los datos de un producto existente."""
        product = self.get_by_id(product_id)
        if product:
            for key, value in product_data.items():
                setattr(product, key, value)
            db.session.commit()
        return product

    def delete(self, product_id):
        """Realiza un borrado lógico del producto (soft delete)."""
        product = self.get_by_id(product_id)
        if product:
            product.activo = False
            db.session.commit()
        return product