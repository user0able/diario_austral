# virtualenv -p /usr/bin/python3.7 /Users/user0able/.virtualenvs/modulesEnv/bin/python3
import datetime

from PyPDF2 import PdfFileMerger
import requests
import os


def agrega_ceros_izquierda(numero):
    return str(numero) if numero >= 10 else "0" + str(numero)


hoy = datetime.datetime.now()
nombre_archivo_salida = "%s-%s-%s.pdf" % (
    hoy.year, agrega_ceros_izquierda(hoy.month), agrega_ceros_izquierda(hoy.day))
pdfs = []
nombres_archivos = []
pdfs_aux = []
ultima_pagina = 0

for i in range(1, 30):
    pdfs.append(  # tienes que pegar aquí y reemplazar el numero de la página por %s para que se automatice el proceso
        "https://impresa.soy-chile.cl/AustralValdivia/240420/Paginas/f3bebad7a203/AustralValdivia/24_04_20_pag_%s.pdf" %
        agrega_ceros_izquierda(i)
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
