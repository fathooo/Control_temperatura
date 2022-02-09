## Materiales:
- ESP8266 NODEMCU
- Sensor DHT11
- Modulo Relé 5volt
- Esterilla de calor para reptiles
- Modulo display
	
	![[attachments/Pasted image 20220209182455.png]]
	![[attachments/Pasted image 20220209182534.png]]
	![[attachments/Pasted image 20220209182556.png]]
	
## Funcionamiento:
- El funcionamiento es sencillo, mi intensión es poder regular la temperatura de un lugar cerrado cuando la temperatura es menor a 24 grados celcius, sirve para el cuidado de animales o para la regulación de temperaturas de plantas agregando un modulo relé con más capacidad de voltaje y amperes.

- Apliqué un rango de temperatura óptima en la que quiero que trabaje, cuando alcanza la temperatura minima se enciende el relé lo cual otorga energía a la esterilla de calor y cuando alcanza la temperatura maxima se apaga el relé, quitandole la energía a la esterilla de calor, disminuyendo así la temperatura, toda esta configuración la hago desde mi navegador.

- Desde mi computador o celular puedo entrar a mi navegador y ver la temperatura y humedad actual en tiempo real, la configuración que tengo actualmente de rango de temperatura y también puedo modificar la configuración con una temperatura minima y maxima y un usuario que servirá como autentificador. 

![[attachments/Pasted image 20220209135234.png]]
	
- Guardé los datos en la nube GCLOUD, más precisamente en RealtimeDatabase.	
	
![[attachments/Pasted image 20220209133653.png]]

-Como se puede ver,  guardo los grados Celcius, la humedad, la fecha y la hora, más adelante descargaremos los datos en json y utilizaré expresiones regulares para poder trabajar con los datos.

![[attachments/Pasted image 20220209143752.png]]

- Hasta acá tenemos el proyecto funcionando y recopilando los datos para su monitorización.

## Analisis de datos

- Para el anasis utilizo python ya que puedo hacer el ordenamiento de la información y realizar graficos.

- Ya que la información viene raw separado con un pipe " | ", utilizo expresiones regulares para ordenar la información y dejarlo en un dataframe con pandas.
 
![[attachments/Pasted image 20220209170624.png]]

- Mi configuración de temperatura era de 27 grados minimo y 28 grados maximo, después de hacer un analisis descriptivo de los datos, podemos determinar que: 

![[attachments/Pasted image 20220209170354.png]]

- Tenemos un total de datos de 2824, con un media de 27.67 grados y una desviación estandar de 0.18, los datos muestran que se alcanzó un minimo de 22.6 grados y un maximo de 29.10. Si ordenamos los datos podemos notar que dentro del 25% la temperatura alcanzada está en los 27.6 grados, el 50% se encuentra el 27.7 grados y el 75% está  27.8 grados por lo que es consistente

- Contamos la cantidad de datos por cada temperatura alcanzada:

![[attachments/Pasted image 20220209170444.png]]

- En el siguiente grafico podemos ver la temperatura promedio en los últimos 7 dias

![[attachments/Pasted image 20220209180204.png]]

- El siguiente grafico son las dos últimas semanas.
![[attachments/Pasted image 20220209181945.png]]

- Podemos notar que existe una correlación débil entre humedad y temp.

![[attachments/Pasted image 20220209172120.png]]
![[attachments/Pasted image 20220209174502.png]]

- El siguiente gráfico de puntos lo confirma (temperatura y humedad promedio por día).
![[attachments/Pasted image 20220209172456.png]]

- Gráfico del total de temperatura y humedad por dia:
![[attachments/Pasted image 20220209172738.png]]


