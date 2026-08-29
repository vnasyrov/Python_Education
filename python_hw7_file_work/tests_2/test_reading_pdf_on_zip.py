from io import BytesIO  # Позволяет работать с байтами как с обычным файлом в памяти
from zipfile import ZipFile  # Позволяет открывать ZIP-архив и читать файлы внутри него
from pypdf import PdfReader  # Открывает PDF и позволяет извлекать текст со страниц

from tests_2.created_zip import ZIP_DIR, create_zip


def test_pdf():
    create_zip()

    archive_path = ZIP_DIR / "results.zip"  # Сохраняем путь к архиву в переменную

    # with ... as ... — открывает ресурс, даёт доступ через переменную,
    # а после завершения блока автоматически закрывает его

    with ZipFile(archive_path) as archive:
        pdf_bytes = archive.read("1mb.pdf")  # Читаем PDF из архива как байты
        pdf_file = BytesIO(pdf_bytes)  # Представляем байты как файл в памяти
        pdf_reader = PdfReader(pdf_file)  # Передаём PDF специальному парсеру

        content = "\n".join(
            page.extract_text() or "" for page in pdf_reader.pages
        )  # Извлекаем и объединяем текст всех страниц

    assert "About PDF Format" in content