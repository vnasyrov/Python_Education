from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = PROJECT_DIR / "resources"
FILES_DIR = RESOURCES_DIR / "tmp"
ZIP_DIR = RESOURCES_DIR / "zip"

files = [FILES_DIR / "1mb.csv", FILES_DIR / "1mb.pdf", FILES_DIR / "1mb.xlsx"]

def create_zip():
    if not ZIP_DIR.exists():
        ZIP_DIR.mkdir()
    with ZipFile(ZIP_DIR / "results.zip", "w", compression=ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, arcname=file.name)

create_zip()