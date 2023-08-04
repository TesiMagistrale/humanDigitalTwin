from domain.model.Person import Person


class PersonService:
    
    def __init__(self, person: Person):
        self.person = person
        self.stereotypes = dict()
        
        
    def add_stereotype(self, stereotype_name, stereotype):
        self.stereotypes[stereotype_name] = stereotype
        
    
        
    """ def compute_data(self, stereotype_name, data):
        if stereotype_name in self.stereotypes:
            self.stereotypes[stereotype_name].compute_data(data) """
        
    
    