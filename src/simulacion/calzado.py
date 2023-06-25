import pandas as pd

from .almacen import Almacen
from .hiperparametros import Hiperparametros
import simpy
from .estado import Estado

class Calzado():


  def __init__(self,env,df_metricas,df_estado,df_estilo,pipe,estado={}):

    self.env = env

    self.historial = [[self.env.now,0]]

    self.df_estilo = df_estilo 

    self.pipe = pipe
    self.estado = estado
    self.df_metricas = df_metricas
    self.df_estado = df_estado
    self.zapateros = simpy.Resource(
        self.env, capacity=Hiperparametros.cantidad_zapateros
      )

 

    self.tiempo_colas = 0
    self.tiempo_proceso = 0


  
  def agregar_simulacion(self):
    self.env.process(self.iniciar_calzado())

  def generador_calzado(self,tiempo,id,tiempo_cola,cantidad):

    inicio = self.env.now

    if self.estado != {}:
      data_estado = (5,len(self.zapateros.queue))
      self.estado.put(data_estado)

    with self.zapateros.request() as req: 
      yield req
      
      yield self.env.timeout(tiempo)

      self.historial.append([self.env.now/60,self.historial[-1][1]+cantidad])

      print(self.historial)



      fin = self.env.now
      df_tmp = pd.DataFrame({"tipo" : [5] , "id" :id, "inicio" : [inicio], "fin" : [fin] , "tiempo_proceso" : [tiempo] })
      self.df_metricas = self.df_metricas.append(df_tmp)
    if self.estado != {}:
      data_estado = (5,len(self.zapateros.queue))
      self.estado.put(data_estado)




  
  def iniciar_calzado(self):

    almacen = Almacen(self.df_estilo,self.env)
    estado = Estado(self.env,self.df_estado)

    while True:
      data = yield self.pipe.get()
      data_estado = yield self.estado.get()

      estado.actualizar(data_estado[0],data_estado[1])
      almacen.almacenar(data[0],data[1],data[2])

      
      proceso, tiempo_cola, cantidad = almacen.validar_completo() 
      self.tiempo_proceso += proceso
      self.tiempo_colas += tiempo_cola      
 

      if proceso != 0:
        c = self.generador_calzado(proceso,data[3],tiempo_cola,cantidad)
        self.env.process(c)
      
      



