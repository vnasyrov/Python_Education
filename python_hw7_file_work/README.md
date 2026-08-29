# Работа с файлами в Python
Файл — это данные, сохранённые на диске. В автотестах мы часто скачиваем файлы, читаем отчёты, проверяем CSV/XLSX/PDF и собираем несколько файлов в ZIP-архив.

Главное правило: путь говорит Python, **где лежит файл**, а режим открытия — **что с ним нужно сделать**.

# Пути к файлам

## Относительный и абсолютный путь
```python

# Относительный путь — считается от текущей рабочей директории
file_path = "resources/users.csv"

# Абсолютный путь — полный адрес файла в системе
# Windows: C:\\Users\\ivan\\project\\resources\\users.csv
# macOS/Linux: /Users/ivan/project/resources/users.csv
```

Относительный путь короче, но тест может запускаться из другой директории. Поэтому надёжнее строить путь от расположения самого Python-файла.

## pathlib — удобная работа с путями
Представим, что проект устроен так:

```text
qaguru_python21_hw7/
├── resources/
│   └── users.csv
└── tests/
    └── test_users.py
```

Код ниже находится в `tests/test_users.py`, а найти нужно `resources/users.csv`.

### Разбираем путь по шагам
```python
from pathlib import Path  # Импортируем класс Path из встроенного модуля pathlib

# Допустим, __file__ содержит путь к запущенному тесту:
# tests/test_users.py

current_file = Path(__file__)
# Результат: Path('tests/test_users.py')

absolute_file = current_file.resolve()
# macOS/Linux: Path('/Users/ivan/qaguru_python21_hw7/tests/test_users.py')
# Windows:     Path('C:/Users/ivan/qaguru_python21_hw7/tests/test_users.py')

tests_dir = absolute_file.parent
# Результат: Path('/Users/ivan/qaguru_python21_hw7/tests')

project_dir = tests_dir.parent
# Результат: Path('/Users/ivan/qaguru_python21_hw7')

resources_dir = project_dir / "resources"
# Результат: Path('/Users/ivan/qaguru_python21_hw7/resources')

users_file = resources_dir / "users.csv"
# Результат: Path('/Users/ivan/qaguru_python21_hw7/resources/users.csv')

print(users_file)
```

Каждый вызов `.parent` поднимает путь на один уровень вверх:

```python
path = Path("/project/tests/test_users.py")

path                 # /project/tests/test_users.py — сам файл
path.parent          # /project/tests               — папка tests
path.parent.parent   # /project                     — корень проекта
```

### Та же запись короче
```python
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
# Path(__file__) — создаём объект пути к test_users.py
# resolve() — делаем путь абсолютным
# первый parent — поднимаемся из test_users.py в tests
# второй parent — поднимаемся из tests в корень проекта

RESOURCES_DIR = PROJECT_DIR / "resources"  # Заходим в папку resources
FILE_PATH = RESOURCES_DIR / "users.csv"    # Указываем файл users.csv

print(FILE_PATH)
# /Users/ivan/qaguru_python21_hw7/resources/users.csv
```

Оператор `/` у объекта `Path` соединяет части пути. Здесь это не математическое деление:

```python
from pathlib import Path

project_dir = Path("/Users/ivan/project")

resources_dir = project_dir / "resources"
# /Users/ivan/project/resources

file_path = project_dir / "resources" / "users.csv"
# /Users/ivan/project/resources/users.csv
```

Python сам использует правильный разделитель для текущей операционной системы, поэтому не нужно вручную добавлять `/` или `\\`.

### Создание пути не создаёт файл
```python
from pathlib import Path

file_path = Path("reports/result.txt")

print(file_path)          # reports/result.txt
print(file_path.exists()) # False, если такого файла пока нет на диске

# Создаём отсутствующую папку reports
file_path.parent.mkdir(parents=True, exist_ok=True)

# Только эта строка действительно создаёт файл и записывает в него текст
file_path.write_text("Тест пройден", encoding="utf-8")

print(file_path.exists()) # True
```

