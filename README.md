# Python Education

Учебный монорепозиторий с домашними работами по Python и автоматизации тестирования.

Каждая домашняя работа находится в отдельной директории, сохраняет исходное название и остаётся самостоятельным мини-проектом со своим кодом, материалами и зависимостями.

> Один курс — один аккуратный репозиторий. Нужный урок легко найти по номеру домашней работы.

## Домашние работы

| № | Директория | Тема |
|---:|---|---|
| 1 | [`python_hw1_introductory_lesson`](https://github.com/vnasyrov/Python_Education/tree/main/python_hw1_introductory_lesson) | Вводное занятие: первый UI-тест с Playwright |
| 2 | [`python_hw2_git`](https://github.com/vnasyrov/Python_Education/tree/main/python_hw2_git) | Git и GitHub: первый тест с Selene |
| 3 | [`python_hw3_tools_and_libraries`](https://github.com/vnasyrov/Python_Education/tree/main/python_hw3_tools_and_libraries) | Инструменты и библиотеки: pytest, фикстуры и Selene |
| 4 | [`python_hw4_python_basics1`](https://github.com/vnasyrov/Python_Education/tree/main/python_hw4_python_basics1) | Основы Python I: типы данных, коллекции и изменяемость |
| 5 | [`python_hw5_selene_basics`](https://github.com/vnasyrov/Python_Education/tree/main/python_hw5_selene_basics) | Selene: поиск элементов и автоматизация формы DemoQA |
| 6 | [`python_hw6_python_basics2`](https://github.com/vnasyrov/Python_Education/tree/main/python_hw6_python_basics2) | Основы Python II: условия, циклы и функции |
| 7 | [`python_hw7_file_work`](https://github.com/vnasyrov/Python_Education/tree/main/python_hw7_file_work) | Работа с файлами: CSV, XLSX, PDF и ZIP |
| 8 | [`python_hw8_python_basics3`](https://github.com/vnasyrov/Python_Education/tree/main/python_hw8_python_basics3) | Основы Python III: ООП, `Product`, `Cart` и pytest |

## Структура репозитория

```text
Python_Education/
├── python_hw1_introductory_lesson/
├── python_hw2_git/
├── python_hw3_tools_and_libraries/
├── python_hw4_python_basics1/
├── python_hw5_selene_basics/
├── python_hw6_python_basics2/
├── python_hw7_file_work/
├── python_hw8_python_basics3/
├── .gitignore
└── README.md
```

Внутри каждой директории находятся файлы конкретного урока:

- исходный код и тесты;
- собственный `requirements.txt`;
- учебные ресурсы;
- README или конспект, если он был в исходном проекте.

## Как начать работу

Клонировать весь учебный репозиторий:

```bash
git clone https://github.com/vnasyrov/Python_Education.git
cd Python_Education
```

Создать и активировать виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate
```

Для Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Установить зависимости нужной домашней работы:

```bash
pip install -r python_hw8_python_basics3/requirements.txt
```

Запустить её тесты:

```bash
pytest python_hw8_python_basics3
```

Путь можно заменить на директорию любого другого урока.

## Принцип организации

```text
корень репозитория
        │
        ├── общее оглавление и навигация
        │
        └── отдельная директория для каждой домашней работы
                ├── свой код
                ├── свои тесты
                ├── свои ресурсы
                └── свои зависимости
```

Такой формат позволяет:

- видеть весь учебный путь в одном месте;
- не смешивать задания разных уроков;
- переходить к нужной работе прямо из таблицы;
- использовать один Git-репозиторий вместо множества отдельных;
- добавлять следующие работы по тому же шаблону.

## Как добавить следующую домашнюю работу

1. Создать директорию с номером и названием урока, например `python_hw9_new_topic`.
2. Поместить внутрь код, тесты, ресурсы и `requirements.txt`.
3. Добавить новую строку в таблицу [«Домашние работы»](#домашние-работы).
4. Зафиксировать изменения одним понятным коммитом.

```bash
git add python_hw9_new_topic README.md
git commit -m "feat: add homework 9"
```
