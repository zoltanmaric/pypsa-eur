# SPDX-FileCopyrightText: Contributors to PyPSA-Eur <https://github.com/pypsa/pypsa-eur>>
#
# SPDX-License-Identifier: MIT

"""
Tests the functionalities of scripts/build_powerplants.py.
"""

import pathlib
import sys

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from shapely.geometry import box

sys.path.append("./scripts")

from build_powerplants import (
    map_to_country_bus,
    add_custom_powerplants,
    replace_natural_gas_fueltype,
    replace_natural_gas_technology,
)

path_cwd = pathlib.Path.cwd()


@pytest.mark.parametrize(
    "query_value,expected",
    [(False, (131, 18)), (True, (137, 18))],
)
def test_add_custom_powerplants(config, query_value, expected):
    """
    Verify what returned by add_custom_powerplants.
    """
    config["electricity"]["custom_powerplants"] = query_value
    custom_powerplants_path = pathlib.Path(
        path_cwd, "test", "test_data", "custom_powerplants_DE.csv"
    )
    ppl_path = pathlib.Path(path_cwd, "test", "test_data", "powerplants_DE.csv")
    ppl_df = pd.read_csv(ppl_path)
    ppl_final = add_custom_powerplants(
        ppl_df,
        custom_powerplants_path,
        config["electricity"]["custom_powerplants"],
    )
    assert ppl_df.shape == (131, 18)
    assert ppl_final.shape == expected


def test_replace_natural_gas_technology():
    """
    Verify what returned by replace_natural_gas_technology.
    """
    input_df = pd.DataFrame(
        {
            "Name": [
                "plant_hydro",
                "plant_ng_1",
                "plant_ng_2",
                "plant_ng_3",
                "plant_ng_4",
            ],
            "Fueltype": [
                "Hydro",
                "Natural Gas",
                "Natural Gas",
                "Natural Gas",
                "Natural Gas",
            ],
            "Technology": [
                "Run-Of-River",
                "Steam Turbine",
                "Combustion Engine",
                "Not Found",
                np.nan,
            ],
        }
    )

    reference_df = pd.DataFrame(
        {
            "Name": [
                "plant_hydro",
                "plant_ng_1",
                "plant_ng_2",
                "plant_ng_3",
                "plant_ng_4",
            ],
            "Fueltype": [
                "Hydro",
                "Natural Gas",
                "Natural Gas",
                "Natural Gas",
                "Natural Gas",
            ],
            "Technology": ["Run-Of-River", "CCGT", "OCGT", "CCGT", "CCGT"],
        }
    )
    modified_df = input_df.assign(Technology=replace_natural_gas_technology)
    comparison_df = modified_df.compare(reference_df)
    assert comparison_df.empty


def test_replace_natural_gas_fueltype():
    """
    Verify what returned by replace_natural_gas_fueltype.
    """
    input_df = pd.DataFrame(
        {
            "Name": [
                "plant_hydro",
                "plant_ng_1",
                "plant_ng_2",
            ],
            "Fueltype": [
                "Hydro",
                "Gas",
                "Natural",
            ],
            "Technology": [
                "Run-Of-River",
                "CCGT",
                "OCGT",
            ],
        }
    )

    reference_df = pd.DataFrame(
        {
            "Name": [
                "plant_hydro",
                "plant_ng_1",
                "plant_ng_2",
            ],
            "Fueltype": [
                "Hydro",
                "Natural Gas",
                "Natural Gas",
            ],
            "Technology": [
                "Run-Of-River",
                "CCGT",
                "OCGT",
            ],
        }
    )
    modified_df = input_df.assign(Fueltype=replace_natural_gas_fueltype)
    comparison_df = modified_df.compare(reference_df)
    assert comparison_df.empty


def test_map_to_country_bus_uses_the_country_column():
    # Region names carry no country prefix (as with ``clusters: all``, where buses keep OSM ids)
    regions = gpd.GeoDataFrame(
        {"country": ["DE", "FR"]},
        index=pd.Index(["relation/1-380", "way/2-225"], name="name"),
        geometry=[box(10, 50, 11, 51), box(2, 48, 3, 49)],
        crs=4326,
    )
    plants = gpd.GeoDataFrame(
        {"Country": ["DE", "FR", "FR"]},
        geometry=gpd.points_from_xy([10.5, 2.5, 3.02], [50.5, 48.5, 48.5]),
        crs=4326,
    )

    assigned = map_to_country_bus(plants, regions)

    # inside their regions; the third plant is ~1.5 km outside and snaps to the nearest one
    assert assigned.bus.tolist() == ["relation/1-380", "way/2-225", "way/2-225"]
    # the regions' country column must not leak into the plant table
    assert "country" not in assigned.columns


def test_a_plant_on_a_shared_region_boundary_gets_one_bus():
    # Two regions meeting at longitude 11: a plant exactly on the seam joins to both.
    regions = gpd.GeoDataFrame(
        {"country": ["DE", "DE"]},
        index=pd.Index(["relation/1-380", "relation/2-220"], name="name"),
        geometry=[box(10, 50, 11, 51), box(11, 50, 12, 51)],
        crs=4326,
    )
    plants = gpd.GeoDataFrame(
        {"Country": ["DE"]},
        geometry=gpd.points_from_xy([11.0], [50.5]),
        crs=4326,
    )

    assigned = map_to_country_bus(plants, regions)

    # One row per plant, not one per region it touches.
    assert len(assigned) == 1
    assert assigned.index.is_unique
    assert assigned.bus.iloc[0] in {"relation/1-380", "relation/2-220"}


def test_a_plant_equidistant_from_two_regions_gets_one_bus():
    # Outside both regions and exactly between them, so sjoin_nearest ties.
    regions = gpd.GeoDataFrame(
        {"country": ["DE", "DE"]},
        index=pd.Index(["relation/1-380", "relation/2-220"], name="name"),
        geometry=[box(10, 50, 11, 51), box(12, 50, 13, 51)],
        crs=4326,
    )
    plants = gpd.GeoDataFrame(
        {"Country": ["DE"]},
        geometry=gpd.points_from_xy([11.5], [50.5]),
        crs=4326,
    )

    assigned = map_to_country_bus(plants, regions)

    assert len(assigned) == 1
    assert assigned.index.is_unique
