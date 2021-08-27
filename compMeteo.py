import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib

# Input
pathObs = 'D:/CPERv/reporteAgosto/' # direccion observaciones
pathWRF = 'D:/CPERv/reporteAgosto/' # direccion pronostico WRF
fileObs = 'MesObservaciones.csv' # nombre del archivo csv observado
fileWRF = 'WRF_data/2021-07-22.csv' # nombre del archivo csv WRF extraido previamente
datetimetagObs = 'TIME_STAMP' # nombre de la etiqueta para la columna datetime
datetimetagWRF = 'Time' # nomnbre de la etiqueta para la columna datetime
granularidad = 5 # en minutos de tipo entero
start_date = '2021-07-23' # Inicio de datos para analisis
end_date = '2021-07-24' # fin de datos para analisis
# Lectura observados
df = pd.read_csv(pathObs+'/'+fileObs)
df[datetimetagObs] = pd.to_datetime(df[datetimetagObs])
df.sort_values(by=[datetimetagObs],inplace=True)
df.drop_duplicates(subset=[datetimetagObs], keep='last', inplace=True)
# lectura de pronostico
dfp =pd.read_csv(pathWRF+'/'+fileWRF)
dfp[datetimetagWRF] = pd.to_datetime(dfp[datetimetagWRF])
dfp.sort_values(by=[datetimetagWRF],inplace=True)
dfp.drop_duplicates(subset=[datetimetagWRF], keep='last',inplace=True)
df.index = df[datetimetagObs]
dfp.index = dfp[datetimetagWRF]
dfp.fillna(0,inplace=True)
del df[datetimetagObs]
del dfp[datetimetagWRF]
# regularizar datos observados a un periodo fijo de granularidad (EX. 5min)
# debido a que WRF con paso adaptativo genera salidas con segundos de retraso
dfp.index = dfp.index.floor(str(granularidad)+'min')
# Generar la mascara para comparar los datos en un intervalo de tiempo de analisis
mask = (df.index > start_date) & (df.index<= end_date)
df = df.loc[mask]
mask = (dfp.index > start_date) & (dfp.index<= end_date)
dfp = dfp.loc[mask]
df_Total = df.merge(dfp, left_index=True, right_index=True)
df_Total = df_Total.resample(str(granularidad)+'min').first()
print(df_Total)
print(df_Total.info())
