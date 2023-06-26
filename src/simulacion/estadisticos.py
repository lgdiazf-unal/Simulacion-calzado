"""
Funciones necesarias para sacar estadisticos de la produccion
"""

def crear_df_pivote(df,df_orden):
    df_t = df.copy()
    df2 = df_t.pivot(index="id",columns='tipo')

    tipos = {
        1 : "corte",
        2 : "suela",
        3 : "plantilla",
        4 : "guarnicion",
        5 : "zapato"
    }

    estados = ["inicio","fin","tiempo_proceso"]
    orden_columnas = []

    for tipo in tipos:
        for estado in estados :
            orden_columnas.append(f"{estado}_{tipos[tipo]}") 

    df2.set_axis(df2.columns.map(lambda x : f"{x[0]}_{tipos[x[1]]}"), axis=1, inplace=True )
    df2 = df2[orden_columnas]

    df2 = df2.join(df_orden.set_index("id"))


    for tipo in tipos :
        df2[f"proceso_par_{tipos[tipo]}"] = ""

        df2[f"proceso_par_{tipos[tipo]}"] = df2.apply(
            lambda row : (row[f"tiempo_proceso_{tipos[tipo]}"])/row["cantidad"]
        ,axis = 1)


        df2[f"cola_{tipos[tipo]}"] = ""
        df2[f"cola_{tipos[tipo]}"] = df2.apply(
            lambda row : (row[f"fin_{tipos[tipo]}"] - row[f"inicio_{tipos[tipo]}"]  -  row[f"tiempo_proceso_{tipos[tipo]}"])
        ,axis = 1)

        df2[f"relacion_{tipos[tipo]}_en_cola"] = ""
        df2[f"relacion_{tipos[tipo]}_en_cola"] = df2.apply(
            lambda row : (row[f"cola_{tipos[tipo]}"] / row[f"fin_{tipos[tipo]}"])
        ,axis = 1)


    return df2



def estadisticos(df,df_orden):
    """
    Funcion que calcula los estadisticos de promedio de proceso
    """
    # para cada orden calcular el inicio, fin, tiempo de proceso y tirmpo en cola
    df_2 = crear_df_pivote(df,df_orden)

    salida = [
        df_2[["proceso_par_corte","proceso_par_guarnicion","proceso_par_suela","proceso_par_plantilla","proceso_par_zapato"]].mean(),

        df_2[["cola_corte","cola_guarnicion","cola_suela","cola_plantilla","cola_zapato"]],

        df_2[["inicio_corte","fin_corte","tiempo_proceso_corte",
                "inicio_guarnicion","fin_guarnicion","tiempo_proceso_guarnicion",
                "inicio_plantilla","fin_plantilla","tiempo_proceso_plantilla",
                "inicio_suela","fin_suela","tiempo_proceso_suela",
                "inicio_zapato","fin_zapato","tiempo_proceso_zapato"
        ]],
        df_2[["relacion_corte_en_cola","relacion_guarnicion_en_cola","relacion_suela_en_cola","relacion_plantilla_en_cola","relacion_zapato_en_cola"]]
    ]

    return salida

    