import pytest
from src.services.seller_service import SellerService
from src.models.order import Order
from src.config.database import db

def test_pending_orders_list(app):
    """Test de listado de pedidos pendientes"""
    with app.app_context():
        service = SellerService()
        
        # Crear algunos pedidos de prueba
        orders = [
            Order(estado="pendiente", total=1000),
            Order(estado="pendiente", total=2000),
            Order(estado="confirmado", total=3000)
        ]
        
        for order in orders:
            db.session.add(order)
        db.session.commit()
        
        pending_orders = service.get_pending_orders()
        assert len(pending_orders) == 2
        assert all(order.estado == "pendiente" for order in pending_orders)

def test_order_confirmation(app):
    """Test de confirmación de pedido"""
    with app.app_context():
        service = SellerService()
        
        # Crear pedido de prueba
        order = Order(estado="pendiente", total=1000)
        db.session.add(order)
        db.session.commit()
        
        # Confirmar pedido
        result = service.confirm_order(order.id)
        assert result.estado == "confirmado"
        
        # Verificar que se actualizó en la base de datos
        updated_order = Order.query.get(order.id)
        assert updated_order.estado == "confirmado"

def test_order_statistics(app):
    """Test de estadísticas de pedidos"""
    with app.app_context():
        service = SellerService()
        
        # Crear pedidos de prueba con diferentes estados
        orders = [
            Order(estado="pendiente", total=1000),
            Order(estado="confirmado", total=2000),
            Order(estado="completado", total=3000),
            Order(estado="completado", total=4000)
        ]
        
        for order in orders:
            db.session.add(order)
        db.session.commit()
        
        stats = service.get_order_statistics()
        assert stats['total_pedidos'] == 4
        assert stats['pedidos_pendientes'] == 1
        assert stats['pedidos_confirmados'] == 1
        assert stats['pedidos_completados'] == 2
        assert stats['total_ventas'] == 10000
