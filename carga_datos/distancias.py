import os

#d_e(e)

def distancia():
    directorio = os.path.dirname(__file__)
    nombre_archivo = os.path.join(directorio, "..", "datos", "distancia.csv")
    archivo = open(nombre_archivo)
    distancia = archivo.readlines()[1:]
    archivo.close()
    distancia = list(map(lambda x: float(x.split("\n")[0]), distancia))
    return distancia