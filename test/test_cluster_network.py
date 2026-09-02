# SPDX-FileCopyrightText: Contributors to PyPSA-Eur <https://github.com/pypsa/pypsa-eur>
#
# SPDX-License-Identifier: MIT

import pathlib
import sys

import geopandas as gpd
import pandas as pd
from shapely.geometry import box

sys.path.append(str(pathlib.Path(__file__).parent.parent / "scripts"))

from cluster_network import cluster_regions


def test_cluster_regions_keeps_the_country_column():
    regions = gpd.GeoDataFrame(
        {"name": ["a", "b", "c"], "country": ["DE", "DE", "FR"]},
        geometry=[box(0, 0, 1, 1), box(1, 0, 2, 1), box(5, 5, 6, 6)],
        crs=4326,
    )
    busmap = pd.Series({"a": "DE0 1", "b": "DE0 1", "c": "FR0 1"})

    clustered = cluster_regions((busmap,), regions, with_country=True)

    assert clustered.set_index("name").country.to_dict() == {
        "DE0 1": "DE",
        "FR0 1": "FR",
    }
