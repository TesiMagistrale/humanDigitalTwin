import asyncio
from domain.model.PersonService import PersonService 
from domain.model.Person import Person
from domain.model.Gender import Gender
from adapters.stereotypes.FtDStereotypeModule import FtDStereotypeModule 

id = "srgnju679m"
first_name = "Mario"
last_name = "Rossi"
birthdate = "2000-09-10"
gender = Gender.MALE
address = "via rosa, 1"

async def main():
    p = Person(id,
                first_name, 
                last_name, 
                birthdate, 
                gender, 
                address
                )
    s = PersonService(p)
    s.add_stereotype(stereotype_name="s", stereotype= FtDStereotypeModule())
    await s.compute_data("s",1)



if __name__ == "__main__":
    asyncio.run(main())