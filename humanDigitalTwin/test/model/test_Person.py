import src
from domain.model.Person import Person
from domain.model.Gender import Gender
from domain.model.SensorStatus import SensorStatus

class TestFitnessToDrive:
    first_name = "Mario"
    last_name = "Rossi"
    birthdate = "2000-09-10"
    gender = Gender.MALE
    address = "via rosa, 1"
    
    def test_person_general_data(self):
        p = Person(self.first_name, 
                   self.last_name, 
                   self.birthdate, 
                   self.gender, 
                   self.address
                   )
        
        expected = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "address": self.address
        }
        
        assert p.get_general_data() == expected
        
        p.add_general_data("licence_year", 2020)
        expected["licence_year"] = 2020
        assert p.get_general_data() == expected
        
        p.update_general_data("licence_year", 2021)
        expected["licence_year"] = 2021
        assert p.get_general_data() == expected
        
    def test_person_active_state(self):
        p = Person(self.first_name, 
                   self.last_name, 
                   self.birthdate, 
                   self.gender, 
                   self.address
                   )
        
        expected = dict()
        
        assert p.get_actual_state() == expected
        
        p.add_actual_state("X", 0.12)
        p.add_actual_state("Y", 1)
        expected["X"] = 0.12
        expected["Y"] = 1
        assert p.get_actual_state() == expected
        
        p.update_actual_state("X", 2)
        expected["X"] = 2
        assert p.get_actual_state() == expected
        
        p.remove_state("X")
        expected.pop("X")
        assert p.get_actual_state() == expected
        
    def test_person_sensors(self):
        p = Person(self.first_name, 
                   self.last_name, 
                   self.birthdate, 
                   self.gender, 
                   self.address
                   )
        
        expected = dict()
        
        assert p.get_sensors() == expected
        
        p.add_sensor("X", SensorStatus.OFF)
        p.add_sensor("Y", SensorStatus.ON)
        expected["X"] = SensorStatus.OFF.name
        expected["Y"] = SensorStatus.ON.name
        assert p.get_sensors() == expected
        
        p.update_sensor_status("X", SensorStatus.ON)
        expected["X"] = SensorStatus.ON.name
        assert p.get_sensors() == expected
        
        p.remove_sensor("X")
        expected.pop("X")
        assert p.get_sensors() == expected
        
        
        