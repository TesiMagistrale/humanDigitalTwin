from abc import ABC, abstractmethod
from domain.ports import StereotypeScript


class PersonServiceNewStereotype(ABC):

    @abstractmethod      
    def add_stereotype(self, stereotype_name, stereotype_script: StereotypeScript):
        pass