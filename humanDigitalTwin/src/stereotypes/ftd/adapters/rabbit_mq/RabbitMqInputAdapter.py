import json
from stereotypes.ftd.adapters.rabbit_mq.RabbitMqClientAdapter import RabbitMqClientAdapter
from stereotypes.ftd.sub_domain.ports.MessageInputPort import MessageInputPort
from stereotypes.ftd.sub_domain.model.FtDParameters import FtDParameters

class RabbitMqInputAdapter(MessageInputPort):

    
    def __init__(self, base_client:RabbitMqClientAdapter):
        self.base_client = base_client
        for queue_name  in self.base_client.queues:
            self.base_client.channel.basic_consume(
                queue=queue_name, 
                on_message_callback=self._on_message, 
                auto_ack=True)
    
    def _on_message(self, ch, method, properties, body):
        data = {
            "queue": method.routing_key,
            "msg" : json.loads(body.decode("utf-8"))
        }
        self.receive(data)
    
    def receive(self, data):
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
                    "sensor_value": msg[FtDParameters.VD.full_name],
                    "timestamp": msg["timestamp"]
                }
                case FtDParameters.E.topic:
                    sensor_value[FtDParameters.E.full_name] = msg
                case FtDParameters.A.topic:
                    sensor_value[FtDParameters.A.full_name] = msg[FtDParameters.A.full_name]
                case FtDParameters.SPEED.topic:
                    sensor_value[FtDParameters.SPEED.full_name] = msg[FtDParameters.SPEED.full_name]
                case _:
                    raise ValueError("wrong topic")
            sensor_value["type"] =  FtDParameters.get_full_name_from_topic(queue)
            self.base_client.service.compute_data(sensor_value)
        except ValueError as e:
            print(f"exception: {e}")