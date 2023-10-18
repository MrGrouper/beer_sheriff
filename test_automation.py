from automation import checkGameComplete, calculatePoints, wrtPoints
import pytest

def test_checkGameComplete():
    assert checkGameComplete(31960, 6) == ['DAL', '2023-10-17T00:15Z', 'True']
    assert checkGameComplete(33996, 5) == ['SEA', 'bye', 'False']

def test_calculatePoints():
    assert calculatePoints(31960, "RB", "True", 6) == 17.0
    assert calculatePoints(28457, "WR", "False", 5) == 1


def test_wrtPoints():
    assert wrtPoints(31960, 6) == 17.0
    assert wrtPoints(28457, 5) == 0.0
    assert wrtPoints(28457, 4) == 9.4


