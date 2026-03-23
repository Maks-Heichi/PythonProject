import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.shop import (  # noqa: E402
    BaseProduct,
    BaseProductEntity,
    Category,
    LawnGrass,
    Order,
    Product,
    ReprMixin,
    Smartphone,
)


@pytest.fixture(autouse=True)
def reset_category_counts():
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    product = Product("iPhone 14 Pro Max", "6.7-дюймовый экран, 1TB памяти", 120000.0, 10)
    assert product.name == "iPhone 14 Pro Max"
    assert product.description == "6.7-дюймовый экран, 1TB памяти"
    assert product.price == 120000.0
    assert product.quantity == 10


def test_category_initialization():
    product1 = Product("Galaxy Z Fold 4", "Развертываемый смартфон с гибким дисплеем", 150000.0, 7)
    product2 = Product("Huawei Mate Xs 2", "Складной телефон премиум-класса", 130000.0, 5)
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


def test_category_add_product_rejects_non_product():
    product = Product("Товар 1", "Описание 1", 100.0, 10)
    category = Category("Категория", "Описание", [product])
    assert Category.product_count == 1

    with pytest.raises(TypeError):
        category.add_product("не продукт")

    assert Category.product_count == 1


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


def test_product_add():
    product_a = Product("Товар A", "Описание", 100.0, 10)
    product_b = Product("Товар B", "Описание", 200.0, 2)
    assert product_a + product_b == 100.0 * 10 + 200.0 * 2


def test_product_add_rejects_different_product_classes():
    smartphone = Smartphone(
        name="iPhone 15",
        description="512GB, Gray space",
        price=210000.0,
        quantity=1,
        efficiency=9.5,
        model="A3102",
        memory=512,
        color="серый",
    )
    grass = LawnGrass(
        name="Трава",
        description="Газонная трава",
        price=500.0,
        quantity=2,
        country="RU",
        germination_period=14,
        color="зеленый",
    )

    with pytest.raises(TypeError):
        _ = smartphone + grass


def test_product_add_allows_same_product_class():
    smartphone_a = Smartphone(
        name="iPhone 15",
        description="512GB, Gray space",
        price=210000.0,
        quantity=1,
        efficiency=9.5,
        model="A3102",
        memory=512,
        color="серый",
    )
    smartphone_b = Smartphone(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет",
        price=180000.0,
        quantity=2,
        efficiency=9.0,
        model="SM-S918B",
        memory=256,
        color="серый",
    )

    assert smartphone_a + smartphone_b == 210000.0 * 1 + 180000.0 * 2


def test_product_str():
    product = Product("Товар", "Описание", 80.0, 15)
    assert str(product) == "Товар, 80.0 руб. Остаток: 15 шт."


def test_category_str():
    product1 = Product("Товар 1", "Описание", 50.0, 10)
    product2 = Product("Товар 2", "Описание", 100.0, 5)
    category = Category("Категория", "Описание", [product1, product2])
    assert str(category) == "Категория, количество продуктов: 15 шт."


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


def test_product_inherits_from_base_product():
    """Product является наследником BaseProduct."""
    product = Product("Товар", "Описание", 100.0, 1)
    assert isinstance(product, BaseProduct)


def test_smartphone_inherits_from_product_and_base_product():
    """Smartphone наследует от Product (и тем самым от BaseProduct)."""
    smartphone = Smartphone(
        name="iPhone",
        description="Описание",
        price=100000.0,
        quantity=1,
        efficiency=9.0,
        model="A15",
        memory=256,
        color="черный",
    )
    assert isinstance(smartphone, Product)
    assert isinstance(smartphone, BaseProduct)


def test_lawn_grass_inherits_from_product_and_base_product():
    """LawnGrass наследует от Product (и тем самым от BaseProduct)."""
    grass = LawnGrass(
        name="Трава",
        description="Газонная",
        price=500.0,
        quantity=2,
        country="RU",
        germination_period=14,
        color="зеленый",
    )
    assert isinstance(grass, Product)
    assert isinstance(grass, BaseProduct)


def test_repr_mixin_prints_on_product_creation(capsys):
    """Миксин печатает информацию при создании Product."""
    Product("Продукт1", "Описание продукта", 1200, 10)
    captured = capsys.readouterr()
    assert "Product(" in captured.out
    assert "'Продукт1'" in captured.out
    assert "'Описание продукта'" in captured.out
    assert "1200" in captured.out
    assert "10" in captured.out


def test_repr_mixin_prints_on_smartphone_creation(capsys):
    """Миксин печатает информацию при создании Smartphone."""
    Smartphone(
        name="iPhone 15",
        description="512GB",
        price=210000.0,
        quantity=1,
        efficiency=9.5,
        model="A3102",
        memory=512,
        color="серый",
    )
    captured = capsys.readouterr()
    assert "Smartphone(" in captured.out
    assert "iPhone 15" in captured.out


