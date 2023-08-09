import asyncio
from typing import Dict
from aio_pika import DeliveryMode, ExchangeType, Message, connect
from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort
from stereotypes.ftd.sub_domain.ports.CommunicationStereotype import CommunicationStereotype

class RabbitMqClientAdapter(CommunicationStereotype):
    
    def __init__(self):
        pass
        
        
    def setup(self, config: Dict[str, str], service: StereotypePort):
        self.service = service 
        self.config = config
        self.queues = []
        

    async def connect(self):
        self.connection = await connect(
            host=self.config['host'],
            port=int(self.config['port']),
            login=self.config['username'],
            password=self.config['password']
        )
        
        self.channel = await self.connection.channel()

        self.exchange = await self.channel.declare_exchange(
            self.config["exchange"], 
            ExchangeType.TOPIC,
        )
        
        
        self.queues = await asyncio.gather(
        *[self._create_and_bind_queue(name, name) for name in self.config["queues"]]
        )
        print("rabbitmq client connect")
        
    async def _create_and_bind_queue(self, queue_name, routing_key):
        queue = await self.channel.declare_queue(queue_name, auto_delete=True)
        await queue.bind(self.exchange, routing_key=routing_key)
        return queue
        
    def start_service(self, data):
        self.service.start(data)

    def stop_service(self, data):
        self.service.stop(data)
        
    async def start(self):
        from stereotypes.ftd.adapters.rabbit_mq.RabbitMqInputAdapter import RabbitMqInputAdapter
        await asyncio.create_task(RabbitMqInputAdapter.create(self))

        await self._cleanup()

    async def _cleanup(self):
        if self.connection:
            await self.connection.close()

    async def stop(self):
        await self.channel.close()