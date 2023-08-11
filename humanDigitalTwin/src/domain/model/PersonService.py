import asyncio
import importlib
from domain.model.Person import Person
from stereotypes.generic import SensorStatus
from stereotypes.generic.StereotypeScript import StereotypeScript
from stereotypes.generic.PersonServicePort import PersonServicePort
from domain.model.util import download_stereotype
from domain.ports.PersonServiceGeneralPort import PersonServiceGeneralPort


class PersonService(PersonServiceGeneralPort, PersonServicePort):
    
    def __init__(self, person: Person):
        self.person = person
        self.stereotypes = dict()
        
    async def add_stereotype(self, stereotype_info):
        if stereotype_info["name"] not in self.stereotypes.keys():
            start_class: StereotypeScript = await download_stereotype(stereotype_info)
            start_class.init(service=self)
            self.stereotypes[stereotype_info["name"]] = start_class
        else:
            raise ValueError
        
    async def get_stereotype(self, stereotype_name) -> StereotypeScript:
        if stereotype_name in self.stereotypes.keys():
            return self.stereotypes[stereotype_name]
        else:
            raise ValueError
        
    async def start_stereotype(self, stereotype_name, data):
        if stereotype_name in self.stereotypes.keys(): 
            stereotype: StereotypeScript = self.stereotypes[stereotype_name]
            asyncio.create_task(stereotype.start(data))
        else:
            raise ValueError
        
    async def stop_stereotype(self, stereotype_name, data):
        if stereotype_name in self.stereotypes.keys(): 
            stereotype: StereotypeScript = self.stereotypes[stereotype_name]
            asyncio.create_task(stereotype.stop(data))
        else:
            raise ValueError
        
    
    """  async def compute_data(self, stereotype_name, data):
        if stereotype_name in self.stereotypes:
            s = self.stereotypes[stereotype_name]
            return await s.compute_data(data)
        else:
            raise ValueError("Wrong stereotype name") """
        
        
    def get_general_data(self):
        """
        Retrieve the general data associated with the person.

        Returns:
            dict: A dictionary containing the general data.
        """
        return self.person.get_general_data()
    
    def update_general_data(self, key, value):
        """
        Update a specific key-value pair in the general data.

        Args:
            key (str): The key to update.
            value: The new value to assign to the key.

        Raises:
            ValueError: If the specified key is not present in the general data.
        """
        self.person.update_general_data(key, value)
        
    def add_general_data(self, key, value):
        """
        Add a new key-value pair to the general data.

        Args:
            key (str): The key to add.
            value: The value to assign to the key.
        """
        self.person.add_general_data(key, value)

    def get_full_name(self):
        """
        Retrieve the full name of the person.

        Returns:
            str: The full name in the format 'first_name last_name'.
        """
        return self.person.get_full_name()
    
    def get_age(self):
        """
        retrieve the age of the person.

        Returns:
            int: The age of the person.
        """
        return self.person.get_age()
    
    def get_sensors(self):
        """
        Retrieve the sensors and their state associated with the person.

        Returns:
            dict: A dictionary containing the  sensors and their stat.
        """
        return self.person.get_sensors()

    def add_sensor(self, sensor_name, status: SensorStatus):
        """
        Add a new sensor with its status to the person's collection of sensors.

        Args:
            sensor_name (str): The name of the sensor.
            status (SensorStatus): The status of the sensor.
        """
        self.person.add_sensor(sensor_name, status)
    
    def update_sensor_status(self, sensor_name, status: SensorStatus):
        """
        Update the status of a specific sensor.

        Args:
            sensor_name (str): The name of the sensor.
            status (SensorStatus): The new status of the sensor.

        Raises:
            ValueError: If the specified sensor is not present in the collection.
        """
        self.person.update_sensor_status(sensor_name, status)
        
    def remove_sensor(self, sensor_name):
        """
        Remove a sensor from the person's collection of sensors.

        Args:
            sensor_name (str): The name of the sensor.

        Raises:
            ValueError: If the specified sensor is not present in the collection.
        """
        self.person.remove_sensor(sensor_name)
        
    def get_actual_state(self):
        """
        Retrieve the actual state associated with the person.

        Returns:
            dict: A dictionary containing the actual state.
        """
        return self.person.get_actual_state()
        
    def add_actual_state(self, object, value):
        """
        Add a new object and its value to the person's actual state data.

        Args:
            object: The object to add.
            value: The value associated with the object.
        """
        self.person.add_actual_state(object, value)
        
    def update_actual_state(self, object, value):
        """
        Update the value associated with a specific object in the actual state data.

        Args:
            object: The object to update.
            value: The new value to assign to the object.

        Raises:
            ValueError: If the specified object is not present in the actual state data.
        """
        self.person.update_actual_state(object, value)
        
    def remove_state(self, object):
        """
        Remove a specific object from the person's actual state data.

        Args:
            object: The object to remove.

        Raises:
            ValueError: If the specified object is not present in the actual state data.
        """
        self.person.remove_state(object)
        
    
    