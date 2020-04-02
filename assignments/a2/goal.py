"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    # TODO: Implement Me
    goals = []
    colours = random.sample(COLOUR_LIST, num_goals)
    for g in range(num_goals):
        rand_goal = random.choice([PerimeterGoal, BlobGoal])
        goals.append(rand_goal(colours[g]))
    return goals


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    # TODO: Implement me
    if not block.children:
        s = 2 ** (block.max_depth - block.level)
        return [[block.colour for _ in range(s)] for _ in range(s)]
    else:
        flat_1 = []
        flat_2 = []
        b_0 = _flatten(block.children[1])
        b_1 = _flatten(block.children[2])
        b_2 = _flatten(block.children[0])
        b_3 = _flatten(block.children[3])
        for a, b, c, d in zip(b_0, b_1, b_2, b_3):
            a.extend(b)
            flat_1.append(a)
            c.extend(d)
            flat_2.append(c)
        return flat_1 + flat_2


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A player goal in the game of Blocky.

    This is a subclass of abstract Goal class

    PerimeterGoal implements score and description method's

    PerimeterGoal computes score based on the block at perimeter of the Block
    """

    def score(self, board: Block) -> int:
        # TODO: Implement me
        flatten_board = _flatten(board)
        score = 0
        for i in range(len(flatten_board)):
            if flatten_board[i][0] == self.colour:
                score += 1
            if flatten_board[i][len(flatten_board) - 1] == self.colour:
                score += 1
            if flatten_board[0][i] == self.colour:
                score += 1
            if flatten_board[len(flatten_board) - 1][i] == self.colour:
                score += 1
        return score

    def description(self) -> str:
        # TODO: Implement me
        return f'Maximize the presence of ' \
               f'{colour_name(self.colour)} on the perimeter'


class BlobGoal(Goal):
    """A player goal in the game of Blocky.

    This is a subclass of abstract Goal class

    BlobGoal implements score and description method's

    BlobGoal computes score based on the largest blob with the Goal colour
    """

    def score(self, board: Block) -> int:
        # TODO: Implement me
        flatten_board = _flatten(board)
        visited: List[List[int]] = [[-1 for _ in range(len(flatten_board))] for
                                    _ in
                                    range(len(flatten_board))]
        score = []
        for i in range(len(flatten_board)):
            for j in range(len(flatten_board)):
                if visited[i][j] == -1 and flatten_board[i][j] == self.colour:
                    score.append(
                        self._undiscovered_blob_size((i, j), flatten_board,
                                                     visited))
                elif visited[i][j] == -1 and flatten_board[i][j] != self.colour:
                    visited[i][j] = 0
        return max(score)

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        # TODO: Implement me
        s = 1
        y, x = pos
        if y >= len(board) or x >= len(board):
            return 0
        visited[y][x] = 1
        if y > 0 and visited[y - 1][x] == -1:
            if board[y - 1][x] == self.colour:
                s += self._undiscovered_blob_size((y - 1, x), board, visited)
            else:
                visited[y - 1][x] = 0
        if y < len(board) - 1 and visited[y + 1][x] == -1:
            if board[y + 1][x] == self.colour:
                s += self._undiscovered_blob_size((y + 1, x), board, visited)
            else:
                visited[y + 1][x] = 0
        if x > 0 and visited[y][x - 1] == -1:
            if board[y][x - 1] == self.colour:
                s += self._undiscovered_blob_size((y, x - 1), board, visited)
            else:
                visited[y][x - 1] = 0
        if x < len(board) - 1 and visited[y][x + 1] == -1:
            if board[y][x + 1] == self.colour:
                s += self._undiscovered_blob_size((y, x + 1), board, visited)
            else:
                visited[y][x + 1] = 0
        return s

    def description(self) -> str:
        # TODO: Implement me
        return f'Maximize {colour_name(self.colour)} to form largest blob'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
