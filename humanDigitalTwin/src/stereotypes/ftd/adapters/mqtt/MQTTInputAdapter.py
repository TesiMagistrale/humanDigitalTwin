import asyncio
import json
from stereotypes.ftd.sub_domain.ports.MessageInputPort import MessageInputPort
from stereotypes.ftd.adapters.mqtt.MQTTClientAdapter import MQTTClientAdapter

class MQTTInputAdapter(MessageInputPort):
    
    def __init__(self):
        pass
        
    @classmethod
    async def create(cls, base_client:MQTTClientAdapter):
        instance = cls()
        await instance._setup(base_client)
        
    async def _setup(self, base_client):
        self.base_client = base_client
        try:
           async with self.base_client.client.messages() as messages:
            async for message in messages:
                await self.receive(str(message.payload.decode("utf-8")))
        except Exception as e:
            print(e)
    
    async def receive(self, data):
        await self.base_client.service.new_elaborated_data(data=json.loads(data))