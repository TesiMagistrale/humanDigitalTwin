import asyncio
from domain.model.PersonService import PersonService 
from domain.model.Person import Person
from domain.model.Gender import Gender

id = "srgnju679m"
first_name = "Mario"
last_name = "Rossi"
birthdate = "2000-09-10"
gender = Gender.MALE
address = "via rosa, 1"

async def main():
    
    p = Person(id,
                first_name, 
                last_name, 
                birthdate, 
                gender, 
                address
                )
    person_service = PersonService(p)
    
    person_service.add_general_data("licence_date", "2015-01-05")
    
    
    # each time that i connect to the vehicle i must do all of this
    from stereotypes.ftd.sub_domain.ports.CommunicationStereotype import CommunicationStereotype
    from stereotypes.ftd.sub_domain.ports.MessageInputPort import MessageInputPort
    from stereotypes.ftd.sub_domain.ports.MessageOutputPort import MessageOutputPort
    from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort

    from stereotypes.ftd.adapters.mqtt.MQTTClientAdapter import MQTTClientAdapter
    from stereotypes.ftd.adapters.mqtt.MQTTInputAdapter import MQTTInputAdapter
    from stereotypes.ftd.adapters.mqtt.MQTTOutputAdapter import MQTTOutputAdapter
    from stereotypes.ftd.sub_domain.model.FtDStereotypeModule import FtDStereotypeModule 
    
    from stereotypes.ftd.adapters.rabbit_mq.RabbitMqClientAdapter import RabbitMqClientAdapter
    from stereotypes.ftd.adapters.rabbit_mq.RabbitMqInputAdapter import RabbitMqInputAdapter
    from stereotypes.ftd.adapters.rabbit_mq.RabbitMqOutputAdapter import RabbitMqOutputAdapter
    from stereotypes.ftd.sub_domain.model.FtDParameters import FtDParameters
    
    #put in a config file:
    mqtt_config = {
    "broker_name": "broker.hivemq.com",
    "input_topic": ["newFtD"],
    "output_topic": "ftdMS",
    "port": 1883
    }
    
    base_mqtt_client: CommunicationStereotype = MQTTClientAdapter()
    mqtt_output: MessageOutputPort = MQTTOutputAdapter(base_mqtt_client, mqtt_config["output_topic"], mqtt_config["input_topic"][0])

    
    #put in a config file:
    rabbitmq_config = {
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
    }
    
    base_rabbit_client: CommunicationStereotype = RabbitMqClientAdapter()
    rabbitmq_output: MessageOutputPort = RabbitMqOutputAdapter(base_rabbit_client, rabbitmq_config["routing_key"])
    
    ftd_service:StereotypePort = FtDStereotypeModule(person_service, mqtt_output, rabbitmq_output)
    
    base_mqtt_client.setup(mqtt_config,
                           ftd_service)
    
    base_rabbit_client.setup(rabbitmq_config,
                             ftd_service)
    
    base_mqtt_client.connect()
    base_rabbit_client.connect()
    
    mqtt_input: MessageInputPort = MQTTInputAdapter(base_mqtt_client)
    rabbitmqt_input: MessageInputPort = RabbitMqInputAdapter(base_rabbit_client)
    
    module_data = {
        "km": 100
    }
    
    base_rabbit_client.start_service(module_data)
    
    
    event = asyncio.Event()
    try:
        asyncio.create_task(base_mqtt_client.start())
        asyncio.create_task(base_rabbit_client.start())
        
        #TODO implement stop module and client self.base_mqtt_client.stop({"km": 200})

        
        await event.wait()
        # Wait for Ctrl+C (KeyboardInterrupt) to gracefully exit
    except Exception or KeyboardInterrupt:
        print("Received KeyboardInterrupt, setting event...")
        event.set()  # Set the event to wake up the worker
        base_mqtt_client.stop()
        base_rabbit_client.stop()
        tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=False)

        
        print("Program exiting...")
    
    
if __name__ == "__main__":
    asyncio.run(main())