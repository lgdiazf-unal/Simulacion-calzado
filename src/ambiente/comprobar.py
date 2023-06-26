from stable_baselines3.common.env_checker import check_env
from ambiente import Calzado_env



def validar_ambiente(orden,hiperparametros):

    env_1 = Calzado_env(orden,hiperparametros)
    # It will check your custom environment and output additional warnings if needed
    _ = check_env(env_1)