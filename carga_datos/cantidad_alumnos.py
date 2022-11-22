import numpy as np

#h_e(e)

def cantidad_alumnos(cantidad_establecimientos):
    np.random.seed(100)
    alumnos = list(map(lambda x: int(x), np.random.normal(290, 5, cantidad_establecimientos)))
    return alumnos