from abc import ABC, abstractmethod

from stereotypes.generic.PersonServicePort import PersonServicePort

class StereotypeScript(ABC):
    
    @abstractmethod
    def init(self, service: PersonServicePort):
        pass
    
    @abstractmethod
    async def start(self, data): 
        pass
    
    @abstractmethod
    async def stop(self, data): 
        pass