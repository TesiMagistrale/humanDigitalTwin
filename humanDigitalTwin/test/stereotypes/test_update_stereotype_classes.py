import stereotypes.classes.age_sereotype_class as age_class
import stereotypes.classes.experience_stereotype_class as ef_class 

class TestStereotypeClasses:
    
    def test_update_age_class(self):
        age = 49
        assert age_class.drive_age_weight(age) == 0
        
        def new_function(age):
            return 0.5
        
        age_class.update_compute_drive_age_weight(new_function)
        assert age_class.drive_age_weight(age) == 0.5
    
    def test_update_experience_class(self):
        licence_year = 4
        yearly_km = 5000
        assert ef_class.drive_experience_and_frequence_weight(licence_year, yearly_km) == 0
        
        def new_function(licence_year, yearly_km):
            return 5.0
        
        ef_class.update_compute_drive_experience_and_frequence_weight(new_function)
        assert ef_class.drive_experience_and_frequence_weight(licence_year, yearly_km) == 5.0