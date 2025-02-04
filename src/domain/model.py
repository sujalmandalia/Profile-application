from eventsourcing.domain import Aggregate, event


class People(Aggregate):
    @event("PersonCreated")
    def __init__(self, name: str, age: int, phone_no: str, address: str):
        self.name = name
        self.age = age
        self.phone_no = phone_no
        self.address = address
        self.is_deleted = False

    @event("PersonNameUpdated")
    def update_name(self, name: str) -> None:
        self.check_not_deleted()
        self.name = name

    @event('PersonAgeUpdated')
    def update_age(self, age: int) -> None:
        self.check_not_deleted()
        self.age = age

    @event('PersonPhoneUpdated')
    def update_phone(self, phone_no: str) -> None:
        self.check_not_deleted()
        self.phone_no = phone_no

    @event('PersonAddressUpdated')
    def update_address(self, address: str) -> None:
        self.check_not_deleted()
        self.address = address

    def check_not_deleted(self):
        if self.is_deleted:
            raise PersonDeletedError(
                f"Profile {self.id} is deleted and cannot perform "
                f"this operation."
            )

    @event('PersonDeleted')
    def delete(self) -> None:
        self.check_not_deleted()
        self.is_deleted = True


class PersonError(Exception):
    pass


class PersonDeletedError(PersonError):
    pass
