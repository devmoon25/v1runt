import pandas as pd
import ast

df_total = pd.read_excel(r"C:\Users\rcDMZConfig\Desktop\RUNT\RUNT\Insumos\runt.xlsx")

# Convertir la columna 'soat' de cadena a lista de listas
df_total['soat'] = df_total['soat'].apply(ast.literal_eval)

# Crear un nuevo DataFrame con la columna 'soat'
df_soat = pd.DataFrame(df_total['soat'].tolist(), columns=['numero_poliza_soat', 'fecha_exp_soat', 'fecha_ini_soat', 'fecha_fin_soat', 'cod_tarifa_soat', 'entidad_soat', 'estado_soat'])

# Eliminar la columna original 'soat'
df_total.drop('soat', axis=1, inplace=True)

# Asignar el nuevo DataFrame a df_total
df_total = pd.concat([df_total, df_soat], axis=1)

# Convertir la columna 'tecnomecanica' de cadena a lista de listas
df_total['tecnomecanica'] = df_total['tecnomecanica'].apply(ast.literal_eval)

# Crear un nuevo DataFrame con la columna 'tecnomecanica'
df_tecno = pd.DataFrame(df_total['tecnomecanica'].tolist(), columns=['tipo_revision_tecno', 'fecha_exp_tecno', 'fecha_vigencia_tecno', 'cda_tecno', 'vigente_tecno', 'nro_cert_tecno', 'info_consistente_tecno'])

# Eliminar la columna original 'tecnomecanica'
df_total.drop('tecnomecanica', axis=1, inplace=True)

# Asignar el nuevo DataFrame a df_total
df_total = pd.concat([df_total, df_tecno], axis=1)

# Convertir la columna 'solicitudes' de cadena a lista de listas
df_total['solicitudes'] = df_total['solicitudes'].apply(ast.literal_eval)

# Crear un nuevo DataFrame con la columna 'solicitudes'
df_solicitudes = pd.DataFrame(df_total['solicitudes'].tolist(), columns=['nro_solicitud_tsp', 'fecha_solicitud_tsp', 'estado_tsp', 'tramites_tsp', 'entidad_tsp'])

# Eliminar la columna original 'solicitudes'
df_total.drop('solicitudes', axis=1, inplace=True)

# Asignar el nuevo DataFrame a df_total
df_total = pd.concat([df_total, df_solicitudes], axis=1)

# Guardar el DataFrame en un archivo Excel
df_total.to_excel(r"C:\Users\rcDMZConfig\Desktop\RUNT\RUNT\Insumos\runt2.xlsx", index=False)




