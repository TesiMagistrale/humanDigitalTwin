from abc import ABC, abstractmethod
from typing import Dict

from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort

class CommunicationStereotype(ABC):
    
    @abstractmethod
    def setup(self, config: Dict[str, str], service: StereotypePort):
        pass
    
    @abstractmethod
    async def connect(self):
        pass
    
    @abstractmethod
    async def stop(self):
        pass
    
    @abstractmethod
    async def start(self):
        pass
    
    @abstractmethod
    def stop_service(self, data):
        pass
    
    @abstractmethod
    def start_service(self, data):
        pass