```py
#%%

import json

import re

import matplotlib.pyplot as plt

import pandas as pd

import seaborn as sns

  
  

def data\_json():

 with open('arduino.json') as file:

 data \= json.load(file)

 data \= data\['Tem\_Hum'\]\["Temp"\].items()

 return data

  
  

def lista\_temp(data):

 temp \= re.compile(r'(\\(\\'.{1,20}\\', \\')?(\\d\\d.\\d\\d) C \\| (\\d\\d.\\d\\d) H \\| (\\d\\d/\\d\\d/\\d\\d\\d\\d) (\\d\\d:\\d\\d:\\d\\d)')

 data \= data\_json()

 lista\_datos \= \[\]

 dict\_datos \= \[\]

  

 for i in data:

 i \= str(i)

 lista\_datos.append(i)

 temperatura \= temp.search(i)

 tempe \= temperatura.group(2)

 hum \= temperatura.group(3)

 dia \= temperatura.group(4)

 hora \= temperatura.group(5)

 dict\_datos.append({"temp": float(tempe), "hum" : float(hum), "dia" : str(dia+' '+hora)})

  

 return dict\_datos

  

def transform\_dias\_dtype(df):

 df\_copy \= df.copy(deep\=True)

  

 df\_copy\['dia'\] \= pd.to\_datetime(

 df\_copy\['dia'\],

 errors \= 'coerce',

 format \='%d/%m/%Y %H:%M:%S'

 )

  

 df\_meanday \= df\_copy.groupby(pd.Grouper(key\='dia', freq\='d')).mean()

 df\_meanday.dropna(inplace\=True)

 return df\_meanday

  
  

#%%

if \_\_name\_\_ \== "\_\_main\_\_":

 df \= pd.DataFrame()

 data \= lista\_temp(data\_json())

 for i in data:

 df \= df.append(i, ignore\_index \= True)

 t \= df\['temp'\]

 print('--------------')

 print(t.describe())

 print('--------------')

 print(t.value\_counts())

 print('--------------')

 h \= df\['hum'\]

 print('--------------')

 print(h.describe())

 print('--------------')

 print(h.value\_counts())

 print('--------------')

  

 print(pd.Series(h))

 print(df.dtypes)

  

 df\_meanday \= transform\_dias\_dtype(df)

  

 #Correlación temp y humedad

 df.corr()

 sns.heatmap(df.corr(), annot\=True)

 #Plot de lineas de temperatura y dias

 ax \= sns.lineplot(data \= df\_meanday.iloc\[\-8:\-1\], x \= 'dia', y \= 'temp')

 plt.xticks(rotation\=45)
```