`Path(...)` только описывает адрес. Файл появляется после `write_text()`, `write_bytes()` или открытия в режиме записи.

### Путь от рабочей директории и путь от файла
```python
from pathlib import Path

print(Path.cwd())
# Папка, ИЗ КОТОРОЙ запустили pytest. Она может меняться.

print(Path(__file__).resolve().parent)
# Папка, В КОТОРОЙ лежит текущий .py-файл. Она не зависит от места запуска.
```

В автотестах путь от `__file__` часто надёжнее: тест найдёт ресурс, даже если `pytest` запустили из IDE, терминала или CI.

## Полезные методы Path
```python
from pathlib import Path

path = Path("resources/users.csv")  # Пока это только объект пути: файл не создаётся

path.exists()       # существует ли путь
path.is_file()      # это файл?
path.is_dir()       # это директория?
path.name           # 'users.csv'
path.stem           # 'users'
path.suffix         # '.csv'
path.parent         # Path('resources')

path.parent.mkdir(parents=True, exist_ok=True)  # Создаём папку resources, если её нет
# parents=True — создать и недостающие родительские папки
# exist_ok=True — не падать, если папка уже существует
```

## os.path — альтернативный способ
```python
import os  # Встроенный модуль: отдельно устанавливать не нужно

CURRENT_FILE = os.path.abspath(__file__)  # Полный путь к текущему .py-файлу
CURRENT_DIR = os.path.dirname(CURRENT_FILE)  # Отбрасываем имя файла, оставляем папку
FILE_PATH = os.path.join(CURRENT_DIR, "resources", "users.csv")  # Соединяем части пути
```

`os.path` встречается в существующих проектах, но в новом коде обычно проще использовать `pathlib`.

# open и контекстный менеджер

## Почему нужен with
```python
with open("example.txt", "r", encoding="utf-8") as file:
    # open(...) открывает файл; as file сохраняет файловый объект в переменную file
    # "r" означает режим чтения, encoding задаёт способ преобразования байтов в текст
    content = file.read()  # Читаем всё содержимое файла в одну строку

# Здесь файл уже закрыт автоматически — даже если внутри блока произошла ошибка
```

`with` — контекстный менеджер. Он берёт на себя закрытие файла. Без него пришлось бы вызывать `file.close()` вручную.

## Режимы открытия файла
```python
# r  — read: прочитать; файл должен существовать
# w  — write: записать; старое содержимое будет удалено
# a  — append: дописать в конец
# x  — создать новый; если файл уже есть, будет FileExistsError
# b  — binary: бинарный режим для PDF, ZIP, картинок и других байтов
# t  — text: текстовый режим, используется по умолчанию

open("notes.txt", "r")   # чтение текста
open("notes.txt", "w")   # запись текста
open("notes.txt", "a")   # добавление текста
open("report.pdf", "rb") # чтение байтов
open("copy.pdf", "wb")   # запись байтов
```

Важно: режим `w` полностью перезаписывает существующий файл. Если старые данные нужны, используем `a`.

## encoding — кодировка текста
```python
with open("example.txt", "r", encoding="utf-8") as file:
    content = file.read()
```

Для текстовых файлов лучше явно указывать `encoding="utf-8"`. Иначе результат может зависеть от операционной системы, а русские буквы могут прочитаться с ошибкой.

# TXT-файлы

## Запись текста
```python
from pathlib import Path

file_path = Path("tmp/example.txt")  # Описываем путь tmp/example.txt
file_path.parent.mkdir(parents=True, exist_ok=True)  # Создаём только папку tmp

with file_path.open("w", encoding="utf-8") as file:
    # Если example.txt не существует — он будет создан
    # Если существует — режим "w" сначала очистит его
    file.write("Первый автотест\n")  # \n переводит курсор на новую строку
    file.write("Второй автотест\n")  # write() возвращает число записанных символов
```

`write()` не добавляет перенос строки автоматически, поэтому `\n` нужно указывать самостоятельно.

