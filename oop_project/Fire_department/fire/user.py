"""secure user management
users are password protected
"""

__author__ = 'Chieh-Ching Chen'

print('dev: loading module ' + __name__)

import string
import random
import json

class User:
    default_name = 'Guest'

    def __init__(self):
        self._name = User.default_name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = str(value)

    def login(self):
        self._name = input("Please enter your username:")
        if self._name != User.default_name:
            return "Access granted to " + self._name + "."
        else:
            return "Access denied."

    def logout(self):
        message = self._name + " has logged out."
        self._name = User.default_name
        return message

    def is_registered(self):
        return self.name != User.default_name

### class User ###

class SecureUser(User):
    def __init__(self):
        super().__init__()
        self.users = self.load_user_data()
        self.current_user = None

    def __repr__(self):
        return f"{self._name}"

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def load_user_data(self):
        try:
            with open("users.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_user_data(self):
        with open("users.json", "w") as file:
            json.dump(self.users, file)

    def check_password_requirements(self, password):
        return (
            8 <= len(password) <= 12 and
            any(char.isupper() for char in password) and
            any(char.islower() for char in password) and
            any(char.isdigit() for char in password) and
            all(char.isalnum() for char in password)
        )

    def register(self):
        self.name = input("Enter a username: ")
        password = input("Enter a password: ")

        if self.name in self.users:
            self.name = User.default_name
            return("Username already exists. Please choose a different one.")
        elif not self.check_password_requirements(password):
            self.name = User.default_name
            return "Password should be 8-12 letters " \
                   "including at least one uppercase letter," \
                   "one lowercase letter, and one digit." \
                   "No special characters are allowed. Please try again." \
                   "Suggested Password:", self.generate_password()
        else:
            self.users[self.name] = password
            self.save_user_data()
            return "Registration successful. You can now log in."

    def login(self):
        self.name = input("Enter your username: ")
        password = input("Enter your password: ")

        if self.name in self.users and self.users[self.name] == password:
            self.current_user = self.name
            return "Access granted to " + self.name + "."
        else:
            self.name = User.default_name
            return "Invalid username or password. Please try again."

    def logout(self):
        if self.current_user:
            message = "{} has logged out.".format(self.current_user)
            self.current_user = None
            self.name = User.default_name
            return message
        else:
            return "No user is currently logged in."
    
    def is_authorized(self):
        # Check if the current user is registered (has a password)
        return self.current_user is not None
### class SecureUser(User) ###
