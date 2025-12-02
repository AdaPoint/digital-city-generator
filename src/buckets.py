from dataclasses import dataclass

# This dataclass represents a bucket of households with specific information
@dataclass
class HouseholdBucket:
    building_type: str  # "SF", "TH", "AP", "MR", "HR"
    bedrooms: int       # 1, 2, 3, 4
    occupants: int      # people per household
    units: int          # number of households in this bucket

    # The meaning of this property is to return the number of households in this bucket
    @property
    def households(self) -> int:
        return self.units

    # The meaning of this property is to return the total number of people in this bucket
    @property
    def people(self) -> int:
        return self.units * self.occupants
