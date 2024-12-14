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
