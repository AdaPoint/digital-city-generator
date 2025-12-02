from dataclasses import dataclass, field
from typing import List, Dict

from buckets import HouseholdBucket

# This class represents the overall composition of our digital city
@dataclass
class CityComposition:
    total_households: int
    city_seed: int
    buckets: List[HouseholdBucket] = field(default_factory=list)
    
    # This method adds our household buckets to our city composition
    def add_bucket(self, bucket: HouseholdBucket) -> None:
        if bucket.units <= 0:
            return
        self.buckets.append(bucket)

    # "@property" is a decorator (a decorator is a special type of function that modifies the behavior of another function)
    # This decorator allows us to access this method as if it were an attribute (pretty much being able to call it without parentheses "()")
    @property
    def total_population(self) -> int:
        return sum(b.people for b in self.buckets)

    @property
    def total_units(self) -> int:
        return sum(b.units for b in self.buckets)

    # This method converts the city composition into a list of dictionary rows
    def to_rows(self) -> List[Dict[str, object]]:
        rows: List[Dict[str, object]] = []
        for b in self.buckets:
            rows.append(
                {
                    "city_total_households": self.total_households,
                    "city_seed": self.city_seed,
                    "building_type": b.building_type,
                    "bedrooms": b.bedrooms,
                    "occupants": b.occupants,
                    "units": b.units,
                }
            )
        return rows