from requests_html import HTMLSession
from datetime import datetime
from json import dump, load

def mostrar_juegos(diccionario):
    for nombre, fechas in diccionario.items():
        print(f"{nombre}")
        for fecha, precio in fechas.items():
            print(f"{fecha}: ${precio}")
        print("")

def cargar_diccionario(archivo):
    try:
        with open(archivo, "r") as file:
            return load(file)
    except:
        return {}

def guardar_diccionario(archivo, diccionario):
    try:
        with open(archivo, "w") as file:
            dump(diccionario, file)
    except:
        mostrar_juegos(diccionario)

def obtener_juegos(pagina):
    url = f"https://tiendaludica.com.ar/#!/categoria/0/pagina/{pagina}/"
    content = HTMLSession().get(url).html
    content.render(sleep = 2)

    lista = []
    for juego in content.find("div.thumbnail"):
        nombre = juego.find("span[title]")[0].text.strip()
        precio = juego.find("span.monto")[0].text.replace(".", "")
        lista.append( (nombre, float(precio.replace(",", "."))) )

    return lista

def main(archivo, paginas):
    diccionario = cargar_diccionario(archivo)

    for pagina in range(paginas + 1):
        print(f"Revisando pagina {pagina}...", end = " ", flush = True)
        juegos = obtener_juegos(pagina)
        print(f"{len(juegos)} juegos.")

        for nombre, precio in juegos:
            if nombre not in diccionario:
                diccionario[nombre] = {}

            diccionario[nombre][fecha] = precio

    guardar_diccionario(archivo, diccionario)

fecha = str(datetime.now().day) + "-" + str(datetime.now().month)
if __name__ == "__main__":
    archivo = input("Ingrese nombre del archivo: ")
    paginas = int(input("Ingrese cantidad de paginas: "))
    main(archivo, paginas)
