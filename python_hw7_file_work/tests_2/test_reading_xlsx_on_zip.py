from io import BytesIO  # Позволяет работать с байтами как с файлом в памяти
from zipfile import ZipFile  # Позволяет открывать ZIP-архивы и читать файлы внутри
from openpyxl import load_workbook  # Позволяет открывать и читать Excel-файлы

from tests_2.created_zip import ZIP_DIR, create_zip

def test_xlsx():
    create_zip()

    archive_path = ZIP_DIR / "results.zip"  # Сохраняем путь к архиву в переменную

    # with ... as ... — открывает ресурс, даёт доступ через переменную,
    # а после завершения блока автоматически закрывает его

    with ZipFile(archive_path) as archive:  # Открываем ZIP как archive
        xlsx_bytes = archive.read("1mb.xlsx")  # Читаем XLSX из архива как байты
        xlsx_file = BytesIO(xlsx_bytes)  # Представляем байты как файл в памяти

        workbook = load_workbook(
            xlsx_file,
            data_only=True,
        )  # Открываем Excel; для формул читаем сохранённые результаты

        sheet = workbook.active  # Получаем активный лист Excel-книги

        actual_name = sheet.cell(
            row=2,
            column=1,
        ).value  # Читаем значение ячейки A2 и сохраняем в actual_name

        workbook.close()  # Закрываем ресурсы Excel-книги

    assert actual_name == "Austen Russel"  # Проверяем значение ячейки A2