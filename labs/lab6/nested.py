"""Lab 6: Recursion

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a few nested list functions for you to practice recursion.
"""
from typing import Union, List


def add_n(obj: Union[int, List], n: int) -> Union[int, List]:
    """Return a new nested list where <n> is added to every item in <obj>.

    >>> add_n(10, 3)
    13
    >>> add_n([1, 2, [1, 2], 4], 10)
    [11, 12, [11, 12], 14]
    """
    if isinstance(obj, int):
        obj += n
        return obj
    else:
        t = []
        for sublist in obj:
            t.append(add_n(sublist, n))
        return t


def nested_list_equal(obj1: Union[int, List], obj2: Union[int, List]) -> bool:
    """Return whether two nested lists are equal, i.e., have the same value.

    Note: order matters.

    >>> nested_list_equal(17, [1, 2, 3])
    False
    >>> nested_list_equal([1, 2, [1, 2], 4], [1, 2, [1, 2], 4])
    True
    >>> nested_list_equal([1, 2, [1, 2], 4], [4, 2, [1, 2], 4])
    False
    """
    if isinstance(obj1, int) or isinstance(obj2, int):
        if obj1 == obj2:
            return True
        return False
    else:
        if len(obj1) != len(obj2):
            return False
        for index in range(len(obj1)):
            if not nested_list_equal(obj1[index], obj2[index]):
                return False
    return True


def duplicate(obj: Union[int, List]) -> Union[int, List]:
    """Return a new nested list with all numbers in <obj> duplicated.

    Each integer in <obj> should appear twice *consecutively* in the
    output nested list. The nesting structure is the same as the input,
    only with some new numbers added. See doctest examples for details.

    If <obj> is an int, return a list containing two copies of it.

    >>> duplicate(1)
    [1, 1]
    >>> duplicate([])
    []
    >>> duplicate([1, 2])
    [1, 1, 2, 2]
    >>> duplicate([1, [2, 3]])  # NOT [1, 1, [2, 2, 3, 3], [2, 2, 3, 3]]
    [1, 1, [2, 2, 3, 3]]
    """
    if isinstance(obj, int):
        return [obj, obj]
    else:
        l = []
        for sublist in obj:
            if isinstance(sublist, list):
                l.append(duplicate(sublist))
            else:
                l.extend(duplicate(sublist))
        return l


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # import python_ta
    # python_ta.check_all()
