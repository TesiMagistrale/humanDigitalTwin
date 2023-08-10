from abc import ABC, abstractmethod

class StereotypePort(ABC):
    
    @abstractmethod
    async def compute_data(self, data):
        pass
    
    @abstractmethod
    async def new_elaborated_data(self, data):
        pass
    
    @abstractmethod
    def start(self, data):
        pass
    
    @abstractmethod
    def stop(self, data):
        pass