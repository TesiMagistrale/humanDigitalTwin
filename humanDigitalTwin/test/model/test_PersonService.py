import importlib
from typing import Type

import pytest
from domain.model.PersonService import PersonService
from adapters.MongoDbAdapter import MongoDbAdapter
from domain.ports import DbPort
import src, os, json, sys
from domain.model.Person import Person
from domain.model.Gender import Gender
from stereotypes.generic.SensorStatus import SensorStatus
from stereotypes.generic.StereotypeScript import StereotypeScript

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
    
    service: Type[PersonService] = None
    
    def init(self):
        try: 
            if self.service == None:
                config_file = "config.json" #"configDocker.json"
                with open((os.path.dirname(os.path.abspath(__file__)) + "/" + config_file).replace ('\\', '/'),'r') as json_file:
                        file = json.load(json_file)
                        
                        http_conf = file['http_config']
                        http_host = http_conf['host']
                        http_port = int(http_conf['port'])

                        mongo = file['mongoDB_config']
                        mongodb_uri = mongo["database_uri"]
                        database_name = mongo["database_name"]
                        
                        
                        if http_host is None or http_port is None :
                            raise ValueError("http_host or http_port is none")
                        elif mongodb_uri is None or database_name is None:
                            raise ValueError("mongodb_uri or database_name is none")
                
                mongodb: DbPort = MongoDbAdapter(mongodb_uri, database_name)
                self.service: Type[PersonService]  = PersonService(self.p, mongodb)
                
        except Exception as exception:
            print(exception)
            raise exception 
    
    @pytest.mark.asyncio
    async def test_stereotypes(self):
        self.init()
        assert "licence_date" not in self.service.get_general_data().keys()
        
        self.service.add_general_data("licence_date", "2016-01-05")
        assert "licence_date" in self.service.get_general_data().keys()
        
        module_name = "ftd"
        stereotype_base_module =  "stereotypes."
        await self.service.add_stereotype({
            "name": module_name,
            "data": None
        })
        
        try:
            importlib.import_module(stereotype_base_module + module_name + ".Start")
        except ImportError as exc:
            assert False, f"'import module raise: {exc}"
            
        assert isinstance(await self.service.get_stereotype(module_name), StereotypeScript)
        
    def test_characteristics(self):
        from datetime import datetime, date, timedelta
        self.init()
        c = str(int(datetime.now().timestamp() * 1000))
        
        assert c not in self.service.get_characteristics().keys()
        
        self.service.add_characteristics(c)
        
        characteristics = self.service.get_characteristics()
        
        assert c in characteristics.keys() and characteristics[c] == {}
        
        value = {
                "date":  int(datetime.now().timestamp() * 1000),
                "value": "test"
            }
        
        self.service.update_characteristics(c, value)
        
        characteristics = self.service.get_characteristics()
        assert c in characteristics.keys() and characteristics[c] == value
        
        self.service.save_data_characteristic(c, "test")

        assert "test" in self.service.get_all_chatacteristic_values(c).values()
        
        
        
        
        