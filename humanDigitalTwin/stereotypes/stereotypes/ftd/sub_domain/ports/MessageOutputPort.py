from abc import ABC, abstractmethod


class MessageOutputPort(ABC):
    
    @abstractmethod
    async def send(self, data):
        pass