```arduino
#include <DHT.h>
#include <LiquidCrystal_I2C.h>
 
#define DHTTYPE DHT11
#define PIN_CALEFACTOR D0

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <FirebaseESP8266.h>
#include <EEPROM.h>

#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>
#include <time.h>


int periodoip = 2000;
unsigned long Tiempoip = 0;


int periodolcd = 4000;
unsigned long Tiempolcd= 0;

int periodotemp = 2000;
unsigned long Tiempotemp = 0;

// 20 minutos
int periodopush_firebase = 1200000;
//int periodopush_firebase = 3000;
unsigned long Tiempopush_firebase = 0;

float t = 0;
float h = 0;


//Wifi / pag_web port 80
#define WIFI_SSID "WIFIUSER****"
#define WIFI_PASSWORD "password****"
ESP8266WebServer server(80);


//---

//Firebase 
FirebaseData fbdo;


const char *FIREBASE_HOST = "FIREBASEHOST****";
const char *FIREBASE_AUTH = "AUTH****";
FirebaseData firebaseData;

//---

//EEPROM CONFIGURATION
#define EEPROM_SIZE 512

int addr = 0;
int addr1 = 18;

float tempmin;
float tempmax;
float tempmin_read;
float tempmax_read;

// Definimos el pin digital donde se conecta el sensor
uint8_t DHTPin = D4;

// set the LCD number of columns and rows
int lcdColumns = 16;
int lcdRows = 2;

// Inicializamos el sensor DHT11
DHT dht(DHTPin , DHTTYPE);
LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows);  


float temp_MIN =  24;
float temp_MAX = 25;


// Reloj
WiFiUDP ntpUDP;
static tm getDateTimeByParams(long time){
    struct tm *newtime;
    const time_t tim = time;
    newtime = localtime(&tim);
    return *newtime;
}

static String getDateTimeStringByParams(tm *newtime, char* pattern = (char *)"%d/%m/%Y %H:%M:%S"){
    char buffer[30];
    strftime(buffer, 30, pattern, newtime);
    return buffer;
}

static String getEpochStringByParams(long time, char* pattern = (char *)"%d/%m/%Y %H:%M:%S"){
//    struct tm *newtime;
    tm newtime;
    newtime = getDateTimeByParams(time);
    return getDateTimeStringByParams(&newtime, pattern);
}


int GTMOffset = 1;
NTPClient timeClient(ntpUDP, "europe.pool.ntp.org", GTMOffset*60*60, 60*60*1000);
//----------------



void setup() {
    // Comenzamos el sensor DHT
    dht.begin();
    lcd.init();               
    lcd.backlight();
    //lcd.noBacklight();
    // initialize digital pin LED_BUILTIN as an output.
    pinMode(D0, OUTPUT);
    Serial.begin(9600);

      // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    }
    
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());


  timeClient.begin();
  timeClient.setTimeOffset(-14400);
  delay ( 1000 );
  if (timeClient.update()){
     Serial.print ( "Adjust local clock" );
     unsigned long epoch = timeClient.getEpochTime();
     // HERE I'M UPDATE LOCAL CLOCK
     setTime(epoch);
  }else{
     Serial.print ( "NTP Update not WORK!!" );
  }
  
  server.on("/", HTTP_GET, handleRoot);       
  server.on("/change_data", HTTP_POST, handle_change_data); 
  server.onNotFound(handleNotFound);          
  server.begin();
  
  Serial.println("HTTP server started");
  EEPROM.begin(EEPROM_SIZE);
  EEPROM.get(addr, tempmin_read);
  EEPROM.get(addr1, tempmax_read);
  temp_MIN = tempmin_read;
  temp_MAX = tempmax_read;
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);


}

  void loop() {
    if(millis() - Tiempotemp > periodotemp){ 
      Tiempotemp = millis();
      h = dht.readHumidity();
      t = dht.readTemperature();
  
      if (isnan(h) || isnan(t)) {
        digitalWrite(D0, HIGH);
        return;
        }

     //Histéresis del calefactor
     if(t <= temp_MIN){
      digitalWrite(D0, LOW);
      lcd.setCursor(0,1);
      Serial.println("ON");
      lcd.print("ON ");
      }

    if(t >= temp_MAX){
      digitalWrite(D0, HIGH);
      lcd.setCursor(0,1);
      Serial.println("OFF");
      lcd.print("OFF");
      }
      
    }

    if(millis() - Tiempolcd > periodolcd){ 
      Tiempolcd = millis();

      // Comprobamos si ha habido algún error en la lectura
      if (isnan(h) || isnan(t)) {
        lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("Error datos DHT11");
        digitalWrite(D0, HIGH);
        return;
        }
        
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print(t);
      lcd.setCursor(5,0);
      lcd.print("C");
      lcd.setCursor(8,0);
      lcd.print(h);
      lcd.setCursor(13,0);
      lcd.print("H");    
     }

     if(millis() - Tiempopush_firebase > periodopush_firebase){ 
      Tiempopush_firebase = millis();
      timeClient.update();
      String dia = getEpochStringByParams(now());
      String nodo = "Tem_Hum"; 
      String temp = String(t);
      String hum = String(h);
      String parrafo = temp + " C " + "| " + hum + " H " + "| " + dia;

      Serial.println("mandando datos firebase");
 
      Firebase.pushString(firebaseData, nodo + "/Temp", parrafo);

      Serial.println("datos enviados");
     }
     
     if(millis() - Tiempoip> periodoip){ 
      Tiempoip= millis();
        lcd.setCursor(4,1);
        lcd.print(WiFi.localIP());
      }
  server.handleClient();
}



/* -------------------------------------------------------------------------------Config de App_web*/

void handleRoot() {

  server.send(200, "text/html", SendHTML());
}

void handleNotFound(){
  server.send(404, "text/plain", "404: Not found"); 
}

void handle_change_data(){
if( ! server.hasArg("temp_Min") || ! server.hasArg("temp_Max") || ! server.hasArg("usuario") 
      || server.arg("temp_Min") == NULL || server.arg("temp_Max") == NULL || server.arg("usuario") == NULL) { // Request without data
    server.send(400, "text/plain", "400: Invalid Request");         // Print Data on screen
    return;
  }

  if( server.hasArg("temp_Min") and server.hasArg("temp_Max") and  server.arg("usuario") == "lol123" ) {
      const String temp_min = server.arg("temp_Min");
      const String temp_max = server.arg("temp_Max");
      float num_min = temp_min.toFloat();
      float num_max = temp_max.toFloat();
      
     if( num_min < num_max ){
      temp_MIN =  temp_min.toFloat();
      temp_MAX =  temp_max.toFloat();
      
      EEPROM.put(addr, temp_MIN);
      addr += sizeof(temp_MIN);
      bool datos = EEPROM.commit();
       if(datos)
          { Serial.println("Write successfully addr1");
          }else {    Serial.println("Write error");}    
          
      EEPROM.put(addr1, temp_MAX);
      addr1 += sizeof(temp_MAX); 
      bool datos1 = EEPROM.commit();
       if(datos1)
          { Serial.println("Write successfully addr2");
          }else {    Serial.println("Write error");}

      Serial.print("--------------- \n");
      Serial.println(temp_MIN);
      Serial.println(temp_MAX);
      Serial.print("--------------- ");

      handleRoot();
      
      
      }else{server.send(400, "text/plain", "400: Invalid Request");        
      return;}
  }}


String SendHTML(){
  String ptr = "<!DOCTYPE html> <html>\n";
  ptr +="<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=no\">\n";
  ptr +="<title>ESP8266 Weather Report</title>\n";
  ptr +="<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}\n";
  ptr +="body{margin-top: 50px;} h1 {color: #444444;margin: 50px auto 30px;}\n";
  ptr +="p {font-size: 24px;color: #444444;margin-bottom: 10px;}\n";
  ptr +="</style>\n";
  ptr +="</head>\n";
  ptr +="<body>\n";
  ptr +="<div id=\"webpage\">\n";
  ptr +="<h1>Temperatura y Humedad";
  
  ptr +="<p>Temperatura: ";
  ptr +=(float)t;
  ptr +="C</p>";
  ptr +="<p>Humedad: ";
  ptr +=(float)h;
  ptr +="%</p>";
 
  ptr +="</div>\n";

  ptr +="<div id=\"separador\">\n";
  ptr += "<h1> ------------------------------------------------------------------------------- "; 
  ptr +="</div>\n";

 ptr +="<div id=\"Datos_configuracion\">\n";
  ptr += "<h1> configuracion actual : "; 
  ptr +="<p>Temp. Min: ";
  ptr += (float)temp_MIN;
  ptr +="C</p>";
  ptr +="<p>Temp Max ";
  ptr += (float)temp_MAX;
  ptr +="C</p>";
  ptr +="</div>\n";

  ptr +="<div id=\"separador\">\n";
  ptr += "<h1> ------------------------------------------------------------------------------- "; 
  ptr +="</div>\n";
  
  ptr +="<div id=\"Formulario\">\n";
  ptr += " <p>Configura una temperatura.</p>";
  ptr  += "<form action=\"/change_data\" method=\"POST\">";
  ptr += "<input type=\"number\"  step=\"0.01\" name=\"temp_Min\" placeholder=\"temp_Min\">";
  ptr += "</br>";
  ptr += "<input type=\"number\" step=\"0.01\" name=\"temp_Max\" placeholder=\"temp_Max\">";
  ptr += "</br>";
  ptr += "<input type=\"password\"  name=\"usuario\" placeholder=\"usuario\">";
    ptr += "</br>";
  ptr += "<input type=\"submit\" value=\"Aceptar\">";
  ptr += "</form>";
  ptr += "\n";
  ptr +="</div>\n";

 

  ptr +="</body>\n";
  ptr +="</html>\n";
  return ptr;
}
```