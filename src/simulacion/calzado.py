import pandas as pd

from .almacen import Almacen
from .hiperparametros import Hiperparametros
import simpy

class Calzado():


  def __init__(self,env,df_metricas,df_finalizados,df_estilo,pipe):

    self.env = env
    self.df_estilo = df_estilo 
    self.df_finalizados = df_finalizados

    self.pipe = pipe
    self.df_metricas = df_metricas
    self.zapateros = simpy.Resource(
        self.env, capacity=Hiperparametros.cantidad_zapateros
      )
    self.tiempo_colas = 0
    self.tiempo_proceso = 0


  
  def agregar_simulacion(self):
    self.env.process(self.iniciar_calzado())

  def generador_calzado(self,tiempo,id,tiempo_cola,cantidad):

    inicio = self.env.now

    with self.zapateros.request() as req: 
      yield req

      # calculo de los pares producidos
      tiempo_par = tiempo/cantidad
      tiempo_inicio_proceso = self.env.now

      arreglo_id = [id for i in range(cantidad)]
      arreglo_tiempo  = [ (tiempo_inicio_proceso +  ((i)*tiempo_par))  for i in range(cantidad)  ]

      df_tmp_fin = pd.DataFrame(
        {
          "id_orden"  : arreglo_id,
          "tiempo" : arreglo_tiempo 
        }
      )
      self.df_finalizados = self.df_finalizados.append(df_tmp_fin)
      

      yield self.env.timeout(tiempo)

      fin = self.env.now
      df_tmp = pd.DataFrame({"tipo" : [5] , "id" :id, "inicio" : [inicio], "fin" : [fin] , "tiempo_proceso" : [tiempo] })
      self.df_metricas = self.df_metricas.append(df_tmp)

  def iniciar_calzado(self):

    almacen = Almacen(self.df_estilo,self.env)


    while True:
      data = yield self.pipe.get()
      almacen.almacenar(data[0],data[1],data[2])

      
      proceso, tiempo_cola, cantidad = almacen.validar_completo() 
      self.tiempo_proceso += proceso
      self.tiempo_colas += tiempo_cola      
 

      if proceso != 0:
        c = self.generador_calzado(proceso,data[3],tiempo_cola,cantidad)
        self.env.process(c)
      
      



