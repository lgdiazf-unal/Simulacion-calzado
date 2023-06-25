"""
funciones necesarias para validar el modelo
"""
from simulacion_calzado import Simulacion_calzado
from orden import Generador_ordenes

# 1. leer orden de produccion real
# 2. correr simulacion
# 3. validar metricas del modelo

def leer_orden(path_orden):
    """
    Funcion que lee la orden de produccion 
    """
    pass


def correr_simulacion(orden_corte,orden_suela,orden_plantilla,df_estilo):
    """
    Correr la simulacion
    """
    simulacion = Simulacion_calzado(orden_corte,orden_suela,orden_plantilla,df_estilo)
    simulacion.generar_simulacion()

    return simulacion




