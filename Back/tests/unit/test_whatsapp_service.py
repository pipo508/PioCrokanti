import pytest
from src.services.whatsapp_service import WhatsAppService
from src.models.order import Order
from src.models.user import User

def test_generate_whatsapp_message():
    """Test de generación de mensaje de WhatsApp"""
    service = WhatsAppService()
    
    order_data = {
        "items": [
            {"nombre": "Hamburguesa Clásica", "cantidad": 2, "precio": 1000},
            {"nombre": "Papas Fritas", "cantidad": 1, "precio": 500}
        ],
        "total": 2500,
        "direccion": "Calle 123",
        "notas": "Sin cebolla"
    }
    
    message = service.generate_message(order_data)
    
    assert "Hamburguesa Clásica" in message
    assert "Papas Fritas" in message
    assert "2500" in message
    assert "Calle 123" in message
    assert "Sin cebolla" in message

def test_generate_whatsapp_link():
    """Test de generación de enlace de WhatsApp"""
    service = WhatsAppService()
    phone_number = "123456789"
    message = "Pedido de prueba"
    
    link = service.generate_link(phone_number, message)
    
    assert link.startswith("https://wa.me/")
    assert phone_number in link
    assert "Pedido" in link

def test_validate_phone_number():
    """Test de validación de número de teléfono"""
    service = WhatsAppService()
    
    assert service.validate_phone_number("123456789") == True
    assert service.validate_phone_number("12345") == False
    assert service.validate_phone_number("abcdefghi") == False
