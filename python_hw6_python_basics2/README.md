# Boolean
Функция bool() преобразует любой объект в True или False. Правило простое: False = пустое ("",[], {}), нулевое (0), ничто (None). True = всё остальное.

## Числа
```python
bool(0)    # False
bool(1)    # True
bool(-1)   # True
```

## Строки
```python
bool("")           # False
bool("Not Found")  # True
```

## None
```python
bool(None)  # False
```

## Списки
```python
bool([])           # False
bool(["admin"])    # True
```

## Словари
```python
bool({})        # False
bool({"id": 1}) # True
```

## Непустой список = True
```python
# Если список непустой = True, неважно что внутри

bool([False])  # True
bool([0])      # True
bool([None])   # True
```

# if / elif / else

## Базовая структура
```python

# Отступы 4 пробела обозначают вложенность

if условие:      # True — выполняется этот блок
    ...
elif условие:    # первое False — проверяем следующее
    ...
else:            # все условия False — выполняется этот блок
    ...

# elif и else не обязательны, elif может быть сколько угодно
```

## Пример проверки статус кода
```python

status_code = 200

if 200 <= status_code < 400:
    print("Код ответа верный")
    print("Сервер отвечает")
elif status_code == 404:
    print("Страница не найдена")
elif status_code == 500:
    print("Ошибка сервера")
else:
    print("Неизвестный код")
```

## Логические операторы or / and
```python

status_code = 200
response_body = ["user1", "user2"]

if status_code == 404 or status_code == 500:  # достаточно одного True
    print("Тест упал!")

if status_code == 200 and response_body != []:  # оба должны быть True
    print("Тест пройден!")

if not response_body:  # not меняет на противоположное
    print("Список пустой")
```

## pass — заглушка
```python

# Используется когда тело блока пока не нужно

response_body = []

if response_body == []:
    pass  # TODO: добавить обработку позже
```

## Синтаксический сахар
```python

# Короткая проверка вместо сравнения с пустым значением

response_body = []
error_message = ""
items_count = 0

>>> Список <<<
# Длинный способ                  # Короткий способ
response_body == []        # →    not response_body   — True,  список пустой
response_body != []        # →    response_body       — False, список пустой

>>> Строка <<<
error_message == ""        # →    not error_message   — True,  строка пустая
error_message != ""        # →    error_message       — False, строка пустая

>>> Число <<<
items_count == 0           # →    not items_count     — True,  счётчик ноль
items_count != 0           # →    items_count         — False, счётчик ноль
```

## Тест падает только при assert
```python

response_body = []

def test_example():
    if response_body:
        pass              # тест пройдет — нет assert, pytest доходит до конца и говорит "ок"

def test_example():
    assert response_body  # тест упадет — [] это False
```

# Циклы (loops)

## While
Циклы в Python нужны для повторения одних и тех же действий несколько раз. While — выполняет тело цикла пока условие истинно.

### Без итератора
```python

i = 10

while i < 15:
    print(i)
    i += 1

# Шаг | i  | i < 15 | что печатаем         | после i += 1
# 1   | 10 | True   | 10                   | i = 11
# 2   | 11 | True   | 11                   | i = 12
# 3   | 12 | True   | 12                   | i = 13
# 4   | 13 | True   | 13                   | i = 14
# 5   | 14 | True   | 14                   | i = 15
# 6   | 15 | False  | цикл остановился     | —
```

### С итератором
```python

# Cчитаем количество повторений

attempts = 3
i = 0  # итератор всегда начинается с 0

while i < attempts:
    print(f"Попытка {i + 1} из {attempts}")
    i += 1

# Шаг | i | i < attempts | что печатаем       | после i += 1
# 1   | 0 | 0 < 3 = True | Попытка 1 из 3     | i = 1
# 2   | 1 | 1 < 3 = True | Попытка 2 из 3     | i = 2
# 3   | 2 | 2 < 3 = True | Попытка 3 из 3     | i = 3
# 4   | 3 | 3 < 3 = False| цикл остановился   | —
```

### Бесконечный цикл
```python
# Забыли увеличить счётчик - цикл будет выполняться бесконечно

attempts = 3
i = 0

while i < attempts:
    print(f"Попытка {i + 1} из {attempts}")
    # i += 1 — забыли, i всегда 0, условие всегда True

# Шаг | i | i < attempts | что печатаем       | i += 1
# 1   | 0 | 0 < 3 = True | Попытка 1 из 3     | забыли
# 2   | 0 | 0 < 3 = True | Попытка 1 из 3     | забыли
# 3   | 0 | 0 < 3 = True | Попытка 1 из 3     | забыли
# ... | 0 | всегда True  | бесконечно         | —
```

