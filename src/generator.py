# src/generator.py

"""
CityGenerator: builds a minimal-core synthetic city.

Pipeline:
1. Draw total households H from [min_households, max_households].
2. Allocate H across building types.
3. For each building type, allocate to bedroom counts.
4. For each (building type, bedrooms), allocate to occupants.
5. Each (bt, bedrooms, occupants, units) becomes a HouseholdBucket.
"""

from dataclasses import dataclass

from city import CityComposition
from buckets import HouseholdBucket
from config import P_BUILDING_TYPE, P_BEDROOMS, P_OCCUPANTS
from utils.random_utils import RNG, allocate_discrete


@dataclass
class CityGenerator:
    seed: int
    min_households: int
    max_households: int

    def __post_init__(self) -> None:
        if self.min_households <= 0 or self.max_households < self.min_households:
            raise ValueError("Invalid household bounds.")
        self.rng = RNG(self.seed)

    def _draw_total_households(self) -> int:
        """
        Draw the total number of households for this city.
        """
        return self.rng.randint(self.min_households, self.max_households)

    def generate_city(self) -> CityComposition:
        """
        Generate a synthetic city composition using the 3-layer funnel.
        """
        total_households = self._draw_total_households()
        city = CityComposition(total_households=total_households, city_seed=self.seed)

        # Layer 1: allocate households to building types
        bt_counts = allocate_discrete(total_households, P_BUILDING_TYPE, self.rng)

        # Layer 2 & 3: expand each building type into buckets
        for bt, h_for_bt in bt_counts.items():
            if h_for_bt <= 0:
                continue

            # Bedrooms distribution for this building type
            bedroom_weights = P_BEDROOMS.get(bt)
            if not bedroom_weights:
                # No explicit bedroom config; treat as all 2BR for now
                bedroom_weights = {2: 1.0}

            # Allocate H_bt households across bedroom counts
            bed_counts = allocate_discrete(h_for_bt, bedroom_weights, self.rng)

            # For each bedroom count, allocate to occupants
            for bed, h_for_bt_bed in bed_counts.items():
                if h_for_bt_bed <= 0:
                    continue

                occ_weights = P_OCCUPANTS.get(bed)
                if not occ_weights:
                    # Fallback: single occupancy
                    occ_weights = {1: 1.0}

                occ_counts = allocate_discrete(h_for_bt_bed, occ_weights, self.rng)

                for occ, units in occ_counts.items():
                    if units <= 0:
                        continue

                    bucket = HouseholdBucket(
                        building_type=bt,
                        bedrooms=bed,
                        occupants=occ,
                        units=units,
                    )
                    city.add_bucket(bucket)

        return city
