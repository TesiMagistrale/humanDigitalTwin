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
    from stereotypes.ftd.sub_domain.ports.CommunicationStereotype import CommunicationStereotype
    from stereotypes.ftd.sub_domain.ports.MessageInputPort import MessageInputPort
    from stereotypes.ftd.sub_domain.ports.MessageOutputPort import MessageOutputPort
    from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort

    from stereotypes.ftd.adapters.mqtt.MQTTClientAdapter import MQTTClientAdapter
    from stereotypes.ftd.adapters.mqtt.MQTTInputAdapter import MQTTInputAdapter
    from stereotypes.ftd.adapters.mqtt.MQTTOutputAdapter import MQTTOutputAdapter
    from stereotypes.ftd.sub_domain.model.FtDStereotypeModule import FtDStereotypeModule 
    
    
    base_mqtt_client: CommunicationStereotype = MQTTClientAdapter()
    mqtt_output: MessageOutputPort = MQTTOutputAdapter(base_mqtt_client)
    ftd_service:StereotypePort = FtDStereotypeModule(None, mqtt_output, mqtt_output)
    mqtt_input: MessageInputPort = MQTTInputAdapter(base_mqtt_client, ftd_service)
    
    #put in a config file:
    mqtt_config = {
        "broker_name": "broker.hivemq.com",
        "topics": ["ftd"],
        "port": 1883
    }
    
    
    base_mqtt_client.setup(mqtt_config["broker_name"], 
                           mqtt_config["port"],
                           mqtt_config["topics"])
    
    base_mqtt_client.connect()
    
    await asyncio.Event().wait()
    
    
    

if __name__ == "__main__":
    asyncio.run(main())