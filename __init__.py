import datetime
from PyPDF2 import PdfReader, PdfMerger, PdfWriter, PageObject


def getFecha():
    return datetime.datetime.now().date()


def pdfReader():
    reader = PdfReader("example.pdf")
    page = reader.pages[0]
    text = page.extract_text()
    text = str(text).strip()
    return text


def pdfCreate():
    new_pdf = PdfWriter()
    page = PageObject.create_blank_page(width=100, height=100)
    new_pdf.add_page(page)
    new_pdf.write("new_pdf.pdf")


def pdfMerger():
    merger = PdfMerger()
    merger.append("example.pdf")
    merger.append("new_pdf.pdf")
    merger.write("merged.pdf")
    merger.close()


print(getFecha())
print(pdfReader())
pdfCreate()
pdfMerger()
