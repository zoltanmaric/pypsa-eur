# SPDX-FileCopyrightText: Contributors to PyPSA-Eur <https://github.com/pypsa/pypsa-eur>
#
# SPDX-License-Identifier: MIT

import pandas as pd

from scripts.add_electricity import load_monthly_fuel_price


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
