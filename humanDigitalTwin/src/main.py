import asyncio
import os, json, sys
from typing import Type
from domain.model.PersonService import PersonService 
from domain.model.Person import Person
from domain.model.Gender import Gender
from domain.ports.PersonServiceGeneralPort import PersonServiceGeneralPort
from adapters.MongoDbAdapter import MongoDbAdapter
from domain.ports.DbPort import DbPort
from adapters.HttpAdapter import HttpAdapter
from domain.ports.HTTPPort import HTTPPort

id = "srgnju679m"
first_name = "Mario"
last_name = "Rossi"
birthdate = "2000-09-10"
gender = Gender.MALE
address = "via rosa, 1"

def main():
    try: 
        config_file = sys.argv[1]
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
        p = Person(id,
                first_name, 
                last_name, 
                birthdate, 
                gender, 
                address
                )
        person_service: PersonServiceGeneralPort = PersonService(p, mongodb)
        person_service.add_general_data("licence_date", "2016-01-05")
        #person_service = PersonService(p, mongodb)
        
        http: HTTPPort = HttpAdapter(http_host, http_port, person_service)
        http.run()
                
    except Exception as exception:
        print(exception)
        raise exception 
    
if __name__ == "__main__":
    main()