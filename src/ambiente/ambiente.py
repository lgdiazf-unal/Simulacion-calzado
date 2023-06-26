import gym
from gym import spaces
import numpy as np
import itertools
from  simulacion  import Simulacion_calzado

class parametros():
  indice_minimo = 0.11

class Calzado_env(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render.modes": ["human"]}

    def __init__(self, orden,hiperparametros):
        super().__init__()
        self.action_space = spaces.Discrete(24)
        self.observation_space = spaces.Box(low=0, high=60,
                                            shape=(9,), dtype=np.float64)
        
        self.simulacion = []
        self.pasos = 0
        self.pasos_maximos = 4
        self.orden = orden
        self.diccionario_acciones = self.get_diccionario_acciones()

        self.hiperparametros = hiperparametros

    def get_diccionario_acciones(self):
      arreglo_indices = range(self.pasos_maximos)
      permutaciones = list(itertools.permutations(arreglo_indices))
      diccionario_aciones = {i : permutaciones[i]  for i in range(len(permutaciones))}

      return diccionario_aciones


    def cambiar_orden(self,action):

      orden_actividad = self.diccionario_acciones[action]
      orden_nuevo = self.orden.orden.copy()
      data = [orden_nuevo[i] for i in orden_actividad ]
      self.orden.actualizar_orden(data)


    def step(self, action):
      self.cambiar_orden(action)

      self.simulacion = Simulacion_calzado(
        self.orden.orden_corte,
        self.orden.orden_suela,
        self.orden.orden_plantilla,
        self.orden.df_estilo)

      self.simulacion.generar_simulacion()
      info = {"paso" : self.pasos , "accion" : action}

      self.reward = (1 /  self.simulacion.get_indice())


      observation_orden = [dato[1] for dato in self.orden.orden]
      self.observation = np.concatenate((observation_orden,self.hiperparametros))

      if self.simulacion.get_indice() > parametros.indice_minimo :
        self.done = True
      else :
        self.done = False
      self.orden.orden = self.orden.generar_datos()
      return self.observation, self.reward, self.done, info

    def reset(self):

      self.orden.orden = self.orden.generar_datos()
      self.orden.run()
      self.pasos = 0

      observation_orden = [dato[1] for dato in self.orden.orden]
      self.observation = np.concatenate((observation_orden,self.hiperparametros))
      
      return self.observation  