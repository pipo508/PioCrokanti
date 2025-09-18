from src.config.database import db
from src.models.Category import Category
from src.utils.exceptions import NotFoundError

class CategoryRepository:
    
    def get_all(self):
        """Obtiene todas las categorías"""
        return Category.query.all()
    
    def get_all_active(self):
        """Obtiene solo las categorías activas"""
        return Category.query.filter_by(activo=True).all()
    
    def get_by_id(self, category_id):
        """Obtiene una categoría por ID"""
        category = Category.query.get(category_id)
        if not category:
            raise NotFoundError(f"Categoría con ID {category_id} no encontrada")
        return category
    
    def get_by_name(self, nombre):
        """Obtiene una categoría por nombre"""
        return Category.query.filter_by(nombre=nombre).first()
    
    def create(self, category_data):
        """Crea una nueva categoría"""
        category = Category(
            nombre=category_data['nombre'],
            descripcion=category_data.get('descripcion')
        )
        db.session.add(category)
        db.session.commit()
        return category
    
    def update(self, category, category_data):
        """Actualiza una categoría existente"""
        if 'nombre' in category_data:
            category.nombre = category_data['nombre']
        if 'descripcion' in category_data:
            category.descripcion = category_data['descripcion']
        if 'activo' in category_data:
            category.activo = category_data['activo']
        
        db.session.commit()
        return category
    
    def delete(self, category):
        """Elimina una categoría (soft delete - marca como inactiva)"""
        category.activo = False
        db.session.commit()
        return category
    
    def hard_delete(self, category):
        """Elimina una categoría permanentemente"""
        db.session.delete(category)
        db.session.commit()
        return category