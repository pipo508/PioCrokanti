from flask import jsonify, request
from src.services.user_service import UserService
from src.utils.exceptions import ValidationError, NotFoundError

class UserController:
    def __init__(self):
        self.user_service = UserService()
    
    def get_all_users(self):
        try:
            users = self.user_service.get_all_users()
            return jsonify([user.to_dict() for user in users]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_user(self, user_id):
        try:
            user = self.user_service.get_user_by_id(user_id)
            return jsonify(user.to_dict()), 200
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def create_user(self):
        try:
            data = request.get_json()
            user = self.user_service.create_user(data)
            return jsonify(user.to_dict()), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def update_user(self, user_id):
        try:
            data = request.get_json()
            user = self.user_service.update_user(user_id, data)
            return jsonify(user.to_dict()), 200
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def delete_user(self, user_id):
        try:
            user = self.user_service.delete_user(user_id)
            return jsonify({'message': 'Usuario eliminado correctamente'}), 200
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
