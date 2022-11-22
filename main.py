from gurobipy import GRB, Model, quicksum
from gurobipy import *

from carga_datos.asistentes_semana import asistentes_semana
from carga_datos.cantidad_alumnos import cantidad_alumnos
from carga_datos.costo_alimentos import costo_alimento
from carga_datos.distancias import distancia
from carga_datos.params_constantes import *


#----------------------- Creacion de Conjuntos ------------------------
A_ = range(1, CANTIDAD_ALIMENTOS + 1)   #alimentos
E_ = range(1, CANTIDAD_ESTABLECIMIENTOS + 1)   #establecimientos
T_ = range(1, CANTIDAD_SEMANAS + 1)   #semanas


#----------------------- Importacion de Parametros ------------------------
costo_alimentos = costo_alimento()
distancias = distancia()
alumnos_por_est = cantidad_alumnos(CANTIDAD_ESTABLECIMIENTOS)
asistencia_semanal = asistentes_semana(alumnos_por_est, CANTIDAD_ESTABLECIMIENTOS, CANTIDAD_SEMANAS)


#----------------------- Definicion de Parametros ------------------------
b_e = ALMACENAMIENTO_MAX
k = COSTO_KM
delta = CAPACIDAD_CAMIONES
alfa = COSTO_ALMACENAMINETO
p = CAPACIDAD_PRODUCCION
j = CONSUMO_ALUMNO

c_a = {(a): costo_alimentos[a - 1] for a in A_}
d_e = {(e): distancias[e - 1] for e in E_}
h_e = {(e): alumnos_por_est[e - 1] for e in E_}
v_et = {(e,t): asistencia_semanal[e - 1][t - 1] for e in E_ for t in T_}


#----------------------- Instancia de Modelo ------------------------
modelo = Model()
modelo.setParam("TimeLimit", 1800)


#----------------------- Creacion de Variables ------------------------
x = modelo.addVars(A_, T_, E_, vtype = GRB.CONTINUOUS)
xr = modelo.addVars(A_, T_, E_, vtype = GRB.CONTINUOUS)
xc = modelo.addVars(A_, T_, E_, vtype = GRB.CONTINUOUS)
y = modelo.addVars(T_, E_, vtype = GRB.INTEGER)


#----------------------- Creacion de Restricciones ------------------------
# R1 STOCK PRIMERA SEMANA
modelo.addConstrs((x[a,1,e] == (xr[a,t,e] - xc[a,t,e]) for a in A_ for t in T_[2:] for e in E_), name="R1")

# R2 INVENTARIO
modelo.addConstrs((x[a,t,e] == (x[a,t-1,e] + xr[a,t,e] - xc[a,t,e]) for a in A_ for t in T_[2:] for e in E_), name = "R2")

# R3 STOCK MINIMO
modelo.addConstrs(((x[a,t-1,e] + xr[a,t,e]) >= (h_e[e] * j) for a in A_ for t in T_[2:] for e in E_), name = "R3")

# R4 CAPACIDAD ALM
modelo.addConstrs(((x[a,t-1,e] + xr[a,t,e]) <= b_e for a in A_ for t in T_[2:] for e in E_), name = "R4")

# R5 CAPACIDAD CAMIONES
modelo.addConstrs((quicksum(xr[a,t,e] for a in A_) <= (y[t,e] * delta) for t in T_ for e in E_), name ="R5")

# R6 CONSUMO MINIMO
modelo.addConstrs((quicksum(xc[a,t,e] for a in A_) >= (v_et[e,t] * j) for t in T_ for e in E_), name ="R6")

# R7 PRODUCCION
modelo.addConstrs((quicksum(quicksum(xr[a,t,e] for e in E_) for a in A_) <= p for t in T_), name="R7")

# R8 NATURALEZA
modelo.addConstrs((x[a,t,e] >= 0 for a in A_ for t in T_ for e in E_), name ="R9.1")
modelo.addConstrs((xr[a,t,e] >= 0 for a in A_ for t in T_ for e in E_), name ="R9.2")
modelo.addConstrs((xc[a,t,e] >= 0 for a in A_ for t in T_ for e in E_), name ="R9.3")
modelo.addConstrs((y[t,e] >= 0 for t in T_ for e in E_), name ="R9.4")


#----------------------- Creacion de Funcion Objetivo ------------------------
modelo.setObjective(quicksum(quicksum(quicksum(c_a[a] * xr[a,t,e] for a in A_) for t in T_) for e in E_) + 
                        quicksum(quicksum(y[t,e] * k * d_e[e] for t in T_) for e in E_) + 
                        quicksum(quicksum(quicksum(alfa * x[a,t,e] for a in A_) for t in T_) for e in E_), GRB.MINIMIZE)


#----------------------- Optimizacion de Modelo ------------------------
modelo.optimize()
try:
    valor_objetivo = modelo.ObjVal
except:
    valor_objetivo = "F"


# Mostrar Resultados
print(valor_objetivo)
