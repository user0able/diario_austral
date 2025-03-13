import datetime
import img2pdf
import requests
from bs4 import BeautifulSoup
from os import remove

"""

This is the "example" module.

The example module supplies one function, factorial().  For example,

>>> factorial(5)
120
"""


def getFecha(dias=0):
    hoy = datetime.date.today()
    print(hoy)
    cantidad_dias_restar = datetime.timedelta(days=dias)
    print(cantidad_dias_restar)
    dia_pasado = hoy - cantidad_dias_restar
    return dia_pasado


fecha = getFecha()


def genera_url():
    print("fecha de la busqueda:")

    temp = requests.get(
        url="https://www.australvaldivia.cl/impresa/%s/%s/%s/papel/"
        % (
            fecha.year,
            fecha.month,
            fecha.day if fecha.day >= 9 else "0" + str(fecha.day),
        )
    )
    print("temp =", temp)
    soup = BeautifulSoup(temp.content, "html.parser")
    soup = soup.find_all("img")

    temp_img_url = None

    for i in soup:
        if "pag_01-1440-" in i.__str__():  # resoluciones: [120, 160, 380, 550, 1440]
            print(i)
            if fecha.day.__str__() in i.__str__():
                print("se eligió este: ", i)
                temp_img_url = i
                break

    temp_img_url = temp_img_url.__str__()[-19:-3]
    codigo_pagina = temp_img_url
    print(codigo_pagina)
    return codigo_pagina


codigo = genera_url()


def descarga_imagenes(cuando=getFecha(), codigo=codigo):
    aux = []
    ultimo = 1
    arreglo_imagenes_guardadas = []
    for hoja in range(1, 50):
        web_base = (
            "https://impresa.soy-chile.cl/AustralValdivia/%s%s%s/AustralValdivia/%s_%s_%s_pag_%s%s"
            % (
                (cuando.day if cuando.day >= 10 else "0" + cuando.day.__str__()),
                cuando.month if cuando.month >= 10 else "0" + cuando.month.__str__(),
                str(cuando.year)[2:4],
                (cuando.day if cuando.day >= 10 else "0" + cuando.day.__str__()),
                cuando.month if cuando.month >= 10 else "0" + cuando.month.__str__(),
                str(cuando.year)[2:4],
                hoja if hoja >= 10 else "0" + hoja.__str__(),
                codigo,
            )
        )

        k = requests.get(web_base)

        if k.status_code == 404:
            print("nope ->", web_base)
            break
        else:
            aux.append(k)
            print("yep ->", web_base)
            f = open("%s.jpg" % hoja if hoja > 9 else "0" + str(hoja) + ".jpg", "wb")
            f.write(k.content)

        ultimo = ultimo + 1

    print(ultimo, type(ultimo))
    for pagina in range(1, ultimo):
        arreglo_imagenes_guardadas.append(
            "%s.jpg" % pagina if pagina > 9 else "0" + pagina.__str__() + ".jpg"
        )

    print(arreglo_imagenes_guardadas)

    with open(
        "%s-%s-%s.pdf"
        % (
            fecha.year,
            fecha.month if fecha.month >= 9 else "0" + str(fecha.month),
            fecha.day if fecha.day >= 9 else "0" + str(fecha.day),
        ),
        "wb",
    ) as archivo_pdf:
        archivo_pdf.write(img2pdf.convert(arreglo_imagenes_guardadas))

    print("borrando archivos jpg")
    for archivo_jpg in arreglo_imagenes_guardadas:
        remove(archivo_jpg)
    print("listo")


descarga_imagenes()
