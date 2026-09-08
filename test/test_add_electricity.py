# SPDX-FileCopyrightText: Contributors to PyPSA-Eur <https://github.com/pypsa/pypsa-eur>
#
# SPDX-License-Identifier: MIT

"""Tests for selected helpers in scripts/add_electricity.py."""

import numpy as np
import pandas as pd
import pypsa
import xarray as xr

from scripts.add_electricity import (
    attach_load,
    attach_storageunits,
    attach_stores,
    estimate_efficiency,
    load_and_aggregate_powerplants,
    load_monthly_fuel_price,
)
from scripts.lib.validation.config.conventional import _EstimateEfficienciesConfig


def test_attach_load(tmp_path):
    """Clustered demand is attached per bus with scaling applied."""

    times = pd.date_range("2000-01-01", periods=2, freq="h")
    buses = ["zone_1", "zone_2"]
    values = np.array([[1.0, 2.0], [3.0, 4.0]])

    data = xr.DataArray(
        values,
        coords={"time": times, "bus": buses},
        dims=["time", "bus"],
        name="electricity demand (MW)",
    )
    load_path = tmp_path / "electricity_demand.nc"
    data.to_netcdf(load_path)

    n = pypsa.Network()
    n.set_snapshots(times)
    n.add("Bus", buses)

    attach_load(n, load_path.as_posix(), scaling=2.0)

    assert sorted(n.loads.index) == buses
    assert sorted(n.loads_t.p_set.columns) == buses
    np.testing.assert_allclose(n.loads_t.p_set[buses].values, 2.0 * values)


def test_attach_storageunits_energy_basis():
    """A dispatched-basis `max_hours` sizes the store to sustain it, at no extra cost."""
    costs = pd.DataFrame(
        {
            "capital_cost": {"iron-air": 157959.0, "battery": 60630.0},
            "marginal_cost": {"iron-air": 0.0, "battery": 0.0},
            "lifetime": {"iron-air": 17.5, "battery": 17.5},
            "efficiency": {
                "iron-air battery charge": 0.74,
                "iron-air battery discharge": 0.63,
                "battery inverter": 0.96,
            },
        }
    )
    max_hours = {"iron-air": 100, "battery": 6}

    n = pypsa.Network()
    n.add("Bus", ["bus_1", "bus_2"])
    attach_storageunits(n, costs, n.buses.index, ["iron-air", "battery"], max_hours)

    su = n.storage_units.set_index("carrier")

    iron_air = su.loc["iron-air"]
    np.testing.assert_allclose(iron_air.max_hours * iron_air.efficiency_dispatch, 100)
    np.testing.assert_allclose(iron_air.capital_cost, 157959.0)

    # Stored-basis carriers must be left alone, despite efficiency_dispatch < 1.
    np.testing.assert_allclose(su.loc["battery"].max_hours, 6)


def test_attach_stores_energy_basis():
    """A dispatched-basis store cost is converted to cost per MWh stored."""
    costs = pd.DataFrame(
        {
            "capital_cost": {
                "iron-air battery": 1000.0,
                "iron-air battery charge": 0.0,
                "iron-air battery discharge": 0.0,
            },
            "marginal_cost": 0.0,
            "lifetime": 17.5,
            "efficiency": {
                "iron-air battery": 1.0,
                "iron-air battery charge": 0.74,
                "iron-air battery discharge": 0.63,
            },
        }
    )

    n = pypsa.Network()
    n.add("Bus", ["bus_1"])
    attach_stores(n, costs, n.buses.index, ["iron-air"])

    np.testing.assert_allclose(n.stores.capital_cost, 630.0)


def test_estimate_efficiency():
    """Efficiency rises with build year (retrofit first), is clipped and degrades with age."""
    ppl = pd.DataFrame(
        {
            "carrier": ["CCGT", "coal", "coal", "biomass", "CCGT"],
            "datein": [2000, 1950, 1970, 2000, np.nan],
            "dateretrofit": [np.nan, np.nan, 2010, np.nan, np.nan],
        }
    )
    config = _EstimateEfficienciesConfig().model_dump()

    eta = estimate_efficiency(ppl, config)

    expected = [
        0.48 * (1 - 0.015),
        0.28 * (1 - 0.065),
        0.43 * (1 - 0.005),
        np.nan,
        np.nan,
    ]
    np.testing.assert_allclose(eta, expected)


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