## Чтение всего файла
```python
from pathlib import Path

file_path = Path("tmp/example.txt")

with file_path.open("r", encoding="utf-8") as file:
    content = file.read()

assert "Первый автотест" in content
```

## Чтение построчно
```python
with open("tmp/example.txt", encoding="utf-8") as file:
    for line in file:          # На каждой итерации получаем одну строку файла
        print(line.strip())    # Убираем пробелы и \n по краям, затем печатаем

# strip() убирает \n и пробелы по краям строки
```

## read, readline и readlines
```python
with open("tmp/example.txt", encoding="utf-8") as file:
    file.read()       # весь файл одной строкой
    file.readline()   # одна следующая строка
    file.readlines()  # список всех оставшихся строк
```

После чтения курсор находится в конце файла. Поэтому три вызова подряд не прочитают файл трижды. Для повторного чтения нужно заново открыть файл или вызвать `file.seek(0)`.

# Скачивание файлов в UI-тестах

## Настройка директории скачивания в Selene
```python
from pathlib import Path  # Нужен для независимых от ОС путей

from selenium import webdriver  # Даёт доступ к настройкам браузера Chrome
from selene import browser       # Объект для управления браузером через Selene

DOWNLOADS_DIR = Path(__file__).resolve().parent / "downloads"  # Папка рядом с тестом
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)  # Chrome ожидает существующую папку

options = webdriver.ChromeOptions()  # Создаём контейнер с настройками Chrome
options.add_experimental_option("prefs", {
    # Браузеру нужна строка с абсолютным путём
    "download.default_directory": str(DOWNLOADS_DIR.resolve()),
    # str(...) нужен, потому что Chrome не понимает объект Path — ему нужна строка
    "download.prompt_for_download": False,  # Не показывать окно «Куда сохранить?»
})

browser.config.driver_options = options  # Передаём подготовленные настройки в Selene
```

Для современных версий Selene отдельно устанавливать `webdriver_manager` обычно не требуется: Selenium Manager управляет драйвером сам.

## Проверка скачанного файла
```python
from pathlib import Path
from time import monotonic, sleep  # monotonic — таймер; sleep — короткая пауза


def wait_for_file(path: Path, timeout: float = 10) -> Path:
    # path: Path и -> Path — подсказки типов, Python сам их не проверяет
    # timeout=10 — значение по умолчанию, его можно заменить при вызове функции
    end_time = monotonic() + timeout  # Запоминаем момент, когда ожидание закончится

    while monotonic() < end_time:  # Повторяем проверку, пока не истёк таймаут
        if path.exists() and path.stat().st_size > 0:
            # exists() — файл появился; st_size > 0 — в нём уже есть данные
            return path  # Сразу завершаем функцию и возвращаем найденный путь
        sleep(0.1)  # Не нагружаем процессор непрерывными проверками

    # Сюда дойдём только после таймаута; raise вручную создаёт ошибку теста
    raise AssertionError(f"Файл не скачался за {timeout} секунд: {path}")


downloaded_file = wait_for_file(DOWNLOADS_DIR / "report.txt")  # Ждём и получаем Path
assert "Success" in downloaded_file.read_text(encoding="utf-8")
```

Фиксированный `sleep(5)` делает тест медленным и нестабильным: иногда файл готов раньше, иногда позже. Лучше ждать конкретное условие с таймаутом.

## Скачивание через requests
```python
from pathlib import Path

import requests  # Сторонняя библиотека для HTTP-запросов

url = "https://example.com/report.pdf"
file_path = Path("downloads/report.pdf")
file_path.parent.mkdir(parents=True, exist_ok=True)

response = requests.get(url, timeout=15)  # Выполняем GET-запрос; ждём не более 15 секунд
response.raise_for_status()  # ошибка, если сервер вернул 4xx или 5xx
file_path.write_bytes(response.content)  # content — тело ответа в виде байтов

assert file_path.exists()              # Проверяем, что файл создался
assert file_path.stat().st_size > 0    # Проверяем, что он не пустой
```

`response.content` содержит байты, поэтому используем `write_bytes()` или режим `wb`.

