from flask import jsonify, request
from src.services.category_service import CategoryService
from src.utils.exceptions import ValidationError, NotFoundError

class CategoryController:
    def __init__(self):
        self.category_service = CategoryService()

    def get_all_categories(self):
        """Obtiene todas las categorías"""
        try:
            categories = self.category_service.get_all_categories()
            return jsonify([category.to_dict() for category in categories]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_active_categories(self):
        """Obtiene solo las categorías activas"""
        try:
            categories = self.category_service.get_active_categories()
            return jsonify([category.to_dict() for category in categories]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_category(self, category_id):
        """Obtiene una categoría por ID"""
        try:
            category = self.category_service.get_category_by_id(category_id)
            return jsonify(category.to_dict()), 200
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def create_category(self):
        """Crea una nueva categoría"""
        try:
            data = request.get_json()
            category = self.category_service.create_category(data)
            return jsonify(category.to_dict()), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            error_message = "Error interno del servidor"
            # TODO: Log the error message
            # current_app.logger.error(error_message, exc_info=True)
            return jsonify({'error': error_message}), 500

    def update_category(self, category_id):
        """Actualiza una categoría existente"""
        try:
            data = request.get_json()
            category = self.category_service.update_category(category_id, data)
            return jsonify(category.to_dict()), 200
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete_category(self, category_id):
        """Desactiva una categoría (soft delete)"""
        try:
            category = self.category_service.delete_category(category_id)
            return jsonify({'message': 'Categoría desactivada correctamente'}), 200
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def permanently_delete_category(self, category_id):
        """Elimina permanentemente una categoría"""
        try:
            category = self.category_service.permanently_delete_category(category_id)
            return jsonify({'message': 'Categoría eliminada permanentemente'}), 200
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500