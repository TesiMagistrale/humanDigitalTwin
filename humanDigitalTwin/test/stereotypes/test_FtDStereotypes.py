import src
from domain.model.Person import Person
from domain.model.Gender import Gender
from stereotypes.generic.SensorStatus import SensorStatus

class TestPersonService:
    id = "srgnju679m"
    first_name = "Mario"
    last_name = "Rossi"
    birthdate = "2000-09-10"
    gender = Gender.MALE
    address = "via rosa, 1"
    
    p = Person(id,
            first_name, 
            last_name, 
            birthdate, 
            gender, 
            address
            )
    
    def test_stereotypes(self):
        pass