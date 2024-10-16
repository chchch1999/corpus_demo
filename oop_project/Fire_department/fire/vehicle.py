"""Vehicle management for the fires department
"""

__author__ = 'Chieh-Ching Chen'

print('dev: loading module ' + __name__)

import copy

class Vehicle:
    # Class-level dictionary to store unique call signs
    unique_call_signs = {}

    MAX_WEIGHT = 100  # Maximum weight
    MAX_FUEL_LEVEL = 500  # Maximum fuel level
    MAX_RANGE = 250  # Maximum range

    def __init__(self, call_sign, purpose, **kwargs):
        # Check that exactly two of the three properties are provided
        properties_provided = sum(property in kwargs for property in ("range", "weight", "fuel_level"))
        if properties_provided != 2:
            raise ValueError("You must provide exactly two of the three properties: 'range', 'weight', and 'fuel_level'")
        
        # Calculate weight and fuel level based on provided properties        
        if 'weight' in kwargs and 'fuel_level' in kwargs:
            self._weight = kwargs['weight']
            self._fuel_level = kwargs['fuel_level']
        elif 'weight' in kwargs and 'range' in kwargs:
            self._fuel_level = kwargs['range'] * kwargs['weight'] / 20
            self._weight = kwargs['weight']
        elif 'fuel_level' in kwargs and 'range' in kwargs:
            self._weight = 20 * kwargs['fuel_level'] / kwargs['range']
            self._fuel_level = kwargs['fuel_level']
        
        # Set properties based on provided values
        for property in kwargs:
            if hasattr(self.__class__, property):
                attribute = getattr(self.__class__, property)
                if hasattr(attribute, 'fset') and attribute.fset is not None:
                    setattr(self, property, kwargs[property])
        
        self._call_sign = call_sign
        self._purpose = purpose

        # Check if the call sign is unique
        if self.call_sign in Vehicle.unique_call_signs:
            raise ValueError("Call sign must be unique")
        else:
            Vehicle.unique_call_signs[self.call_sign] = self.call_sign
    
    @property
    def call_sign(self):
        return self._call_sign

    @call_sign.setter
    def call_sign(self, value):
        # Check if the new call sign is a string
        if not isinstance(value, str):
            raise ValueError("Call sign must be a string")
        self._call_sign = value

    @property
    def purpose(self):
        return self._purpose

    @purpose.setter
    def purpose(self, value):
        # Check if the new purpose is a string
        if not isinstance(value, str):
            raise ValueError("Purpose must be a string")
        self._purpose = value
    
    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        # Check if the new weight is positive and within the maximum limit
        if 0 < value <= Vehicle.MAX_WEIGHT:
            self._weight = value
        else:
            raise ValueError(f"Weight must be positive and less than or equal to {Vehicle.MAX_WEIGHT}")

    @property
    def fuel_level(self):
        return self._fuel_level

    @fuel_level.setter
    def fuel_level(self, value):
        # Check if the new fuel level is non-negative and within the maximum limit
        if 0 <= value <= Vehicle.MAX_FUEL_LEVEL:
            self._fuel_level = value
        else:
            raise ValueError(f"Fuel level must be non-negative and less than or equal to {Vehicle.MAX_FUEL_LEVEL}")

    @property
    def range(self):
        self._range = 20 * self._fuel_level / self._weight
        return self._range

    @range.setter
    def range(self, value):
        if 0 <= value <= Vehicle.MAX_RANGE:
            self._range = value
            self._fuel_level = (value * self._weight) / 20
            self._weight = 20 * self._fuel_level / value
        else:
            raise ValueError(f"Range must be non-negative and less than or equal to {Vehicle.MAX_RANGE}")

    def __str__(self):
        return f"Call Sign: {self.call_sign}, Purpose: {self.purpose}, Weight: {self.weight} t, " \
               f"Fuel Level: {self.fuel_level} liters, Range: {self.range} km"
    
    def __repr__(self):
        return f"Vehicle(call_sign='{self.call_sign}', purpose='{self.purpose}', " \
               f"weight={self.weight}, fuel_level={self.fuel_level}, range_km={self.range})"

    def __lt__(self, other):
        # Compare vehicles based on their range
        if not isinstance(other, Vehicle):
            raise TypeError(f"'==' not supported between Vehicle and {type(other).__name__}")
        else:
            return self.range < other.range

    def __eq__(self, other):
        # Check if two vehicles are equal based on their call sign
        if not isinstance(other, Vehicle):
            raise TypeError(f"'==' not supported between Vehicle and {type(other).__name__}")
        else:
            return self.call_sign == other.call_sign

    def __copy__(self):
        # Create a shallow copy of the vehicle
        new_call_sign = self.call_sign + " copy"
        new_vehicle = Vehicle(
            call_sign = new_call_sign,
            purpose = self.purpose,
            weight = self.weight,
            fuel_level = self.fuel_level
        )
        
        return new_vehicle

    def to_dict(self):
        # Convert object attributes to a dictionary
        vehicle_dict = {
            "call_sign": self.call_sign,
            "purpose": self.purpose,
            "weight": self.weight,
            "fuel_level": self.fuel_level,
        }
        if self.range is not None:
            vehicle_dict["_range"] = self.range
        return vehicle_dict