import sqlite3
import pandas as pd

#Cosas de bd

#------Conectamos la base de datos----
conn = sqlite3.connect('database/database.sqlite')

# Creamos cursor para ejecutar consultas
cursor = conn.cursor() # type: ignore

# Cargamos los datos de una tabla en un df
query = f"SELECT * FROM {'apicall'};"
df_apicall = pd.read_sql_query(query, conn)

query = f"SELECT * FROM {'commerce'};"
df_commerce = pd.read_sql_query(query, conn)

#-----limpieza inicial----

# Unimos apicall y commerce
df = pd.merge(df_apicall, df_commerce, on='commerce_id')

# Filtramos las empresas activas
df = df[df['commerce_status'] == 'Active']

df['date_api_call'] = pd.to_datetime(df['date_api_call'])
#Cambiamos el tipo de datos a fecha ya que en un principio es  de tipo object

# Filtrar por julio y agosto de 2024
df = df[
    (df['date_api_call'].dt.month.isin([7, 8])) &
    (df['date_api_call'].dt.year == 2024)
]
print("Necesito que imprima algo")

#Función para calcular la comision, los descuentos y el iva
def calcular_comision(empresa, peticiones_exitosas, peticiones_no_exitosas):
    comision = 0

    # Calculamos la comisión base según el contrato de la empresa
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

    # Aplicamos descuentos sobre la comisión (antes de calcular el IVA)
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

    # Calculamos el IVA (19% sobre la comisión final)
    iva = comision * 0.19

    # Calculamos el valor total (comisión + IVA)
    valor_total = comision + iva

    # Retornamos la comisión, el IVA y el valor total
    return comision, iva, valor_total


print("Necesito que imprima otra cosa")