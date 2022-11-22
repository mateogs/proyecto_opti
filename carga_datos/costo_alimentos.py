import os

#c_a(a)

def costo_alimento():
    directorio = os.path.dirname(__file__)
    nombre_archivo = os.path.join(directorio, "..", "datos", "costo_alimento.csv")
    archivo = open(nombre_archivo)
    costo_alimento = archivo.readlines()[1:]
    archivo.close()
    costo_alimento = list(map(lambda x: int(x.split("\n")[0].split(",")[1]), costo_alimento))
    return costo_alimento