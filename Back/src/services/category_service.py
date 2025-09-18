from src.repositories.category_repository import CategoryRepository
from src.utils.exceptions import ValidationError, NotFoundError

class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()
    
    def get_all_categories(self):
        """Obtiene todas las categorías"""
        return self.category_repository.get_all()
    
    def get_active_categories(self):
        """Obtiene solo las categorías activas"""
        return self.category_repository.get_all_active()
    
    def get_category_by_id(self, category_id):
        """Obtiene una categoría por ID con validación"""
        if not category_id or not str(category_id).isdigit():
            raise ValidationError("ID de categoría inválido")
        
        return self.category_repository.get_by_id(int(category_id))
    
    def create_category(self, category_data):
        """Crea una nueva categoría con validaciones"""
        self._validate_category_data(category_data)
        
        # Verificar que no exista una categoría con el mismo nombre
        existing_category = self.category_repository.get_by_name(category_data['nombre'])
        if existing_category:
            raise ValidationError(f"Ya existe una categoría con el nombre '{category_data['nombre']}'")
        
        return self.category_repository.create(category_data)
    
    def update_category(self, category_id, category_data):
        """Actualiza una categoría existente"""
        category = self.get_category_by_id(category_id)
        
        # Validar solo los campos que se están actualizando
        if 'nombre' in category_data:
            self._validate_category_name(category_data['nombre'])
            # Verificar que no exista otra categoría con el mismo nombre
            existing_category = self.category_repository.get_by_name(category_data['nombre'])
            if existing_category and existing_category.id != category.id:
                raise ValidationError(f"Ya existe otra categoría con el nombre '{category_data['nombre']}'")
        
        return self.category_repository.update(category, category_data)
    
    def delete_category(self, category_id):
        """Desactiva una categoría (soft delete)"""
        category = self.get_category_by_id(category_id)
        return self.category_repository.delete(category)
    
    def permanently_delete_category(self, category_id):
        """Elimina permanentemente una categoría"""
        category = self.get_category_by_id(category_id)
        # TODO: Verificar que no tenga productos asociados antes de eliminar
        return self.category_repository.hard_delete(category)
    
    def _validate_category_data(self, category_data):
        """Valida los datos completos de una categoría"""
        if not category_data:
            raise ValidationError("No se proporcionaron datos de la categoría")
        
        self._validate_category_name(category_data.get('nombre'))
    
    def _validate_category_name(self, nombre):
        """Valida el nombre de la categoría"""
        if not nombre:
            raise ValidationError("El nombre de la categoría es obligatorio")
        
        if not isinstance(nombre, str):
            raise ValidationError("El nombre debe ser un texto")
        
        if len(nombre.strip()) == 0:
            raise ValidationError("El nombre de la categoría no puede estar vacío")
        
        if len(nombre) > 100:
            raise ValidationError("El nombre de la categoría no puede exceder 100 caracteres")