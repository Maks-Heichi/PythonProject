import pytest

from src.shop import Category, Product


def test_product_initialization():
    product = Product(
        "iPhone 14 Pro Max", "6.7-дюймовый экран, 1TB памяти", 120000.0, 10
    )
    assert product.name == "iPhone 14 Pro Max"
    assert product.description == "6.7-дюймовый экран, 1TB памяти"
    assert product.price == 120000.0
    assert product.quantity == 10


def test_category_initialization():
    product1 = Product(
        "Galaxy Z Fold 4", "Развертываемый смартфон с гибким дисплеем", 150000.0, 7
    )
    product2 = Product(
        "Huawei Mate Xs 2", "Складной телефон премиум-класса", 130000.0, 5
    )
    category = Category("Смартфоны", "Лучшие смартфоны рынка", [product1, product2])
    assert category.name == "Смартфоны"
    assert len(category.products) == 2
    assert Category.category_count == 1
    assert Category.product_count == 12
