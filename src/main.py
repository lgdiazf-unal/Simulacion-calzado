import os
import sys
import yaml

from simulacion import Hiperparametros

with open('./config/config.yaml','r') as config_file :
    data_config = yaml.safe_load(config_file)

path_estilo = data_config["path_estilo"]
path_suela = data_config["path_suela"]
path_plantilla = data_config["path_plantilla"]
path_modelos = data_config["path_modelos"]
path_logs = data_config["path_logs"]
nombre_modelo = data_config["nombre_modelo"]


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



def validar_carpetas():
    if not os.path.exists(path_modelos):
        os.makedirs(path_modelos)
    if not os.path.exists(path_logs):
        os.makedirs(path_logs)

def entrenar(tipo):

    from ambiente import Calzado_env
    from orden import Generador_ordenes
    from stable_baselines3 import PPO,A2C

    validar_carpetas()    
    orden =  Generador_ordenes(path_estilo,path_suela,path_plantilla)
    env=Calzado_env(orden,hiperparametros)
    env.reset()

    if tipo=="ppo" :
        model =  PPO('MlpPolicy', env, verbose=1,tensorboard_log=path_logs)
    else :
        model =  A2C('MlpPolicy', env, verbose=1,tensorboard_log=path_logs)

    TIMESTEPS = 10000

    for i in range(30):
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=nombre_modelo)
        
        model.save(f"{path_modelos}/{TIMESTEPS*i}")

    env.close()


if __name__ == "__main__" :
    argumentos = sys.argv[1:]
    accion = argumentos[0]

    if accion == "entrenar" :
        entrenar(argumentos[1])