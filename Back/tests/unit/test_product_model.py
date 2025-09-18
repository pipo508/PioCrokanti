import pytest
from src.models.product import Product
from src.config.database import db

def test_create_product():
    """Test de creación de producto"""
    product = Product(
        nombre="Hamburguesa Clásica",
        descripcion="Hamburguesa con lechuga, tomate y queso",
        precio=1000,
        categoria="Hamburguesas",
        disponible=True
    )
    
    assert product.nombre == "Hamburguesa Clásica"
    assert product.precio == 1000
    assert product.disponible == True

def test_product_to_dict():
    """Test de serialización de producto a diccionario"""
    product = Product(
        nombre="Hamburguesa Clásica",
        descripcion="Hamburguesa con lechuga, tomate y queso",
        precio=1000,
        categoria="Hamburguesas",
        disponible=True
    )
    
    product_dict = product.to_dict()
    assert product_dict["nombre"] == "Hamburguesa Clásica"
    assert product_dict["precio"] == 1000
    assert product_dict["disponible"] == True

def test_product_price_validation():
    """Test para verificar que el precio no puede ser negativo"""
    with pytest.raises(ValueError):
        product = Product(
            nombre="Hamburguesa Clásica",
            descripcion="Hamburguesa con lechuga, tomate y queso",
            precio=-100,
            categoria="Hamburguesas",
            disponible=True
        )
