from abc import ABC, abstractmethod

from stereotypes.generic import StereotypeScript


class PersonServiceGeneralPort(ABC):

    @abstractmethod      
    async def add_stereotype(self, stereotype_info):
        pass
    
    @abstractmethod      
    async def get_stereotype(self, stereotype_name) -> StereotypeScript:
        pass
    
    @abstractmethod      
    async def start_stereotype(self, stereotype_name, data):
        pass
    
    @abstractmethod
    async def stop_stereotype(self, stereotype_name, data):
        pass
    
    @abstractmethod      
    def get_general_data(self):
        pass
    
    @abstractmethod 
    def update_general_data(self, key, value):
        pass
    
    @abstractmethod    
    def add_general_data(self, key, value):
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
    def get_actual_state(self):
        pass