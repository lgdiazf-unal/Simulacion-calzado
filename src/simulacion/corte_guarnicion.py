import simpy
import random
import pandas as pd

from .hiperparametros import Hiperparametros


class Corte_Guarnicion():
  def __init__(self,env,cortes,df_metricas,pipe={}):
    self.df_metricas = df_metricas
    self.env = env
    self.cortadores = simpy.Resource(
        self.env, capacity=Hiperparametros.cantidad_cortadores
      )
    self.guarnecedores = simpy.Resource(
        self.env, capacity=Hiperparametros.cantidad_gurnecedores
      )

    self.tiempo_colas = 0

    self.cortes = cortes
    self.id_cortadores = [
        id for id in range(Hiperparametros.cantidad_cortadores)
        ]

    self.tiempo_total = 0
    self.tiempo_proceso = 0

    self.pipe = pipe
    self.datos = {}

  
  def get_id_cortador(self):
    id = self.id_cortadores[0]
    if len(self.id_cortadores) == 1:
      self.id_cortadores = []
    else :  
      self.id_cortadores = self.id_cortadores[1:]
    return id




  def get_laminas(self,area_actual,area_necesaria):
    area = area_actual
    laminas_adicionales = 0
    while area < area_necesaria :
      area += random.gauss(
          Hiperparametros.area_media,Hiperparametros.area_desv
        ) 
      laminas_adicionales += 1 
    return laminas_adicionales





  def agregar_simulacion(self):
    """
    Funcion que agrega a los cortadores a la simulacion
    """
    _ = [
      self.env.process(self.generador_cortador(corte)) 
      for corte in self.cortes
    ]



  def get_tiempo_cambio_cuero(self,id_cortador,cuero,area_media,area_desv):
    tiempo_cambio = 0

    if id_cortador not in self.datos: 
      self.datos[id_cortador] = {
        "cuero" : cuero, 
        "area" : random.gauss(
          area_media,area_desv
        )}
    if cuero != self.datos[id_cortador]["cuero"]:
      self.datos[id_cortador]["cuero"] = cuero
      self.datos[id_cortador] = {
        "cuero" : cuero, 
        "area" : random.gauss(
          area_media,area_desv
        )}

      tiempo_cambio = random.expovariate(
        1.0 / Hiperparametros.intervalo_cambio_laminas
        )
    return tiempo_cambio

  def generador_cortador(self,corte):

    inicio_tiempo_cola = self.env.now 

    with self.cortadores.request() as req: 
      yield req
      inicio_proceso = self.env.now
      self.tiempo_colas += (inicio_proceso - inicio_tiempo_cola)
      id_cortador = self.get_id_cortador()
      estilo = corte["estilo"]
      cuero = corte["cuero"]
      cantidad = corte["cantidad"]

      area_total  = sum([ random.gauss(corte["area_media"],corte["area_desv"]) for i in  range(cantidad)])
      tiempo_cambio = self.get_tiempo_cambio_cuero(
        id_cortador,cuero,corte["area_media"],corte["area_desv"]
        )
      numero_laminas = self.get_laminas(self.datos[id_cortador]["area"],area_total)

      tiempo_tarea = sum(
        [random.gauss(corte["corte_media"],corte["corte_desv"]) for i in range(cantidad)]
        )
      tiempo_lamina = sum(
        [
          random.expovariate(1.0 / Hiperparametros.intervalo_cambio_laminas) 
          for i in range(numero_laminas)
        ]
        )

      tiempo_total = tiempo_cambio + tiempo_tarea + tiempo_lamina

      yield self.env.timeout(tiempo_total)

      
      self.id_cortadores.append(id_cortador)

      fin_proceso = self.env.now
      self.tiempo_proceso += (fin_proceso - inicio_proceso)

      df_tmp = pd.DataFrame({
        "tipo" : [1] , 
        "id" :[corte["id"]], 
        "inicio" : [inicio_proceso], 
        "fin" : [fin_proceso] 
        })

      self.df_metricas = self.df_metricas.append(df_tmp)

      g = self.generador_guarnicion(corte["guarnicion_media"],corte["guarnicion_desv"],cantidad,estilo,corte["id"])
      self.env.process(g)


  def generador_guarnicion(self,media_g,desv_g,cantidad,estilo,id_tarea):
    
    inicio_tiempo_cola = self.env.now

    with self.guarnecedores.request() as req:
      yield req
      fin_tiempo_cola = self.env.now
      self.tiempo_colas += (fin_tiempo_cola  - inicio_tiempo_cola)
      inicio = self.env.now
      t = sum([random.gauss(media_g,desv_g) for i in  range(cantidad)])

      yield self.env.timeout(t)

      fin = self.env.now
      self.tiempo_proceso += (fin-fin_tiempo_cola)

      df_tmp = pd.DataFrame({"tipo" : [4] , "id" :[id_tarea], "inicio" : [inicio], "fin" : [fin] })
      self.df_metricas = self.df_metricas.append(df_tmp)
      if self.pipe != {}:
        data = (1,estilo,cantidad,id_tarea)
        self.pipe.put(data)