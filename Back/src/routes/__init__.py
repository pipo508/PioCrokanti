from flask import Blueprint
from src.routes.user_routes import user_bp

def register_routes(app):
    """Register all blueprints/routes with the Flask application."""
    # Registrar el blueprint de usuarios
    app.register_blueprint(user_bp, url_prefix='/api/users')

    # Aquí puedes agregar más blueprints cuando los crees
    # Por ejemplo:
    # app.register_blueprint(order_bp, url_prefix='/api/orders')
    # app.register_blueprint(product_bp, url_prefix='/api/products')
