import json
from stereotypes.ftd.adapters.mqtt.MQTTClientAdapter import MQTTClientAdapter
from stereotypes.ftd.sub_domain.ports.MessageOutputPort import MessageOutputPort

class MQTTOutputAdapter(MessageOutputPort):
    
    def __init__(self, base_client:MQTTClientAdapter, out_topic, receiver_topic):
        self.base_client = base_client
        self.out_topic = out_topic
        self.receiver_topic = receiver_topic
    
    def send(self, data):
        '''
        message example:
        {"person_id": 1, 
        "cd": {"sensor_value": 0, "timestamp": 1690467368112, "speed": 20}, 
        "vd": {"sensor_value": 0, "timestamp": 1690467368112, "speed": 20}, 
        "ea": {"timestamp": 1690467368112, 
            "emotion_sensor": {"anger": 0.45699999999999996, "happiness": 0.01895, "fear": 0.0030499999999999998, "sadness": 0.00065, "neutral": 0.0024, "disgust": 0.013025, "surprise": 0.004925}, "arousal_sensor": 0.0}, 
        "age": 0.049254, 
        "df": 0.1, 
        "out_topic": "topicP1"}
        '''
        data["out_topic"] = self.receiver_topic
        self.base_client.client.publish(self.out_topic , json.dumps(data, default=str))