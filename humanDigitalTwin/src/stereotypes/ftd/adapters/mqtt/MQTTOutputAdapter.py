import json
from stereotypes.ftd.adapters.mqtt.MQTTClientAdapter import MQTTClientAdapter
from stereotypes.ftd.sub_domain.ports.MessageOutputPort import MessageOutputPort

class MQTTOutputAdapter(MessageOutputPort):
    
    def __init__(self, base_client:MQTTClientAdapter):
        self.base_client = base_client
    
    def send(self, data):
        self.base_client.client.publish(data["out_topic"] , json.dumps(data, default=str))