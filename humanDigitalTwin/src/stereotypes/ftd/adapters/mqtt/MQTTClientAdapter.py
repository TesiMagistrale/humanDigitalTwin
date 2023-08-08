import json
from typing import Dict
import paho.mqtt.client as mqtt
from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort
from stereotypes.ftd.sub_domain.ports.CommunicationStereotype import CommunicationStereotype

class MQTTClientAdapter(CommunicationStereotype):
    
    def __init__(self):
        self.client = mqtt.Client()
        
        
    def setup(self, config: Dict[str, str], service: StereotypePort):
        self.broker_address = config["broker_name"]
        self.topics = config["input_topic"]
        self.port = config["port"]
        self.service = service 
        
        self.client.on_connect = self._on_connect
        self.connected = False
        

    def connect(self):
        self.client.connect(self.broker_address, port=self.port)
        
    async def start(self):
        self.client.loop_start()
    
    def stop(self):
        self.client.loop_stop()
        print("Client stopped")

    def start_service(self, data):
        self.service.start(data)

    def stop_service(self, data):
        self.service.stop(data)

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code "+str(rc))
        for topic in self.topics:
            self.client.subscribe(topic)
        
        self.connected = True