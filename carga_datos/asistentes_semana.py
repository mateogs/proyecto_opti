import numpy as np

#v_et

def asistentes_semana(alumnos_por_est, cantidad_establecimientos, cantidad_semanas):
    np.random.seed(100)
    asistencias = []
    for est in range(cantidad_establecimientos):
        asistencia = list(np.random.binomial(alumnos_por_est[est], 0.9, cantidad_semanas))
        asistencias.append(asistencia)
    return asistencias