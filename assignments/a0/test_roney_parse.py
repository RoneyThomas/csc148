from datetime import datetime
from gym import *

ac = load_data('athletic-centre.txt', 'Athletic Centre')


# print(ac._schedule.keys())
def test_instructor_hours():
    assert ac.instructor_hours(datetime(2020, 1, 14, 9, 0),
                               datetime(2020, 1, 14, 11, 0)) == {1: 1, 2: 0,
                                                                 3: 1, 4: 0,
                                                                 5: 1}
    assert ac.instructor_hours(datetime(2020, 1, 14, 9, 0),
                               datetime(2020, 1, 14, 12, 0)) == {1: 1, 2: 0,
                                                                 3: 1, 4: 0,
                                                                 5: 2}
    assert ac.instructor_hours(datetime(2020, 1, 14, 9, 0),
                               datetime(2020, 1, 14, 18, 0)) == {1: 2, 2: 1,
                                                                 3: 2, 4: 0,
                                                                 5: 2}


def test_payroll():
    assert (1, 'Diane', 2, 59.0) in ac.payroll(datetime(2020, 1, 14, 9, 0),
                                               datetime(2020, 1, 14, 18, 0),
                                               25.0)
    assert (2, 'David', 1, 26.5) in ac.payroll(datetime(2020, 1, 14, 9, 0),
                                               datetime(2020, 1, 14, 18, 0),
                                               25.0)
    assert (3, 'Jennifer', 2, 56.0) in ac.payroll(datetime(2020, 1, 14, 9, 0),
                                               datetime(2020, 1, 14, 18, 0),
                                               25.0)
    assert (4, 'Michelle', 0, 0.0) in ac.payroll(datetime(2020, 1, 14, 9, 0),
                                                  datetime(2020, 1, 14, 18, 0),
                                                  25.0)
    assert (5, 'Mario Badr', 2, 59.0) in ac.payroll(datetime(2020, 1, 14, 9, 0),
                                                 datetime(2020, 1, 14, 18, 0),
                                                 25.0)



if __name__ == '__main__':
    import pytest

    pytest.main(['test_roney_parse.py'])
