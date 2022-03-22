#   Librerias 
#import time
import serial
#import numpy as np
#import matplotlib.pyplot as plt
from scipy import io
from scipy.signal import butter, filtfilt 
from paho.mqtt import client as mqtt_client
from datetime import datetime

#   Las siguientes 3 líneas se ejecutan en la terminal de la Raspberry pi 4
# hcitool scan
# sdptool records 24:71:89:EC:69:DC
# sudo rfcomm bind 0 24:71:89:EC:69:DC 1

#   Datos necesarios para conexión MQTT 
broker = '148.206.49.17'
port = 1883
topic = "eegIoT/data"
topicFilt = "eegIoT/data/Filtro"
client_id = 'luz_publica'
username = 'eegIoT'
password = '1234'

#   variables globales incializadas con marcas de tiempo. Se utilizaran para controlar y registrar los datos de la señal EEG.
dt1 = datetime.now()
dt2 = datetime.now()

def connect_mqtt():
    '''
        Procedimiento que se encarga de establecer la conexión a MQTT
    '''
    def on_connect(client, userdata, flags, rc):
        '''
            Procedimiento anidado que imprime, soi la conexión al broker MQTT es exitosa o no.
        '''
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id) 
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    '''
        Este procedimiento se encarga de publicar los datos de la señal EEG en crudo y filtrada.
    '''
    SYNC = 0xAA
    EXCODE = 0x55
    CODES = {0x02: 'POOR_SIGNAL',
             0x04: 'ATTENTION',
             0x05: 'MEDITATION',
             0x16: 'BLINK',
             0x80: 'RAW',
             0x83: 'ASIC_EEG_POWER'}

    #   Declaración de variables globales, estas variables su tipo de dato será una lista.
    global data
    global dataFilt
    
    time = list(range(512))
    data = [0]*512
    dataFilt = [0]*512
   
    print('*********')

    def parse(payload):
        '''
            Este procedimiento, se encarga de analizar los datos de la diadema Neurosky
        '''
        global i
        i = []
        global data
        payload_parser_state = 'new_data_row'
        for byte in payload:
            count = 1
            if payload_parser_state == 'new_data_row':
                if byte == EXCODE:
                    nex = 1
                    payload_parser_state = 'excode'
                else:
                    code = byte
                    payload_parser_state = 'decoded'
            elif payload_parser_state == 'excode':
                if byte == EXCODE:
                    nex += 1
                    payload_parser_state = 'excode'
                else:
                    code = byte
                    payload_parser_state = 'decoded'
            elif payload_parser_state == 'decoded':
                if code < 0x80:
                    value = byte
                    #print('{}: {}'.format(CODES[code], value))
                    if CODES[code] == 'POOR_SIGNAL' and value > 0:
                        print('mala señal')
                    payload_parser_state = 'new_data_row'
                else:
                    vlength = byte
                    values = []
                    payload_parser_state = 'multiple'
            elif payload_parser_state == 'multiple':
                if vlength > 0:
                    values.append(byte)
                    vlength -= 1
                    if vlength > 0:
                        payload_parser_state = 'multiple'
                    else:
                        if CODES[code] == 'RAW':
                            value = values[0] * 256 + values[1]
                            if value > 32767:
                                value -= 65536
                            data = data[1:] + [value]
                            
                            global dt2, dt1
                            #filtro
                            global dataFilt
                            
                            fichero = open('datos.txt', 'r') # abre el archivo de texto en modo lectura
                            a = fichero.read() #    Lee el archivo 
                            print(a)
                            mm = a.split(' ') # Extrae la información en tipo lista para utilizar el rango de frecuencias que se ocuparan para el filtro pasa-banda
                            
                            ws = 512 #  frecuencia de muestreo
                            #   Convierte los datos de la lista en flotantes 
                            ent = float(mm[0]) 
                            sal = float(mm[1])
                            NOrden = 4 #Número de orden del filtro
                            
                            b, a= butter(NOrden,[ent,sal], fs =ws, btype ='band') # Filtro butterworth pasa-banda
                            dataFilt = list(filtfilt(b, a, data)) # Almacena los datos de la señal EEG en una lista
                            dt2 = datetime.now() 
                            fichero = open('almacenar.txt', 'r')    # abre el archivo de texto en modo lectura
                            almacena = fichero.read() #    Lee el archivo y almacena los datos en una variable (los datos son 'true' o 'false'
                            
                            if almacena == 'true': 
                                '''
                                    En esta condición si la valiable almancena es true, entonces los datos de la señal EEG
                                    se irán guardando en un archivo de texto con su respectiva marca de tiempo.
                                '''
                                fichero = open('./texto.txt', 'a', encoding ='utf-8')
                                fichero.write(str(dt2)+(' ')+str(data)+('\n')) #    Aquí se empieza a escribir los datos se la señal EEG en el archivo de texto
                                dt2 = datetime.now()
                                diferencia = (dt2-dt1) #    Se realiza para después saber en que momento se enviarán los datos 
                                                       #    al broker MQTT y así ser vislumbrados en el entorno grafico de NODE-red
                                total_s = diferencia.total_seconds() #  La diferencia la pasamos a segundos y se almacena en la variable
                                
                                if total_s >= 0.25: 
                                    '''
                                        Si la varible total_s es igual o mayor a 0.25 segundos, entonces se empezará a
                                        publicar los dato de la señal de EEG tanto los datos en crudo y filtrados.
                                    '''
                                    dt1 = datetime.now()   
                                    client.publish(topic, str(data))
                                    client.publish(topicFilt, str(dataFilt))
                                    
                                fichero = open('almacenar.txt', 'r')
                                almacena = fichero.read()
                                
                            
                            diferencia = (dt2-dt1)
                            total_s = diferencia.total_seconds()
                            if total_s >= 0.25:
                                dt1 = datetime.now()   
                                client.publish(topic, str(data))
                                client.publish(topicFilt, str(dataFilt))
                           
                        if CODES[code] == 'ASIC_EEG_POWER':
                            value = []
                            for i in range(0,24,3):
                                value.append(values[i]+values[i+1]*256+values[i+2]*256*256)
                            total = sum(value)
                            if total > 0:
                                value = [v/total for v in value]
                        payload_parser_state = 'new_data_row'
        

    inp = serial.Serial('/dev/rfcomm0', baudrate=57600) # Establece la comunicación serial
    parser_state = 'idle'

    with inp:
        dt1 = datetime.now()
        while(1):
            byte = int.from_bytes(inp.read(), byteorder='little', signed=False)
            if byte == SYNC and parser_state == 'idle':
                parser_state = 'sync01'
            elif byte == SYNC and parser_state == 'sync01':
                parser_state = 'sync02'
            elif byte == SYNC and parser_state == 'sync02':
                parser_state = 'sync02'
            elif byte > SYNC and parser_state == 'sync02':
                parser_state = 'idle'
            elif byte < SYNC and parser_state == 'sync02':
                count = byte
                payload = []
                checksum = 0
                parser_state = 'packet'
            elif parser_state == 'packet' and count > 0:
                count -= 1
                payload.append(byte)
                checksum += byte
            elif parser_state == 'packet' and count == 0:
                if (checksum & 0xFF) ^ 0xFF == byte:
                    parse(payload)
                else:
                    print('packet con error')
                parser_state = 'idle'
        
def run():
    client = connect_mqtt() #   Se crea una instancia 
    client.loop_start() 
    publish(client)


if __name__ == '__main__':
    '''
        El main principal va a dejar el archivo de texto (se encarga de regitrar la señal) en limpio. 
    '''
    fichero = open('texto.txt', 'w') 
    fichero.write(' ')
    fichero.close()
    run()
