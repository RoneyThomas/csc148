from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple, Optional, Dict, Union


def first_at_depth(obj: Union[int, List], d: int) -> Optional[int]:
    """
    >>> first_at_depth([10, [[20]], [30,40]], 0)
    -1
    >>> first_at_depth([10, [[20]], [30,40]], 1)
    10
    >>> first_at_depth([10, [[20]], [30,40]], 6)
    -1
    """
    if isinstance(obj, int):
        if d == 0:
            return obj
        return -1
    else:
        if d == 0:
            return -1
        for o in obj:
            if first_at_depth(o, d - 1) != -1:
                return first_at_depth(o, d - 1)
        return -1


def add_one(obj: Union[int, List]) -> None:
    """
    >>> lst = 1
    >>> add_one(lst)
    >>> lst
    1
    >>> lst = []
    >>> add_one(lst)
    >>> lst
    []
    >>> lst = [1,[2,3],[[[5]]]]
    >>> add_one(lst)
    >>> lst
    [2, [3, 4], [[[6]]]]
    """
    if isinstance(obj, int):
        return None
    else:
        for i in range(len(obj)):
            if isinstance(obj[i], int):
                obj[i] += 1
            else:
                add_one(obj[i])


if __name__ == '__main__':
    import doctest

    doctest.testmod()
