from abc import ABC, abstractmethod

class MessageInputPort(ABC):
    
    @abstractmethod
    async def receive(self, data):
        pass