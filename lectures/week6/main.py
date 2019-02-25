from typing import Union, List, Optional


def unique(obj: Union[int, List]) -> List[int]:
    """
    >>> unique([1, [2, 2], 2, 4, 4, [2, 2], 2, 4, 4])
    [1, 2, 4]
    >>> unique([1, [2, 3], 4])
    [1, 2, 3, 4]
    >>> unique([[1,2],[1,2,3,4]])
    [1, 2, 3, 4]
    >>> unique([[1,[1,2,4,5]],[1,2,3,4]])
    [1, 2, 4, 5, 3]
    """
    if isinstance(obj, int):
        return [obj]
    else:
        s = []
        for sublist in obj:
            temp = unique(sublist)
            for item in temp:
                if item not in s:
                    s.extend([item])
        return s


def first_at_depth(obj: Union[int, List], d: int) -> Optional[int]:
    """
    >>> first_at_depth([[1,2], 3],1)
    3
    >>> first_at_depth([[1,2], 3],2)
    1
    >>> first_at_depth([[1,2], 3],0)

    >>> first_at_depth([[[1,2,3],4],5],2)
    4
    >>> first_at_depth([4,[3,[2,[1]]]],3)
    2
    >>> first_at_depth([[[2,2,2],2],2],10)

    """
    if isinstance(obj, int):
        if d == 0:
            return obj
        else:
            return
    else:
        if d == 0:
            return None
        else:
            for sublist in obj:
                result = first_at_depth(sublist, d-1)
                if isinstance(result, int):
                    return result


if __name__ == '__main__':
    import doctest

    doctest.testmod()
