from abc import ABC, abstractmethod

from stereotypes.generic import StereotypeScript


class PersonServiceNewStereotypePort(ABC):

    @abstractmethod      
    async def add_stereotype(self, stereotype_info):
        pass
    
    @abstractmethod      
    async def get_stereotype(self, stereotype_name) -> StereotypeScript:
        pass