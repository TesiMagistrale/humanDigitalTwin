import asyncio
import json

import aio_pika
from stereotypes.ftd.adapters.rabbit_mq.RabbitMqClientAdapter import RabbitMqClientAdapter
from stereotypes.ftd.sub_domain.ports.MessageInputPort import MessageInputPort
from stereotypes.ftd.sub_domain.model.FtDParameters import FtDParameters

class RabbitMqInputAdapter(MessageInputPort):

    
    def __init__(self):
        pass
    
    @classmethod
    async def create(cls, base_client:RabbitMqClientAdapter, queue):
        instance = cls()
        await instance._setup(base_client, queue)
        
    async def _setup(self, base_client, queue):
        self.base_client = base_client
        self.queue = queue
        try:
            async with self.queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        data = {
                            "queue": message.routing_key,
                            "msg": json.loads(message.body.decode("utf-8"))
                        }
                        await self.receive(data)
        except Exception as e:
            print(e)
    
    async def receive(self, data):
        queue = data["queue"]
        msg = data["msg"]
        sensor_value = {}
        try:
            match queue:#TODO cambia in base a come definiamo i messaggi scambiati
                case FtDParameters.CD.topic:
                    sensor_value[FtDParameters.CD.full_name] = {
                    "sensor_value": msg[FtDParameters.CD.full_name],
                    "timestamp": msg["timestamp"]
                }
                case FtDParameters.VD.topic:
                    sensor_value[FtDParameters.VD.full_name]= {
                    "sensor_value": msg["start"], #msg[FtDParameters.VD.full_name],
                    "timestamp": msg["timestamp"]
                }
                case FtDParameters.E.topic:
                    sensor_value[FtDParameters.E.full_name] = {"neutral": str(1), "happiness": str(1), "surprise": str(1), "sadness": str(1), "anger": str(1), "disgust": str(1), "fear": str(1)}#msg
                case FtDParameters.A.topic:
                    sensor_value[FtDParameters.A.full_name] = {"arousal": 0}#msg[FtDParameters.A.full_name]
                case FtDParameters.SPEED.topic:
                    sensor_value[FtDParameters.SPEED.full_name] = {
                        "speed": msg['VehicleDynamics']['speed']['x'], #msg[FtDParameters.SPEED.full_name],
                        "timestamp": msg['VehicleDynamics']['timestamp']
                    }
                case _:
                    raise ValueError("wrong topic")
            sensor_value["type"] =  FtDParameters.get_full_name_from_topic(queue)
            await self.base_client.service.compute_data(sensor_value)
        except ValueError as e:
            print(f"exception: {e}")