def test_repr_mixin_prints_on_lawn_grass_creation(capsys):
    """Миксин печатает информацию при создании LawnGrass."""
    LawnGrass(
        name="Трава",
        description="Газонная",
        price=500.0,
        quantity=2,
        country="RU",
        germination_period=14,
        color="зеленый",
    )
    captured = capsys.readouterr()
    assert "LawnGrass(" in captured.out
    assert "Трава" in captured.out


def test_product_has_repr_mixin_in_chain():
    """Product использует ReprMixin в цепочке наследования."""
    assert ReprMixin in Product.__mro__


def test_base_product_is_abstract():
    """BaseProduct нельзя инстанцировать напрямую (абстрактный класс)."""
    with pytest.raises(TypeError):
        BaseProduct("Товар", "Описание", 100.0, 1)


def test_product_rejects_zero_quantity():
    """Товар с нулевым количеством не может быть создан."""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Товар", "Описание", 100.0, 0)


def test_category_average_price():
    """Средний ценник = сумма цен / количество товаров."""
    product1 = Product("Товар 1", "Описание", 100.0, 10)
    product2 = Product("Товар 2", "Описание", 200.0, 5)
    product3 = Product("Товар 3", "Описание", 300.0, 3)
    category = Category("Категория", "Описание", [product1, product2, product3])
    assert category.average_price() == 200.0  # (100 + 200 + 300) / 3


def test_category_average_price_empty():
    """Пустая категория возвращает 0."""
    category = Category("Пустая", "Описание", [])
    assert category.average_price() == 0


def test_category_average_price_single_product():
    """Категория с одним товаром — средняя цена = цена товара."""
    product = Product("Товар", "Описание", 500.0, 1)
    category = Category("Категория", "Описание", [product])
    assert category.average_price() == 500.0


def test_new_product_rejects_zero_quantity():
    """new_product с нулевым количеством выбрасывает ValueError."""
    product_data = {
        "name": "Товар",
        "description": "Описание",
        "price": 100.0,
        "quantity": 0,
    }
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product.new_product(product_data)


# --- Тесты для класса Order и BaseProductEntity ---


def test_order_creation():
    """Заказ создаётся с продуктом, количеством и итоговой стоимостью."""
    product = Product("Товар", "Описание", 100.0, 10)
    order = Order(product, 3)
    assert order.product is product
    assert order.quantity == 3
    assert order.total_cost == 300.0


def test_order_total_cost():
    """Итоговая стоимость заказа = цена * количество."""
    product = Product("Телефон", "Описание", 50000.0, 5)
    order = Order(product, 2)
    assert order.total_cost == 100000.0


def test_order_str():
    """Строковое представление заказа."""
    product = Product("Товар", "Описание", 100.0, 10)
    order = Order(product, 2)
    assert "Заказ: Товар" in str(order)
    assert "2" in str(order)
    assert "200.0" in str(order)


def test_order_rejects_non_product():
    """Заказ принимает только продукт."""
    with pytest.raises(TypeError):
        Order("не продукт", 1)


def test_order_rejects_zero_quantity():
    """Количество в заказе должно быть положительным."""
    product = Product("Товар", "Описание", 100.0, 10)
    with pytest.raises(ValueError):
        Order(product, 0)


def test_order_rejects_negative_quantity():
    """Количество в заказе должно быть положительным."""
    product = Product("Товар", "Описание", 100.0, 10)
    with pytest.raises(ValueError):
        Order(product, -1)


def test_order_inherits_from_base_product_entity():
    """Order наследует от BaseProductEntity."""
    product = Product("Товар", "Описание", 100.0, 10)
    order = Order(product, 1)
    assert isinstance(order, BaseProductEntity)


def test_category_inherits_from_base_product_entity():
    """Category наследует от BaseProductEntity."""
    product = Product("Товар", "Описание", 100.0, 1)
    category = Category("Категория", "Описание", [product])
    assert isinstance(category, BaseProductEntity)


def test_base_product_entity_is_abstract():
    """BaseProductEntity нельзя инстанцировать напрямую."""
    with pytest.raises(TypeError):
        BaseProductEntity()


def test_order_with_smartphone():
    """Заказ можно создать с товаром-смартфоном."""
    smartphone = Smartphone(
        name="iPhone",
        description="Описание",
        price=100000.0,
        quantity=5,
        efficiency=9.0,
        model="A15",
        memory=256,
        color="черный",
    )
    order = Order(smartphone, 2)
    assert order.total_cost == 200000.0
    assert order.product is smartphone
