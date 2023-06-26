"""
Funciones necesarias para comprobar el ambiente de simulacion
"""
import yaml
from orden import Generador_ordenes
from ambiente import validar_ambiente
from simulacion import Simulacion_calzado

jornada = 9.5


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


#validar_ambiente(orden)


simulacion = Simulacion_calzado(
            orden.orden_corte,
            orden.orden_suela,
            orden.orden_plantilla,
            orden.df_estilo
)
    
simulacion.generar_simulacion()

print(simulacion.get_indice())


