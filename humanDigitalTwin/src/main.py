import asyncio
from typing import Type
from domain.model.PersonService import PersonService 
from domain.model.Person import Person
from domain.model.Gender import Gender
from domain.ports.PersonServiceUseStereotypePort import PersonServiceNewStereotypePort

id = "srgnju679m"
first_name = "Mario"
last_name = "Rossi"
birthdate = "2000-09-10"
gender = Gender.MALE
address = "via rosa, 1"

def main():
    
    p = Person(id,
                first_name, 
                last_name, 
                birthdate, 
                gender, 
                address
                )
    person_service: Type[PersonService] = PersonService(p)
    person_service.add_general_data("licence_date", "2015-01-05")

    module_name = "ftd"
    """ await person_service.add_stereotype({
        "name": module_name
    })
    
    stereotype = await person_service.get_stereotype(module_name)
    
    print(person_service.get_actual_state())
    print(person_service.get_sensors())
    
    # each time that i connect to the vehicle i must do all of this
    
    from stereotypes.ftd.sub_domain.model.FtDParameters import FtDParameters

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
    
    module_data_start = {
        "km": 100
    }
    module_data_stop = {
        "km": 200
    }
    
    stereotype.init(person_service)
    
    event = asyncio.Event()
    try:
        data = {
            "rabbitmq_config" : rabbitmq_config,
            "module": module_data_start
        }
        task = asyncio.create_task(stereotype.start(data))

        await asyncio.sleep(30)

        data = {
            "module": module_data_stop
        }
        
        print(person_service.get_actual_state())
        print(person_service.get_sensors())
        
        await stereotype.stop(data)
        event.set()
        await event.wait()
        
        print(person_service.get_actual_state())
        print(person_service.get_sensors()) 
    except Exception or KeyboardInterrupt as e:
        print("Received KeyboardInterrupt, setting event...")
        import traceback
        traceback.print_exc()
          # Set the event to wake up the worker
        tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=False)

        print("Program exiting...")
        """
    
    from adapters.HttpAdapter import HttpAdapter
    from domain.ports.HTTPPort import HTTPPort
    
    http: HTTPPort = HttpAdapter("localhost", 8000, person_service)
    http.run()
        
        
    
    
    
if __name__ == "__main__":
    main()