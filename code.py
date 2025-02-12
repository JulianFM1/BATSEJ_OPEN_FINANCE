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