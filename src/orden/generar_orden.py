import random
import pandas as pd


class Parametros_orden():
  cantidad_ordenes = 4

class Generador_ordenes():

  def __init__(self,path_estilo,path_suela,path_plantilla):

    self.df_estilo = pd.read_csv(path_estilo)
    self.df_suela = pd.read_csv(path_suela)
    self.df_plantilla = pd.read_csv(path_plantilla)

    self.df_completo = []

    self.generar_df()

    self.orden_corte = []
    self.orden_plantilla = []
    self.orden_suela = []

    self.id_tarea_corte = 1
    self.id_tarea_suela = 1 
    self.id_tarea_plantilla = 1 

    self.lim_inf = 18
    self.lim_sup =  20

    self.orden = self.generar_datos()

    self.run()


  def reiniciar_conteo(self):

    self.orden_corte = []
    self.orden_plantilla = []
    self.orden_suela = []

    self.id_tarea_corte = 1
    self.id_tarea_suela = 1 
    self.id_tarea_plantilla = 1

  def run(self):
    self.reiniciar_conteo()
    _ = [self.get_orden(orden[0],orden[1]) for orden in self.orden]


  def actualizar_orden(self,orden):
    self.reiniciar_conteo()
    self.orden = orden
    _ = [self.get_orden(orden[0],orden[1]) for orden in self.orden]

  def generar_df(self):
    df1_suela=self.df_estilo.copy()  
    df1_suela["tmp_id_suela"]=df1_suela["id_suela"]
    self.df_suela.columns = ["id","media_suela","desv_suela"]
    df_1 = df1_suela.set_index("tmp_id_suela").join(
      self.df_suela.set_index("id"),
      lsuffix="_corte",
      rsuffix="_suela"
    )


    df_1["tmp_id_plantilla"] = df_1["id_plantilla"]

    self.df_plantilla.columns = ["id","media_plantilla","desv_plantilla"]

    self.df_completo = df_1.set_index("tmp_id_plantilla").join(
      self.df_plantilla.set_index("id"),
      rsuffix="_plantilla"
      )


  def generar_datos(self):
    return [
        (id_estilo,random.randint(self.lim_inf,self.lim_sup)) 
        for id_estilo in range(1,Parametros_orden.cantidad_ordenes+1)
        ]

  def get_orden(self,id_estilo,cantidad):

    datos = self.df_completo[self.df_completo["id_estilo"]==id_estilo].values[0]
    corte = {
        "id" : self.id_tarea_corte , 
        "estilo" : id_estilo , 
        "corte_media" : datos[1], 
        "corte_desv" : datos[2],
        "cantidad" : cantidad,
        "area_media" : datos[7],
        "area_desv" : datos[8],
        "guarnicion_media" : datos[3],
        "guarnicion_desv" : datos[4],
        "cuero" : datos[11]
      }

    self.id_tarea_corte += 1
    self.orden_corte.append(corte)

    suela = {
        "id" : self.id_tarea_suela,
        "estilo" : id_estilo,
        "id_suela" : datos[9],
        "cantidad" : cantidad,
        "suela_media" : datos[12],
        "suela_desv" : datos[13]
    }

    self.id_tarea_suela += 1
    self.orden_suela.append(suela)

    plantilla = {
      "id" : self.id_tarea_plantilla, 
      "estilo" : id_estilo,
      "id_plantilla" : datos[10],
      "cantidad" : cantidad,
      "plantilla_media" : datos[14],
      "plantilla_desv" : datos[15],
        
    }

    self.id_tarea_plantilla += 1
    self.orden_plantilla.append(plantilla)
  