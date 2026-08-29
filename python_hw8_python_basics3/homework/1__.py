from homework.models import Cart, Product

book = Product("book", 100, "This is a book", 1000)
cup = Product("cup", 50, "This is a cup", 500)

cart = Cart()
cart.add_product(book, 3)
cart.add_product(cup, 2)

print("сумма:", cart.get_total_price())
cart.buy()
print("склад книг:", book.quantity)
print("склад чашек:", cup.quantity)
print("корзина:", cart.products)
