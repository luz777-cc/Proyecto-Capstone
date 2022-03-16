# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 19:36:49 2022

@author: mapor


Notas importantes: hace falta optimizar el código, eliminar métodos casi iguales, 
eliminar variables globales, organizar propiedades de los ejes y documentar con docstrings, entre otros.
"""

# IMPORTANTE: PARA QUE FUNCIONE CON KIVY, REINSTALAR CON PIP MATPLOTLIB 3.1.3 (DOWNGRADE)
import random
import numpy as np
from scipy.fft import fft, fftfreq, fftshift
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publisher

buffer = 512
valueRaw = [0]*buffer
valueFilt = [0]*buffer
params = 'params'
row = 0

subscription = ''

class MQTTconnector():
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.broker = '148.206.49.17'
        self.port = 1883
        self.topicRaw = "eegIoT/data"
        self.topicFilt = "eegIoT/data/Filtro" 
        self.topic_entrada = "eegIoT/data/frecuencias"       
        self.client_id_pub = f'eegIoTpub_{random.randint(0, 100)}'
        self.client_id_sub1 = f'eegIoTsub1_{random.randint(0, 100)}'        
        self.client_id_sub2 = f'eegIoTsub2_{random.randint(0, 100)}'        
        self.username = 'eegIoT'
        self.password = '1234'
        
    def on_connect(self, client, userdata, flags, rc):
        
        global params        
        print(params)
        client.publish(self.topic_entrada, params)
    
    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Conectado al broker...")
            else:
                print("Falla de conexión código: %d\n", rc)
                
        global subscription
        if subscription == 'raw':
            client = mqtt_client.Client(self.client_id_sub1)        
        else:
            client = mqtt_client.Client(self.client_id_sub2)            
        client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        
        return client
    
    def subscribeRaw(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            
            global valueRaw        
            
            val = msg.payload.decode("utf-8")
            x = val.split('[')
            x = x[1].split(']')
            x = x[0].split(',')
            
            valueRaw = [float(i) for i in x]            
            
        client.subscribe(self.topicRaw)
        client.on_message = on_message
        
    def subscribeFilt(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            
            global valueFilt        
            
            val = msg.payload.decode("utf-8")
            x = val.split('[')
            x = x[1].split(']')
            x = x[0].split(',')
            
            valueFilt = [float(i) for i in x]

        client.subscribe(self.topicFilt)                    
        client.on_message = on_message
    
    def run(self):
        global subscription
        
        subscription = 'raw'
        clientRaw = self.connect_mqtt()
        self.subscribeRaw(clientRaw)
        
        subscription = 'filt'
        clientFilt = self.connect_mqtt()
        self.subscribeFilt(clientFilt)
        
        clientRaw.loop_start()
        clientFilt.loop_start()
        
        
class CustomButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.font_size = "18sp"
       
class EEGreaderApp(App):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = list(range(buffer))
        self.dataRaw = [0]*buffer        
        self.dataFilt = [0]*buffer        
        
        self.fig = plt.figure (constrained_layout = True)        
        self.fig.set_facecolor((0.5,0.5,0.5))
        
        gs = GridSpec(3,2, figure = self.fig)
        self.axRaw = self.fig.add_subplot(gs[0,:])
        self.axRaw.set_facecolor((0.1,0.1,0.1))
        self.axRaw.set_title('EEG (Fpz) - raw',fontdict={'color':(0.9,0.9,0.9),'size':18})   

        self.axFilt = self.fig.add_subplot(gs[1,:])
        self.axFilt.set_facecolor((0.1,0.1,0.1))

        self.axFFTraw= self.fig.add_subplot(gs[-1, 0])
        self.axFFTraw.set_facecolor((0.1,0.1,0.1))

        self.axFFTfilt= self.fig.add_subplot(gs[-1, -1])
        self.axFFTfilt.set_facecolor((0.1,0.1,0.1))

        self.canvas = self.fig.canvas
        
        self.linesRaw, = self.axRaw.plot(self.time, self.dataRaw, 'm', linewidth=3)        
        self.linesFilt, = self.axFilt.plot(self.time, self.dataFilt, 'c', linewidth=3)        

        self.axFilt.set_title('EEG (Fpz) - filtered',fontdict={'color':(0.9,0.9,0.9),'size':18})        
        self.axRaw.set_ylim(-800, 800)      
        
        self.axRaw.tick_params(
                        # Los cambios aplican al eje x: 
                        axis='x',          
                        # Tanto ticks principales como menores son afectados:
                        which='both',      
                        # Se deshabilitan ticks en el eje de hasta abajo
                        bottom=False,      
                        # También los de hasta arriba
                        top=False,         
                        # Y también etiquetas del eje de hasta abajo:
                        labelbottom=False) 
        
        self.axFilt.set_ylim(-250, 250)              
        
        xf = fftfreq(buffer, 1/buffer)
        xf = fftshift(xf)
        self.linesFFTraw, = self.axFFTraw.plot(xf, [10]*buffer, 'm', linewidth=3)  
        self.axFFTraw.set_title('Raw signal PSD',fontdict={'color':(0.9,0.9,0.9),'size':18})
        self.axFFTraw.set_xlim(0, 90) 
        self.axFFTraw.set_ylim(0, 25)         
        
        self.linesFFTfilt, = self.axFFTfilt.plot(xf, [10]*buffer, 'c', linewidth=3)                
        self.axFFTfilt.set_title('Filtered signal PSD',fontdict={'color':(0.9,0.9,0.9),'size':18})
        self.axFFTfilt.set_xlim(0, 90) 
        self.axFFTfilt.set_ylim(0, 25) 

        # Para el layout de Kivy:
        self.grid = GridLayout()
        
    def press(self,button):
        
        if (button.text == "Delta"):
            self.freqA.text = "0.1"
            self.freqB.text = "4"
        elif (button.text == "Theta"):
            self.freqA.text = "4"
            self.freqB.text = "7"
        elif (button.text == "Alpha"):
            self.freqA.text = "7"
            self.freqB.text = "12"
        elif (button.text == "Beta"):
            self.freqA.text = "12"
            self.freqB.text = "30"
        elif (button.text == "Gamma"):
            self.freqA.text = "30"
            self.freqB.text = "60"
        else:
            global params 
            if (button.text == "Filter"):
                '''Publicar valores
                    - Si el usuario deja vacío el cuadro de texto
                    - Si coloca caracteres diferentes de números o punto
    
                    Se asigna cero a cualquiera de los text input                
                '''
                try:
                    a = str(float(self.freqA.text))                
                except:
                    self.freqA.text = '0'
                    a = '0'     
                finally:
                    try: 
                        b = str(float(self.freqB.text))
                    except:
                        self.freqB.text = '0'
                        b = '0'
                           
                params = a + " " + b
            if (button.text == "Start"):
                params = "true"
                self.rec.background_color = (1,0,0,0.6)
                
            if (button.text == "Stop"):
                params = "false"
                self.rec.background_color = (0,0,0,0)
        
            client1 = mqtt_client.Client(client_id=f'eegIoTpub_{random.randint(0, 100)}', clean_session=False)
            client1.on_connect = MQTTconnector().on_connect           
            client1.connect(host='148.206.49.17', port=1883)
            client1.loop_start()
            client1.loop_stop()
  
    def build(self):
        
        Window.clearcolor = (0.5,0.5,0.5,1)
        
        self.grid.rows = 3
        self.grid.padding = "10dp"
        self.grid.spacing = "10dp"
        
        box = BoxLayout(size_hint_y = None, height = "500 dp")        
        box.add_widget(self.canvas)
        self.grid.add_widget(box)
        
        box = BoxLayout(spacing = "10sp")        
        self.freqA = TextInput(font_size="15sp", multiline=False)
        self.freqB = TextInput(font_size="15sp", multiline=False)
        self.rec = CustomButton(background_color = (0,0,0,0))
        box.add_widget(self.rec)
        label = Label(text = "Low cut:", color = (0,0,0), font_size = "15sp", halign="right", valign="middle")
        label.bind(size=label.setter('text_size')) 
        box.add_widget(label)        
        box.add_widget(self.freqA)        
        label = Label(text = "High cut:", color = (0,0,0), font_size = "15sp", halign="right", valign="middle")
        label.bind(size=label.setter('text_size')) 
        box.add_widget(label)
        box.add_widget(self.freqB)       
        box.add_widget(CustomButton(text = "Filter", color = (0.9,0.9,0.0), on_press=self.press))        
        box.add_widget(CustomButton(text = "Start", color = (0.0,0.9,0.9), on_press=self.press))
        box.add_widget(CustomButton(text = "Stop", color = (0.0,0.9,0.9), on_press=self.press))
        
        self.grid.add_widget(box)
        
        box = BoxLayout(spacing = "7sp")
                
        box.add_widget(CustomButton(text = "Delta", color = (0.9,0.9,0.9), on_press=self.press))
        box.add_widget(CustomButton(text = "Theta", color = (0.9,0.9,0.9), on_press=self.press))
        box.add_widget(CustomButton(text = "Alpha", color = (0.9,0.9,0.9), on_press=self.press))
        box.add_widget(CustomButton(text = "Beta", color = (0.9,0.9,0.9), on_press=self.press))
        box.add_widget(CustomButton(text = "Gamma", color = (0.9,0.9,0.9), on_press=self.press))
        self.grid.add_widget(box)
        
        Clock.schedule_interval(self.update,0)
        return self.grid
     
    def update(self, *args):
        
        global valueRaw, valueFilt, valAcum, row, buffer
        
        self.dataRaw = valueRaw        
        self.dataFilt = valueFilt
        
        self.linesRaw.set_ydata(self.dataRaw)
        self.linesFilt.set_ydata(self.dataFilt)         
        
        yf = fft(self.dataRaw)
        yplot = fftshift(yf)        
        yplot = 1.0/buffer * np.abs(yplot)        
        
        self.linesFFTraw.set_ydata(yplot) 
        
        yf = fft(self.dataFilt)
        yplot = fftshift(yf)        
        yplot = 1.0/buffer * np.abs(yplot)  
        
        self.linesFFTfilt.set_ydata(yplot)
        
        self.canvas.draw_idle()
        self.canvas.flush_events()
        
mqttConn = MQTTconnector()        
eegReaderApp = EEGreaderApp()

if __name__ == '__main__':    
    mqttConn.run()
    eegReaderApp.run()  
    