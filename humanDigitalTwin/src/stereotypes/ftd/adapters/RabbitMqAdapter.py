import paho.mqtt.client as mqtt
import json
from stereotypes.ftd.sub_domain.ports import CommunicationStereotype


class RabbitMqAdapter(CommunicationStereotype):
#TODO adapt to rabbit mq    
    def __init__(self):
        self.client = mqtt.Client()
        
    def setup(self, broker_address:str, port:int, topics:list):
        
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(self.broker_address, port=self.port)
        self.client.loop_start()

        while not self.connected:
            pass

    def stop(self):
        self.client.loop_stop()
        print("Client stopped")

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code "+str(rc))
        self.client.subscribe(self.in_topic)
        self.connected = True