# CSV-файлы
CSV — текстовая таблица. Одна строка файла обычно соответствует строке таблицы, а значения разделены запятой, точкой с запятой или другим символом.

## Чтение CSV как списка
```python
import csv  # Встроенный модуль для чтения и записи табличных CSV-файлов

with open("resources/users.csv", encoding="utf-8-sig", newline="") as file:
    # newline="" позволяет модулю csv самому правильно обрабатывать переносы строк
    # delimiter=";" сообщает, что колонки в этом файле разделены точкой с запятой
    # csv.reader создаёт перебираемый reader, а list(...) сразу читает все строки
    rows = list(csv.reader(file, delimiter=";"))

assert rows[1][0] == "1"       # вторая строка, первый столбец
assert rows[1][1] == "Иван"    # вторая строка, второй столбец
```

Индексы начинаются с нуля: `rows[1][0]` — вторая строка и первый столбец. `utf-8-sig` полезен для CSV, сохранённых Excel с BOM.

## DictReader — обращение по названию колонки
```python
import csv

with open("resources/users.csv", encoding="utf-8-sig", newline="") as file:
    # DictReader берёт названия колонок из первой строки файла
    # Каждую следующую строку он превращает в словарь вида {"Username": "ivan", ...}
    users = list(csv.DictReader(file, delimiter=";"))

assert users[0]["Username"] == "ivan"
assert users[0]["Email"] == "ivan@example.com"
```

`DictReader` обычно понятнее индексов: первая строка CSV становится названиями ключей словаря.

## Частая ошибка с разделителем
```python
# Файл: id;name;email

csv.reader(file)                # по умолчанию ждёт запятую — строка может стать одной колонкой
csv.reader(file, delimiter=";") # правильно для этого файла
```

# XLSX-файлы
Для формата `.xlsx` используется сторонняя библиотека `openpyxl`:

```bash
pip install openpyxl
```

## Чтение ячеек
```python
from openpyxl import load_workbook  # Функция для открытия существующего XLSX-файла

workbook = load_workbook("resources/users.xlsx", data_only=True)  # Открываем книгу
sheet = workbook.active  # Берём активный лист — тот, который был выбран при сохранении

assert sheet.cell(row=2, column=1).value == 1  # Ячейка A2 через номера строки/столбца
assert sheet["B2"].value == "Иван"            # Та же идея через адрес ячейки

workbook.close()  # Освобождаем открытый файл
```

В `openpyxl` номера строк и столбцов начинаются с **1**, а не с 0. `data_only=True` возвращает сохранённый результат формулы вместо текста самой формулы.

## Перебор строк
```python
from openpyxl import load_workbook

workbook = load_workbook(
    "resources/users.xlsx",
    read_only=True,  # Читаем без редактирования и тратим меньше памяти
    data_only=True,  # Получаем результат формулы, а не строку вроде "=A1+B1"
)
sheet = workbook.active

# iter_rows перебирает строки листа; values_only=True возвращает простые значения
# list(...) загружает все полученные строки в память в виде списка кортежей
rows = list(sheet.iter_rows(values_only=True))

assert rows[0] == ("id", "name", "email")
assert rows[1][1] == "Иван"

workbook.close()
```

`values_only=True` возвращает значения ячеек, а не объекты `Cell`. Для больших файлов полезен `read_only=True`.

Формат `.xls` старее `.xlsx`; для него может понадобиться библиотека `xlrd`. Это разные форматы, несмотря на похожие расширения.

# PDF-файлы
Для чтения PDF используется сторонняя библиотека `pypdf`:

```bash
pip install pypdf
```

## Количество страниц и текст
```python
from pypdf import PdfReader  # Класс для чтения структуры и текста PDF

reader = PdfReader("resources/report.pdf")  # Открываем PDF и разбираем его структуру

assert len(reader.pages) == 2  # pages — коллекция страниц; len() возвращает их число

first_page_text = reader.pages[0].extract_text() or ""
# pages[0] — первая страница; extract_text() пытается достать из неё текст
# or "" подставит пустую строку, если extract_text() вернёт None
assert "Отчёт о тестировании" in first_page_text
```

