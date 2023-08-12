import asyncio
import importlib
from datetime import datetime
import json
from domain.model.Person import Person
from domain.ports.DbPort import DbPort
from stereotypes.generic import SensorStatus
from stereotypes.generic.StereotypeScript import StereotypeScript
from stereotypes.generic.PersonServicePort import PersonServicePort
from domain.model.util import download_stereotype
from domain.ports.PersonServiceGeneralPort import PersonServiceGeneralPort


class PersonService(PersonServiceGeneralPort, PersonServicePort):
    
    GENERAL_DATA = "general_data"
    CHARACTERISTICS = "characteristics"
    
    def __init__(self, person: Person, db: DbPort):
        self.person = person
        self.db = db
        self.stereotypes = dict()
        
        self.db.insert(self.person.get_person_id(), self.GENERAL_DATA, self.get_general_data())
        self.db.insert(self.person.get_person_id(), self.CHARACTERISTICS, self.get_characteristics())
        
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
        
    def get_stereotype_data(self, stereotype_name, data_type):
        if stereotype_name in self.stereotypes.keys(): 
            stereotype: StereotypeScript = self.stereotypes[stereotype_name]
            return stereotype.get_stereotype_data(data_type)
        else:
            raise ValueError
        
    def get_stereotype_data_range(self, stereotype_name, data_type, start, end):
        if stereotype_name in self.stereotypes.keys(): 
            stereotype: StereotypeScript = self.stereotypes[stereotype_name]
            return stereotype.get_stereotype_data_range(data_type, start, end)
        else:
            raise ValueError
        
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
        self.db.update_general_data(
            self.person.get_person_id,
            self.GENERAL_DATA,
            key,
            value
            )
        self.person.update_general_data(key, value)
        
    def add_general_data(self, key, value):
        """
        Add a new key-value pair to the general data.

        Args:
            key (str): The key to add.
            value: The value to assign to the key.
        """
        if key not in self.person.get_characteristics().keys():
            self.db.new_person_info(
                self.person.get_person_id(), 
                self.GENERAL_DATA,
                key,
                value
                )
            self.person.add_general_data(key, value)
        else:
            raise ValueError("key yet present")

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
        
    def get_characteristics(self):
        """
        Retrieve the characteristics associated with the person.

        Returns:
            dict: A dictionary containing the characteristics.
        """
        return self.person.get_characteristics()
    
    def update_characteristics(self, key, value):
        """
        Update a specific key-value pair in the characteristics.

        Args:
            key (str): The key to update.
            value: The new value to assign to the key.

        Raises:
            ValueError: If the specified key is not present in the characteristics.
        """
        self.person.update_characteristics(key, value)
        
    def add_characteristics(self, key):
        """
        Add a new key-value pair to the characteristics.

        Args:
            key (str): The key to add.
            value: The value to assign to the key.
        """
        if key not in self.person.get_characteristics().keys():
            self.db.new_person_info(
                self.person.get_person_id(), 
                self.CHARACTERISTICS,
                key,
                {}
                )
            self.person.add_characteristics(key, {})
        
    def save_data_characteristic(self, key, value):
        """
        Add a new key-value pair to the characteristics db.

        Args:
            key (str): The key to add.
            value: The value to assign to the key.
        """
        self.db.new_chatacteristic_value(
            self.person.get_person_id(), 
            self.CHARACTERISTICS,
            key,
            {
                "date":  int(datetime.now().timestamp() * 1000),
                "value": value
            }
        )
        
    def get_characteristic_range_values(self, characteristic, start, end):
        """
        Get all the characteristic values in a range.

        Args:
            characteristic (str): The characteristic to get.
            start (str): the start data ranget in a forma YYYY-MM-DD.
            end (str): the end data range in a format YYYY-MM-DD.
        """
        return self.db.get_characteristic_range_values(
            self.person.get_person_id(), 
            self.CHARACTERISTICS,
            characteristic,
            int(datetime.strptime(start, '%Y-%m-%d').timestamp()*1000),
            int(datetime.strptime(end, '%Y-%m-%d').timestamp()*1000),
        )
        
    def get_all_chatacteristic_values(self, characteristic):
        """
        Get all the characteristic values.

        Args:
            characteristic (str): The characteristic to get.
        """
        return self.db.get_all_chatacteristic_values(
            self.person.get_person_id(), 
            self.CHARACTERISTICS,
            characteristic,
        )
    
    