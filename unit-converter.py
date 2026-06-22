#!/usr/bin/env python3
"""
Unit Converter
==============
A versatile unit converter for length, weight, temperature, volume, and more.

Features:
- Length, Weight, Temperature, Volume, Area, Speed
- Interactive mode (great for Pydroid)
- Easy to extend with more units

Author: RetroMatt2077
"""

import argparse
from typing import Dict, Callable


# Conversion factors and functions
CONVERSIONS = {
    "length": {
        "meter": 1,
        "kilometer": 0.001,
        "centimeter": 100,
        "millimeter": 1000,
        "inch": 39.3701,
        "foot": 3.28084,
        "yard": 1.09361,
        "mile": 0.000621371,
    },
    "weight": {
        "kilogram": 1,
        "gram": 1000,
        "milligram": 1_000_000,
        "pound": 2.20462,
        "ounce": 35.274,
        "ton": 0.00110231,
    },
    "temperature": {
        # Special handling required
    },
    "volume": {
        "liter": 1,
        "milliliter": 1000,
        "gallon": 0.264172,
        "quart": 1.05669,
        "pint": 2.11338,
        "cup": 4.22675,
    },
    "speed": {
        "kmh": 1,
        "mph": 0.621371,
        "mps": 0.277778,
        "knot": 0.539957,
    }
}


def celsius_to_fahrenheit(c: float) -> float:
    return (c * 9/5) + 32


def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5/9


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    # Convert to Celsius first
    if from_unit.lower() in ["c", "celsius"]:
        c = value
    elif from_unit.lower() in ["f", "fahrenheit"]:
        c = fahrenheit_to_celsius(value)
    else:
        raise ValueError("Unsupported temperature unit")

    # Convert from Celsius to target
    if to_unit.lower() in ["c", "celsius"]:
        return c
    elif to_unit.lower() in ["f", "fahrenheit"]:
        return celsius_to_fahrenheit(c)
    else:
        raise ValueError("Unsupported temperature unit")


def convert_unit(value: float, from_unit: str, to_unit: str, category: str) -> float:
    if category == "temperature":
        return convert_temperature(value, from_unit, to_unit)

    units = CONVERSIONS.get(category.lower())
    if not units:
        raise ValueError(f"Unknown category: {category}")

    if from_unit.lower() not in units or to_unit.lower() not in units:
        raise ValueError("Invalid unit for this category")

    # Convert to base unit then to target unit
    base = value / units[from_unit.lower()]
    result = base * units[to_unit.lower()]
    return result


def main():
    parser = argparse.ArgumentParser(description="🔄 Unit Converter")
    parser.add_argument("-c", "--category", choices=["length", "weight", "temperature", "volume", "speed"],
                        default="length", help="Category to convert")
    parser.add_argument("-v", "--value", type=float, help="Value to convert")
    parser.add_argument("-f", "--from", dest="from_unit", help="From unit")
    parser.add_argument("-t", "--to", dest="to_unit", help="To unit")
    parser.add_argument("-p", "--prompt", action="store_true",
                        help="Interactive mode (recommended on Pydroid)")

    args = parser.parse_args()

    if args.prompt or not (args.value and args.from_unit and args.to_unit):
        print("🔄 Unit Converter\n")
        print("Available categories: length, weight, temperature, volume, speed")
        
        category = input("Enter category: ").strip().lower()
        if category not in CONVERSIONS and category != "temperature":
            print("❌ Invalid category!")
            return

        value = float(input("Enter value: "))
        from_unit = input("From unit: ").strip()
        to_unit = input("To unit: ").strip()

        try:
            result = convert_unit(value, from_unit, to_unit, category)
            print(f"\n✅ {value} {from_unit} = {result:.4f} {to_unit}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        try:
            result = convert_unit(args.value, args.from_unit, args.to_unit, args.category)
            print(f"\n✅ {args.value} {args.from_unit} = {result:.4f} {args.to_unit}")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
