# src/city.py

"""
CityComposition: the full synthetic city at the minimal-core level.

Stores:
- total households (scalar)
- seed used to generate the city
- list of HouseholdBuckets
"""

from dataclasses import dataclass, field
from typing import List, Dict

from buckets import HouseholdBucket


@dataclass
class CityComposition:
    total_households: int
    city_seed: int
    buckets: List[HouseholdBucket] = field(default_factory=list)

    def add_bucket(self, bucket: HouseholdBucket) -> None:
        """
        Add a bucket to the city.
        Buckets with zero or negative units are ignored.
        """
        if bucket.units <= 0:
            return
        self.buckets.append(bucket)

    @property
    def total_population(self) -> int:
        """Total people across all buckets."""
        return sum(b.people for b in self.buckets)

    @property
    def total_units(self) -> int:
        """Total households (sum of units) across all buckets."""
        return sum(b.units for b in self.buckets)

    def to_rows(self) -> List[Dict[str, object]]:
        """
        Convert the city into a list of dict rows for CSV/DataFrame export.

        Schema:
        - city_total_households
        - city_seed
        - building_type
        - bedrooms
        - occupants
        - units
        """
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