# src/buckets.py

"""
HouseholdBucket: the atomic category in the Digital City.

Each bucket represents many identical households:
- same building type
- same number of bedrooms
- same number of occupants
"""

from dataclasses import dataclass


@dataclass
class HouseholdBucket:
    building_type: str  # "SF", "TH", "AP", "MR", "HR"
    bedrooms: int       # 1, 2, 3, 4
    occupants: int      # people per household
    units: int          # number of households in this bucket

    @property
    def households(self) -> int:
        """Alias for units (households)."""
        return self.units

    @property
    def people(self) -> int:
        """Total people in this bucket."""
        return self.units * self.occupants
