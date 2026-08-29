"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cup():
    return Product("cup", 50, "This is a cup", 100)

class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(1)
        assert product.check_quantity(1000)
        assert not product.check_quantity(1001)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        quantity_before = product.quantity
        product.buy(5)
        assert product.quantity == quantity_before - 5

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(1001)


@pytest.fixture
def cart():
    return Cart()


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_add_new_product(self, cart, product):
        cart.add_product(product, 3)
        assert cart.products[product] == 3

    def test_add_existing_product(self, cart, product):
        cart.add_product(product)   # Arrange: товар уже в корзине
        cart.add_product(product, 3)    # Act: добавляем ещё
        assert cart.products[product] == 4  # Assert

    def test_remove_product(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 3)
        assert cart.products[product] == 2

    def test_remove_without_count(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_more_than_that(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product, 100)
        assert product not in cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, 5)
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, cart, product, cup):
        cart.add_product(product, 5)
        cart.add_product(cup, 3)
        assert cart.get_total_price() == 5 * product.price + 3 * cup.price

    def test_cart_buy(self, cart, product, cup):
        product_quantity_before = product.quantity
        cup_quantity_before = cup.quantity

        cart.add_product(product, 5)
        cart.add_product(cup, 3)
        cart.buy()

        assert cart.products == {}
        assert product.quantity == product_quantity_before - 5
        assert cup.quantity == cup_quantity_before - 3

    def test_cart_buy_more_than_available(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            cart.buy()
