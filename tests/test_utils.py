import pandas as pd
from extac import utils


def test_convert_list_of_dicts_to_dataframe():
    list_of_dicts = [{"a": [1, 2, 3]}, {"b": [10, 11, 12]}]
    df = utils.convert_list_of_dicts_to_dataframe(list_of_dicts)
    assert df.equals(pd.DataFrame({"a": [1, 2, 3], "b": [10, 11, 12]}))
