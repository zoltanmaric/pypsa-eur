# SPDX-FileCopyrightText: Contributors to PyPSA-Eur <https://github.com/pypsa/pypsa-eur>
#
# SPDX-License-Identifier: MIT

"""
Tests that the OpenStreetMap substation name is carried through the OSM
processing pipeline into buses.csv as the "osm_name" column.
"""

import pathlib
import sys

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point, Polygon

sys.path.append("./scripts")

from scripts.build_osm_network import (
    BUSES_COLUMNS,
    _finalise_network,
)
from scripts.clean_osm_data import _aggregate_substations, _finalise_substations


@pytest.fixture
def substations_dataframe():
    """
    Two substations, one carrying an OSM name and one without.

    The named substation is split over two OSM objects (suffixed ids), the
    first of which has no name, so that the aggregation strategy is exercised.
    """
    polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    return pd.DataFrame(
        {
            "id": ["way/1-0", "way/1-1", "way/2-0"],
            "name": [None, "Altbach", None],
            "voltage": [380000, 380000, 220000],
            "country": ["DE", "DE", "DE"],
            "power": ["substation", "substation", "substation"],
            "substation": ["transmission", "transmission", "transmission"],
            "frequency": ["50", "50", "50"],
            "under_construction": [False, False, False],
            "start_date": [None, None, None],
            "geometry": [Point(0.5, 0.5), Point(0.5, 0.5), Point(2.5, 2.5)],
            "polygon": [polygon, polygon, polygon],
        }
    )


def test_aggregate_substations_takes_first_non_empty_name(substations_dataframe):
    """
    Substations merged from several OSM objects keep the first non-empty name.
    """
    df = _aggregate_substations(substations_dataframe)
    names = df.set_index("id")["name"]
    assert names["way/1"] == "Altbach"
    assert names["way/2"] == ""


def test_finalise_substations_name_is_empty_string(substations_dataframe):
    """
    A substation without an OSM name yields an empty string, never NaN.
    """
    df = _finalise_substations(_aggregate_substations(substations_dataframe))
    names = df.set_index("bus_id")["name"]
    assert names["way/1"] == "Altbach"
    assert names["way/2"] == ""
    assert not names.isna().any()


def _empty_frame(columns, dtypes=None):
    dtypes = dtypes or {}
    return pd.DataFrame(
        {col: pd.Series(dtype=dtypes.get(col, object)) for col in columns}
    )


def test_osm_name_reaches_buses_csv(tmp_path, substations_dataframe):
    """
    The OSM name survives into buses.csv as "osm_name", empty where unnamed.
    """
    assert "osm_name" in BUSES_COLUMNS

    all_buses = gpd.GeoDataFrame(
        {
            "bus_id": ["way/1-380", "way/2-220"],
            "station_id": ["way/1", "way/2"],
            "name": ["Altbach", ""],
            "voltage": [380000.0, 220000.0],
            "dc": [False, False],
            "country": ["DE", "DE"],
            "contains": ["way/1", "way/2"],
            "geometry": [Point(0.5, 0.5), Point(2.5, 2.5)],
        },
        crs="EPSG:4326",
    )

    lines = _empty_frame(
        ["line_id", "contains_lines", "circuits", "underground", "geometry"]
        + ["bus0", "bus1"],
        {"voltage": float, "length": float},
    )
    lines["voltage"] = pd.Series(dtype=float)
    lines["length"] = pd.Series(dtype=float)

    transformers = _empty_frame(
        ["transformer_id", "bus0", "bus1", "s_nom", "station_id", "geometry"],
        {"voltage_bus0": float, "voltage_bus1": float},
    )
    transformers["voltage_bus0"] = pd.Series(dtype=float)
    transformers["voltage_bus1"] = pd.Series(dtype=float)

    links = _empty_frame(["link_id"])
    converters = _empty_frame(["converter_id"])

    buses, _, _, _, _ = _finalise_network(
        all_buses, converters, lines, links, transformers
    )

    assert "osm_name" in buses.columns

    path_buses = pathlib.Path(tmp_path, "buses.csv")
    buses.to_csv(path_buses, quotechar="'")
    buses_csv = pd.read_csv(
        path_buses, quotechar="'", index_col=0, keep_default_na=False
    )

    assert buses_csv.loc["way/1-380", "osm_name"] == "Altbach"
    assert buses_csv.loc["way/2-220", "osm_name"] == ""
    assert "name" not in buses_csv.columns


def test_osm_name_empty_when_source_column_missing():
    """
    Buses arriving without a name column (e.g. DC buses) get an empty string.
    """
    all_buses = gpd.GeoDataFrame(
        {
            "bus_id": ["way/3-380"],
            "station_id": ["way/3"],
            "voltage": [380000.0],
            "dc": [True],
            "country": ["DE"],
            "contains": ["way/3"],
            "geometry": [Point(1.0, 1.0)],
        },
        crs="EPSG:4326",
    )

    lines = _empty_frame(
        ["line_id", "contains_lines", "circuits", "underground", "geometry"]
        + ["bus0", "bus1"]
    )
    lines["voltage"] = pd.Series(dtype=float)
    lines["length"] = pd.Series(dtype=float)

    transformers = _empty_frame(
        ["transformer_id", "bus0", "bus1", "s_nom", "station_id", "geometry"]
    )
    transformers["voltage_bus0"] = pd.Series(dtype=float)
    transformers["voltage_bus1"] = pd.Series(dtype=float)

    buses, _, _, _, _ = _finalise_network(
        all_buses,
        _empty_frame(["converter_id"]),
        lines,
        _empty_frame(["link_id"]),
        transformers,
    )

    assert buses.loc["way/3-380", "osm_name"] == ""