### Как работает цикл изнутри
```python
attempts = 3
i = 0

1. while 0 < 3:     ← True — заходим в цикл
2.     print(...)   ← печатаем "Попытка 1 из 3"
3.     i += 1       ← i = 1

4. while 1 < 3:     ← True — заходим в цикл
5.     print(...)   ← печатаем "Попытка 2 из 3"
6.     i += 1       ← i = 2

7. while 2 < 3:     ← True — заходим в цикл
8.     print(...)   ← печатаем "Попытка 3 из 3"
9.     i += 1       ← i = 3

10. while 3 < 3:    ← False — выходим из цикла
```

## for
```python

>>> Синтаксис <<<

for переменная in последовательность:
    код, который выполняется для каждого элемента
    действие(переменная)

>>> Основные типы последовательностей <<<

# 1. Строки (перебор посимвольно)
s = "Hello"
for char in s:
    print(char)  # H, e, l, l, o

# 2. Списки (перебор элементов)
l = [1, 2, 3]
for item in l:
    print(item)  # 1, 2, 3

# 3. Словари (перебор ключей) - по умолчанию словари перебираются по ключам
d = {"a": 1, "b": 2}
for key in d:
    print(key)  # a, b

# Идентичная запись перебора по ключам
d = {"a": 1, "b": 2}
for key in d.keys:
    print(key)  # a, b

# 4. Словари (перебор значений)
d = {"a": 1, "b": 2}
for value in d.values:
    print(value)  # 1, 2

# 5. Словари (перебор пар ключ-значение)
d = {"a": 1, "b": 2}
for key, value in d.items():
    print(key, value)  # a 1, b 2

# 6. Словари (список словарей)
users = [
    {"name": "User1", "age": 21},
    {"name": "User2", "age": 22}
]
for user in users:
    # цикл for возвращает в переменную user словари: {'name': 'User1', 'age': 21} {'name': 'User2', 'age': 22}
    print(f"Пользователю {user['name']} {user['age']} лет") # Пользователю User1 21 лет Пользователю User2, 22 лет

# 7. Range (числовые последовательности)
for i in range(3):
    print(i)  # 0, 1, 2

>>> Важные особенности <<<

# 1. Отступы обязательны (4 пробела)
for i in range(3):
    print(i)  # с отступом - внутри цикла
print("Готово")  # без отступа - после цикла

# 2. Переменная цикла существует после цикла
for x in [1, 2, 3]:
    print(f"Внутри цикла: x = {x}")
    # Внутри цикла: x = 1
    # Внутри цикла: x = 2
    # Внутри цикла: x = 3
# После цикла переменная x всё ещё доступна
print(f"После цикла: x = {x}")
# После цикла: x = 3 (последнее значение)
```
### Вложенные циклы
```python

>>> Вложенные циклы for <<<

users = ["admin", "user1"]
sections = ["главная", "профиль", "настройки"]

for user in users:
    for section in sections:
        print(f"Проверяем доступ {user} к разделу {section}")

# Внешний цикл user = "admin":
#     Внутренний цикл section = "главная":   печатаем "Проверяем доступ admin к разделу главная"
#     Внутренний цикл section = "профиль":   печатаем "Проверяем доступ admin к разделу профиль"
#     Внутренний цикл section = "настройки": печатаем "Проверяем доступ admin к разделу настройки"
#
# Внешний цикл user = "user1":
#     Внутренний цикл section = "главная":   печатаем "Проверяем доступ user1 к разделу главная"
#     Внутренний цикл section = "профиль":   печатаем "Проверяем доступ user1 к разделу профиль"
#     Внутренний цикл section = "настройки": печатаем "Проверяем доступ user1 к разделу настройки"

>>> Вложенные циклы while <<<

i = 0
j = 0

while i < 2:
    while j < 3:
        print(i, j)
        j += 1
    i += 1
    j = 0  # сбрасываем j, иначе внутренний цикл не запустится второй раз

# Внешний цикл i = 0:
#     Внутренний цикл j = 0: печатаем 0 0, j = 1
#     Внутренний цикл j = 1: печатаем 0 1, j = 2
#     Внутренний цикл j = 2: печатаем 0 2, j = 3
#     Внутренний цикл j = 3: 3 < 3 = False — выходим, i = 1, j = 0
#
# Внешний цикл i = 1:
#     Внутренний цикл j = 0: печатаем 1 0, j = 1
#     Внутренний цикл j = 1: печатаем 1 1, j = 2
#     Внутренний цикл j = 2: печатаем 1 2, j = 3
#     Внутренний цикл j = 3: 3 < 3 = False — выходим, i = 2, j = 0
#
# Внешний цикл i = 2: 2 < 2 = False — выходим из внешнего цикла

>>> Цикл с шагом между итерациями <<<

total_pages = 10

for page in range(1, total_pages, 2):  # range(start, stop, step)
    print(f"Проверяем страницу {page}")

# range(1, 10, 2) → 1, 3, 5, 7, 9
# start = 1  — начинаем с первой страницы
# stop  = 10 — останавливаемся до 10
# step  = 2  — каждую вторую страницу
```

