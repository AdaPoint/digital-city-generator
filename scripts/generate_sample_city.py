# This imports "csv" for when we write the generated city data to the CSV file
import csv
# This is for handing the file paths
from pathlib import Path
# This imports the CityGenerator class from "generator.py" (in the src folder)
from src.generator import CityGenerator


def main() -> None:
    # This sets the configuration for the generator
    seed = 123
    min_households = 20000
    max_households = 50000
    # This creates the generator instance
    gen = CityGenerator(
        seed=seed,
        min_households=min_households,
        max_households=max_households,
    )
    # This generates the city composition by using a method from the generator instance
    city = gen.generate_city()
    # This converts the city compositions into a list of rows for the CSV file
    rows = city.to_rows()

    # This prepares the output directory and file path
    out_dir = Path("data") / "samples"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"city_seed{seed}.csv"
    # This is pretty much saying that if there are no rows, then there isn't anything to write /:
    if not rows:
        print("No rows generated; nothing to write.")
        return
    # This takes the keys from the first row because they are the column headers
    fieldnames = list(rows[0].keys())
    # This opens the output file for writing
    with out_path.open("w", newline="", encoding="utf-8") as f:
        # This instantiates a CSV writer object that will write the dictionary rows we created to the file
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    # This basically prints out that it has successfully generated the city and the CSV file
    print("City generated.")
    print(f"  Seed:        {city.city_seed}")
    print(f"  Households:  {city.total_households}")
    print(f"  Population:  {city.total_population}")
    print(f"  Buckets:     {len(city.buckets)}")
    print(f"CSV written to: {out_path}")


if __name__ == "__main__":
    main()
