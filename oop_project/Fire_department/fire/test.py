"""Unittest for the vehicle management
"""

__author__ = 'Chieh-Ching Chen'

print('dev: loading module ' + __name__)

import unittest
from .vehicle import Vehicle
from .user import User, SecureUser

class TestVehicle(unittest.TestCase):
    def setUp(self):
        # Create a dictionary to hold test vehicles for easy cleanup in tearDown
        self.test_vehicles = {}

    def tearDown(self):
        # Remove test vehicles from the unique_call_signs dictionary
        for call_sign, vehicle in self.test_vehicles.items():
            Vehicle.unique_call_signs.pop(call_sign, None)

    def test_unique_call_sign(self):
        # Test that call signs are unique
        # Create two vehicles with the same call sign and check for a ValueError
        with self.assertRaises(ValueError):
            Vehicle("Engine 1", "engine", weight=50, fuel_level=100)
            Vehicle("Engine 1", "Engine for car", weight=60, fuel_level=80)

    def test_invalid_properties(self):
        # Test that providing an invalid combination of properties raises a ValueError
        # Should raise a ValueError as exactly two properties should be provided
        with self.assertRaises(ValueError):
            Vehicle("Engine 2", "engine 2", weight=70, fuel_level=200, range=400)

    def test_valid_combinations(self):
        # Test valid combinations of properties
        # Test with weight and fuel_level provided
        vehicle1 = Vehicle("Engine 3", "engine for scooter", weight=50, fuel_level=150)
        self.assertEqual(vehicle1.weight, 50)
        self.assertEqual(vehicle1.fuel_level, 150)
        self.assertEqual(vehicle1.range, 20 * 150 / 50)

        # Test with range and weight provided
        vehicle2 = Vehicle("Engine 4", "Engine for use", range=100, weight=30)
        self.assertEqual(vehicle2.weight, 30)
        self.assertEqual(vehicle2.fuel_level, 100 * 30 / 20)
        self.assertEqual(vehicle2.range, 100)

        # Test with fuel_level and range provided
        vehicle3 = Vehicle("Engine 5", "Engine for airplane", fuel_level=200, range=200)
        self.assertEqual(vehicle3.weight, 200 * 20 / 200)
        self.assertEqual(vehicle3.fuel_level, 200)
        self.assertEqual(vehicle3.range, 200)

    def test_weight_range(self):
        # Test weight property and setter
        # Create a vehicle and change its weight
        vehicle = Vehicle("Ladder 1", "for climbing", weight=70, fuel_level=200)
        vehicle.weight = 80
        self.assertEqual(vehicle.weight, 80)  # Check if weight was updated

        # Try setting a negative weight, which should raise a ValueError
        with self.assertRaises(ValueError):
            vehicle.weight = -10

        # Try setting a weight above the maximum allowed
        with self.assertRaises(ValueError):
            vehicle.weight = 110

    def test_fuel_level_range(self):
        # Test fuel_level property and setter
        # Create a vehicle and change its fuel level
        vehicle = Vehicle("Ladder 2", "for landing", weight=80, fuel_level=150)
        vehicle.fuel_level = 200
        self.assertEqual(vehicle.fuel_level, 200)  # Check if fuel level was updated

        # Try setting a negative fuel level, which should raise a ValueError
        with self.assertRaises(ValueError):
            vehicle.fuel_level = -10

        # Try setting a fuel level above the maximum allowed
        with self.assertRaises(ValueError):
            vehicle.fuel_level = 600

    def test_range_calculation(self):
        # Test the range property and setter, and range calculation
        # Create a vehicle with initial values
        vehicle = Vehicle("Ladder 3", "for fun", weight=10, fuel_level=300)
        
        # Change the range, which should update fuel level and weight 
        vehicle.range = 200
        self.assertEqual(vehicle.range, 200)  # Check if range was updated
        self.assertEqual(vehicle.fuel_level, 100)  # Check if fuel level was updated
        self.assertEqual(vehicle.weight, 10)  # Check if weight was updated

        # Try setting a negative range, which should raise a ValueError
        with self.assertRaises(ValueError):
            vehicle.range = -10

        # Try setting a range above the maximum allowed
        with self.assertRaises(ValueError):
            vehicle.range = 1100

    def test_comparison_methods(self):
        # Test the __lt__ and __eq__ methods
        vehicle1 = Vehicle("Chair 1", "for sleep", weight=100, fuel_level=500)
        vehicle2 = Vehicle("Window 1", "for see", weight=90, fuel_level=400)
        vehicle3 = Vehicle("Chair 2", "for sit", weight=50, fuel_level=200)

        # Test less than (__lt__)
        self.assertTrue(vehicle2 < vehicle1)  # Check if vehicle2 has less range than vehicle1
        self.assertTrue(vehicle3 < vehicle2)  # Check if vehicle2 has less range than vehicle3
        self.assertFalse(vehicle1 < vehicle2)
        
        # Test equal (__eq__)
        self.assertTrue(vehicle1 == vehicle1)  # Check if a vehicle is equal to itself
        self.assertTrue(vehicle2 == vehicle2)
        self.assertTrue(vehicle3 == vehicle3)
        self.assertFalse(vehicle1 == vehicle2)  # Check if different vehicles are not equal

    def test_copy_method(self):
        # Test the __copy__ method
        vehicle = Vehicle("Happy 1", "Be happy", weight=30, fuel_level=450)
        
        # Create a copy of the vehicle
        copied_vehicle = vehicle.__copy__()

        # Check if the copied vehicle is not the same object as the original
        self.assertIsNot(vehicle, copied_vehicle)
        
        # Check if the copied vehicle has the same attributes as the original
        self.assertEqual(str(vehicle.call_sign) + " copy", copied_vehicle.call_sign)
        self.assertEqual(vehicle.purpose, copied_vehicle.purpose)
        self.assertEqual(vehicle.weight, copied_vehicle.weight)
        self.assertEqual(vehicle.fuel_level, copied_vehicle.fuel_level)
        self.assertEqual(vehicle.range, copied_vehicle.range)
