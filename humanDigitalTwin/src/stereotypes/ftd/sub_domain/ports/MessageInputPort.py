from abc import ABC, abstractmethod

class MessageInputPort(ABC):
    
    @abstractmethod
    def receive(self, data):
        pass