#   Librerias 
import paho.mqtt.client


class Conectar():
    '''
        Está clase se encarga de la conexión al broker MQTT
    '''
    def __init__(self):
        self.broker = '148.206.49.17' # Broker a conectar
        self.port = 1883    #   Puerto
        self.topic_entrada = "eegIoT/data/frecuencias" 
        self.client_id = 'luz_PublicaIoT'
        self.client_idLuz = 'LuzSuscribeIoT'
        self.username = 'eegIoT'
        self.password = '1234'
        
    def on_connect(self, client, userdata, flags, rc):
        '''
            Este procedimiento se encarga de mantener la conexión por medio de un cliente suscrito
        '''
        print('connected (%s)' % client._client_id)
        client.subscribe(self.topic_entrada, qos=0) #   El cliente se suscribe.

    def on_message(self, client, userdata, message):
        '''
            Este procedimiento, tiene como fin recibir los mensajes del topic suscrito y 
            guardarlos (temporalmente) en un archivo de texto. Estos datos se utilizaran 
            para el código que pública los datos de la señal de EEG.
        '''
        print('------------------------------')
        a = message.payload.decode() #  'a' es una varible que contiene las instrucciones enviadas desde NODE-red
        print(type(a))
        if a == 'true' or a == 'false': #   Si 'a' tiene como valor 'true' o 'false', entra.
            print(a)
            fichero = open('almacenar.txt', 'w') # Abre un archivo de tezto en forma de escritura
            fichero.write(a) # Escribe en el archivo el contenido de 'a'
            fichero.close() # Se cierra el archivo de texto 
        elif len(a.split(' ')) == 2: #convertimos la variable a lista son los espacios, para ser analizados
                                     #entonces, si el tamaño de la lista contiene 2 elemtons (quiere decir que se mandaron los rangos de frecuencias para el filtro), entra a la condición
            print('con split ',a)
            fichero = open('datos.txt', 'w')
            fichero.write(a)
            fichero.close()
        else:
            print("dato erroneo")

    def run(self):
        '''
            Este procedimiento, crea instancias de un cliente, para después ser conectado y 
            después recibir mensajes.
        '''
        client = paho.mqtt.client.Client(client_id='luz-subsIoT', clean_session=False) #    instancia de un cliente
        client.on_connect = self.on_connect #   Conectar al cliente como suscriptor 
        client.on_message = self.on_message #   cliente recibe los mesajes al topico suscrito
        client.connect(self.broker, self.port) # conexión al broker público y el puerto 
        
        client.loop_forever()

if __name__ == '__main__':
    Conectar().run()
