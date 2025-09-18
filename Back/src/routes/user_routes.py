from flask import Blueprint
from src.controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)
user_controller = UserController()

# Obtener todos los usuarios
@user_bp.route('/', methods=['GET'])
def get_users():
    return user_controller.get_all_users()

# Obtener un usuario específico
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return user_controller.get_user(user_id)

# Crear un nuevo usuario
@user_bp.route('/', methods=['POST'])
def create_user():
    return user_controller.create_user()

# Actualizar un usuario
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return user_controller.update_user(user_id)

# Eliminar un usuario
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return user_controller.delete_user(user_id)
