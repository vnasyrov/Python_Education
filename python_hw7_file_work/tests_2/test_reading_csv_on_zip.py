import csv  # Инструменты для чтения CSV-файлов
from io import TextIOWrapper  # Преобразует байты в текст
from zipfile import ZipFile  # Позволяет открывать ZIP-архив и читать файлы внутри него

from tests_2.created_zip import ZIP_DIR, create_zip

def test_csv():  # Pytest распознаёт тест по префиксу test_
    create_zip()  # Создаём ZIP-архив с файлами

    archive_path = ZIP_DIR / "results.zip"  # Сохраняем путь к архиву в переменную

    # with ... as ... — открывает ресурс, даёт доступ через переменную,
    # а после завершения блока автоматически закрывает его

    with ZipFile(archive_path) as archive:  # Открываем ZIP как archive
        with archive.open("1mb.csv") as binary_file:  # Открываем CSV как поток байтов
            with TextIOWrapper(
                binary_file,
                encoding="utf-8-sig",  # Преобразуем байты в текст и убираем BOM
                newline="",  # Оставляем обработку переносов строк модулю csv
            ) as text_file:  # Получаем текстовую версию файла
                users = list(
                    csv.DictReader(
                        text_file,
                        delimiter=",",  # Столбцы в этом CSV разделены запятыми
                    )
                )  # Получаем список словарей: один словарь на строку CSV

    assert users[0]["ID"] == "1"  # Проверяем ID первой строки данных