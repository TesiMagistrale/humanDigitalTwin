from abc import ABC, abstractmethod


class StereotypePort(ABC):
    """
    Represents the basic stereotype port.
    """
    @abstractmethod
    def compute_data(self, data):
        pass
    
    @abstractmethod
    def start(self):
        pass