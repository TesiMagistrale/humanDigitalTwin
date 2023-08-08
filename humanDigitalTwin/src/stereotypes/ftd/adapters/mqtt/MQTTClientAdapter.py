import json
import paho.mqtt.client as mqtt
from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort
from stereotypes.ftd.sub_domain.ports.CommunicationStereotype import CommunicationStereotype

class MQTTClientAdapter(CommunicationStereotype):
    
    def __init__(self):
        self.client = mqtt.Client()
        self.connected = False
        
        
    def setup(self, broker_address:str, port:int, topics:list):
        self.broker_address = broker_address
        self.topics = topics
        self.port = port
        
        self.client.on_connect = self._on_connect
        #self.client.on_message = self._on_message
        

    def connect(self):
        self.client.connect(self.broker_address, port=self.port)
        self.client.loop_start()

        while not self.connected:
            pass

    def stop(self):
        self.client.loop_stop()
        print("Client stopped")

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code "+str(rc))
        for topic in self.topics:
            self.client.subscribe(topic)
        
        self.connected = True