# virtualenv -p /usr/bin/python3.7 /Users/user0able/.virtualenvs/modulesEnv/bin/python3
import datetime

from PyPDF2 import PdfFileMerger
import requests
from bs4 import BeautifulSoup

pdfs = []
nombres_archivos = []
pdfs_aux = []
ultima_pagina = 0


def getFecha(
        dias=0):  # cantidad de días hacia atrás que buscará el diario :3 / está en 0, porque lo buscará para hoy we :)
    hoy = datetime.date.today()
    cantidad_dias_restar = datetime.timedelta(days=dias)
    dia_pasado = hoy - cantidad_dias_restar
    print("fecha elegida: ", dia_pasado)
    return dia_pasado


def agrega_ceros_izquierda(numero):
    return str(numero) if numero >= 10 else "0" + str(numero)


def genera_url_fecha(fecha=getFecha()):
    url = requests.get("https://www.australvaldivia.cl/impresa/%s/%s/%s/full/cuerpo-principal/1/" %
                       (
                           fecha.year,
                           agrega_ceros_izquierda(fecha.month),
                           agrega_ceros_izquierda(fecha.day)
                       )
                       )
    return url


url = genera_url_fecha()

soup = BeautifulSoup(url.content, 'html.parser')
links = []
soup.find_all("section")
temp_link = ''
for link in soup.find_all("section"):
    temp_link = link.get("data-page")
    if temp_link:
        break

for numero in range(1, 50):
    # print(numero, )
    test_link = temp_link.replace("01.pdf", agrega_ceros_izquierda(numero) + ".pdf")
    if requests.get(test_link).status_code == 200:
        pdfs.append(test_link)  # añade el nombre del pdf a la lista "pdfs"
        nombre_temporal_archivo = open('temp/metadata_%s' % test_link[-10:], 'wb').write(
            requests.get(test_link).content)
    else:
        print("hasta la vista beibi")
        ultima_pagina = numero
        break

print(pdfs)

pdfs_locales = []
for n in range(1, ultima_pagina):
    pdfs_locales.append('temp/metadata_pag_%s.pdf' % agrega_ceros_izquierda(n))

print(pdfs_locales)
fusionador = PdfFileMerger()

for pdf in pdfs_locales:
    fusionador.append(open(pdf, 'rb'))

nombre_archivo_salida = "%s-%s-%s.pdf" % (
    agrega_ceros_izquierda(getFecha().year),
    agrega_ceros_izquierda(getFecha().month),
    agrega_ceros_izquierda(getFecha().day),
)

with open(nombre_archivo_salida, 'wb') as salida:
    fusionador.write(salida)
