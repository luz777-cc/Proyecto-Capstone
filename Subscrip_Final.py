import paho.mqtt.client


class Conectar():
    def __init__(self):
        self.broker = '148.206.49.17'
        self.port = 1883
        self.topic_entrada = "eegIoT/data/frecuencias"
        self.client_id = 'luz_PublicaIoT'
        self.client_idLuz = 'LuzSuscribeIoT'
        self.username = 'eegIoT'
        self.password = '1234'
        
    def on_connect(self, client, userdata, flags, rc):
        print('connected (%s)' % client._client_id)
        client.subscribe(self.topic_entrada, qos=0)        

    def on_message(self, client, userdata, message):
        print('------------------------------')
        a = message.payload.decode()
        print(type(a))
        if a == 'true' or a == 'false':
            print(a)
            fichero = open('almacenar.txt', 'w')
            fichero.write(a)
            fichero.close()
        elif len(a.split(' ')) == 2:
            print('con split ',a)
            fichero = open('datos.txt', 'w')
            fichero.write(a)
            fichero.close()
        else:
            print("dato erroneo")

    def run(self):
        client = paho.mqtt.client.Client(client_id='luz-subsIoT', clean_session=False)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.broker, self.port)
        
        client.loop_forever()

if __name__ == '__main__':
    Conectar().run()