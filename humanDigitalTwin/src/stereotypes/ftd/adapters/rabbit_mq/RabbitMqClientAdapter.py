import json
from typing import Dict
import paho.mqtt.client as mqtt
import pika
from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort
from stereotypes.ftd.sub_domain.ports.CommunicationStereotype import CommunicationStereotype

class RabbitMqClientAdapter(CommunicationStereotype):
    
    def __init__(self):
        self.client = mqtt.Client()
        
        
    def setup(self, config: Dict[str, str], service: StereotypePort):
        self.service = service 
        self._parameters = pika.ConnectionParameters(
            config['host'], 
            int(config['port']), 
            credentials= pika.PlainCredentials(config['username'], config['password'])
            )
        self.queues = config["queues"]
        self.exchange = config["exchange"]

        

    def connect(self):
        self._connection = pika.BlockingConnection(self._parameters)
        self.channel = self._connection.channel()
        print("Connected client rabbitmq")
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')
        for name in self.queues:
            #self.channel.queue_declare(queue=name, auto_delete=True) this is on the car
            self.channel.queue_bind( exchange=self.exchange, queue=name, routing_key=name)
        


    def start_service(self, data):
        self.service.start(data)

    def stop_service(self, data):
        self.service.stop(data)
        
    async def start(self):
        self.channel.start_consuming()

    def stop(self):
        self.channel.close()
        self._connection.close()