Страницы, как элементы списка, нумеруются с 0. Первая страница — `pages[0]`.

## Текст со всех страниц
```python
from pypdf import PdfReader

reader = PdfReader("resources/report.pdf")

# Выражение справа по очереди извлекает текст каждой страницы
# join соединяет полученные строки, вставляя между страницами перенос \n
full_text = "\n".join(page.extract_text() or "" for page in reader.pages)

assert "Passed: 10" in full_text
```

`extract_text()` не распознаёт текст на сканах-картинках. Для таких PDF потребуется OCR. Метод также может вернуть `None`, поэтому добавляем `or ""`.

# ZIP-архивы
Модуль `zipfile` встроен в Python — устанавливать его не нужно.

## Список файлов внутри архива
```python
from zipfile import ZipFile  # Встроенный класс для открытия ZIP-архивов

with ZipFile("resources/archive.zip") as archive:
    # namelist() возвращает список полных имён всех файлов внутри архива
    file_names = archive.namelist()

assert "users.csv" in file_names
assert "report.pdf" in file_names
```

Важно: внутри ZIP пути всегда записываются относительно архива. Файл может называться не `users.csv`, а `data/users.csv`.

## Чтение TXT прямо из ZIP
```python
from zipfile import ZipFile

with ZipFile("resources/archive.zip") as archive:
    # read() возвращает байты файла без распаковки на диск
    # decode("utf-8") превращает эти байты в обычную строку Python
    content = archive.read("result.txt").decode("utf-8")

assert "SUCCESS" in content
```

`archive.read()` возвращает байты. Для текста их нужно декодировать, а PDF и картинки оставляем байтами.

## Чтение CSV прямо из ZIP
```python
import csv
from io import TextIOWrapper  # Оборачивает бинарный поток и превращает его в текстовый
from zipfile import ZipFile

with ZipFile("resources/archive.zip") as archive:
    # ZIP хранит данные как байты, поэтому сначала получаем бинарный поток
    with archive.open("users.csv") as binary_file:
        # Модуль csv работает с текстом: TextIOWrapper выполняет преобразование
        with TextIOWrapper(binary_file, encoding="utf-8-sig", newline="") as text_file:
            users = list(csv.DictReader(text_file, delimiter=";"))  # Читаем строки-словари

assert users[0]["Username"] == "ivan"
```

`archive.open()` отдаёт бинарный поток. `TextIOWrapper` превращает его в текстовый, понятный модулю `csv`.

## Создание ZIP-архива
```python
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
# ZIP_DEFLATED — алгоритм сжатия; ZipFile — класс для работы с архивом

files = [Path("tmp/result.txt"), Path("tmp/users.csv")]  # Что положим в архив

with ZipFile("tmp/results.zip", "w", compression=ZIP_DEFLATED) as archive:
    # "w" создаёт новый архив или перезаписывает существующий
    for file_path in files:  # По очереди берём каждый путь из списка files
        # arcname оставляет внутри ZIP только имя файла, без исходных папок tmp/...
        archive.write(file_path, arcname=file_path.name)
```

`arcname` задаёт имя файла внутри архива. Без него в ZIP может попасть лишняя часть исходного пути.

# Временные файлы в pytest

## Фикстура tmp_path
```python
def test_text_file(tmp_path):
    # tmp_path не нужно создавать самостоятельно — эту фикстуру передаёт pytest
    # Для каждого теста pytest создаёт отдельную временную директорию
    file_path = tmp_path / "result.txt"  # Указываем файл внутри временной папки
    file_path.write_text("SUCCESS", encoding="utf-8")  # Создаём и заполняем файл

    assert file_path.exists()  # Тест упадёт, если файл не создался
    assert file_path.read_text(encoding="utf-8") == "SUCCESS"  # Проверяем содержимое
```

`tmp_path` уже является объектом `Path`. Это хороший выбор для тестов: файлы одного запуска не смешиваются с файлами другого, а проект не засоряется результатами.

