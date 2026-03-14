from src.shop import Category, Product

if __name__ == "__main__":
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации,"
        " но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(category1.name)
    print(category1.description)
    print(category1.products)

    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром,"
        " станет вашим другом и помощником",
        [product4],
    )

    print(category2.products)

    product5 = Product("LG OLED 65", "65 дюймов, 4K", 200000.0, 3)
    category2.add_product(product5)
    print(category2.products)

    product_data = {
        "name": "Google Pixel 8",
        "description": "128GB, Черный",
        "price": 60000.0,
        "quantity": 10,
    }
    new_product = Product.new_product(product_data)
    print(new_product.name, new_product.price)

    print(Category.category_count)
    print(Category.product_count)
