import yaml
from orden import Generador_ordenes
from simulacion import Simulacion_calzado
import numpy as np
import pandas as pd
import math
import random
from scipy.stats import ttest_ind


jornada = 9.5


with open('./config/config.yaml','r') as config_file :
    data_config = yaml.safe_load(config_file)

path_estilo = data_config["path_estilo"]
path_suela = data_config["path_suela"]
path_plantilla = data_config["path_plantilla"]


orden =  Generador_ordenes(path_estilo,path_suela,path_plantilla)

# definir ordenes reales

orden_prueba = []

for i in range(230):
    for i in range(4):
        orden_prueba.append((i+1,2))

orden_real_1 = [(1,2),(2,1),(3,2),(4,1)]


orden.actualizar_orden(orden_prueba)

def crear_df_pivote(df,df_orden):
    df_t = df.copy()
    df2 = df_t.pivot(index="id",columns='tipo')

    tipos = {
        1 : "corte",
        2 : "suela",
        3 : "plantilla",
        4 : "guarnicion",
        5 : "zapato"
    }

    estados = ["inicio","fin","tiempo_proceso"]
    orden_columnas = []

    for tipo in tipos:
        for estado in estados :
            orden_columnas.append(f"{estado}_{tipos[tipo]}") 

    df2.set_axis(df2.columns.map(lambda x : f"{x[0]}_{tipos[x[1]]}"), axis=1, inplace=True )
    df2 = df2[orden_columnas]

    df2 = df2.join(df_orden.set_index("id"))


    for tipo in tipos :
        df2[f"proceso_par_{tipos[tipo]}"] = ""

        df2[f"proceso_par_{tipos[tipo]}"] = df2.apply(
            lambda row : (row[f"tiempo_proceso_{tipos[tipo]}"])/row["cantidad"]
        ,axis = 1)


        df2[f"cola_{tipos[tipo]}"] = ""
        df2[f"cola_{tipos[tipo]}"] = df2.apply(
            lambda row : (row[f"fin_{tipos[tipo]}"] - row[f"inicio_{tipos[tipo]}"]  -  row[f"tiempo_proceso_{tipos[tipo]}"])
        ,axis = 1)

    return df2


def estadisticos(df,df_orden):
    """
    Funcion que calcula los estadisticos de promedio de proceso
    """
    # para cada orden calcular el inicio, fin, tiempo de proceso y tirmpo en cola
    df_2 = crear_df_pivote(df,df_orden)

    print(df_2[["proceso_par_corte","proceso_par_guarnicion","proceso_par_zapato"]].mean())

    print(df_2[["cola_corte","cola_guarnicion","cola_zapato"]].describe())

    print(df_2[["inicio_corte","fin_corte","tiempo_proceso_corte",
                "inicio_guarnicion","fin_guarnicion","tiempo_proceso_guarnicion",
                "inicio_zapato","fin_zapato","tiempo_proceso_zapato"
                ]])
    
    # g = df.groupby("tipo")

    # for i,j in g:
    #     print(f"tipo : {i} proceso {j['tiempo_proceso'].sum()} maximo {j['fin'].max()}")
    #     #print(j[["inicio","fin","tiempo_proceso"]].describe())

    # print(f"tarea completa en {df['fin'].max()/60} horas ")



def evaluar_simulacion(datos_reales,datos_simulacion):

    print(ttest_ind(datos_reales, datos_simulacion))
    

reales = [67.0, 93.0, 86.0, 90.0, 92.0, 85.0, 82.0, 95.0, 90.0, 95.0, 92.0, 83.0, 91.0, 92.0, 93.0, 92.0, 92.0, 85.0, 87.0, 158.0]

tiempo = []
datos_iteracion = []




for i in range(10):

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




        




