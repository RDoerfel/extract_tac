import pandas as pd
import numpy as np
from extac import utils


def test_convert_dict_to_df():
    d = {"a": [1, 2, 3], "b": [4, 5, 6]}
    df = utils.convert_dict_to_df(d)
    assert isinstance(df, pd.DataFrame)
    assert np.all(df.columns == ["a", "b"])
    assert np.all(df.values == np.array([[1, 4], [2, 5], [3, 6]]))


def test_convert_dict_to_df_one_entry():
    d = {"a": np.array([1]), "b": np.array([4])}
    df = utils.convert_dict_to_df(d)
    assert isinstance(df, pd.DataFrame)
    assert np.all(df.columns == ["a", "b"])
    assert np.all(df.values == np.array([[1, 4]]))


def test_get_measure_func_mean():
    measure_func = utils._get_measure_func("mean")
    assert measure_func == np.mean


def test_get_measure_func_median():
    measure_func = utils._get_measure_func("median")
    assert measure_func == np.median


def test_get_measure_func_std():
    measure_func = utils._get_measure_func("std")
    assert measure_func == np.std


def test_get_measure_func_invalid():
    try:
        utils._get_measure_func("invalid")
    except ValueError as e:
        assert str(e) == "Invalid measure string"
    else:
        assert False, "Expected ValueError"


def test_pivot_and_sort_data():
    # Mock data in long format
    data = [
        {"timepoint": 0, "roi": "roi1", "measure": "mean", "value": 1.0},
        {"timepoint": 1, "roi": "roi1", "measure": "mean", "value": 2.0},
        {"timepoint": 0, "roi": "roi1", "measure": "median", "value": 1.5},
        {"timepoint": 1, "roi": "roi1", "measure": "median", "value": 2.5},
        {"timepoint": 0, "roi": "roi2", "measure": "mean", "value": 4.0},
        {"timepoint": 1, "roi": "roi2", "measure": "mean", "value": 5.0},
        {"timepoint": 0, "roi": "roi2", "measure": "median", "value": 4.5},
        {"timepoint": 1, "roi": "roi2", "measure": "median", "value": 5.5},
    ]

    df_pivoted = utils.pivot_and_sort_data(data)

    # Assertions
    assert list(df_pivoted.columns) == ["timepoint", "roi", "mean", "median"]
    assert df_pivoted.shape == (4, 4)  # 2 ROIs x 2 timepoints
    assert df_pivoted.loc[0, "mean"] == 1.0
    assert df_pivoted.loc[3, "median"] == 5.5
