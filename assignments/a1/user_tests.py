import datetime
import pytest

from application import create_customers, process_event_history, import_data
from customer import Customer
from contract import TermContract, MTMContract, PrepaidContract
from phoneline import PhoneLine
from filter import DurationFilter, CustomerFilter, ResetFilter, LocationFilter

from test_filter import LocationFilter1

def test_reading() -> None:
    input_dictionary = import_data()
    customers = create_customers(input_dictionary)
    assert len(customers) == 50

    process_event_history(input_dictionary, customers)
    all_calls = []
    for c in customers:
        hist = c.get_history()
        all_calls.extend(hist[0])
    assert len(all_calls) == 1000


def test_filter() -> None:
    input_dictionary = import_data()
    customers = create_customers(input_dictionary)
    process_event_history(input_dictionary, customers)
    all_calls = []
    for c in customers:
        hist = c.get_history()
        all_calls.extend(hist[0])

    d_f = DurationFilter()
    assert len(d_f.apply(customers, all_calls, "G300")) == 169
    assert len(d_f.apply(customers, all_calls, "G359")) == 3
    assert len(d_f.apply(customers, all_calls, "G360")) == 0
    assert len(d_f.apply(customers, all_calls, "G350")) == 25
    assert len(d_f.apply(customers, all_calls, "L300")) == 827
    assert len(d_f.apply(customers, all_calls, "L350")) == 970
    assert len(d_f.apply(customers, all_calls, "L1")) == 0
    assert len(d_f.apply(customers, all_calls, "L5")) == 3
    assert len(d_f.apply(customers, all_calls, "L4")) == 1
    assert len(d_f.apply(customers, all_calls, "3434")) == 1000

    c_f = CustomerFilter()
    assert len(d_f.apply(customers, all_calls, "8965")) == 1000
    assert len(c_f.apply(customers, all_calls, "8695")) == 52
    assert len(c_f.apply(customers, all_calls, "6096")) == 32

    l_f = LocationFilter()
    l_f_1 = LocationFilter1()
    assert len(l_f.apply(customers, all_calls, "-79.49878, 43.60212, -79.48999, 43.73017")) == \
        len(l_f_1.apply(customers, all_calls, "-79.49878, 43.60212, -79.48999, 43.73017"))
    assert len(l_f.apply(customers, all_calls,
                         "-79.5, 43.60212, -79.2, 43.73017")) == \
           len(l_f_1.apply(customers, all_calls,
                           "-79.5, 43.60212, -79.2, 43.73017"))
    assert len(l_f.apply(customers, all_calls,
                         "-79.5, 43.60212, -79.3, 43.73017")) == \
           len(l_f_1.apply(customers, all_calls,
                           "-79.5, 43.60212, -79.3, 43.73017"))


if __name__ == '__main__':
    test_reading()
    test_filter()
    # pytest.main(['user_tests.py'])
