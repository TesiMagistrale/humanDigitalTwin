import json

from aio_pika import Message
from stereotypes.ftd.adapters.rabbit_mq import RabbitMqClientAdapter
from stereotypes.ftd.sub_domain.ports.MessageOutputPort import MessageOutputPort

class RabbitMqOutputAdapter(MessageOutputPort):
    
    def __init__(self, base_client:RabbitMqClientAdapter, routing_key):
        self.base_client = base_client
        self.routing_key = routing_key
    
    async def send(self, data):
        print(data) #TODO remove
        try:
            await self.base_client.exchange.publish(
                message=Message(json.dumps(data, default=str).encode("utf-8")),
                routing_key=self.routing_key
            )
        except Exception as e:
            print(e)
            raise e