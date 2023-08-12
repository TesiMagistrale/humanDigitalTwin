from abc import ABC, abstractmethod


class DbPort(ABC):
    @abstractmethod
    def insert(self, id, collection_name, data):
        """ 
        Initialize a new person in the corresponding collection
        """
        pass
    
    @abstractmethod    
    def new_person_info(self, id, collection_name, info, date, value):
        """ create a new person information inside the corresponding collection """
        pass
    
    def update_general_data(self, id, collection_name, key, value):
        """ Update the value of a general data """
        pass
    
    @abstractmethod  
    def new_chatacteristic_value(self, id, collection_name, characteristic, value):
        """ Add a new characteristic value to the charachteristic history """
        pass
    
    @abstractmethod   
    def get_all_chatacteristic_values(self, id, collection_name, characteristic):
        """ return all the values about a characteristic """
        pass

    @abstractmethod   
    def get_characteristic_range_values(self, id, collection_name, characteristic, start, end):
        """ return the values of a characteristic between start date and end date """
        pass