from abc import ABC, abstractmethod

class CommunicationStereotype(ABC):
    
    @abstractmethod
    def setup(self):
        pass
    
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass