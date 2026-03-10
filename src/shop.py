class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.products = products

    category_count = 0  # Количество созданных категорий
    product_count = 0  # Общее количество товаров во всех категориях

    def __init__(self, name: str, description: str, products: list) -> None:

        self.name = name
        self.description = description
        self.products = products
        Category.category_count += 1  # Увеличили счётчик категорий
        for _ in products:  # Увеличили счётчик товаров
            Category.product_count += _
