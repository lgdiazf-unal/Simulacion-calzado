"""
Funciones necesarias para comprobar el ambiente de simulacion
"""
import yaml
from orden import Generador_ordenes
from ambiente import validar_ambiente
from simulacion import Simulacion_calzado,Hiperparametros,estadisticos
import random




# configuraciones
with open('./config/config.yaml','r') as config_file :
    data_config = yaml.safe_load(config_file)

path_estilo = data_config["path_estilo"]
path_suela = data_config["path_suela"]
path_plantilla = data_config["path_plantilla"]


orden =  Generador_ordenes(path_estilo,path_suela,path_plantilla)


orden_prueba = []

for i in range(1):
    for i in range(4):
        orden_prueba.append((i+1,2))

orden_real_1 = [(1,2),(2,1),(3,2),(4,1)]
orden.actualizar_orden(orden_prueba)



# comprobar  la recompensa

def validar_inidice(arreglo_ordenes):

    for datos_orden  in arreglo_ordenes:

        orden.actualizar_orden(datos_orden)

        simulacion = Simulacion_calzado(
                    orden.orden_corte,
                    orden.orden_suela,
                    orden.orden_plantilla,
                    orden.df_estilo
        )
            
        simulacion.generar_simulacion()

        df_orden = pd.DataFrame(orden.orden_corte)[["id","cantidad"]]

        arreglo_estadisticos = estadisticos(simulacion.df_metricas,df_orden)

        print(datos_orden)
        print(simulacion.get_indice())




# comprobar la implementacion del ambiente

def validar_implementacion_ambiente(orden):
    cantidad_cortadores = Hiperparametros.cantidad_cortadores
    cantidad_gurnecedores = Hiperparametros.cantidad_gurnecedores
    cantidad_lineas_produccion_plantilla = Hiperparametros.cantidad_lineas_produccion_plantilla
    cantidad_lineas_produccion_suela = Hiperparametros.cantidad_lineas_produccion_suela
    cantidad_zapateros = Hiperparametros.cantidad_zapateros

    hiperparametros = [
        cantidad_cortadores ,
        cantidad_gurnecedores,
        cantidad_lineas_produccion_plantilla ,
        cantidad_lineas_produccion_suela,
        cantidad_zapateros
    ]
    validar_ambiente(orden,hiperparametros)


def generar_ordenes():

    arreglo_ordenes = []

    for i in range(10):
        datos_iteracion = []
        for i in range(4):
            datos_iteracion.append((i+1,random.randint(1, 2)))
            random.shuffle(datos_iteracion)
        arreglo_ordenes.append(datos_iteracion)
        
    return arreglo_ordenes




arreglo_ordenes = generar_ordenes()
validar_inidice(arreglo_ordenes)