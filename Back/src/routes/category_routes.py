from flask import Blueprint
from src.controllers.category_controller import CategoryController

category_bp = Blueprint('category', __name__)
category_controller = CategoryController()

# Obtener todas las categorías
@category_bp.route('/', methods=['GET'])
def get_categories():
    return category_controller.get_all_categories()

# Obtener solo categorías activas
@category_bp.route('/active', methods=['GET'])
def get_active_categories():
    return category_controller.get_active_categories()

# Obtener una categoría específica
@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    return category_controller.get_category(category_id)

# Crear una nueva categoría
@category_bp.route('/', methods=['POST'])
def create_category():
    return category_controller.create_category()

# Actualizar una categoría
@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    return category_controller.update_category(category_id)

# Desactivar (soft delete) una categoría
@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    return category_controller.delete_category(category_id)

# Eliminar permanentemente una categoría
@category_bp.route('/<int:category_id>/permanent', methods=['DELETE'])
def permanently_delete_category(category_id):
    return category_controller.permanently_delete_category(category_id)
