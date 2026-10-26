import argparse
import math
from pathlib import Path

import pandas as pd


GROUP_COLUMNS = ["Sex", "WeightClassKg"]
LIFT_COLUMNS = {
    "Best3SquatKg": "Squat",
    "Best3BenchKg": "Bench",
    "Best3DeadliftKg": "Deadlift",
    "TotalKg": "Total",
}
LEVEL_MULTIPLIERS = {
    "Untrained": -2.5,
    "Novice": -2.0,
    "Intermediate": -1.0,
    "Advanced": 0.0,
    "Master": 1.0,
    "Elite": 2.0,
    "World class": 2.5,
}


def load_results(csv_path: Path) -> pd.DataFrame:
    """Load the original cohort without restricting sex or weight class."""
    filter_columns = ["BirthYearClass", "Event", "Equipment", "Tested"]
    data = pd.read_csv(
        csv_path,
        usecols=GROUP_COLUMNS + filter_columns + list(LIFT_COLUMNS),
        dtype={column: "string" for column in GROUP_COLUMNS + filter_columns},
        low_memory=False,
    )
    eligible = (
        data["BirthYearClass"].eq("14-18")
        & data["Event"].eq("SBD")
        & data["Equipment"].eq("Raw")
        & data["Tested"].eq("Yes")
    )
    return (
        data.loc[eligible, GROUP_COLUMNS + list(LIFT_COLUMNS)]
        .dropna(subset=GROUP_COLUMNS)
        .copy()
    )


def calculate_standards(
    results: pd.DataFrame, increment: float = 2.5
) -> pd.DataFrame:
    """Return one row per sex, weight class, and lift; all weights are kg."""
    if not math.isfinite(increment) or increment <= 0:
        raise ValueError("The rounding increment must be positive and finite.")

    lifts = results.melt(
        id_vars=GROUP_COLUMNS,
        value_vars=list(LIFT_COLUMNS),
        var_name="Lift",
        value_name="WeightKg",
    )
    weights = pd.to_numeric(lifts["WeightKg"], errors="coerce")
    # Exclude missing/invalid values and failed lifts independently per lift.
    lifts["WeightKg"] = weights.where(weights.gt(0) & weights.lt(math.inf))
    lifts["Lift"] = lifts["Lift"].map(LIFT_COLUMNS)

    summary = (
        lifts.groupby(GROUP_COLUMNS + ["Lift"], sort=False)["WeightKg"]
        .agg(Count="count", MeanKg="mean", StdDevKg="std")
        .reset_index()
    )
    for level, multiplier in LEVEL_MULTIPLIERS.items():
        threshold = summary["MeanKg"] + multiplier * summary["StdDevKg"]
        # Like Python's round(), exact halfway values round to even.
        summary[level] = (threshold / increment).round() * increment

    # Sort numerically, placing an open class after its matching capped class.
    return (
        summary.assign(
            _class_limit=pd.to_numeric(summary["WeightClassKg"].str.rstrip("+")),
            _open_class=summary["WeightClassKg"].str.endswith("+"),
        )
        .sort_values(["Sex", "_class_limit", "_open_class"], kind="stable")
        .drop(columns=["_class_limit", "_open_class"])
        .reset_index(drop=True)
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="OpenPowerlifting source CSV")
    parser.add_argument(
        "--output", type=Path, default=Path("strength_standards.csv")
    )
    args = parser.parse_args()

    results = load_results(args.input)
    if results.empty:
        parser.error("No entries match the filters and have a sex and weight class.")

    standards = calculate_standards(results)
    standards.to_csv(args.output, index=False)
    print(standards.round(2).to_string(index=False, na_rep="N/A"))
    print(f"\nSaved {len(standards)} rows to {args.output}")


if __name__ == "__main__":
    main()
