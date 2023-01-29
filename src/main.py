from ambiente import Calzado_env
from orden import Generador_ordenes

from stable_baselines3 import PPO,A2C
import os


path_estilo = "./data/estilo_gen.csv"
path_suela = "./data/suela_gen.csv"
path_plantilla = "./data/plantilla_gen.csv"

path_modelos = "modelos/ppo_indice_4"
path_logs = "logs"

if not os.path.exists(path_modelos):
    os.makedirs(path_modelos)

if not os.path.exists(path_logs):
    os.makedirs(path_logs)


# generar orden
orden =  Generador_ordenes(path_estilo,path_suela,path_plantilla)
env=Calzado_env(orden)
env.reset()
model =  PPO('MlpPolicy', env, verbose=1,tensorboard_log=path_logs)
TIMESTEPS = 10000

for i in range(30):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="ppo_indice_4")
    
    model.save(f"{path_modelos}/{TIMESTEPS*i}")

env.close()