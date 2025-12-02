"""
Configuration for the minimal-core Digital City generator.

This file defines:
- building type probability distribution
- bedroom distribution per building type
- occupancy (household size) distribution per bedroom count

All numbers here are probabilities and should roughly sum to 1.0 per group.
"""

from typing import Dict


# This is the overall building type distribution.
P_BUILDING_TYPE: Dict[str, float] = {
    "SF": 0.45,  # Single-family
    "TH": 0.10,  # Townhouse / rowhouse
    "AP": 0.30,  # Low-rise apartments
    "MR": 0.10,  # Mid-rise apartments
    "HR": 0.05,  # High-rise apartments
}


# This is the bedroom distribution per building type.
# Interpret as; Keys: building_type -> {bedrooms -> probability}
P_BEDROOMS: Dict[str, Dict[int, float]] = {
    "SF": {1: 0.10, 2: 0.35, 3: 0.40, 4: 0.15},
    "TH": {1: 0.15, 2: 0.45, 3: 0.30, 4: 0.10},
    "AP": {1: 0.40, 2: 0.40, 3: 0.15, 4: 0.05},
    "MR": {1: 0.30, 2: 0.45, 3: 0.20, 4: 0.05},
    "HR": {1: 0.50, 2: 0.35, 3: 0.10, 4: 0.05},
}


# This is the occupancy (household size) distribution per bedroom count.
# Interpret as; Keys: bedrooms -> {occupants -> probability}
P_OCCUPANTS: Dict[int, Dict[int, float]] = {
    1: {1: 0.80, 2: 0.20},
    2: {1: 0.15, 2: 0.55, 3: 0.25, 4: 0.05},
    3: {2: 0.20, 3: 0.50, 4: 0.25, 5: 0.05},
    4: {2: 0.10, 3: 0.30, 4: 0.40, 5: 0.15, 6: 0.05},
}
