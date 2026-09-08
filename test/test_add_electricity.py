# SPDX-FileCopyrightText: Contributors to PyPSA-Eur <https://github.com/pypsa/pypsa-eur>
#
# SPDX-License-Identifier: MIT

import pandas as pd

from scripts.add_electricity import (
    load_and_aggregate_powerplants,
    load_monthly_fuel_price,
)

COSTS = pd.DataFrame(
    {
        "VOM": 1.0,
        "FOM": 1.0,
        "efficiency": 0.4,
        "capital_cost": 100.0,
        "marginal_cost": 10.0,
        "fuel": 20.0,
        "lifetime": 30.0,
    },
    index=["CCGT", "nuclear"],
)


def test_disaggregated_plants_without_names_get_named(tmp_path):
    ppl = pd.DataFrame(
        {
            "Name": [None, None, "Big Nuke"],
            "Fueltype": ["Natural Gas", "Natural Gas", "Nuclear"],
            "Technology": ["CCGT", "CCGT", "Steam Turbine"],
            "Set": ["PP", "PP", "PP"],
            "Country": ["DE", "DE", "FR"],
            "Capacity": [400.0, 600.0, 1600.0],
            "Efficiency": [0.55, 0.5, 0.33],
            "DateIn": [2000.0, 2010.0, 1990.0],
            "DateOut": [None, None, None],
            "lat": [52.0, 52.1, 48.0],
            "lon": [13.0, 13.1, 2.0],
            "bus": ["DE0 1", "DE0 1", "FR0 1"],
        }
    )
    fn = tmp_path / "powerplants.csv"
    ppl.to_csv(fn)

    generators = load_and_aggregate_powerplants(
        str(fn), COSTS, exclude_carriers=["CCGT"]
    )

    assert generators.loc["FR0 1 nuclear", "p_nom"] == 1600.0
    assert set(generators.index) == {"FR0 1 nuclear", "DE0 1 CCGT 0", "DE0 1 CCGT 1"}


def test_load_monthly_fuel_price_covers_a_window_off_the_month_boundary(tmp_path):
    fn = tmp_path / "monthly_fuel_price.csv"
    pd.DataFrame(
        {"gas": [30.0, 40.0]},
        index=pd.to_datetime(["2024-08-01", "2024-09-01"]),
    ).to_csv(fn)

    snapshots = pd.date_range("2024-08-29", periods=12, freq="2h")
    prices = load_monthly_fuel_price(fn, snapshots)

    assert not prices.isna().any().any()
    assert (prices["gas"] == 30.0).all()
