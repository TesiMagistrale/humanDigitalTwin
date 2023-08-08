import json
from stereotypes.ftd.sub_domain.ports.MessageInputPort import MessageInputPort
from stereotypes.ftd.adapters.mqtt.MQTTClientAdapter import MQTTClientAdapter
from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort

class MQTTInputAdapter(MessageInputPort):
    
    def __init__(self, base_client:MQTTClientAdapter, service: StereotypePort):
        self.base_client = base_client
        self.service = service
        self.base_client.client.on_message = self._on_message
    
    def _on_message(self, client, userdata, message):
        self.receive(str(message.payload.decode("utf-8")))
    
    def receive(self, data):
        self.service.new_elaborated_data(data=json.loads(data))