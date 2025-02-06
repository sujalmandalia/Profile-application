from eventsourcing.domain import Aggregate, event


class People(Aggregate):
    @event("PersonCreated")
    def __init__(self, person: dict):
        self.name = person["name"]
        self.age = person["age"]
        self.full_address = person["full_address"]
        self.phone_no = person["phone_no"]
        self.is_deleted = False

    @event("PersonNameUpdated")
    def update_name(self, person: dict) -> None:
        self.check_not_deleted()
        self.name = person["name"]

    @event('PersonAgeUpdated')
    def update_age(self, person: dict) -> None:
        self.check_not_deleted()
        self.age = person["age"]

    @event('PersonPhoneUpdated')
    def update_phone(self, person: dict) -> None:
        self.check_not_deleted()
        self.phone_no = person["phone_no"]

    @event('PersonAddressUpdated')
    def update_address(self, person: dict) -> None:
        self.check_not_deleted()
        self.full_address = person["full_address"]

    def check_not_deleted(self):
        if self.is_deleted:
            raise PersonDeletedError(
                f"Profile {self.id} is deleted and cannot perform "
                f"this operation."
            )

    @event('PersonDeleted')
    def delete(self,person: dict) -> None:
        self.check_not_deleted()
        self.is_deleted = True


class PersonError(Exception):
    pass


class PersonDeletedError(PersonError):
    pass