### range / break / continue / else / enumerate
```python

>>> range <<<

for i in range(5):          # range(stop)         → 0, 1, 2, 3, 4
    print(i)

for i in range(2, 5):       # range(start, stop)  → 2, 3, 4
    print(i)

for i in range(2, 10, 2):   # range(start, stop, step) → 2, 4, 6, 8
    print(i)

>>> break — прерывает цикл <<<

status_codes = [200, 200, 404, 200]

for code in status_codes:
    if code == 404:
        print("Найдена ошибка — останавливаем проверку")
        break
    print(f"Код {code} — ок")

# Код 200 — ок
# Код 200 — ок
# Найдена ошибка — останавливаем проверку

>>> continue — пропускает текущую итерацию <<<

status_codes = [200, 404, 200, 500, 200]

for code in status_codes:
    if code != 200:
        continue            # пропускаем плохие коды
    print(f"Код {code} — ок")

# Код 200 — ок
# Код 200 — ок
# Код 200 — ок

>>> else — выполняется после завершения цикла <<<

status_codes = [200, 200, 200]

for code in status_codes:
    print(f"Проверяем код {code}")
else:
    print("Все коды проверены")

# Проверяем код 200
# Проверяем код 200
# Проверяем код 200
# Все коды проверены

>>> enumerate — возвращает индекс и значение элемента <<<

status_codes = [200, 404, 500]

for i, code in enumerate(status_codes):
    if code != 200:
        print(f"Тест упал на проверке {i + 1}: код {code}")

# Тест упал на проверке 2: код 404
# Тест упал на проверке 3: код 500

# шаг 1: i = 0, code = 200 — ок, ничего не печатаем
# шаг 2: i = 1, code = 404 — печатаем "Тест упал на проверке 2: код 404"
# шаг 3: i = 2, code = 500 — печатаем "Тест упал на проверке 3: код 500"
```

# Параметры функции
## Определение и вызов функции
```python

def check_code(actual, expected):
    if actual == expected:
        print(f"Тест пройден: код {actual} совпадает с ожидаемым")
    else:
        print(f"Тест упал: ожидали {expected}, получили {actual}")

check_code(200, 200)  # вызов функции — имя функции + скобки () = вызов
# Тест пройден: код 200 совпадает с ожидаемым"
```

### Позиционные аргументы
```python
# Передаются по порядку

def check_code(actual, expected):
    if actual == expected:
        print(f"Тест пройден: код {actual} совпадает с ожидаемым")
    else:
        print(f"Тест упал: ожидали {expected}, получили {actual}")

check_code(200, 200)  # actual = 200, expected = 200
check_code(404, 200)  # actual = 404, expected = 200

# Тест пройден: код 200 совпадает с ожидаемым
# Тест упал: ожидали 200, получили 404
```

### Именованные аргументы
```python
# Порядок не важен

def check_code(actual, expected):
    if actual == expected:
        print(f"Тест пройден: код {actual} совпадает с ожидаемым")
    else:
        print(f"Тест упал: ожидали {expected}, получили {actual}")

check_code(actual=404, expected=200)
check_code(expected=200, actual=404)  # то же самое — порядок не важен

# Тест упал: ожидали 200, получили 404
# Тест упал: ожидали 200, получили 404
```

### Аргументы по умолчанию
```python
# Аргумент необязателен при вызове

def check_code(actual, expected=200):  # 200 — значение по умолчанию
    if actual == expected:
        print(f"Тест пройден: код {actual} совпадает с ожидаемым")
    else:
        print(f"Тест упал: ожидали {expected}, получили {actual}")

check_code(200)       # expected не передали — используется 200 по умолчанию
check_code(404)       # expected не передали — используется 200 по умолчанию
check_code(200, 201)  # expected передали — используется 201

# Тест пройден: код 200 совпадает с ожидаемым
# Тест упал: ожидали 200, получили 404
# Тест упал: ожидали 201, получили 200
```

