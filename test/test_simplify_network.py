# SPDX-FileCopyrightText: Contributors to PyPSA-Eur <https://github.com/pypsa/pypsa-eur>
#
# SPDX-License-Identifier: MIT

"""
Tests the functionalities of scripts/simplify_network.py.
"""

import sys
from functools import reduce

import pandas as pd
import pypsa
import pytest

sys.path.append("./scripts")

from scripts.cluster_network import cluster_regions
from scripts.prepare_network import set_line_s_max_pu
from scripts.simplify_network import simplify_network_to_380


@pytest.fixture
def two_voltage_level_network():
    """
    A minimal network with a 380 kV and a 220 kV bus joined by a transformer.

    The transformer runs from the lower to the higher voltage level (bus0 ->
    bus1), matching what `base_network.py` builds: `simplify_network_to_380`
    maps bus0 onto bus1, so the 380 kV bus is the one that survives the lift.
    """
    n = pypsa.Network()
    n.add("Bus", "380_a", v_nom=380.0, x=0.0, y=0.0, country="DE", carrier="AC")
    n.add("Bus", "380_b", v_nom=380.0, x=1.0, y=0.0, country="DE", carrier="AC")
    n.add("Bus", "220_a", v_nom=220.0, x=0.0, y=1.0, country="DE", carrier="AC")
    n.add(
        "Line",
        "line_380",
        bus0="380_a",
        bus1="380_b",
        v_nom=380.0,
        s_nom=2000.0,
        type="Al/St 240/40 4-bundle 380.0",
        num_parallel=1,
        length=100.0,
    )
    n.add(
        "Transformer",
        "trafo",
        bus0="220_a",
        bus1="380_a",
        s_nom=1000.0,
    )
    n.add("Load", "load_220", bus="220_a", p_set=100.0)
    return n


def test_simplify_network_to_380_removes_transformers(two_voltage_level_network):
    """
    With to_380 enabled, transformers are removed and voltage levels flattened.
    """
    n = two_voltage_level_network
    n, trafo_map = simplify_network_to_380(n, "Al/St 240/40 4-bundle 380.0")

    assert n.transformers.empty
    assert (n.buses.v_nom == 380.0).all()
    assert "220_a" not in n.buses.index
    # The load moved from the 220 kV bus onto the 380 kV bus behind the trafo.
    assert n.loads.at["load_220", "bus"] == "380_a"
    assert trafo_map["220_a"] == "380_a"


def test_identity_busmap_keeps_transformers(two_voltage_level_network):
    """
    With to_380 disabled, the identity busmap keeps transformers and v_nom.

    This mirrors the `else` branch of the `to_380` switch in
    `simplify_network.py`'s `__main__`, and checks that the identity busmap is
    a valid first element for both `reduce(lambda x, y: x.map(y), ...)` and
    `cluster_regions`.
    """
    n = two_voltage_level_network
    trafo_map = pd.Series(n.buses.index, index=n.buses.index)

    assert not n.transformers.empty
    assert set(n.buses.v_nom) == {380.0, 220.0}

    busmaps = [trafo_map]
    busmap_s = reduce(lambda x, y: x.map(y), busmaps[1:], busmaps[0])
    assert busmap_s.equals(trafo_map)
    assert set(busmap_s.index) == set(n.buses.index)

    # A second busmap composed on top of the identity must behave as usual.
    second = pd.Series(["380_a", "380_a", "220_a"], index=["380_a", "380_b", "220_a"])
    composed = reduce(lambda x, y: x.map(y), [trafo_map, second][1:], trafo_map)
    assert composed.to_dict() == second.to_dict()


def test_cluster_regions_accepts_identity_busmap(two_voltage_level_network):
    """
    `cluster_regions` tolerates an identity busmap as its first element.
    """
    gpd = pytest.importorskip("geopandas")
    shapely = pytest.importorskip("shapely.geometry")

    n = two_voltage_level_network
    trafo_map = pd.Series(n.buses.index, index=n.buses.index)

    regions = gpd.GeoDataFrame(
        {
            "name": list(n.buses.index),
            "country": ["DE"] * len(n.buses),
            "geometry": [shapely.box(i, 0, i + 1, 1) for i in range(len(n.buses))],
        },
        crs="EPSG:4326",
    )

    clustered = cluster_regions([trafo_map], regions, with_country=True)
    assert set(clustered["name"]) == set(n.buses.index)


def test_set_line_s_max_pu_caps_transformers(two_voltage_level_network):
    """
    The N-1 margin is applied to transformers, not only to lines.

    Upstream never needed this because the 380 kV lift removed transformers
    before `prepare_network` ran; `to_380: false` is what exposes it.
    """
    n = two_voltage_level_network
    set_line_s_max_pu(n, 0.7)

    assert (n.lines["s_max_pu"] == 0.7).all()
    assert not n.transformers.empty
    assert (n.transformers["s_max_pu"] == 0.7).all()
