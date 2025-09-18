import pytest
from src.models.user import User
from src.config.database import db

def test_create_user():
    """Test de creación de usuario"""
    user = User(
        nombre="Juan",
        apellido="Pérez",
        telefono="123456789",
        direccion="Calle 123"
    )
    
    assert user.nombre == "Juan"
    assert user.apellido == "Pérez"
    assert user.telefono == "123456789"
    assert user.direccion == "Calle 123"
    assert user.nombre_completo == "Juan Pérez"

def test_user_to_dict():
    """Test de serialización de usuario a diccionario"""
    user = User(
        nombre="Juan",
        apellido="Pérez",
        telefono="123456789",
        direccion="Calle 123"
    )
    
    user_dict = user.to_dict()
    assert user_dict["nombre"] == "Juan"
    assert user_dict["apellido"] == "Pérez"
    assert user_dict["telefono"] == "123456789"
    assert user_dict["direccion"] == "Calle 123"
    assert user_dict["nombre_completo"] == "Juan Pérez"

def test_unique_phone(app):
    """Test para verificar que no se pueden crear dos usuarios con el mismo teléfono"""
    user1 = User(
        nombre="Juan",
        apellido="Pérez",
        telefono="123456789",
        direccion="Calle 123"
    )
    db.session.add(user1)
    db.session.commit()

    user2 = User(
        nombre="Pedro",
        apellido="Gómez",
        telefono="123456789",
        direccion="Calle 456"
    )
    db.session.add(user2)
    
    with pytest.raises(Exception):
        db.session.commit()
