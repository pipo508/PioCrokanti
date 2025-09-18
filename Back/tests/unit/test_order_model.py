import pytest
from datetime import datetime
from src.models.order import Order
from src.models.user import User
from src.config.database import db

def test_create_order(app):
    """Test de creación de pedido"""
    with app.app_context():
        # Crear usuario de prueba
        user = User(
            nombre="Juan",
            apellido="Pérez",
            telefono="123456789",
            direccion="Calle 123"
        )
        db.session.add(user)
        db.session.commit()

        # Crear pedido
        order = Order(
            user_id=user.id,
            items=[
                {"producto_id": 1, "cantidad": 2, "precio": 1000},
                {"producto_id": 2, "cantidad": 1, "precio": 800}
            ],
            total=2800,
            estado="pendiente",
            notas="Sin cebolla"
        )
        
        assert order.user_id == user.id
        assert order.total == 2800
        assert order.estado == "pendiente"
        assert len(order.items) == 2

def test_order_status_transitions(app):
    """Test de transiciones de estado del pedido"""
    with app.app_context():
        # Crear usuario y pedido de prueba
        user = User(
            nombre="Juan",
            apellido="Pérez",
            telefono="123456789",
            direccion="Calle 123"
        )
        db.session.add(user)
        db.session.commit()

        order = Order(
            user_id=user.id,
            items=[{"producto_id": 1, "cantidad": 2, "precio": 1000}],
            total=2000,
            estado="pendiente"
        )

        # Probar transiciones de estado
        assert order.estado == "pendiente"
        
        order.confirmar_pedido()
        assert order.estado == "confirmado"
        
        order.iniciar_preparacion()
        assert order.estado == "en_preparacion"
        
        order.completar_pedido()
        assert order.estado == "completado"

def test_order_whatsapp_link(app):
    """Test de generación de enlace de WhatsApp"""
    with app.app_context():
        user = User(
            nombre="Juan",
            apellido="Pérez",
            telefono="123456789",
            direccion="Calle 123"
        )
        db.session.add(user)
        db.session.commit()

        order = Order(
            user_id=user.id,
            items=[
                {"producto_id": 1, "cantidad": 2, "precio": 1000, "nombre": "Hamburguesa"}
            ],
            total=2000,
            estado="pendiente"
        )

        whatsapp_link = order.generar_link_whatsapp()
        assert "wa.me" in whatsapp_link
        assert "Hamburguesa" in whatsapp_link
        assert "2000" in whatsapp_link
