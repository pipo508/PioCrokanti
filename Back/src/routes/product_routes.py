# src/modules/product/product_routes.py

from flask import Blueprint, request
from src.controllers.product_controller import ProductController

product_bp = Blueprint('products', __name__)
product_controller = ProductController()

@product_bp.route('/', methods=['GET'])
def get_products():
    return product_controller.get_all_products()

@product_bp.route('/', methods=['POST'])
def create_product():
    return product_controller.create_product()

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return product_controller.get_product(product_id)

@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return product_controller.update_product(product_id)

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def deactivate_product(product_id):
    return product_controller.deactivate_product(product_id)

@product_bp.route('/<int:product_id>/activate', methods=['PUT'])
def activate_product(product_id):
    return product_controller.activate_product(product_id)
