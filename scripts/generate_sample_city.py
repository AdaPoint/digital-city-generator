# scripts/generate_sample_city.py

"""
Generate a sample city CSV using the minimal-core generator.

Usage (from project root):
    python scripts/generate_sample_city.py

Make sure your PYTHONPATH includes ./src, e.g.:

Linux/macOS:
    export PYTHONPATH=./src:$PYTHONPATH

Windows (PowerShell):
    $env:PYTHONPATH = ".\src;$env:PYTHONPATH"
"""

import csv
from pathlib import Path

from src.generator import CityGenerator


def main() -> None:
    # Configure generator
    seed = 123
    min_households = 20000
    max_households = 50000

    gen = CityGenerator(
        seed=seed,
        min_households=min_households,
        max_households=max_households,
    )

    city = gen.generate_city()
    rows = city.to_rows()

    # Ensure output directory exists
    out_dir = Path("data") / "samples"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"city_seed{seed}.csv"

    if not rows:
        print("No rows generated; nothing to write.")
        return

    fieldnames = list(rows[0].keys())

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("City generated.")
    print(f"  Seed:        {city.city_seed}")
    print(f"  Households:  {city.total_households}")
    print(f"  Population:  {city.total_population}")
    print(f"  Buckets:     {len(city.buckets)}")
    print(f"CSV written to: {out_path}")


if __name__ == "__main__":
    main()
