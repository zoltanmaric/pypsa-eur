# SPDX-FileCopyrightText: Contributors to PyPSA-Eur <https://github.com/pypsa/pypsa-eur>
#
# SPDX-License-Identifier: MIT

"""
Tests the functionalities of scripts/build_osm_network.py.
"""

import string
import sys

sys.path.append("./scripts")

from scripts.build_osm_network import _segment_suffixes


def test_the_first_suffixes_are_the_plain_alphabet():
    assert _segment_suffixes(26) == list(string.ascii_lowercase)


def test_there_is_one_suffix_per_segment_past_the_alphabet():
    # A line crossing 27 buses used to get 26 suffixes, which pandas rejected as a length mismatch.
    assert len(_segment_suffixes(27)) == 27
    assert len(_segment_suffixes(1000)) == 1000


def test_the_suffixes_continue_two_letters_wide():
    assert _segment_suffixes(28)[26:] == ["aa", "ab"]
    assert _segment_suffixes(703)[-1] == "aaa"


def test_the_suffixes_are_unique():
    suffixes = _segment_suffixes(500)
    assert len(set(suffixes)) == len(suffixes)