## Возврат значений
```python

>>> Возврат одного значения <<<

def check_code(actual, expected):
    if actual == expected:
        return True   # если True — функция останавливается здесь
    return False      # сюда код дойдёт только если условие выше было False

result = check_code(200, 200)  # сохраняем результат в переменную
print(result)                  # → True

if result:
    print("Тест пройден")      # используем результат дальше

>>> Возврат нескольких значений <<<

# Распаковываются по порядку

def get_response():
    return 200, "OK"
code, message = get_response()  # распаковываем в две переменные по порядку
print(code)                     # → 200
print(message)                  # → OK
```

## Переменное количество аргументов
### *args
```python

>>> *args — переменное количество позиционных аргументов <<<

def check_codes(*args):      # * — собирает все аргументы в кортеж
    print(args)

check_codes(200)                   # → (200,)
check_codes(200, 404)              # → (200, 404)
check_codes(200, 404, 500)         # → (200, 404, 500)

>>> *args — перебор внутри функции <<<

def check_codes(*args):
    for code in args:
        print(code)

check_codes(200, 404, 500)
# → 200
# → 404
# → 500
```

### **kwargs
```python

>>> **kwargs — переменное количество именованных аргументов <<<

def check_response(**kwargs):   # ** — собирает все именованные аргументы в словарь
    print(kwargs)

check_response(code=200)                         # → {'code': 200}
check_response(code=200, message="OK")           # → {'code': 200, 'message': 'OK'}
check_response(code=200, message="OK", url="/")  # → {'code': 200, 'message': 'OK', 'url': '/'}

>>> **kwargs — обращение к значениям внутри функции <<<

def check_response(**kwargs):
    print(kwargs['code'])      # → 200
    print(kwargs['message'])   # → OK

check_response(code=200, message="OK")

# *args   — собирает просто значения        → кортеж (200, 404)
# **kwargs — собирает именованные значения  → словарь {'code': 200}
```

## Области видимости
```python

>>> Глобальная область видимости — переменная доступна во всём файле <<<

status_code = 200              # объявлена вне функции — глобальная

def check_code():
    print(status_code)         # функция видит глобальную переменную

check_code()                   # → 200
print(status_code)             # → 200

>>> Локальная область видимости — переменная доступна только внутри функции <<<

def check_code():
    status_code = 200          # объявлена внутри функции — локальная
    print(status_code)         # → 200

check_code()                   # → 200
print(status_code)             # → NameError: name 'status_code' is not defined
```

## Лямбда-функции
```python

# Лямбда-функция — анонимная функция с одним выражением

>>> Сравнение обычной функции vs лямбда - одно и то же <<<

def add(a, b):                 # обычная функция
    return a + b

add = lambda a, b: a + b       # то же самое через лямбду

>>> Как читать лямбду <<<
add = lambda a, b: a + b
#             ↑       ↑
#        аргументы  выражение
#   (что принимает) (что возвращает)

>>> Пример <<<

"""Примеры"""

add = lambda a, b: a + b
print(add(10, 15))  # → 25
print(add(20, 30))  # → 50

# обычная функция — название есть, строк сколько угодно, нужен return
# лямбда         — названия нет,  одна строка,          return не нужен
```

## Функция - тоже объект
```python

# Функцию можно передавать как аргумент

>>> Проблема: как отсортировать список словарей <<<

users = [
    {"name": "Oleg", "age": 32},
    {"name": "Sergey", "age": 24},
    {"name": "Maria", "age": 18},
]

# users.sort()  # ОШИБКА! Python не знает, по какому полю сортировать
```

### Решение: Обычная функция
```python

users = [
    {"name": "Oleg", "age": 32},
    {"name": "Sergey", "age": 24},
    {"name": "Maria", "age": 18},
]

def get_age(user):
    return user["age"]  # Функция возвращает возраст пользователя

users.sort(key=get_age)  # Сортирует по возрасту
print(users)
# Результат: [{'name': 'Maria', 'age': 18}, {'name': 'Sergey', 'age': 24}, {'name': 'Oleg', 'age': 32}]
```

### Решение: Лямбда-функция
```python

users = [
    {"name": "Oleg", "age": 32},
    {"name": "Sergey", "age": 24},
    {"name": "Maria", "age": 18},
]

users.sort(key=lambda user: user["age"])
print(users)
# Результат: [{'name': 'Maria', 'age': 18}, {'name': 'Sergey', 'age': 24}, {'name': 'Oleg', 'age': 32}]
```

### Решение: itemgetter (синтаксический сахар)
```python

from operator import itemgetter

users = [
    {"name": "Oleg", "age": 32},
    {"name": "Sergey", "age": 24},
    {"name": "Maria", "age": 18},
]

users.sort(key=itemgetter("age"))
print(users)
# Результат: [{'name': 'Maria', 'age': 18}, {'name': 'Sergey', 'age': 24}, {'name': 'Oleg', 'age': 32}]
```
