# This imports dataclass so that we can use it to define "CityGenerator"
from dataclasses import dataclass
# This imports our other classes that we need to generate the city
from city import CityComposition
from buckets import HouseholdBucket
from config import P_BUILDING_TYPE, P_BEDROOMS, P_OCCUPANTS
from utils.random_utils import RNG, allocate_discrete

# This is the main class that generates the city
@dataclass
class CityGenerator:
    seed: int
    min_households: int
    max_households: int

    # "__post_init__" is a method I realized I needed for this generator to work properly, after some research
    # What it does is that it actually runs after the dataclass has been initialized as opposed to during initialization
    def __post_init__(self) -> None:
        # This checks if the household configurations that were set by us are valid
        if self.min_households <= 0 or self.max_households < self.min_households:
            # Right here we have an exception that will raise an error if the household values are not proper
            raise ValueError("Invalid household bounds.")
        # If everything is valid, the program then initializes the RNG object (random number generator) with the seed we provided
        self.rng = RNG(self.seed)
        
    # This method picks a random number (integer) between the min and max we set for households
    def _draw_total_households(self) -> int:
        return self.rng.randint(self.min_households, self.max_households)
    
    # This is the main method that generates the city composition
    # The "->" syntax pretty much tells the program that this method will return a CityComposition object
    def generate_city(self) -> CityComposition:
        total_households = self._draw_total_households()
        city = CityComposition(total_households=total_households, city_seed=self.seed)

        # This first layer distributes households across building types
        # So it generates single-family, multi-family, apartments, etc.
        # "allocate_discrete" is a function that will distribute the households we created according to the weights we set in the config
        bt_counts = allocate_discrete(total_households, P_BUILDING_TYPE, self.rng)

        # "bt" stands for building type, "h_for_bt" stands for households for building type
        # This is a classic "for loop" that iterates through each building type and its corresponding household count
        for bt, h_for_bt in bt_counts.items():
            # This check makes sure that if there are no households for the building type, it will skip to the next iteration
            if h_for_bt <= 0:
                continue

            # What this does is retrieve the bedroom distribution weights for the currecnt building type
            bedroom_weights = P_BEDROOMS.get(bt)
            # This check makes sure that if there are no bedroom weights for the building type, it will fall back to the default of the 2-bedroom configuration
            if not bedroom_weights:
                bedroom_weights = {2: 1.0}

            # This will allocate the households for the building type across bedroom counts according to the weights we set
            bed_counts = allocate_discrete(h_for_bt, bedroom_weights, self.rng)

            # For each bedroom count, allocate to occupants
            for bed, h_for_bt_bed in bed_counts.items():
                # This check makes sure that if there are no households for the bedroom count, then it will simply skip to tthe next iteration
                if h_for_bt_bed <= 0:
                    continue

                # This retrieves the occupancy weights for the current bedroom count
                occ_weights = P_OCCUPANTS.get(bed)
                if not occ_weights:
                    occ_weights = {1: 1.0}
                # This allocates the households for the building type and bedroom count across occupancy counts according to the weights we set
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
        # Finally, the method returns the generated city composition
        return city
