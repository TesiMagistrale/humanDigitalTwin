import asyncio
from stereotypes.generic.SensorStatus import SensorStatus
from stereotypes.generic.PersonServicePort import PersonServicePort
from stereotypes.generic.StereotypeScript import StereotypeScript
from stereotypes.ftd.sub_domain.ports.CommunicationStereotype import CommunicationStereotype
from stereotypes.ftd.sub_domain.ports.MessageOutputPort import MessageOutputPort
from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort

from stereotypes.ftd.adapters.mqtt.MQTTClientAdapter import MQTTClientAdapter
from stereotypes.ftd.adapters.mqtt.MQTTOutputAdapter import MQTTOutputAdapter
from stereotypes.ftd.sub_domain.model.FtDStereotypeModule import FtDStereotypeModule 
from stereotypes.ftd.sub_domain.model.FtDParameters import FtDParameters 

from stereotypes.ftd.adapters.rabbit_mq.RabbitMqClientAdapter import RabbitMqClientAdapter
from stereotypes.ftd.adapters.rabbit_mq.RabbitMqOutputAdapter import RabbitMqOutputAdapter


class Start(StereotypeScript):
    
    def __init__(self):
        self.sensors = [
            "cognitive_distraction_camera",
            "visual_distraction_camera",
            "emotions_camera",
            "car_speedometer",
            "arousal_sensor"
        ]
        try:
            import os, json
            with open((os.path.dirname(os.path.abspath(__file__)) + "/config.json").replace ('\\', '/'),'r') as json_file: #/configDocker.json
                file = json.load(json_file)
                
                self.mqtt_config = file["mqtt"]
                self.ms_http_config = file["http"]
        except Exception as exception:
            print(exception)
            
    def init(self, service: PersonServicePort):
        self.person_service = service
        
        self.base_mqtt_client: CommunicationStereotype = MQTTClientAdapter()
        self.mqtt_output: MessageOutputPort = MQTTOutputAdapter(
            self.base_mqtt_client, 
            self.mqtt_config["output_topic"],
            self. mqtt_config["input_topic"][0]
            )
        
        for sensor in self.sensors:
            if sensor not in self.person_service.get_sensors().keys():
                self.person_service.add_sensor(sensor_name=sensor, status=SensorStatus.OFF)
        
        self.person_service.add_characteristics("yearly_km")

    
    
    async def start(self, data): 
        try: 
            rabbitmq_config = data["rabbitmq_config"]
            """ {
            "host": "localhost",
            "port": 5672,
            "username": "guest",
            "password": "guest",
            "queues": [FtDParameters.CD.topic, 
                    FtDParameters.VD.topic,
                    FtDParameters.SPEED.topic,
                    FtDParameters.E.topic,
                    FtDParameters.A.topic],
            "exchange": "ftdStereotype",
            "routing_key": "car"
        } """
        
            self.base_rabbit_client1: CommunicationStereotype = RabbitMqClientAdapter()
            self.base_rabbit_client2: CommunicationStereotype = RabbitMqClientAdapter()
            
            self.rabbitmq_output: MessageOutputPort = RabbitMqOutputAdapter(
                self.base_rabbit_client1, 
                rabbitmq_config["routing_key"])
            
            ftd_service:StereotypePort = FtDStereotypeModule(
                self.person_service, 
                self.mqtt_output, 
                self.rabbitmq_output,
                self.sensors
                )
            
            self.base_mqtt_client.setup(self.mqtt_config,
                            ftd_service)
        
            self.base_rabbit_client1.setup(rabbitmq_config,
                                    ftd_service)
            self.base_rabbit_client2.setup(rabbitmq_config,
                                    ftd_service)
            
            await self.base_mqtt_client.connect()
            await self.base_rabbit_client1.connect()
            await self.base_rabbit_client2.connect()
            
            module_data = data["module"] 
            
            self.base_rabbit_client2.start_service(module_data)
            
            self.tasks = [
                asyncio.create_task(self.base_mqtt_client.start()),
                asyncio.create_task(self.base_rabbit_client1.start()),
                asyncio.create_task(self.base_rabbit_client2.start())
            ]
        except Exception:
            import traceback
            traceback.print_exc()
    
    async def stop(self, data): 
        for task in self.tasks:
            task.cancel()
            
        await self.base_mqtt_client.stop()
        await self.base_rabbit_client1.stop()
        await self.base_rabbit_client2.stop()
        module_data = data["module"] 
        self.base_rabbit_client2.stop_service(module_data)
        
    def get_stereotype_data(self, data_type):
        allowed_data_types = [
            FtDParameters.CD.value, 
            FtDParameters.VD.value,
            FtDParameters.E.value + FtDParameters.A.value,
            "ftd"
        ]
        
        if data_type in allowed_data_types:
            import requests
            url  = "http://" + self.ms_http_config["host"] + ":" + str(self.ms_http_config["port"]) + "/all"
            resp = requests.get(url, {
                "id": self.person_service.get_general_data()["id"],
                "data_type": data_type
            })
            if resp.status_code == 200:
                return resp.json()
            else:
                return resp.raise_for_status()
        else:
            raise ValueError("wrong data_type")
        
    def get_stereotype_data_range(self, data_type, start, end):
        allowed_data_types = [
            FtDParameters.CD.value, 
            FtDParameters.VD.value,
            FtDParameters.E.value + FtDParameters.A.value,
            "ftd"
        ]
        
        if data_type in allowed_data_types:
            import requests
            from datetime import datetime
            url  = "http://" + self.ms_http_config["host"] + ":" + str(self.ms_http_config["port"]) + "/range"
            resp = requests.get(url, {
                "id": self.person_service.get_general_data()["id"],
                "data_type": data_type,
                "start": int(datetime.strptime(start, '%Y-%m-%d').timestamp()*1000),
                "end": int(datetime.strptime(end, '%Y-%m-%d').timestamp()*1000),
            })
            if resp.status_code == 200:
                return resp.json()
            else:
                return resp.raise_for_status()
        else:
            raise ValueError("wrong data_type") 