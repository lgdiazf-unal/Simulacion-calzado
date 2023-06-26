import random 

class Almacen():

  def __init__(self,df_estilo,env):
    self.df_estilo = df_estilo
    self.env = env
    self.almacen = {}


  def almacenar(self,tipo,estilo,cantidad):
    if tipo != 1:
      if tipo in self.almacen:
        if estilo in self.almacen[tipo]:
          self.almacen[tipo][estilo] = self.almacen[tipo][estilo] + cantidad
        else : 
          self.almacen[tipo][estilo] = cantidad
      else : 
        self.almacen[tipo] = {estilo : cantidad}
    
    else :

      if tipo in self.almacen:
       
        if estilo in self.almacen[tipo]:
          self.almacen[tipo][estilo] = self.almacen[tipo][estilo].append([cantidad, self.env.now ])
        else : 
          self.almacen[tipo][estilo] = [[cantidad, self.env.now ]]
      else : 
        self.almacen[tipo] = {estilo : [[cantidad, self.env.now ]]}




  def eliminar_estilos_vacios(self,corte):
    if self.almacen[1][corte] == []:
      self.almacen[1].pop(corte)


    
  def validar_completo(self):


    
    if 1 in self.almacen:
      

      # recorrer los estilos de guarnicion
 
      for i in self.almacen[1]:
        if self.almacen[1][i] != []:

          cantidad_solicitada = self.almacen[1][i][0][0]
          informacion_estilo = self.df_estilo[self.df_estilo["id_estilo"] == i].values[0]

          if cantidad_solicitada > 0 :
            id_plantilla = informacion_estilo[10]
            id_suela = informacion_estilo[9]
            cantidad_suela = 0
            cantidad_plantilla = 0

            if 2 in self.almacen and 3 in self.almacen:

              if id_suela in self.almacen[2] :
                cantidad_suela = self.almacen[2][id_suela]

              if id_plantilla in self.almacen[3]:
                cantidad_plantilla = self.almacen[3][id_plantilla]

              if ((cantidad_solicitada <= cantidad_suela) and (cantidad_solicitada <= cantidad_plantilla)):

                
                self.almacen[2][id_suela] = self.almacen[2][id_suela] - cantidad_solicitada
                self.almacen[3][id_plantilla] = self.almacen[3][id_plantilla] - cantidad_solicitada

                tiempo_cola = self.env.now - self.almacen[1][i][0][1]

                self.almacen[1][i] = self.almacen[1][i][1:]
                
                proceso = sum([random.gauss(informacion_estilo[5],informacion_estilo[6]) for i in range(cantidad_solicitada)])

                
                self.eliminar_estilos_vacios(i)
              
                return (proceso,tiempo_cola,cantidad_solicitada) 
      
     
    return (0,0,0)
