from block import generate_board, Block
from blocky import _block_to_squares
from settings import COLOUR_LIST, BLACK

import pytest
import random


def test_block():
    block = generate_board(4, 750)
    assert len(block.children) == 4
    assert block.max_depth == 4
    assert block.level == 0
    assert block.colour is None
    assert block.size == 750
    block = block.children[0]
    assert block.level == 1
    assert block.size == 375
    for c in block.children:
        if len(c.children) == 0:
            assert c.smashable() is True
        else:
            assert c.smashable() is False

    block = generate_board(0, 750)
    assert block.colour is not None
    assert len(block.children) == 0
    assert block.level == 0
    assert block.max_depth == 0
    assert block.size == 750
    assert block.smash() is False
    assert block.swap(0) is False
    assert block.swap(1) is False
    assert block.rotate(1) is False
    assert block.rotate(3) is False

    block = generate_board(1, 750)
    assert block.colour is None
    assert len(block.children) == 4
    assert block.children[0].size == 375
    assert block.children[1].colour is not None
    assert block.children[2].colour is not None
    assert block.children[3].colour is not None
    assert block.children[1].position == (0, 0)
    assert block.children[0].position == (375, 0)
    assert block.children[2].position == (0, 375)
    assert block.children[3].position == (375, 375)
    assert block.children[0].smashable() is False
    assert block.children[1].smash() is False
    assert block.children[2].smashable() is False
    assert block.children[3].smash() is False

    block = generate_board(4, 750)
    block_copy = block.create_copy()
    assert block == block_copy
    block.swap(1)
    for i, j in zip(block.children, block_copy.children):
        assert i.position == j.position
    block.swap(0)
    for i, j in zip(block.children, block_copy.children):
        assert i.position == j.position

    main_block = Block((0, 0), 200, colour=None, level=0, max_depth=2)
    child_block_1 = Block((100, 0), 100, colour=COLOUR_LIST[0], level=1,
                          max_depth=2)
    child_block_2 = Block((0, 0), 100, colour=COLOUR_LIST[1], level=1,
                          max_depth=2)
    child_block_3 = Block((0, 100), 100, colour=COLOUR_LIST[2], level=1,
                          max_depth=2)
    child_block_4 = Block((100, 100), 100, colour=COLOUR_LIST[3], level=1,
                          max_depth=2)
    main_block.children = [child_block_1, child_block_2, child_block_3,
                           child_block_4]

    assert main_block.swap(1)
    assert main_block.children[0].colour == COLOUR_LIST[3]
    assert main_block.children[1].colour == COLOUR_LIST[2]
    assert main_block.children[3].colour == COLOUR_LIST[0]
    assert main_block.children[2].colour == COLOUR_LIST[1]

    assert main_block.swap(1)
    assert main_block.swap(0)
    assert main_block.children[0].colour == COLOUR_LIST[1]
    assert main_block.children[3].colour == COLOUR_LIST[2]
    assert main_block.children[1].colour == COLOUR_LIST[0]
    assert main_block.children[2].colour == COLOUR_LIST[3]

    assert main_block.swap(0)
    assert main_block.rotate(1)
    assert main_block.children[0].colour == COLOUR_LIST[1]
    assert main_block.children[1].colour == COLOUR_LIST[2]
    assert main_block.children[2].colour == COLOUR_LIST[3]
    assert main_block.children[3].colour == COLOUR_LIST[0]

    assert main_block.rotate(3)
    assert main_block.children[0].colour == COLOUR_LIST[0]
    assert main_block.children[1].colour == COLOUR_LIST[1]
    assert main_block.children[2].colour == COLOUR_LIST[2]
    assert main_block.children[3].colour == COLOUR_LIST[3]

    block = generate_board(1, 750)
    assert block.children[0].paint(BLACK)
    assert block.paint(BLACK) is False
    block.children[0].paint(COLOUR_LIST[0])
    block.children[1].paint(COLOUR_LIST[0])
    block.children[2].paint(COLOUR_LIST[0])
    assert block.combine()
    assert len(block.children) == 0


def test_blocky():
    block = generate_board(0, 750)
    blocky = _block_to_squares(block)
    assert isinstance(blocky, list)
    assert blocky[0][0] in COLOUR_LIST
    assert blocky[0][1] == (0, 0)
    assert blocky[0][2] == 750
    print(block)

    main_block = Block((0, 0), 200, colour=None, level=0, max_depth=2)
    child_block_1 = Block((100, 0), 100, colour=COLOUR_LIST[0], level=1,
                          max_depth=2)
    child_block_2 = Block((0, 0), 100, colour=COLOUR_LIST[1], level=1,
                          max_depth=2)
    child_block_3 = Block((0, 100), 100, colour=COLOUR_LIST[2], level=1,
                          max_depth=2)
    child_block_4 = Block((100, 100), 100, colour=COLOUR_LIST[3], level=1,
                          max_depth=2)
    main_block.children = [child_block_1, child_block_2, child_block_3,
                           child_block_4]
    blocky = _block_to_squares(main_block)
    assert len(blocky) == 4
    assert blocky[0][0] in COLOUR_LIST
    assert blocky[0][1] == (100, 0)
    assert blocky[0][2] == 100
    assert blocky[1][0] in COLOUR_LIST
    assert blocky[1][1] == (0, 0)
    assert blocky[1][2] == 100
    assert blocky[2][0] in COLOUR_LIST
    assert blocky[2][1] == (0, 100)
    assert blocky[2][2] == 100
    assert blocky[3][0] in COLOUR_LIST
    assert blocky[3][1] == (100, 100)
    assert blocky[3][2] == 100


if __name__ == '__main__':
    pytest.main(['roney-tests.py'])
