# Урок 7. Основы Python. Часть III — ООП

Объектно-ориентированное программирование помогает хранить **данные** и действия над ними **вместе**. В домашней работе эти идеи используются для реализации интернет-магазина:

- [`homework/models.py`](homework/models.py) — классы `Product` и `Cart`;
- [`homework/test_shop.py`](homework/test_shop.py) — тесты для этих классов.

> Главная идея урока: объект знает своё состояние и сам выполняет действия, которые относятся к нему.

## Содержание

- [Зачем вообще нужно ООП](#зачем-вообще-нужно-ооп)
- [Класс и объект](#класс-и-объект)
- [`self` — «я сам»](#self--я-сам)
- [Атрибуты и аннотации типов](#атрибуты-и-аннотации-типов)
- [`return` и `raise`](#return-и-raise)
- [Присваивание и изменение состояния](#присваивание-и-изменение-состояния)
- [Как читать traceback](#как-читать-traceback)
- [Объект как ключ словаря](#объект-как-ключ-словаря)
- [Аргументы по умолчанию](#аргументы-по-умолчанию)
- [Логика домашней работы](#логика-домашней-работы)
- [Тестирование с pytest](#тестирование-с-pytest)
- [Частые ошибки](#частые-ошибки)
- [Что пригодится дальше](#что-пригодится-дальше)
- [Короткая памятка](#короткая-памятка)

# Зачем вообще нужно ООП

Без классов данные и действия живут порознь, а связь между ними приходится держать в голове:

```python
person = {"name": "Иван", "age": 25}


def say_hello(p):
    print(f"Привет, меня зовут {p['name']}")


say_hello({"title": "Книга"})
# KeyError: 'name' — передали словарь не того вида
```

У такого подхода быстро появляются проблемы:

- опечатку в ключе, например `"nmae"`, Python заранее не заметит;
- каждой функции нужно вручную передавать подходящий словарь;
- когда объектов и действий становится много, код начинает расползаться.

Класс объединяет данные и действия: набор полей описан в одном месте, а методы работают с конкретным объектом.

# Класс и объект

**Класс** — форма для печенья. **Объект** — печенька, сделанная с помощью этой формы.

```python
class Person:                         # форма
    def __init__(self, name, age):    # конструктор вызывается при создании объекта
        self.name = name              # атрибут — данные внутри объекта
        self.age = age

    def say_hello(self):              # метод — действие объекта
        print(f"Привет, я {self.name}, мне {self.age}")


ivan = Person("Иван", 25)            # объект № 1
maria = Person("Мария", 30)          # объект № 2

ivan.say_hello()
```

| Термин | Что это | Пример |
|---|---|---|
| Класс | Форма, описание будущих объектов | `class Person:` |
| Объект, или экземпляр | Конкретный объект, созданный по классу | `ivan = Person("Иван", 25)` |
| Атрибут | Данные внутри объекта | `self.name` |
| Метод | Действие объекта | `ivan.say_hello()` |

## Правило точки

Слева от точки указано, **чей** метод или атрибут нужен. Справа — **какой именно**.

```python
product.buy(3)       # просим конкретный товар купить 3 штуки
self.clear()         # объект вызывает собственный метод
self.products        # объект обращается к собственному атрибуту
```

Один и тот же атрибут можно увидеть с двух сторон:

```python
class Product:
    def buy(self, quantity):
        self.quantity -= quantity    # изнутри: «моё количество»


product.quantity                     # снаружи: количество этого товара
```

Это одно поле — меняется только точка зрения: «моя рука» и «рука Ивана».

# `self` — «я сам»

`self` — ссылка на конкретный объект, у которого вызван метод. Python автоматически подставляет объект первым аргументом.

```python
def __init__(self, name, age):
#            ↑     ↑     ↑
#            │     │     └── 25 — передаём мы
#            │     └──────── "Иван" — передаём мы
#            └────────────── объект — подставляет Python
```

## Как создаётся объект

```text
① ivan = Person("Иван", 25)
        └─ Python создаёт пустой объект             __dict__ == {}
② Python вызывает __init__, self указывает на объект
③ self.name = name   → появляется поле name        {'name': 'Иван'}
④ self.age = age     → появляется поле age         {'name': 'Иван', 'age': 25}
⑤ локальные name и age исчезают, объект остаётся
⑥ готовый объект получает имя ivan
```

Посмотреть процесс можно с помощью `print(self.__dict__)` в начале и в конце `__init__`.

> Атрибут экземпляра появляется именно в строке `self.x = ...`. До выполнения этой строки его ещё нет.

`self` существует только внутри методов класса. В тесте нужно обращаться к объекту по имени переменной — например, `cart` или `product`.

```python
self.quantity       # внутри метода класса
product.quantity    # снаружи класса
```

Если написать `self` вне метода, возникнет ошибка:

```text
NameError: name 'self' is not defined
```

# Атрибуты и аннотации типов

Аннотация типа описывает ожидаемый тип, но сама по себе не создаёт атрибут экземпляра.

```python
class Box:
    weight: int             # нет «=» — это только аннотация

    def __init__(self):
        self.color = "red"  # присваивание реально создаёт атрибут


box = Box()

print(box.__dict__)         # {'color': 'red'}
print(box.weight)           # AttributeError
```

| Запись | Как читается |
|---|---|
| `name: str` | Значение `name` ожидается строкой |
| `-> bool` | Метод должен вернуть `True` или `False` |
| `dict[Product, int]` | Ключ словаря — `Product`, значение — `int` |

Квадратные скобки в `dict[Product, int]` не означают список. Они уточняют тип ключей и значений словаря.

# `return` и `raise`

Выражение без `return` вычислится, но результат будет потерян:

```python
def check_quantity(self, quantity) -> bool:
    self.quantity >= quantity       # ❌ результат вычислен и выброшен
```

Безусловный `return True` тоже неверен — метод перестанет учитывать аргумент:

```python
def check_quantity(self, quantity) -> bool:
    return True                     # ❌ всегда True
```

Сравнение уже возвращает логическое значение, поэтому достаточно вернуть его:

```python
def check_quantity(self, quantity) -> bool:
    return self.quantity >= quantity    # ✅ True или False
```

| Конструкция | Что делает | Что происходит дальше |
|---|---|---|
| `return` | Возвращает значение вызывающему коду | Программа продолжает работу |
| `raise` | Выбрасывает исключение | Обычное выполнение прерывается |

```python
def buy(self, quantity):
    if self.check_quantity(quantity):
        self.quantity -= quantity
    else:
        raise ValueError(
            f"На складе {self.quantity}, запрошено {quantity}"
        )
```

`ValueError` — тип ошибки для неподходящего значения. Полезное сообщение с фактическими числами сильно упрощает разбор падения в CI.

# Присваивание и изменение состояния

Знак `=` — это действие, а не математическое равенство. Сначала вычисляется правая часть со старым значением, затем результат записывается слева.

```python
self.quantity = self.quantity - quantity
#      ↑                ↑
#    новое            старое
```

Короткая форма делает то же самое:

```python
self.quantity -= quantity
```

Переменная с числом хранит снимок значения, а не «живую ссылку» на атрибут:

```python
quantity_before = product.quantity    # снимок: 1000
product.buy(5)

print(quantity_before)                # 1000
print(product.quantity)               # 995
```

# Как читать traceback

Traceback удобно читать снизу вверх: **что случилось → где случилось → кто вызвал**.

```text
ValueError: на ноль делить нельзя!     ← что: тип и сообщение
  raise ValueError(...)  line 3        ← где возникла ошибка
  print(divide(10, 0))   line 7        ← кто вызвал функцию
```

```text
Process finished with exit code 0     → программа завершилась успешно
Process finished with exit code 1     → программа завершилась с ошибкой
```

# Объект как ключ словаря

Корзина хранит товар и выбранное количество в словаре:

```python
products: dict[Product, int]    # {товар: количество в корзине}
```

Ключ словаря должен быть **хешируемым**. Например, список использовать нельзя:

```python
data = {}
data[[1, 2, 3]] = "привет"
# TypeError: unhashable type: 'list'
```

В домашней работе объект `Product` можно использовать как ключ благодаря методу `__hash__`:

```python
def __hash__(self):
    return hash(self.name + self.description)
```

> Поля, от которых зависит хеш, не следует менять, пока объект используется как ключ словаря.

Ключ и значение — не одно и то же. Представим телефонную книжку:

```python
phone_book = {"Иван": 555}

"Иван"               # ключ
phone_book["Иван"]   # значение: 555
```

| Телефонная книжка | Корзина |
|---|---|
| `phone_book` — весь словарь | `self.products` — вся корзина |
| `"Иван"` — ключ | `product` — товар-ключ |
| `phone_book["Иван"]` — номер | `self.products[product]` — количество |

Три похожих имени легко перепутать:

| Имя | Что это |
|---|---|
| `Product` | Класс, форма для товаров |
| `product` | Переменная с конкретным товаром |
| `self.products` | Словарь товаров внутри корзины |

Основные операции со словарём корзины:

```python
product in self.products          # есть ли такой ключ
self.products[product] = 3        # записать значение
self.products[product] += 3       # увеличить существующее значение
del self.products[product]        # удалить одну позицию
self.products = {}                # очистить всю корзину
```

# Аргументы по умолчанию

```python
def add_product(self, product, buy_count=1):
    ...


def remove_product(self, product, remove_count=None):
    ...
```

Если `buy_count` не передали, Python использует `1`.

`None` служит флажком «значение не передали». Здесь важно различать два действия:

- `remove_product(product, 1)` — убрать одну штуку;
- `remove_product(product)` — убрать позицию целиком.

Для проверки `None` принято использовать `is`:

```python
if remove_count is None:
    ...
```

# Логика домашней работы

## Добавление товара

Если товар уже есть в корзине, увеличиваем количество. Иначе создаём новую позицию.

```python
def add_product(self, product, buy_count=1):
    if product in self.products:
        self.products[product] += buy_count
    else:
        self.products[product] = buy_count
```

## Удаление товара

Если количество не передано или оно больше количества в корзине, удаляем позицию целиком. Иначе уменьшаем количество.

```python
def remove_product(self, product, remove_count=None):
    if remove_count is None or remove_count > self.products[product]:
        del self.products[product]
    else:
        self.products[product] -= remove_count
```

## Очистка корзины

```python
def clear(self):
    self.products = {}
```

Метод заменяет словарь товаров новым пустым словарём.

## Подсчёт стоимости

```python
def get_total_price(self) -> float:
    total_price = 0

    for product in self.products:
        total_price += self.products[product] * product.price
        #              └─ количество в корзине ┘   └─ цена товара ┘

    return total_price
```

Копилка `total_price` создаётся **до** цикла, а `return` находится **после** него. Иначе метод обработает только первый товар.

## Покупка

```python
def buy(self):
    for product in self.products:
        product.buy(self.products[product])

    self.clear()
```

Каждый товар сам проверяет остаток на складе и сам выбрасывает `ValueError`, если товара не хватает. Корзина только сообщает, сколько единиц нужно купить.

Это разделение ответственности:

```text
ТОВАР (product)                    КОРЗИНА (self.products)
├── price = 100       цена         └── book: 3       сколько хотим купить
└── quantity = 1000   остаток
```

- «Сколько есть?» → `product.quantity`;
- «Сколько берём?» → `self.products[product]`.

> Корзина не дублирует проверку склада. Логика остатка находится в одном месте — в `Product`.

# Тестирование с pytest

## Запуск тестов

Из корня проекта:

```bash
pytest homework/test_shop.py
```

Подробный вывод:

```bash
pytest -v
```

Если pytest пишет `ERROR: file or directory not found`, сначала проверьте текущую директорию и путь к файлу.

## Фикстуры

```python
import pytest


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()
```

В тесте достаточно указать имя фикстуры в аргументах:

```python
def test_add_product(cart, product):
    ...
```

Зачем нужны фикстуры:

- не дублируется подготовка данных;
- перед каждым тестом создаётся свежий объект;
- тесты не портят состояние друг друга.

Одна фикстура возвращает один результат. Код после первого `return` уже не выполнится.

## AAA: структура теста

```python
def test_product_buy(product):
    quantity_before = product.quantity               # Arrange — подготовили
    product.buy(5)                                   # Act — выполнили действие
    assert product.quantity == quantity_before - 5   # Assert — проверили
```

| Поведение метода | Как проверить |
|---|---|
| Возвращает значение | `assert product.check_quantity(5)` |
| Меняет состояние объекта | `assert product.quantity == ...` |
| Удаляет ключ из словаря | `assert product not in cart.products` |
| Полностью очищает корзину | `assert cart.products == {}` |

Проверка граничных значений для склада из `1000` единиц:

```python
assert product.check_quantity(1000)
assert not product.check_quantity(1001)
```

## `pytest.raises`: ожидаем ошибку

```python
def test_cart_buy_more_than_available(cart, product):
    cart.add_product(product, 1001)

    with pytest.raises(ValueError):
        cart.buy()
```

| Что произошло | В обычном коде | В `pytest.raises` |
|---|---:|---:|
| Ошибка возникла | ❌ | ✅ |
| Ошибки не было | ✅ | ❌ `Failed: DID NOT RAISE` |

`raise` бросает исключение в рабочем коде, а `pytest.raises` ловит ожидаемое исключение в тесте.

Внутри `with` должна быть только подозреваемая строка. Иначе тест может случайно поймать ошибку не из того места.

## Правила хороших тестов

### Проверяйте границы

Ошибки чаще живут на значениях `N - 1`, `N` и `N + 1`, а не в середине диапазона.

```python
product.check_quantity(500)     # не заметит ошибку «>» вместо «>=»
product.check_quantity(1000)    # заметит
```

### Не используйте магические числа

```python
assert product.quantity == 995                    # ❌ откуда взялось 995?
assert product.quantity == quantity_before - 5    # ✅ видна формула
```

Для нескольких товаров:

```python
assert cart.get_total_price() == 5 * product.price + 3 * cup.price
```

### Проверяйте зону ответственности метода

```python
# remove_product отвечает за один товар
assert product not in cart.products    # ✅
assert not cart.products               # ❌ может остаться другой товар

# clear отвечает за всю корзину
assert cart.products == {}             # ✅
```

### Один тест — один сценарий

По имени упавшего теста должно быть понятно, что сломалось:

```python
def test_remove_product_1(...):             # ❌ непонятно
    ...


def test_add_new_product(...):              # ✅
    ...


def test_add_existing_product(...):         # ✅
    ...


def test_remove_more_than_in_cart(...):     # ✅
    ...
```

Имя не должно противоречить сценарию. Если тест называется `..._when_count_not_passed`, внутри не должно быть `remove_product(product, 100)`.

### Проверяйте всё заявленное поведение

`Cart.buy()` списывает товары со склада **и** очищает корзину, поэтому нужно проверить оба результата:

```python
def test_cart_buy(cart, product, cup):
    product_quantity_before = product.quantity
    cup_quantity_before = cup.quantity

    cart.add_product(product, 5)
    cart.add_product(cup, 3)
    cart.buy()

    assert cart.products == {}
    assert product.quantity == product_quantity_before - 5
    assert cup.quantity == cup_quantity_before - 3
```

Полезный вопрос к тесту: **если удалить половину реализации метода, тест это заметит?** Если нет, проверок недостаточно.

# Частые ошибки

| Симптом | Причина | Как исправить |
|---|---|---|
| Метод всегда возвращает `True` | Написан `return True` вместо сравнения | Вернуть само сравнение |
| `NotImplementedError` | В коде осталась заглушка задания | Реализовать метод и удалить заглушку |
| `Failed: DID NOT RAISE ValueError` | Ошибка не возникла или `pytest.raises` попал в рабочий код | `raise` оставить в модели, `pytest.raises` — в тесте |
| `KeyError: 'name'` | В словаре нет такого ключа | Проверить имя ключа и условие `in` |
| `AttributeError: ... has no attribute 'weight'` | Есть только `weight: int`, но нет присваивания | Создать атрибут через `self.weight = ...` |
| `TypeError: unhashable type: 'list'` | Список использован как ключ словаря | Использовать хешируемый ключ |
| `NameError: name 'self' is not defined` | `self` написан вне метода класса | Обращаться через имя объекта |
| `ERROR: file or directory not found` | pytest запущен не из той директории | Проверить текущую папку и путь |
| Тест зелёный, но ничего не проверяет | Нет `assert` | Добавить проверку результата |

> Главный урок: зелёный тест ещё не гарантирует рабочий код. Тест должен падать при поломанной реализации.

# Что пригодится дальше

Эти темы есть в конспекте, но для основной части домашней работы не обязательны.

## Инкапсуляция

Инкапсуляция помогает скрывать внутренние детали объекта и предоставлять понятный интерфейс через методы и свойства.

```python
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
```

## Наследование

Новый класс может использовать и расширять поведение существующего:

```python
class Student(Person):
    def __init__(self, name, age, grade):
        super().__init__(name, age)
        self.grade = grade
```

## Полиморфизм

Объекты разных классов можно использовать одинаково, если у них есть общий интерфейс:

```python
def get_sound(pet):
    return pet.speak()    # сработает и для Dog, и для Cat
```

## Декораторы методов

```python
@property        # обращение как к атрибуту: obj.name
@classmethod     # первый аргумент — cls, то есть класс
@staticmethod    # нет ни self, ни cls
```

## Магические методы

| Метод | Для чего нужен |
|---|---|
| `__init__` | Инициализация нового объекта |
| `__str__` | Человекочитаемая строка, например для `print` |
| `__repr__` | Представление объекта для разработки и отладки |
| `__eq__` | Сравнение через `==` |
| `__len__` | Поддержка `len(obj)` |
| `__hash__` | Получение хеша, например для ключа словаря |

## `dataclass`

Для класса, который в основном хранит данные, можно не писать `__init__` вручную:

```python
from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int
```

## Enum и принципы разработки

`Enum` — набор именованных констант. Он полезен, когда значение должно быть выбрано из заранее известного ограниченного списка.

Основные принципы:

- **DRY** — не дублируй код;
- **KISS** — выбирай простое решение;
- **YAGNI** — не пиши функциональность впрок;
- **SOLID, S** — у класса должна быть одна зона ответственности.

# Короткая памятка

```python
class Product:
    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        return self.quantity >= quantity

    def buy(self, quantity):
        if not self.check_quantity(quantity):
            raise ValueError(
                f"На складе {self.quantity}, запрошено {quantity}"
            )

        self.quantity -= quantity
```

```python
class Cart:
    def __init__(self):
        self.products = {}

    def add_product(self, product, buy_count=1):
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def get_total_price(self) -> float:
        total_price = 0

        for product in self.products:
            total_price += self.products[product] * product.price

        return total_price
```

Запомнить проще всего так:

1. `self` — конкретный объект.
2. `self.x = ...` — создание или изменение атрибута.
3. `return` — вернуть результат, `raise` — выбросить ошибку.
4. `product.quantity` — остаток на складе.
5. `self.products[product]` — количество в корзине.
6. Хороший тест проверяет результат, границы и заявленное поведение метода.
