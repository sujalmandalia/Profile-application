from __future__ import annotations
import json
from typing import TYPE_CHECKING
from domain.model import People, PersonDeletedError
from eventsourcing.application import Application
from config.dbconfig import cursor

if TYPE_CHECKING:
    from uuid import UUID


class PeopleApplication(Application):
    #To autmatically take the snapshots (will take snapshots after every 5 intervals)
    snapshotting_intervals = {People: 5}
    def addPeople(self, name: str, age: int, phone_no: str, full_address: dict) -> UUID:
        details = {
            "name": name,
            "age": age,
            "full_address": full_address,
            "phone_no": phone_no,
            "is_deleted": False,
        }
        person = People(details)
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
            details = {
                "name": name,
                "age": person.age,
                "full_address": person.full_address,
                "phone_no": person.phone_no,
                "is_deleted": person.is_deleted,
            }
            person.update_name(details)
            self.save(person)
        except PersonDeletedError as e:
            raise e
        except KeyError:
            raise (f"Person with id {person_id} not found")

    def update_age(self, person_id: UUID, age: int) -> None:
        try:
            person = self.get_profile(person_id=person_id)
            details = {
                "name": person.name,
                "age": age,
                "full_address": person.full_address,
                "phone_no": person.phone_no,
                "is_deleted": person.is_deleted,
            }
            person.update_age(details)
            self.save(person)
        except PersonDeletedError as e:
            raise e
        except KeyError:
            raise ValueError(f"Person with id {person_id} not found")

    def update_phone(self, person_id: UUID, phone_no: str) -> None:
        try:
            person = self.get_profile(person_id=person_id)
            details = {
                "name": person.name,
                "age": person.age,
                "full_address": person.full_address,
                "phone_no": phone_no,
                "is_deleted": person.is_deleted,
            }
            person.update_phone(details)
            self.save(person)
        except PersonDeletedError as e:
            raise e
        except KeyError:
            raise ValueError(f"Person with id {person_id} not found")

    def update_address(self, person_id: UUID, full_address: dict) -> None:
        try:
            person = self.get_profile(person_id=person_id)
            details = {
                "name": person.name,
                "age": person.age,
                "full_address": full_address,
                "phone_no": person.phone_no,
                "is_deleted": person.is_deleted,
            }
            person.update_address(details)
            self.save(person)
        except PersonDeletedError as e:
            raise e
        except KeyError:
            raise ValueError(f"Person with id {person_id} not found")

    def delete_profile(self, person_id: UUID) -> None:
        try:
            person = self.get_profile(person_id=person_id)
            details = {
                "name": person.name,
                "age": person.age,
                "full_address": person.full_address,
                "phone_no": person.phone_no,
                "is_deleted": True,
            }
            person.delete(details)
            self.save(person)
        except PersonDeletedError as e:
            raise e
        except KeyError:
            raise ValueError(f"Person with id {person_id} not found")

    def get_all_profiles(self):
        query = """
        SELECT p1.originator_id, 
        (convert_from(p1.state, 'UTF8')::jsonb)->'person' AS person
        FROM peopleapplication_events p1
        JOIN (
        SELECT originator_id, MAX(originator_version) AS max_version
        FROM peopleapplication_events p2
        GROUP BY originator_id
        ) p2 
        ON p1.originator_id = p2.originator_id 
        AND p1.originator_version = p2.max_version;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        for record_id , details in result:
            print(f"Originator_id: {record_id}")
            print(f"Name: {details['name']}")
            print(f"Age: {details['age']}")
            print(f"Full Address: {details.get('full_address')}")
            print(f"Phone Number: {details['phone_no']}")
            print("---------------------------------------")
