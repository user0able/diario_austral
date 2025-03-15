import os
import datetime

from PyPDF2 import PdfReader, PdfMerger, PdfWriter, PageObject


def getFecha():
    return datetime.datetime.now().date()


def pdfReader():
    reader = PdfReader("example.pdf")
    page = reader.pages[0]
    text = page.extract_text()
    text = str(text).strip()
    print(text)
    return text


def pdfCreate():
    new_pdf = PdfWriter()
    page = PageObject.create_blank_page(width=100, height=100)
    new_pdf.add_page(page)
    new_pdf.write("new_pdf.pdf")
    print("PDF creado")


def pdfMerger():
    merger = PdfMerger()
    merger.append("example.pdf")
    merger.append("new_pdf.pdf")
    merger.write("merged.pdf")
    merger.close()
    print("PDFs unidos")


def cleanTempFiles():
    temp_directory = "temp"
    if os.path.exists(temp_directory):
        os.rmdir(temp_directory)
    os.mkdir(temp_directory)
    print("Directorio temporal creado")


def main():
    pass


getFecha()
pdfReader()
pdfCreate()
pdfMerger()
cleanTempFiles()
