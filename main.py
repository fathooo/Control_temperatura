#%%
import json
import re 
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns 


def data_json():
    with open('arduino.json') as file:
        data = json.load(file)
        data = data['Tem_Hum']["Temp"].items()
    return data


def lista_temp(data):
    temp = re.compile(r'(\(\'.{1,20}\', \')?(\d\d.\d\d) C \| (\d\d.\d\d) H \| (\d\d/\d\d/\d\d\d\d) (\d\d:\d\d:\d\d)')
    data = data_json()
    lista_datos = []
    dict_datos = []

    for i in data:
        i = str(i)
        lista_datos.append(i)
        temperatura = temp.search(i)
        tempe = temperatura.group(2)
        hum = temperatura.group(3)
        dia = temperatura.group(4)
        hora = temperatura.group(5)
        dict_datos.append({"temp": float(tempe), "hum" : float(hum), "dia" : str(dia+' '+hora)})

    return dict_datos

def transform_dias_dtype(df):
    df_copy = df.copy(deep=True)

    df_copy['dia'] = pd.to_datetime(
        df_copy['dia'],
        errors = 'coerce',
        format ='%d/%m/%Y %H:%M:%S'
        )

    df_meanday = df_copy.groupby(pd.Grouper(key='dia', freq='d')).mean()
    df_meanday.dropna(inplace=True)
    return df_meanday


#%%
if __name__ == "__main__":
    df = pd.DataFrame()
    data = lista_temp(data_json())
    for i in data:
        df = df.append(i, ignore_index = True)
    
    t = df['temp']
    print('--------------')
    print(t.describe())
    print('--------------')
    print(t.value_counts())
    print('--------------')
  
    h = df['hum']
    print('--------------')
    print(h.describe())
    print('--------------')
    print(h.value_counts())
    print('--------------')

    print(pd.Series(h))
    print(df.dtypes)

    df_meanday = transform_dias_dtype(df)

    #Correlación temp y humedad
    df.corr()
    sns.heatmap(df.corr(), annot=True)
    #Plot de lineas de temperatura y dias
    ax = sns.lineplot(data = df_meanday.iloc[-8:-1], x = 'dia', y = 'temp')
    plt.xticks(rotation=45)