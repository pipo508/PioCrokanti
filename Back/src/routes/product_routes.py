# src/modules/product/product_routes.py

from flask import Blueprint, request # Importa request
from ..controllers.product_controller import ProductController

# El prefijo '/api/products' ya está definido en app.py
product_bp = Blueprint('products', __name__)
product_controller = ProductController()

# ANTES: @product_bp.route('/products', methods=['GET'])
# AHORA:
@product_bp.route('/', methods=['GET']) # <-- CAMBIO AQUÍ
def get_products():
    return product_controller.get_all_products()

# ANTES: @product_bp.route('/products', methods=['POST'])
# AHORA:
@product_bp.route('/', methods=['POST']) # <-- CAMBIO AQUÍ
def create_product():
    return product_controller.create_product()

# ANTES: @product_bp.route('/products/<int:product_id>', methods=['GET'])
# AHORA:
@product_bp.route('/<int:product_id>', methods=['GET']) # <-- CAMBIO AQUÍ
def get_product(product_id):
    return product_controller.get_product(product_id)

# ANTES: @product_bp.route('/products/<int:product_id>', methods=['PUT'])
# AHORA:
@product_bp.route('/<int:product_id>', methods=['PUT']) # <-- CAMBIO AQUÍ
def update_product(product_id):
    return product_controller.update_product(product_id)

# ANTES: @product_bp.route('/products/<int:product_id>', methods=['DELETE'])
# AHORA:
@product_bp.route('/<int:product_id>', methods=['DELETE']) # <-- CAMBIO AQUÍ
def delete_product(product_id):
    return product_controller.delete_product(product_id)