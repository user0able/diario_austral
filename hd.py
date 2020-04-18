import datetime

from PyPDF2 import PdfFileMerger
import requests
import os

os.mkdir('temp')

hoy = datetime.datetime.now()
nombre_archivo_salida = "%s-%s-%s.pdf" % (hoy.year, hoy.month, hoy.day)
pdfs = []
nombres_archivos = []
pdfs_aux = []
ultima_pagina = 0

for i in range(1, 30):
    pdfs.append( # tienes que pegar aquí y reemplazar el numero de la página por %s para que se automatice el proceso
        "https://impresa.soy-chile.cl/AustralValdivia/170420/Paginas/ee1a36622e05/AustralValdivia/17_04_20_pag_%s.pdf" %
        (str(i) if i >= 10 else '0' + str(i))
    )

for y in pdfs:
    url = requests.get(y)
    if url.status_code == 200:
        print("testeando: " + y)
        nombre_temporal_archivo = open('temp/metadata_%s' % y[-10:], 'wb').write(url.content)
        pdfs_aux.append('temp/metadata_%s' % y[-10:])
    else:
        break

print(pdfs_aux)
fusionador = PdfFileMerger()

for pdf in pdfs_aux:
    fusionador.append(open(pdf, 'rb'))

with open(nombre_archivo_salida, 'wb') as salida:
    fusionador.write(salida)

os.rmdir("/temp/")
