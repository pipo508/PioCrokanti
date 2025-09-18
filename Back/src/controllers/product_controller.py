# src/modules/product/product_controller.py

from flask import jsonify, request
from src.services.product_service import ProductService
from src.utils.exceptions import ValidationError, NotFoundError

class ProductController:
    def __init__(self):
        self.product_service = ProductService()

    def get_all_products(self):
        try:
            products = self.product_service.get_all_products()
            return jsonify([product.to_dict() for product in products]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_product(self, product_id):
        try:
            product = self.product_service.get_product_by_id(product_id)
            return jsonify(product.to_dict()), 200
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def create_product(self):
        try:
            data = request.get_json()
            product = self.product_service.create_product(data)
            return jsonify(product.to_dict()), 201
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': "Error interno del servidor"}), 500

    def update_product(self, product_id):
        try:
            data = request.get_json()
            product = self.product_service.update_product(product_id, data)
            return jsonify(product.to_dict()), 200
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except ValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete_product(self, product_id):
        try:
            self.product_service.delete_product(product_id)
            return jsonify({'message': 'Producto desactivado correctamente'}), 200
        except NotFoundError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500