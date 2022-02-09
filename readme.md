## Materiales:
- ESP8266 NODEMCU
- Sensor DHT11
- Modulo Relé 5volt
- Esterilla de calor para reptiles
- Modulo display
	
	![20220209182455.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209133653.png)
	![20220209182534.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209182534.png)
	![20220209182556.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209182556.png)
	
## Funcionamiento:
- El funcionamiento es sencillo, mi intensión es poder regular la temperatura de un lugar cerrado cuando la temperatura es menor a 24 grados celcius, sirve para el cuidado de animales o para la regulación de temperaturas de plantas agregando un modulo relé con más capacidad de voltaje y amperes.

- Apliqué un rango de temperatura óptima en la que quiero que trabaje, cuando alcanza la temperatura minima se enciende el relé lo cual otorga energía a la esterilla de calor y cuando alcanza la temperatura maxima se apaga el relé, quitandole la energía a la esterilla de calor, disminuyendo así la temperatura, toda esta configuración la hago desde mi navegador.

- Desde mi computador o celular puedo entrar a mi navegador y ver la temperatura y humedad actual en tiempo real, la configuración que tengo actualmente de rango de temperatura y también puedo modificar la configuración con una temperatura minima y maxima y un usuario que servirá como autentificador. 

![20220209135234.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209135234.png)
	
- Guardé los datos en la nube GCLOUD, más precisamente en RealtimeDatabase.	
	
![20220209133653.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209133653.png)

-Como se puede ver,  guardo los grados Celcius, la humedad, la fecha y la hora, más adelante descargaremos los datos en json y utilizaré expresiones regulares para poder trabajar con los datos.

![20220209143752.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209143752.png)

- Hasta acá tenemos el proyecto funcionando y recopilando los datos para su monitorización.

## Analisis de datos

- Para el anasis utilizo python ya que puedo hacer el ordenamiento de la información y realizar graficos.

- Ya que la información viene raw separado con un pipe " | ", utilizo expresiones regulares para ordenar la información y dejarlo en un dataframe con pandas.
 
![20220209170624.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209170624.png)

- Mi configuración de temperatura era de 27 grados minimo y 28 grados maximo, después de hacer un analisis descriptivo de los datos, podemos determinar que: 

![20220209170354.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209170354.png)

- Tenemos un total de datos de 2824, con un media de 27.67 grados y una desviación estandar de 0.18, los datos muestran que se alcanzó un minimo de 22.6 grados y un maximo de 29.10. Si ordenamos los datos podemos notar que dentro del 25% la temperatura alcanzada está en los 27.6 grados, el 50% se encuentra el 27.7 grados y el 75% está  27.8 grados por lo que es consistente

- Contamos la cantidad de datos por cada temperatura alcanzada:

![20220209170444.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209170444.png)

- En el siguiente grafico podemos ver la temperatura promedio en los últimos 7 dias

![20220209180204.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209180204.png)

- El siguiente grafico son las dos últimas semanas.
![20220209181945.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209181945.png)

- Podemos notar que existe una correlación débil entre humedad y temp.

![20220209172120.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209172120.png)
![20220209174502.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209174502.png)

- El siguiente gráfico de puntos lo confirma (temperatura y humedad promedio por día).
![20220209172456.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209172456.png)

- Gráfico del total de temperatura y humedad por dia:
![20220209172738.png](https://github.com/fathooo/Control_temperatura/blob/main/attachments/Pasted%20image%2020220209172738.png)

