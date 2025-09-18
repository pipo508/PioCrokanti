from src.routes.order_routes import order_bp
from src.routes.product_routes import product_bp
from src.routes.user_routes import user_bp

def register_routes(app):
    """Register all blueprints/routes with the Flask application."""
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(user_bp, url_prefix='/api/users')
