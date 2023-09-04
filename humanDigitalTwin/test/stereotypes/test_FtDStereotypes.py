import asyncio
import importlib
from typing import Type
import aio_pika
import aiomqtt as mqtt

import pytest
from domain.model.PersonService import PersonService
from adapters.MongoDbAdapter import MongoDbAdapter
from domain.ports import DbPort

import src, os, json, sys
from domain.model.Person import Person
from domain.model.Gender import Gender
from stereotypes.generic.SensorStatus import SensorStatus
from stereotypes.generic.StereotypeScript import StereotypeScript
from stereotypes.ftd.Start import Start

from datetime import datetime, date, timedelta

class TestFtdStereotype:
    id = "srgnju679m"
    first_name = "Mario"
    last_name = "Rossi"
    birthdate = "2000-09-10"
    gender = Gender.MALE
    address = "via rosa, 1"
    
    p = Person(id,
            first_name, 
            last_name, 
            birthdate, 
            gender, 
            address
            )
    
    service: Type[PersonService] = None
    
    rabbitmq_config = {
                        "host": "localhost",
                        "port": 5672, #5675, 
                        "username": "guest",
                        "password": "guest",
                        "queues": ["NP_UNITO_DCDC",
                        "AITEK_EVENTS",
                        "Emotions",
                        "NP_UNIPR_AROUSAL",
                        "RL_VehicleDynamics"],
                        "exchange": "ftdStereotype",
                        "routing_key": "car"
    }
    
    message = {"ftd": 1}
    
    def init(self):
        try: 
            if self.service == None:
                config_file = "config.json" #"configDocker.json"
                with open((os.path.dirname(os.path.abspath(__file__)) + "/" + config_file).replace ('\\', '/'),'r') as json_file:
                        file = json.load(json_file)
                        
                        http_conf = file['http']
                        self.http_host = http_conf['host']
                        self.http_port = int(http_conf['port'])

                        mongo = file['mongoDB_config']
                        self.mongodb_uri = mongo["database_uri"]
                        self.database_name = mongo["database_name"]
                        
                        mqtt = file['mqtt']
                        self.broker_name = mqtt['broker_name']
                        self.mqtt_port = int(mqtt['port'])
                        self.output_topic = mqtt['input_topic'][0]
                        self.input_topic = mqtt['output_topic']
                        
                        if self.http_host is None or self.http_port is None :
                            raise ValueError("http_host or http_port is none")
                        elif self.mongodb_uri is None or self.database_name is None:
                            raise ValueError("mongodb_uri or database_name is none")
                
                mongodb: DbPort = MongoDbAdapter(self.mongodb_uri, self.database_name)
                self.service: Type[PersonService]  = PersonService(self.p, mongodb)
                
        except Exception as exception:
            print(exception)
            raise exception 
        
    @pytest.mark.asyncio
    async def on_message_mqtt(self):
        try:
           async with self.mqtt_client.messages() as messages:
            async for message in messages:
                """message example:
                {"person_id": 1, 
                "cd": {"sensor_value": 0, "timestamp": 1690467368112, "speed": 20}, 
                "vd": {"sensor_value": 0, "timestamp": 1690467368112, "speed": 20}, 
                "ea": {"timestamp": 1690467368112, 
                    "emotion_sensor": {"anger": 0.45699999999999996, "happiness": 0.01895, "fear": 0.0030499999999999998, "sadness": 0.00065, "neutral": 0.0024, "disgust": 0.013025, "surprise": 0.004925}, "arousal_sensor": 0.0}, 
                "age": 0.049254, 
                "df": 0.1, 
                "out_topic": "topicP1"} """
                self.received_message_mqtt.set()
                for key in json.loads(str(message.payload.decode("utf-8"))).keys():
                    assert key in ["person_id", "cd", "ea", "vd", "age", "df", "out_topic"]

                await self.mqtt_client.publish(self.output_topic, json.dumps(self.message))
                
        except Exception as e:
            print(e)
        
    @pytest.mark.asyncio
    async def receive_rabbit(self, queue):
        try:
            async with self.rabbitmq_connection.channel() as channel:
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            self.received_message_rabbit.set()
                            assert json.loads(message.body.decode("utf-8")) == self.message
        except Exception as e:
            print("x")
            import traceback
            traceback.print_exception(e)
        
    @pytest.mark.asyncio
    async def on_message_rabbitmq (self, queue):
        await asyncio.gather(self.receive_rabbit(queue))
    
    @pytest.mark.asyncio
    async def test_stereotype_form_person_service(self):
        self.init()
        #config fake client mqtt
        self.mqtt_client = mqtt.Client(self.broker_name, self.mqtt_port)
        
        await self.mqtt_client.connect()
        print("fake client connected")
        await self.mqtt_client.subscribe(self.input_topic)
        self.received_message_mqtt = asyncio.Event()
        t0 = asyncio.create_task(self.on_message_mqtt())
        
        #config fake client rabbitmq
        self.rabbitmq_connection = await aio_pika.connect(
            host=self.rabbitmq_config['host'],
            port=int(self.rabbitmq_config['port']),
            login=self.rabbitmq_config['username'],
            password=self.rabbitmq_config['password']
        )
        
        self.received_message_rabbit = asyncio.Event()

                
        self.channel = await self.rabbitmq_connection.channel()

        self.exchange = await self.channel.declare_exchange(
            self.rabbitmq_config["exchange"], 
            aio_pika.ExchangeType.TOPIC,
        )
        
        queue = await self.channel.declare_queue(self.rabbitmq_config["queues"][0], auto_delete=True)
        await queue.bind(self.exchange, routing_key=self.rabbitmq_config["queues"][0])
        
        queue = await self.channel.declare_queue(self.rabbitmq_config["routing_key"], auto_delete=True)
        await queue.bind(self.exchange, routing_key=self.rabbitmq_config["routing_key"])
        
            
        t1 = asyncio.create_task(self.on_message_rabbitmq(queue))

        #initialize and start stereotype
        assert self.service.get_actual_state() == {}
        self.service.add_general_data("licence_date", "2016-01-05")
        assert "licence_date" in self.service.get_general_data().keys()
        
        module_name = "ftd"
        stereotype_base_module =  "stereotypes."
        await self.service.add_stereotype({
            "name": module_name,
            "data": None
        })
        
        assert "yearly_km" in self.service.get_characteristics().keys()
        
        self.service.update_characteristics("yearly_km", {
                "date": str(datetime.today() - timedelta(days=1)),
                "value": 5000
            })
        
        try:
            importlib.import_module(stereotype_base_module + module_name + ".Start")
        except ImportError as exc:
            assert False, f"'import module raise: {exc}"
        
        assert isinstance(await self.service.get_stereotype(module_name), StereotypeScript)
        
        start_data = {
                    "rabbitmq_config" : self.rabbitmq_config,
                    "module": {
                        "km": 100
                    }
                }

        await self.service.start_stereotype(module_name, start_data)

        # Publish a message
        async with self.rabbitmq_connection.channel() as publish_channel:
            cd_message = json.dumps({"timestamp": 1690467368112, "eyesOffRoad": 0, "cognitive_distraction": 0,
                        "eyesOffRoad_confidence": 0,
                        "cognitive_distraction_confidence": 0,
                        "eyesOffRoad_pred_1s": 0.0, 
                        "cognitive_distraction_pred_1s": 0.0})
            await publish_channel.default_exchange.publish(
                aio_pika.Message(body=cd_message.encode("utf-8")), routing_key=self.rabbitmq_config["queues"][0]
            )
                

        # wait for messages 
        await self.received_message_mqtt.wait()
        assert self.received_message_mqtt.is_set()
        
        await self.received_message_rabbit.wait()
        assert self.received_message_rabbit.is_set()
        
        assert self.service.get_actual_state()["ftd"] == 1
        
        #stop stereotype
        end_data = {
                    "module": {
                        "km": 200
                    }
                }


        await self.service.stop_stereotype(module_name, end_data)
        t0.cancel()
        t1.cancel()
        
        await self.channel.close()
        await self.mqtt_client.disconnect()
        
        await asyncio.sleep(5) #needed for stopping time
        assert self.service.get_actual_state() == {}
        