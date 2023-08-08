import json
from stereotypes.ftd.adapters.rabbit_mq import RabbitMqClientAdapter
from stereotypes.ftd.sub_domain.ports.MessageOutputPort import MessageOutputPort

class RabbitMqOutputAdapter(MessageOutputPort):
    
    def __init__(self, base_client:RabbitMqClientAdapter, routing_key):
        self.base_client = base_client
        self.routing_key = routing_key
    
    def send(self, data):
        self.base_client.channel.basic_publish(
            exchange=self.base_client.exchange,
            routing_key= self.routing_key,
            body=json.dumps(data)
        )
        print(data)