import yaml
from orden import Generador_ordenes
from simulacion import Simulacion_calzado,crear_df_pivote,estadisticos
import numpy as np
import pandas as pd
import math
import random
from scipy.stats import ttest_ind


jornada = 9.5

# leer parametros
with open('./config/config.yaml','r') as config_file :
    data_config = yaml.safe_load(config_file)

path_estilo = data_config["path_estilo"]
path_suela = data_config["path_suela"]
path_plantilla = data_config["path_plantilla"]


reales = [67.0, 93.0, 86.0, 90.0, 92.0, 85.0, 82.0, 95.0, 90.0, 95.0, 92.0, 83.0, 91.0, 92.0, 93.0, 92.0, 92.0, 85.0, 87.0, 158.0]
tiempo = []
datos_iteracion = []


# generar orden
orden =  Generador_ordenes(path_estilo,path_suela,path_plantilla)

# definir ordenes reales
orden_prueba = []

for i in range(230):
    for i in range(4):
        orden_prueba.append((i+1,2))

orden_real_1 = [(1,2),(2,1),(3,2),(4,1)]


orden.actualizar_orden(orden_prueba)


def evaluar_simulacion(datos_reales,datos_simulacion):
    print(ttest_ind(datos_reales, datos_simulacion))
    


def get_error(a,b):
    arreglo1 = np.array(a)
    arreglo2 = np.array(b)
    max_longitud = max(len(arreglo1), len(arreglo2))
    arreglo1 = np.resize(arreglo1, max_longitud)
    arreglo2 = np.resize(arreglo2, max_longitud)

    errores = np.abs(arreglo1 - arreglo2)
    errores_normalizados = (errores - np.min(errores)) / (np.max(errores) - np.min(errores))

    return np.mean(errores_normalizados)

   # print(np.mean(errores_normalizados))


def generar_simulacion():
    simulacion = Simulacion_calzado(
            orden.orden_corte,
            orden.orden_suela,
            orden.orden_plantilla,
            orden.df_estilo
    )
    
    simulacion.generar_simulacion()
    df_metrica = simulacion.df_metricas
    df_finalizados  = simulacion.df_finalizados





    #print(df_finalizados.describe())

    #print(tiempo.append(df_metrica["fin"].max()/60))

    df_finalizados["dias"] = ""
    df_finalizados["dias"] = df_finalizados.apply(lambda row : math.ceil((row["tiempo"]/(60*jornada))), axis=1)

    datos = []

    for i,j in df_finalizados.groupby("dias"):
        datos_iteracion.append(j['dias'].count())
        datos.append(j['dias'].count())
        #print(f"{i} : {j['dias'].count()}")

    #print(f"iteracion pares realizados {np.mean(datos)} con {np.std(datos)} en {len(datos)} dias")

    #print(f"pares realizados {np.mean(datos_iteracion)} con {np.std(datos_iteracion)} en {len(datos_iteracion)} dias")
    evaluar_simulacion(reales,datos)
    print(datos)

    # a_t = df_finalizados["tiempo"].values

    # for i in range(len(a_t)-1):
    #     print(f"tiempo muerto  : {a_t[i+1] - a_t[i]}")

    #print(simulacion.df_finalizados)

    df_orden = pd.DataFrame(orden.orden_corte)[["id","cantidad"]]
    #estadisticos(df_metrica,df_orden)
    # print(f"media {np.mean(tiempo)} std {np.std(tiempo)}")

    return [datos,simulacion.get_indice()]


# convergencia



limite = 0.0004

data1  = generar_simulacion()
indice1 = data1[1]


for i in range(10):
    iteracion = 1
    while True:
        print(f"iteracion {iteracion}")
        data2 = generar_simulacion()
        indice2 = data2[1]
        error = abs(indice2-indice1)/indice2
        print(error,limite)

        if error < limite:
            break

        indice1 = indice2
        iteracion = iteracion + 1

    

  
    
   




