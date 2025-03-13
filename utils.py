import datetime
import requests


def get_fecha(dias=0):
    hoy = datetime.date.today()
    print(hoy)
    cantidad_dias_restar = datetime.timedelta(days=dias)
    print(cantidad_dias_restar)
    dia_pasado = hoy - cantidad_dias_restar
    return dia_pasado


def agrega_ceros_izquierda(numero):
    return str(numero) if numero >= 10 else "0" + str(numero)


def genera_url_fecha(fecha=get_fecha()):
    url = requests.get("https://www.australvaldivia.cl/impresa/%s/%s/%s/full/cuerpo-principal/1/" %
                       (
                           fecha.year,
                           agrega_ceros_izquierda(fecha.month),
                           agrega_ceros_izquierda(fecha.day)
                       )
                       )
    return url
