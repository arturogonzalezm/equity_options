"""
Unit tests for the app.py file
"""

import pytest
import pandas as pd

from app import color_negative_red_positive_green, apply_color


# Test for color_negative_red_positive_green function
@pytest.mark.parametrize("input_val, expected", [
    (-10, 'color: red'),
    (0, 'color: black'),
    (10, 'color: green'),
    ('not_a_number', '')  # Expect no style for non-numeric values
])
def test_color_negative_red_positive_green(input_val, expected):
    """
    Test the color_negative_red_positive_green function with different input values
    :param input_val: Input value to test
    :param expected: Expected output style
    :return: None
    """
    assert color_negative_red_positive_green(input_val) == expected


# Test for apply_color function
def test_apply_color():
    """
    Test the apply_color function with a DataFrame containing numeric and non-numeric columns
    :return: None
    """
    data = {
        'A': [1, -1, 0],
        'B': [10.5, -10.5, 0],
        'C': ['not_a_number', 'not_a_number', 'not_a_number']
    }
    df = pd.DataFrame(data)

    styled_df = apply_color(df)

    # Check the styles for numeric columns
    assert styled_df['A'][0] == 'color: green'
    assert styled_df['A'][1] == 'color: red'
    assert styled_df['A'][2] == 'color: black'
    assert styled_df['B'][0] == 'color: green'
    assert styled_df['B'][1] == 'color: red'
    assert styled_df['B'][2] == 'color: black'

    # Check the styles for non-numeric column (should be empty)
    assert styled_df['C'][0] == ''
    assert styled_df['C'][1] == ''
    assert styled_df['C'][2] == ''


if __name__ == "__main__":
    pytest.main()
