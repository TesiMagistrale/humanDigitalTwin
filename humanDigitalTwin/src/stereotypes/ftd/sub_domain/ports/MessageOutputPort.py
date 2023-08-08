from abc import ABC, abstractmethod


class MessageOutputPort(ABC):
    
    @abstractmethod
    def send(self, data):
        pass