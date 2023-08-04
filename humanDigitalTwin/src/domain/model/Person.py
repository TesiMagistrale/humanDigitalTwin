from datetime import datetime
from domain.model.Gender import Gender
from domain.model.SensorStatus import SensorStatus

class Person:
    """
    A class representing a Person
    """
    
    def __init__(self, first_name:str, last_name:str, birthdate:str, gender:Gender, address:str):
        """
        Initialize a Person instance.

        Args:
            first_name (str): The first name of the person.
            last_name (str): The last name of the person.
            birthdate (str): The birthdate of the person in 'YYYY-MM-DD' format.
            gender (str): The gender of the person.
            address (str): The address of a person.
        """
        try:
            datetime.strptime(birthdate, '%Y-%m-%d')
        except ValueError as e:
            raise ValueError()
        
        self.general_data = {
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate,
            "gender": gender,
            "address": address
        }
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.gender = gender.name
        self.address = address
        
        self.actual_state = dict() #object:value
        self.sensors = dict() #sensor: on/off

    def get_general_data(self):
        """
        Retrieve the general data associated with the person.

        Returns:
            dict: A dictionary containing the general data.
        """
        return self.general_data
    
    def update_general_data(self, key, value):
        """
        Update a specific key-value pair in the general data.

        Args:
            key (str): The key to update.
            value: The new value to assign to the key.

        Raises:
            ValueError: If the specified key is not present in the general data.
        """
        if key in self.general_data:
            self.general_data[key] = value
        else:
            raise ValueError("Key not found in general data.")
        
    def add_general_data(self, key, value):
        """
        Add a new key-value pair to the general data.

        Args:
            key (str): The key to add.
            value: The value to assign to the key.
        """
        self.general_data[key] = value

    def get_full_name(self):
        """
        Retrieve the full name of the person.

        Returns:
            str: The full name in the format 'first_name last_name'.
        """
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        """
        Calculate and retrieve the age of the person based on birthdate.

        Returns:
            int: The age of the person.
        """
        # Calculate age based on birthdate (assuming birthdate is in 'YYYY-MM-DD' format)
        today = datetime.today()
        birthdate = datetime.strptime(self.birthdate, '%Y-%m-%d')
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
    
    def get_sensors(self):
        """
        Retrieve the sensors and their state associated with the person.

        Returns:
            dict: A dictionary containing the  sensors and their stat.
        """
        return self.sensors

    def add_sensor(self, sensor_name, status: SensorStatus):
        """
        Add a new sensor with its status to the person's collection of sensors.

        Args:
            sensor_name (str): The name of the sensor.
            status (SensorStatus): The status of the sensor.
        """
        self.sensors[sensor_name] = status.name
    
    def update_sensor_status(self, sensor_name, status: SensorStatus):
        """
        Update the status of a specific sensor.

        Args:
            sensor_name (str): The name of the sensor.
            status (SensorStatus): The new status of the sensor.

        Raises:
            ValueError: If the specified sensor is not present in the collection.
        """
        if sensor_name in self.sensors:
            self.sensors[sensor_name] = status.name
        else:
            raise ValueError("Sensor not found.")
        
    def remove_sensor(self, sensor_name):
        """
        Remove a sensor from the person's collection of sensors.

        Args:
            sensor_name (str): The name of the sensor.

        Raises:
            ValueError: If the specified sensor is not present in the collection.
        """
        if sensor_name in self.sensors:
            self.sensors.pop(sensor_name)
        else:
            raise ValueError("Sensor not found.")
        
    def get_actual_state(self):
        """
        Retrieve the actual state associated with the person.

        Returns:
            dict: A dictionary containing the actual state.
        """
        return self.actual_state
        
    def add_actual_state(self, object, value):
        """
        Add a new object and its value to the person's actual state data.

        Args:
            object: The object to add.
            value: The value associated with the object.
        """
        self.actual_state[object] = value
        
    def update_actual_state(self, object, value):
        """
        Update the value associated with a specific object in the actual state data.

        Args:
            object: The object to update.
            value: The new value to assign to the object.

        Raises:
            ValueError: If the specified object is not present in the actual state data.
        """
        if object in self.actual_state:
            self.actual_state[object] = value
        else:
            raise ValueError("Object not found.")
        
    def remove_state(self, object):
        """
        Remove a specific object from the person's actual state data.

        Args:
            object: The object to remove.

        Raises:
            ValueError: If the specified object is not present in the actual state data.
        """
        if object in self.actual_state:
            self.actual_state.pop(object)
        else:
            raise ValueError("Object not found.")