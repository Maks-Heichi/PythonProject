from abc import ABC, abstractmethod


class ReprMixin:
    """Миксин для вывода в консоль информации о создании объекта."""

    def __init__(self, *args, **kwargs):
        args_repr = ", ".join(repr(a) for a in args)
        if kwargs:
            kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            print(f"{type(self).__name__}({args_repr}, {kwargs_repr})")
        else:
            print(f"{type(self).__name__}({args_repr})")
        super().__init__()


class BaseProduct(ABC):
    """Базовый абстрактный класс для всех продуктов.
    Содержит только абстрактные методы. Инициализация — в наследниках.
    """

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление продукта."""
        pass


class Product(ReprMixin, BaseProduct):
    """Класс продукта."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__(name, description, price, quantity)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif value < self.__price:
            confirm = input("Подтвердите понижение цены (y/n): ")
            if confirm == "y":
                self.__price = value
        else:
            self.__price = value

    def __add__(self, other):
        if not isinstance(other, BaseProduct):
            return NotImplemented
        if type(self) is not type(other):
            raise TypeError("Можно складывать только продукты одного класса")
        return self.price * self.quantity + other.price * other.quantity

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    @classmethod
    def new_product(cls, product_data: dict, products_list: list = None):
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        if products_list:
            for existing in products_list:
                if existing.name == name:
                    existing.quantity += quantity
                    existing.price = max(existing.price, price)
                    return existing

        return cls(name, description, price, quantity)


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class BaseProductEntity(ABC):
    """Базовый абстрактный класс для сущностей, связанных с продуктами (Категория, Заказ)."""

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление сущности."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Название/идентификатор сущности."""
        pass


class Order(BaseProductEntity):
    """Заказ — один товар, количество и итоговая стоимость."""

    def __init__(self, product: BaseProduct, quantity: int):
        if not isinstance(product, BaseProduct):
            raise TypeError("В заказе может быть указан только продукт")
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        self._product = product
        self._quantity = quantity
        self._total_cost = product.price * quantity

    @property
    def product(self) -> BaseProduct:
        """Товар, который был куплен."""
        return self._product

    @property
    def quantity(self) -> int:
        """Количество купленного товара."""
        return self._quantity

    @property
    def total_cost(self) -> float:
        """Итоговая стоимость заказа."""
        return self._total_cost

    @property
    def name(self) -> str:
        return f"Заказ: {self._product.name}"

    def __str__(self) -> str:
        return (
            f"{self.name}, количество: {self._quantity} шт., "
            f"итого: {self._total_cost} руб."
        )


class Category(BaseProductEntity):
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list) -> None:
        self._name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products)

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self._name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только продукты")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        result = ""
        for product in self.__products:
            result += f"{product}\n"
        return result

    def average_price(self) -> float:
        """Подсчёт среднего ценника всех товаров в категории."""
        try:
            total = sum(product.price for product in self.__products)
            return total / len(self.__products)
        except ZeroDivisionError:
            return 0
