import sqlite3
import pandas as pd
import os

"""Conectamos la base de datos """
conn = sqlite3.connect('database/database.sqlite')
# type: ignore

""" Cargamos los datos de una tabla en un df """
query = f"SELECT * FROM {'apicall'};"
df_apicall = pd.read_sql_query(query, conn)

query = f"SELECT * FROM {'commerce'};"
df_commerce = pd.read_sql_query(query, conn)


""" Unimos los df de apicall y commerce """
df = pd.merge(df_apicall, df_commerce, on='commerce_id')

""" Filtramos los df para que solo queden las empresas activas """
df = df[df['commerce_status'] == 'Active']

"""Cambiamos el tipo de datos de date_api_call a datetime y fitramos por meses de julio y agosto """
df['date_api_call'] = pd.to_datetime(df['date_api_call'])
df = df[
    (df['date_api_call'].dt.month.isin([7, 8])) &
    (df['date_api_call'].dt.year == 2024)
]

def calcular_comision(empresa, peticiones_exitosas, peticiones_no_exitosas):
    """
    Calcula la comision, el iva y el valor total segun la empresa y el número de peticiones
    
    Parametros:
    empresa (str): 
    peticiones_exitosas (int)
    peticiones_no_exitosas (int)
    
    Retorna:
    tupla con (comisión, IVA, valor total)
    """

    comision = 0

    """ Calculamos la comisión según el contrato de cada empresa"""
    if empresa == "Innovexa Solutions":
        comision = peticiones_exitosas * 300
    elif empresa == "NexaTech Industries":
        if peticiones_exitosas <= 10000:
            comision = peticiones_exitosas * 250
        elif 10001 <= peticiones_exitosas <= 20000:
            comision = (10000 * 250) + ((peticiones_exitosas - 10000) * 200)
        else:
            comision = (10000 * 250) + (10000 * 200) + ((peticiones_exitosas - 20000) * 170)
    elif empresa == "QuantumLeap Inc.":
        comision = peticiones_exitosas * 600
    elif empresa == "Zenith Corp.":
        if peticiones_exitosas <= 22000:
            comision = peticiones_exitosas * 250
        else:
            comision = (22000 * 250) + ((peticiones_exitosas - 22000) * 130)
    elif empresa == "FusionWave Enterprises":
        comision = peticiones_exitosas * 300

    """ Aplicamos descuentos sobre la comision antes del iva"""
    if empresa == "Zenith Corp." and peticiones_no_exitosas > 6000:
        descuento = comision * 0.05
        comision -= descuento
    elif empresa == "FusionWave Enterprises":
        if 2500 <= peticiones_no_exitosas <= 4500:
            descuento = comision * 0.05
            comision -= descuento
        elif peticiones_no_exitosas > 4500:
            descuento = comision * 0.08
            comision -= descuento

    """ Calculamos el iva 19% """
    iva = comision * 0.19

    """ Calculamos el valor total (comisión + iva) """
    valor_total = comision + iva

    """ Retornamos la comisi0n, el iva y el valor total"""
    return comision, iva, valor_total


def procesar_mes(df, mes):
    """
    Procesa los datos de un mes específico para cada empres
    
    Parametros:
    df (DataFrame): Datos filtrados por empresa y peticiones.
    mes (int): Mes a procesar ej: 7 para julio, 8 para agosto
    
    Retorna:
    Df: Resultados con las comisiones calculadas.
    """

    resultados_mes = []
    
    """Filtrar por mes"""
    df_mes = df[df['date_api_call'].dt.month == mes]
    
    """Calcularmos comisiones para cada empresa en el mes"""
    for empresa, grupo in df_mes.groupby('commerce_name'):
        peticiones_exitosas = len(grupo[grupo['ask_status'] == 'Successful'])
        peticiones_no_exitosas = len(grupo[grupo['ask_status'] == 'Unsuccessful'])
        
        comision, iva, valor_total = calcular_comision(empresa, peticiones_exitosas, peticiones_no_exitosas)
        
        """buscamos el NIT y  correo de la empresa """
        commerce_nit = grupo['commerce_nit'].iloc[0]  # Tomamos el primer valor
        commerce_email = grupo['commerce_email'].iloc[0] 
        
        resultados_mes.append({
            'Fecha-Mes': mes,
            'Nombre': empresa,
            'Nit': commerce_nit,
            'Valor_comision': comision,
            'valor_iva': iva,
            'Valor_total': valor_total,
            'Correo': commerce_email
        })
    
    return pd.DataFrame(resultados_mes)


""" Procesamos julio y agosto"""
julio = procesar_mes(df, 7)  # Mes 7 = julio
agosto = procesar_mes(df, 8)  # Mes 8 = agosto

""" Combinamos los resultados de ambos"""
df_resultados = pd.concat([julio, agosto], ignore_index=True)

"""código para exportar los restultados en excel"""

"""Creamos la carpeta resultado si no existe """
if not os.path.exists('resultado'):
    os.makedirs('resultado')

"""Guardamos el df en un archivo Excel dentro de la carpeta resultado """
ruta_archivo = os.path.join('resultado', 'resultados_comisiones.xlsx')
df_resultados.to_excel(ruta_archivo, index=False)

print(f"Archivo guardado en: {ruta_archivo}")