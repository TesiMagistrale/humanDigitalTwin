from abc import ABC, abstractmethod
from stereotypes.generic.SensorStatus import SensorStatus


class PersonServicePort(ABC):
    
    @abstractmethod      
    def get_general_data(self):
        pass
    
    @abstractmethod 
    def update_general_data(self, key, value) -> None:
        pass
    
    @abstractmethod    
    def add_general_data(self, key, value) -> None:
        pass
    
    @abstractmethod 
    def get_full_name(self):
        pass
    
    @abstractmethod 
    def get_age(self):
        pass
    
    @abstractmethod 
    def get_sensors(self):
        pass
    
    @abstractmethod 
    def add_sensor(self, sensor_name, status: SensorStatus) -> None:
        pass
    
    @abstractmethod 
    def update_sensor_status(self, sensor_name, status: SensorStatus) -> None:
        pass
    
    @abstractmethod     
    def remove_sensor(self, sensor_name) -> None:
        pass
    
    @abstractmethod     
    def get_actual_state(self):
        pass
    
    @abstractmethod     
    def add_actual_state(self, object, value) -> None:
        pass
    
    @abstractmethod     
    def update_actual_state(self, object, value) -> None:
        pass
    
    @abstractmethod     
    def remove_state(self, object) -> None:
        pass