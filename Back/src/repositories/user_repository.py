from src.config.database import db
from src.models.User import User

class UserRepository:
    def get_all(self):
        return User.query.all()
    
    def get_by_id(self, user_id):
        return User.query.get(user_id)
    
    def get_by_telefono(self, telefono):
        return User.query.filter_by(telefono=telefono).first()
    
    def create(self, user_data):
        user = User(
            nombre=user_data['nombre'],
            apellido=user_data['apellido'],
            telefono=user_data['telefono'],
            direccion=user_data['direccion']
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    def update(self, user_id, user_data):
        user = self.get_by_id(user_id)
        if user:
            user.nombre = user_data.get('nombre', user.nombre)
            user.apellido = user_data.get('apellido', user.apellido)
            user.telefono = user_data.get('telefono', user.telefono)
            user.direccion = user_data.get('direccion', user.direccion)
            db.session.commit()
        return user
    
    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user
