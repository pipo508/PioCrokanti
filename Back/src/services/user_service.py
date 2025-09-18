from src.repositories.user_repository import UserRepository
from src.utils.exceptions import ValidationError, NotFoundError

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
    
    def get_all_users(self):
        return self.user_repository.get_all()
    
    def get_user_by_id(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(f'Usuario con ID {user_id} no encontrado')
        return user
    
    def create_user(self, user_data):
        # Validar datos requeridos
        required_fields = ['nombre', 'apellido', 'telefono', 'direccion']
        for field in required_fields:
            if field not in user_data:
                raise ValidationError(f'El campo {field} es requerido')
        
        # Verificar si ya existe un usuario con ese teléfono
        existing_user = self.user_repository.get_by_telefono(user_data['telefono'])
        if existing_user:
            raise ValidationError('Ya existe un usuario con ese número de teléfono')
        
        return self.user_repository.create(user_data)
    
    def update_user(self, user_id, user_data):
        # Verificar si el usuario existe
        user = self.get_user_by_id(user_id)
        
        # Si se actualiza el teléfono, verificar que no exista
        if 'telefono' in user_data and user_data['telefono'] != user.telefono:
            existing_user = self.user_repository.get_by_telefono(user_data['telefono'])
            if existing_user:
                raise ValidationError('Ya existe un usuario con ese número de teléfono')
        
        return self.user_repository.update(user_id, user_data)
    
    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        return self.user_repository.delete(user_id)
