from abc import ABC, abstractmethod

class FitnessToDriveCalculatorPort(ABC):
    
    @abstractmethod
    def compute_ftd(self):
        pass