# Удаление файлов и директорий

## Удаление через pathlib
```python
from pathlib import Path

file_path = Path("tmp/result.txt")  # Путь к файлу, который хотим удалить
empty_dir = Path("tmp/empty")       # Путь к пустой папке

if file_path.exists():   # Проверка защищает от FileNotFoundError
    file_path.unlink()  # удалить файл

if empty_dir.exists():   # rmdir сработает, только если директория пустая
    empty_dir.rmdir()   # удалить только пустую директорию
```

## Удаление директории со всем содержимым
```python
import shutil
from pathlib import Path

directory = Path("tmp/downloads")  # Сначала точно задаём безопасную целевую папку

if directory.exists():             # Не вызываем удаление для несуществующего пути
    shutil.rmtree(directory)        # Рекурсивно удаляем папку и всё внутри неё
```

`shutil.rmtree()` удаляет всю директорию без возможности восстановления. В тестах сначала проверяем, что путь указывает именно на подготовленную временную папку, а не на директорию проекта или пользователя.

# Пример файлового автотеста
```python
import csv  # Понадобится для разбора results.csv
from io import TextIOWrapper  # Превратит байты из ZIP в текст
from zipfile import ZipFile   # Откроет скачанный архив


def test_downloaded_archive(downloads_dir):
    # downloads_dir предполагается фикстурой, которая возвращает объект Path
    archive_path = downloads_dir / "test-results.zip"  # Ожидаемый путь к архиву

    # Текст после запятой pytest покажет при падении проверки
    assert archive_path.exists(), "Архив не скачался"
    assert archive_path.stat().st_size > 0, "Архив пустой"

    with ZipFile(archive_path) as archive:  # Архив закроется автоматически после блока
        assert "results.csv" in archive.namelist()  # Проверяем состав архива

        # Открываем вложенный CSV прямо в архиве, не извлекая его на диск
        with archive.open("results.csv") as binary_file:
            with TextIOWrapper(binary_file, encoding="utf-8-sig") as text_file:
                rows = list(csv.DictReader(text_file))  # Каждая строка станет словарём

    assert len(rows) == 3                   # В CSV должно быть три строки данных
    assert rows[0]["status"] == "passed"   # У первой строки ожидаем нужный статус
```

Логика проверки идёт от общего к частному:

1. Файл появился.
2. Файл не пустой.
3. ZIP действительно открывается.
4. Внутри есть нужный файл.
5. Содержимое файла соответствует ожиданиям.

# Частые ошибки
```python
# 1. Режим w случайно уничтожает старое содержимое
open("result.txt", "w")

# 2. Забыли кодировку — проблема может проявиться только на другой ОС
open("result.txt")

# 3. Склеили путь строками — разделители отличаются в разных ОС
file_path = directory + "/" + file_name

# Лучше
file_path = Path(directory) / file_name

# 4. Перепутали текст и байты
file.write(response.content)       # ошибка, если файл открыт как 'w'
file.write(response.content.decode("utf-8"))  # текст

# 5. Проверили файл до окончания скачивания
assert downloaded_file.exists()   # может быть слишком рано

# 6. Перепутали индексы
rows[0]              # первая строка CSV
reader.pages[0]      # первая страница PDF
sheet.cell(row=1, column=1)  # первая ячейка XLSX
```

# Короткая памятка
```python
from pathlib import Path

path = Path("tmp/result.txt")

path.exists()                         # проверить существование
path.read_text(encoding="utf-8")      # прочитать текст
path.write_text("OK", encoding="utf-8")  # записать текст
path.read_bytes()                      # прочитать байты
path.write_bytes(b"OK")               # записать байты
path.stat().st_size                    # размер файла в байтах
path.unlink()                          # удалить файл
```

Для TXT используем `open` или методы `Path`, для CSV — `csv`, для XLSX — `openpyxl`, для PDF — `pypdf`, для ZIP — `zipfile`. Почти всегда открываем ресурсы через `with`, явно задаём кодировку текста и строим пути через `pathlib`.
