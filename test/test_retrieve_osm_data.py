# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Contributors to PyPSA-Eur <https://github.com/pypsa/pypsa-eur>
#
# SPDX-License-Identifier: MIT
"""Tests for retrieve_osm_data."""

import pathlib
import sys
from unittest.mock import patch

import pytest
import requests

sys.path.append("./scripts")

from scripts.retrieve_osm_data import retrieve_osm_data


@pytest.mark.parametrize("max_tries", [1, 3, 5])
def test_max_tries_is_honoured(tmp_path, max_tries):
    """The caller's max_tries decides how often a failing feature is retried."""
    output = {"substations_way": str(tmp_path / "substations_way.json")}

    with (
        patch(
            "scripts.retrieve_osm_data.requests.post",
            side_effect=requests.exceptions.ConnectionError("boom"),
        ) as post,
        patch("scripts.retrieve_osm_data.time.sleep"),
    ):
        retrieve_osm_data(
            country="DE",
            output=output,
            features=["substations_way"],
            max_tries=max_tries,
        )

    assert post.call_count == max_tries
    assert not pathlib.Path(output["substations_way"]).exists()
