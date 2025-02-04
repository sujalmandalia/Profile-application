from __future__ import annotations
from typing import TYPE_CHECKING
from domain.model import People, PersonDeletedError
from eventsourcing.application import Application
from config.dbconfig import cursor

if TYPE_CHECKING:
    from uuid import UUID


class PeopleApplication(Application):
    def addPeople(self, name: str, age: int, phone_no: str, address: str) -> UUID:
        person = People(name=name, age=age, phone_no=phone_no, address=address)
        self.save(person)
        return person.id

    def get_profile(self, person_id: UUID) -> People:
        profile = self.repository.get(person_id)
        if profile.is_deleted:
          raise PersonDeletedError("Profile is deleted")
        else:
          return profile

    def update_name(self, person_id: UUID, name: str) -> None:
        try:
            person = self.get_profile(person_id=person_id)
            person.update_name(name)
            self.save(person)
        except PersonDeletedError as e:
            raise e
        except KeyError:
           raise ValueError(f"Person with id {person_id} not found")
         
    def update_age(self, person_id: UUID, age: int) -> None:
        try:
            person = self.get_profile(person_id=person_id)
            person.update_age(age)
            self.save(person)
        except PersonDeletedError as e:
            raise e
        except KeyError:
            raise ValueError(f"Person with id {person_id} not found")

    def update_phone(self, person_id: UUID, phone_no: str) -> None:
        try:
            person = self.get_profile(person_id=person_id)
            person.update_phone(phone_no)
            self.save(person)
        except PersonDeletedError as e:
            raise e
        except KeyError:
            raise ValueError(f"Person with id {person_id} not found")

    def update_address(self, person_id: UUID, address: str) -> None:
        try:
            person = self.get_profile(person_id=person_id)
            person.update_address(address)
            self.save(person)
        except PersonDeletedError as e:
            raise e
        except KeyError:
            raise ValueError(f"Person with id {person_id} not found")

    def delete_profile(self, person_id: UUID) -> None:
        try:
            person = self.get_profile(person_id=person_id)
            person.delete()
            self.save(person)
        except PersonDeletedError as e:
            raise e
        except KeyError:
            raise ValueError(f"Person with id {person_id} not found")

      
    def get_all_profiles(self):
        query = """
        select distinct originator_id
        from peopleapplication_events;
        """
        cursor.execute(query)
        aggregateIds = cursor.fetchall()
        for aggregates in aggregateIds:
            profile_id = aggregates[0]
            profile_details = self.repository.get(profile_id)
            print(f"Name: {profile_details.name}, age: {profile_details.age}, phone_no: {profile_details.phone_no}, address: {profile_details.address}")
            print("----------------------------------------------------------")
