import simpy
import random
import pandas as pd

from .hiperparametros import Hiperparametros
from .corte_guarnicion import Corte_Guarnicion
from .suela_plantilla import Suela_Plantilla
from .calzado import Calzado



class Simulacion_calzado():

  def __init__(self,orden_corte,orden_suela,orden_plantilla,df_estilo):
    self.env = simpy.Environment()

    self.orden_corte = orden_corte
    self.orden_suela = orden_suela
    self.orden_plantilla = orden_plantilla

    self.df_estilo = df_estilo

    self.tiempo_colas = 0

    self.capacidad_suela = simpy.Resource(self.env, capacity=Hiperparametros.cantidad_lineas_produccion_suela)
    self.capacidad_plantilla = simpy.Resource(self.env, capacity=Hiperparametros.cantidad_lineas_produccion_plantilla)

    self.df_metricas = pd.DataFrame()
    self.df_metricas["tipo"] = []
    self.df_metricas["id"] = []
    self.df_metricas["inicio"] = []
    self.df_metricas["fin"] = []
    self.df_metricas["tiempo_proceso"] = []


    self.df_estado = pd.DataFrame()
    self.df_estado["fecha"] = []
    self.df_estado["corte"] = []
    self.df_estado["guarnicion"] = []
    self.df_estado["suela"] = []
    self.df_estado["plantilla"] = []
    self.df_estado["zapato"] = []


    self.pipe = simpy.Store(self.env)
    self.estado =  simpy.Store(self.env)

    self.tiempo_total = 0

    self.tiempo_colas = 0
    self.tiempo_proceso = 0

  def generar_simulacion(self):
    actividades = [
        Corte_Guarnicion(self.env,self.orden_corte,self.df_metricas,self.df_estado,self.pipe,self.estado),
        Suela_Plantilla(self.env,self.orden_suela,2,self.capacidad_suela,self.df_metricas,self.df_estado,self.pipe,self.estado),
        Suela_Plantilla(self.env,self.orden_plantilla,3,self.capacidad_plantilla,self.df_metricas,self.df_estado,self.pipe,self.estado),
        Calzado(self.env,self.df_metricas,self.df_estado,self.df_estilo,self.pipe,self.estado)
    ]
    _ = [actividad.agregar_simulacion() for actividad in actividades]

    self.env.run()

    self.tiempo_total = self.env.now

    self.tiempo_colas = sum([actividad.tiempo_colas for actividad in actividades])
    self.tiempo_proceso = sum([actividad.tiempo_proceso for actividad in actividades])


    _ = list(map(self.agregar_metricas,actividades))

  def get_indice(self):

    indice = self.tiempo_colas  / (self.tiempo_colas + self.tiempo_proceso )
    return indice

  def agregar_metricas(self,actividad):
    self.df_metricas = self.df_metricas.append(actividad.df_metricas)
    self.df_estado = self.df_estado.append(actividad.df_estado)