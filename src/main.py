import os
from application.service import PeopleApplication
from dotenv import load_dotenv
load_dotenv()

os.environ["PERSISTENCE_MODULE"] = os.getenv("PERSISTENCE_MODULE")
os.environ["POSTGRES_DBNAME"] = os.getenv("POSTGRES_DBNAME")
os.environ["POSTGRES_HOST"] = os.getenv("POSTGRES_HOST")
os.environ["POSTGRES_PORT"] = os.getenv("POSTGRES_PORT")
os.environ["POSTGRES_USER"] = os.getenv("POSTGRES_USER")
os.environ["POSTGRES_PASSWORD"] = os.getenv("POSTGRES_PASSWORD")

def create_profile(app):
  name = input("Enter the name : ")
  age =  int(input("Enter the age : "))
  phone_no = input("Enter your phone : ")
  
  print("Enter address details:")
  street = input("Street: ")
  city = input("City: ")
  state = input("State: ")
  zip_code = input("Zip Code: ")

  full_address = {
        "street": street,
        "city": city,
        "state": state,
        "zip_code": zip_code
  }
  
  profile_id = app.addPeople(name,age,phone_no,full_address)
  print(f"The created profile id is {profile_id}")

def get_profile(app):
  profile_id = input("Enter profile id: ")
  profile_details = app.get_profile(profile_id)
  print(f"Name: {profile_details.name}, age: {profile_details.age}, phone_no: {profile_details.phone_no}, full_address: {profile_details.full_address}")

def delete_profile(app):
  profile_id = input("Enter your profile id: ")
  app.delete_profile(profile_id)
  print(f"Profile with id {profile_id} deleted successfully")

def update_name(app):
  profile_id = input("Enter your profile id: ")
  name = input("Enter Name : ")
  app.update_name(profile_id,name)
  print(f"Profile with id {profile_id} updated successfully")
  
def update_age(app):
  profile_id = input("Enter your profile id: ")
  age = int(input("Enter age : "))
  app.update_age(profile_id,age)
  print(f"Profile with id {profile_id} updated successfully")
  
def update_phone(app):
  profile_id = input("Enter your profile id: ")
  phone = input("Enter phone : ")
  app.update_phone(profile_id,phone)
  print(f"Profile with id {profile_id} updated successfully")
  
def update_address(app):
  profile_id = input("Enter your profile id: ")
  print("Enter address details:")
  street = input("Street: ")
  city = input("City: ")
  state = input("State: ")
  zip_code = input("Zip Code: ")
  full_address = {
        "street": street,
        "city": city,
        "state": state,
        "zip_code": zip_code
  }
  app.update_address(profile_id,full_address)
  print(f"Profile with id {profile_id} updated successfully")

def get_all_profile(app):
  app.get_all_profiles()
  
def main():

    app = PeopleApplication()

    while True:
        print("\nChoose an option:")
        print("1. Create Profile")
        print("2. Get Profile")
        print("3. Delete Profile")
        print("4. Update name")
        print("5. Update age")
        print("6. Update phone number")
        print("7. Update address")
        print("8. Get All Profiles")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_profile(app)
        elif choice == "2":
            get_profile(app)
        elif choice == "3":
            delete_profile(app)
        elif choice == "4":
            update_name(app)
        elif choice == "5":
            update_age(app)
        elif choice == "6":
            update_phone(app)
        elif choice == "7":
            update_address(app)
        elif choice == "8":
            get_all_profile(app)
        elif choice == "9":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
main()