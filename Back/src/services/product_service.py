# src/modules/product/product_service.py

from src.repositories.product_repository import ProductRepository# Asumimos que tienes un repositorio de categorías para validación
from src.repositories.category_repository import CategoryRepository
from src.utils.exceptions import ValidationError, NotFoundError

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()
        self.category_repository = CategoryRepository() # Para validar categorías
    
    # ... el resto del archivo se mantiene igual ...
    def get_all_products(self):
        return self.product_repository.get_all()
    
    def get_product_by_id(self, product_id):
        product = self.product_repository.get_by_id(product_id)
        if not product or not product.activo:
            raise NotFoundError(f'Producto con ID {product_id} no encontrado')
        return product
    
    def create_product(self, product_data):
        # 1. Validar datos requeridos
        required_fields = ['nombre', 'precio', 'cantidad_personas', 'category_id']
        for field in required_fields:
            if field not in product_data:
                raise ValidationError(f'El campo {field} es requerido')
        
        # 2. Verificar si la categoría existe
        category = self.category_repository.get_by_id(product_data['category_id'])
        if not category or not category.activo:
             raise ValidationError(f"La categoría con ID {product_data['category_id']} no existe o está inactiva.")
        
        return self.product_repository.create(product_data)
    
    def update_product(self, product_id, product_data):
        # Verificar si el producto existe antes de actualizar
        product = self.get_product_by_id(product_id)
        
        # Si se está actualizando la categoría, verificar que la nueva exista
        if 'category_id' in product_data:
            category = self.category_repository.get_by_id(product_data['category_id'])
            if not category or not category.activo:
                raise ValidationError(f"La categoría con ID {product_data['category_id']} no existe o está inactiva.")

        return self.product_repository.update(product_id, product_data)
    
    def delete_product(self, product_id):
        # Verificar que el producto exista antes de eliminarlo
        self.get_product_by_id(product_id) 
        return self.product_repository.delete(product_id)