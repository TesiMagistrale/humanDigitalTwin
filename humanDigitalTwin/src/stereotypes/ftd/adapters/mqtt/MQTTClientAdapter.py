import asyncio
import json
from typing import Dict
import aiomqtt as mqtt
from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort
from stereotypes.ftd.sub_domain.ports.CommunicationStereotype import CommunicationStereotype

class MQTTClientAdapter(CommunicationStereotype):
    
    def __init__(self):
        pass
        
        
    def setup(self, config: Dict[str, str], service: StereotypePort):
        self.broker_address = config["broker_name"]
        self.topics = config["input_topic"]
        self.port = config["port"]
        self.service = service 
        self.client = mqtt.Client(self.broker_address, self.port)
        self.connected = False
        

    async def connect(self):
        await self.client.connect()
        print("Connected to MQTT broker")
        for topic in self.topics:
            await self.client.subscribe(topic)
        
        self.connected = True
        
    async def start(self):
        from stereotypes.ftd.adapters.mqtt.MQTTInputAdapter import MQTTInputAdapter
        await asyncio.create_task(MQTTInputAdapter.create(self))

    
    async def stop(self):
        await self.client.disconnect()
        print("Client stopped")

    def start_service(self, data):
        self.service.start(data)

    def stop_service(self, data):
        self.service.stop(data)
        