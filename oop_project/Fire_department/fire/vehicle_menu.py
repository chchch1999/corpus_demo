"""vehicle menu for the fires department
"""

__author__ = 'Chieh-Ching Chen'

print('dev: loading module ' + __name__)

import os
import json
from .option import SafeOption
from .vehicle import Vehicle

class VehicleManager(SafeOption):

    def __init__(self, filename="vehicles.json"):
        super().__init__(message="Vehicle Manager Menu:\n0: Exit\n1: Make New Vehicle", action=self.run)
        self._filename = filename
        self._current_vehicle = None
        self._vehicles = self.load_vehicles()

    @property
    def filename(self):
        return self._filename

    @property
    def vehicles(self):
        return self._vehicles

    @property
    def current_vehicle(self):
        return self._current_vehicle

    def load_vehicles(self):
        try:
            with open(self.filename, "r") as file:
                return [Vehicle(**data) for data in json.load(file)]
        except FileNotFoundError:
            return []

    def save_vehicles(self):
        vehicle_data = [vehicle.to_dict() for vehicle in self.vehicles]
        with open(self.filename, "w") as file:
            json.dump(vehicle_data, file, indent=4)

    def run(self):
        while True:
            print("Vehicle Manager Menu:")
            print("0: Exit")
            print("1: Make New Vehicle")

            # Sort the vehicles by range in ascending order
            self.vehicles.sort()

            # Display the list of vehicles in the fleet menu
            self.display_fleet_menu()

            choice = input("Enter your choice (0-1 or vehicle key): ").strip()

            if choice == "0":
                break
            elif choice == "1":
                self.create_new_vehicle()
            elif choice in self.vehicle_keys():
                self.vehicle_menu(self.get_vehicle_by_key(choice))
            else:
                print("Invalid choice. Please enter a valid option or vehicle key.")

    def create_new_vehicle(self):
        call_sign = input("Enter the call sign for the new vehicle: ")
        purpose = input("Enter the purpose for the new vehicle: ")
        try:
            weight = float(input("Enter the weight for the new vehicle (in tons): "))
            fuel_level = float(input("Enter the fuel level for the new vehicle (in liters): "))

            new_vehicle = Vehicle(call_sign, purpose, weight = weight, fuel_level = fuel_level)
            self.vehicles.append(new_vehicle)
            self.save_vehicles()
            print(f"New vehicle {new_vehicle.call_sign} has been created.")
        except ValueError as e:
            print(f"Invalid input. Error: {e}\nPlease try again.")

    def vehicle_menu(self, vehicle):
        self._current_vehicle = vehicle
        while True:
            print(f"\nVehicle Menu for {vehicle.call_sign}:")
            print("0: Back")
            print("1: Delete Vehicle")
            print("2: Copy Vehicle")
            print("3: Display Current Call Sign")
            print("4: Display Current Purpose")
            print("5: Display Current Weight")
            print("6: Display Current Fuel Level")
            print("7: Display Current Range")

            choice = input("Enter your choice: ").strip()

            if choice == "0":
                self._current_vehicle = None
                self._message = ""
                break
            elif choice == "1":
                self.delete_vehicle(vehicle)
                break
            elif choice == "2":
                self.copy_vehicle(vehicle)
                break
            elif choice == "3":
                print(f"Current Call Sign: {vehicle.call_sign}")
            elif choice == "4":
                print(f"Current Purpose: {vehicle.purpose}")
            elif choice == "5":
                print(f"Current Weight: {vehicle.weight} (tons)")
                self.update_numeric_property(vehicle, "weight", "Weight (in tons)")
            elif choice == "6":
                print(f"Current Fuel level: {vehicle.fuel_level} (liters)")
                self.update_numeric_property(vehicle, "fuel_level", "Fuel Level (in liters)")
            elif choice == "7":
                print(f"Current Range: {vehicle.range} (km)")
                self.update_numeric_property(vehicle, "range", "Range (in km)")
            else:
                print("Invalid choice. Please enter a valid option.")

    def delete_vehicle(self, vehicle):
        confirmation = input(f"Are you sure you want to delete vehicle {vehicle.call_sign}? (Y/N): ").strip().lower()
        if confirmation == "y":
            self.vehicles.remove(vehicle)
            self.save_vehicles()
            print(f"Vehicle {vehicle.call_sign} has been deleted.")
        else:
            print(f"Vehicle {vehicle.call_sign} was not deleted.")

    def copy_vehicle(self, vehicle):
        copied_vehicle = vehicle.__copy__()
        self.vehicles.append(copied_vehicle)
        self.save_vehicles()
        print(f"Vehicle {vehicle.call_sign} has been copied as {copied_vehicle.call_sign}.")

    def update_numeric_property(self, vehicle, property_name, display_name):
        try:
            new_value = float(input(f"Enter the new {display_name}: "))
            setattr(vehicle, property_name, new_value)
            self.save_vehicles()
            print(f"{display_name} updated successfully.")

        except ValueError as e:
            print(f"Invalid {display_name}. Error: {e}\nPlease enter a valid numeric value.")

    def vehicle_keys(self):
        # Generate vehicle keys (letters a, b, c, ...) for the fleet menu
        return [chr(ord('a') + i) for i in range(len(self.vehicles))]

    def display_fleet_menu(self):
        # Display the fleet menu with vehicle keys, call signs, and ranges
        for i, vehicle in enumerate(self.vehicles):
            key = chr(ord('a') + i)
            print(f"{key}: {vehicle.call_sign}, range {vehicle.range} km")

    def get_vehicle_by_key(self, key):
        # Retrieve the vehicle corresponding to the given key
        index = ord(key) - ord('a')
        if 0 <= index < len(self.vehicles):
            return self.vehicles[index]
        return None