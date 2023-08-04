from domain.model.Person import Person
from domain.ports.StereotypePort import StereotypePort

class PersonService:
    
    def __init__(self, person: Person):
        self.person = person
        self.stereotypes = dict()
        
        
    def add_stereotype(self, stereotype_name, stereotype):
        self.stereotypes[stereotype_name] = stereotype
        
    
        
    async def compute_data(self, stereotype_name, data):
        if stereotype_name in self.stereotypes:
            s:StereotypePort = self.stereotypes[stereotype_name]
            return await s.compute_data(data)
        else:
            raise ValueError("Wrong stereotype name")
        
    
    