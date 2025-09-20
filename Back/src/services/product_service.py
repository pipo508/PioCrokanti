# src/modules/product/product_service.py

from src.repositories.product_repository import ProductRepository
from src.repositories.category_repository import CategoryRepository
from src.utils.exceptions import ValidationError, NotFoundError

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()
        self.category_repository = CategoryRepository()
    
    def get_all_products(self):
        return self.product_repository.get_all()
    
    def get_product_by_id(self, product_id, check_active=False):
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundError(f'Producto con ID {product_id} no encontrado')
        if check_active and not product.activo:
            raise NotFoundError(f'Producto con ID {product_id} no está activo')
        return product
    
    def create_product(self, product_data):
        required_fields = ['nombre', 'precio', 'cantidad_personas', 'category_id']
        for field in required_fields:
            if field not in product_data:
                raise ValidationError(f'El campo {field} es requerido')
        
        category = self.category_repository.get_by_id(product_data['category_id'])
        if not category or not category.activo:
             raise ValidationError(f"La categoría con ID {product_data['category_id']} no existe o está inactiva.")
        
        return self.product_repository.create(product_data)
    
    def update_product(self, product_id, product_data):
        product = self.get_product_by_id(product_id)
        
        if 'category_id' in product_data:
            category = self.category_repository.get_by_id(product_data['category_id'])
            if not category or not category.activo:
                raise ValidationError(f"La categoría con ID {product_data['category_id']} no existe o está inactiva.")

        return self.product_repository.update(product_id, product_data)
    
    def deactivate_product(self, product_id):
        product = self.get_product_by_id(product_id)
        return self.product_repository.deactivate(product)

    def activate_product(self, product_id):
        product = self.get_product_by_id(product_id)
        return self.product_repository.activate(product)
