import yaml
from orden import Generador_ordenes
from simulacion import Simulacion_calzado
import numpy as np
import pandas as pd

with open('./config/config.yaml','r') as config_file :
    data_config = yaml.safe_load(config_file)

path_estilo = data_config["path_estilo"]
path_suela = data_config["path_suela"]
path_plantilla = data_config["path_plantilla"]


orden =  Generador_ordenes(path_estilo,path_suela,path_plantilla)

# definir ordenes reales
orden_real_1 = [(1,5),(2,12),(3,22),(4,10)]
# orden_real_2 = [(1,8),(2,12),(3,22),(4,10)]
# orden_real_3 = [(1,9),(2,10),(3,4),(4,21)]


orden.actualizar_orden(orden_real_1)


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
        
        df2[f"cola_{tipos[tipo]}"] = ""
        df2[f"cola_{tipos[tipo]}"] = df2.apply(
            lambda row : (row[f"fin_{tipos[tipo]}"] - row[f"inicio_{tipos[tipo]}"] - row[f"tiempo_proceso_{tipos[tipo]}"])/row["cantidad"]
        ,axis = 1)



    

    return df2




def estadisticos(df,df_orden):
    """
    Funcion que calcula los estadisticos de promedio de proceso
    """
    # para cada orden calcular el inicio, fin, tiempo de proceso y tirmpo en cola
    df_2 = crear_df_pivote(df,df_orden)




    print(df_2)




    

    # g = df.groupby("tipo")

    # for i,j in g:
    #     print(f"tipo : {i} proceso {j['tiempo_proceso'].sum()} maximo {j['fin'].max()}")
    #     #print(j[["inicio","fin","tiempo_proceso"]].describe())

    # print(f"tarea completa en {df['fin'].max()/60} horas ")


tiempo = []

for i in range(1):

    simulacion = Simulacion_calzado(
            orden.orden_corte,
            orden.orden_suela,
            orden.orden_plantilla,
            orden.df_estilo
    )

    simulacion.generar_simulacion()
    df_estado = simulacion.df_estado
    df_metrica = simulacion.df_metricas

   # print(df_estado)

    print(tiempo.append(df_metrica["fin"].max()/60))

    df_orden = pd.DataFrame(orden.orden_corte)[["id","cantidad"]]
    estadisticos(df_metrica,df_orden)



    # print(f"media {np.mean(tiempo)} std {np.std(tiempo)}")

    




