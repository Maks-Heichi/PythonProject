import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.shop import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counts():
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


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
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_category_add_product():
    product1 = Product("Товар 1", "Описание 1", 100.0, 10)
    category = Category("Категория", "Описание", [product1])
    assert Category.product_count == 1

    product2 = Product("Товар 2", "Описание 2", 200.0, 5)
    category.add_product(product2)
    assert Category.product_count == 2
    assert "Товар 2, 200.0 руб. Остаток: 5 шт." in category.products


def test_category_products_property():
    product1 = Product("Телефон", "Описание", 50000.0, 10)
    product2 = Product("Ноутбук", "Описание", 100000.0, 5)
    category = Category("Электроника", "Описание", [product1, product2])

    assert "Телефон, 50000.0 руб. Остаток: 10 шт.\n" in category.products
    assert "Ноутбук, 100000.0 руб. Остаток: 5 шт.\n" in category.products


def test_category_products_private():
    product = Product("Товар", "Описание", 100.0, 1)
    category = Category("Категория", "Описание", [product])
    with pytest.raises(AttributeError):
        _ = category.__products


def test_product_price_getter():
    product = Product("Товар", "Описание", 500.0, 1)
    assert product.price == 500.0


def test_product_price_setter_valid():
    product = Product("Товар", "Описание", 500.0, 1)
    product.price = 600.0
    assert product.price == 600.0


def test_product_price_setter_zero(capsys):
    product = Product("Товар", "Описание", 500.0, 1)
    product.price = 0
    assert product.price == 500.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_product_price_setter_negative(capsys):
    product = Product("Товар", "Описание", 500.0, 1)
    product.price = -100
    assert product.price == 500.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_product_price_setter_lower_confirmed():
    product = Product("Товар", "Описание", 500.0, 1)
    with patch("builtins.input", return_value="y"):
        product.price = 300.0
    assert product.price == 300.0


def test_product_price_setter_lower_declined():
    product = Product("Товар", "Описание", 500.0, 1)
    with patch("builtins.input", return_value="n"):
        product.price = 300.0
    assert product.price == 500.0


def test_new_product():
    product_data = {
        "name": "Новый товар",
        "description": "Описание нового товара",
        "price": 1000.0,
        "quantity": 20,
    }
    product = Product.new_product(product_data)
    assert product.name == "Новый товар"
    assert product.description == "Описание нового товара"
    assert product.price == 1000.0
    assert product.quantity == 20


def test_new_product_duplicate_higher_price():
    existing = Product("Существующий", "Описание", 500.0, 10)
    product_data = {
        "name": "Существующий",
        "description": "Новое описание",
        "price": 700.0,
        "quantity": 5,
    }
    result = Product.new_product(product_data, [existing])
    assert result is existing
    assert result.quantity == 15
    assert result.price == 700.0


def test_new_product_duplicate_lower_price():
    existing = Product("Существующий", "Описание", 800.0, 10)
    product_data = {
        "name": "Существующий",
        "description": "Новое описание",
        "price": 500.0,
        "quantity": 5,
    }
    result = Product.new_product(product_data, [existing])
    assert result is existing
    assert result.quantity == 15
    assert result.price == 800.0
