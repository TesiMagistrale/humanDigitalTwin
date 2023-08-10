from abc import ABC, abstractmethod

class HTTPPort(ABC):
    @abstractmethod
    def setup(self):
        pass
    
    @abstractmethod
    def run(self):
        pass