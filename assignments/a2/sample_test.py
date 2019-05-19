import pytest
from typing import Optional, Tuple
import pygame
from tm_trees import TMTree, FileSystemTree
from papers_1 import PaperTree

leaf1 = TMTree('a', [], 12)
leaf2 = TMTree('b', [], 18)
leaf3 = TMTree('c', [], 25)
leaf4 = TMTree('d', [], 25)
Tree1 = TMTree('A', [leaf1, leaf2])
Tree2 = TMTree('B', [leaf3, leaf4])
Root = TMTree('R', [Tree1, Tree2])

def test():
    Root.update_rectangles((0, 0, 80, 50))
    assert Root.data_size == 80
    Root.expand()
    assert Root.get_tree_at_position((30, 25))._name == 'A'
    Root.expand_all()
    assert Root.get_tree_at_position((30, 25))._name == 'b'
    sub = []
    for i in range(49):
        temp = TMTree('a', [], 20)
        sub.append(temp)
    for i in range(5):
        sub[-1]._subtrees.append(TMTree('c', [], 4))
    subsub = []
    for i in range(4):
        temp = TMTree('b', [], 5)
        subsub.append(temp)
    sub.append(TMTree('a', subsub))
    Root1 = TMTree('R', sub)
    Root1.update_rectangles((0, 0, 110, 50))
    Root1.expand_all()
    assert len(Root1.get_rectangles()) == 57
    assert Root1.get_rectangles()[-1][0] == (98, 36, 12, 14)
    assert Root1.get_tree_at_position((110, 36)).rect == (98, 24, 12, 12)
    assert Root1.get_tree_at_position((98, 45)).rect == (96, 40, 2, 10)


if __name__ == '__main__':
    pytest.main(['sample_test.py'])
