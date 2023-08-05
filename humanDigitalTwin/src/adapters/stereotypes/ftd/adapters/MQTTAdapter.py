from adapters.stereotypes.ftd.sub_domain.ports.MQTTPort import MQTTPort
from adapters.stereotypes.ftd.sub_domain.ports.FitnessToDriveCalculatorPort import FitnessToDriveCalculatorPort

class MQTTAdapter(MQTTPort, FitnessToDriveCalculatorPort):
    
    def __init__(self):
        pass
    
    def setup(self):
        pass
    
    
    def connect(self):
        pass
    
    
    def stop(self):
        pass
    
    def compute_ftd(self):
        pass