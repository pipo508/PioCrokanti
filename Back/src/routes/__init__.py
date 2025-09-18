from flask import Blueprint, app
from src.routes.user_routes import user_bp
from src.controllers.health_check import health_bp
from src.routes.category_routes import category_bp
from src.routes.order_routes import order_bp
from src.routes.product_routes import product_bp


def register_routes(app):
    """Register all blueprints/routes with the Flask application."""
    # Registrar el blueprint de usuarios
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(health_bp, url_prefix='/api/health')

    # Aquí puedes agregar más blueprints cuando los crees
    # Por ejemplo:
    # app.register_blueprint(order_bp, url_prefix='/api/orders')
    # app.register_blueprint(product_bp, url_prefix='/api/products')
