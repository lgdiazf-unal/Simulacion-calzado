"""
Funciones necesarias para determinar el estado del ambiente
se determina el encolamiento
"""
import pandas as pd
class Estado():

    def __init__(self,env,df_estado) :
        self.env = env
        self.df_estado = df_estado
        self.corte = self.guarnicion = self.suela = self.plantilla = self.zapato = 0

    def actualizar(self,tipo,cantidad):
        """
        crea un df temporal y lo agrega al df_estado 
        """

        #print(tipo,cantidad) 
        if tipo == 1:
            self.corte = cantidad
        elif tipo == 2:
            self.suela = cantidad
        elif tipo == 3 :
            self.plantilla = cantidad
        elif tipo == 4 :
            self.guarnicion = cantidad
        else:
            self.zapato = cantidad

        df_tmp = pd.DataFrame({
            "fecha" : [self.env.now],
            "corte" : [self.corte],
            "guarnicion" : [self.guarnicion],
            "suela" : [self.suela],
            "plantilla" : [self.plantilla],
            "zapato" : [self.zapato]
        })

        self.df_estado = self.df_estado.append(df_tmp)

        #print(self.df_estado)