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
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple, Union
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """
    # TODO: Implement Me
    players = []
    goals = generate_goals(num_human + num_random + len(smart_players))

    for i in range(num_human):
        players.append(HumanPlayer(i, goals[i]))

    for i in range(num_random):
        players.append(RandomPlayer(num_human + i, goals[num_human + i]))

    base = num_human + num_random
    for i, x in enumerate(smart_players):
        players.append(SmartPlayer(base + i, goals[base + i], x))
    return players


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """
    # TODO: Implement me
    # Returning the block at the right level
    # No need to check if the location is in the block as we
    # Are selecting the right block in the elif statement
    if block.level == level:
        return block
    for child in block.children:
        if child.position[0] <= location[0] < (
                child.position[0] + child.size) and child.position[1] <= \
                location[1] < (child.position[1] + child.size):
            return _get_block(child, location, level)
    return None


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    return action[0], action[1], block


class HumanPlayer(Player):
    """A human player.
    """
    # === Private Attributes ===
    # _level:
    #     The level of the Block that the user selected most recently.
    # _desired_action:
    #     The most recent action that the user is attempting to do.
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0
    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, self._level)

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)
            self._desired_action = None
            return move


def _random_move(choices: List, board: Block) -> \
        Tuple[Tuple[str, Optional[int]], Tuple[int, int], int]:
    """Returns a randomly selected move which can be applied
    to a Block with children
    """
    chances = 3
    move: Union[
        Tuple[Tuple[str, Optional[int]], Tuple[int, int], int], None] = None
    while move is None and chances >= 0:
        choice = random.choice(choices)
        if choice == 1 and board.combine():
            move = (COMBINE, board.position,
                    board.level)
        elif choice == 2 and board.rotate(random.choice([1, 3])):
            choice = random.choice([ROTATE_CLOCKWISE,
                                    ROTATE_COUNTER_CLOCKWISE])
            move = (choice, board.position, board.level)
        elif choice == 3 and board.swap(random.choice([0, 1])):
            choice = random.choice([SWAP_HORIZONTAL, SWAP_VERTICAL])
            move = (choice, board.position, board.level)
        chances -= 1
        if move is not None:
            return move
    if move is None:
        return _random_move(choices, board)


def _generate_action(board: Block, n: int, colour: Tuple[int, int, int],
                     goal: Optional[Goal] = None) -> \
        (List[Tuple[Tuple[str, Optional[int]], Tuple[int, int], int]],
         Optional[List[int]]):
    """Returns a randomly selected move which can be applied to a Block
    """
    action = []
    chances = 3 * n
    scores: List[Block] = []
    while len(action) < n and chances >= 0:
        sample_board = board.create_copy()
        test_board = sample_board
        move: Tuple[Tuple[str, Optional[int]], Tuple[int, int], int] = tuple()
        # First we are randomly selecting a level we want
        level = random.randint(board.level, board.max_depth)
        # This while loop sets the current block to randomly selected level
        while test_board.level < level:
            # We only increase level if we have children
            if test_board.children:
                test_board = test_board.children[random.randint(0, 3)]
            else:
                break
        # If our current block has children
        # then valid moves are combine, swap and rotate.
        # The moves are selected randomly
        if test_board.children:
            if level == board.max_depth - 1:
                move = _random_move([1, 2, 3], test_board)
            else:
                move = _random_move([2, 3], test_board)
        # If there is no children then the valid moves are smash and pain
        # paint can only be applied if our current level==max_level
        # smash can be only applied if our current level < max_level
        elif test_board.smash():
            move = (SMASH, test_board.position, test_board.level)
        elif test_board.level == board.max_depth and test_board.paint(
                colour):
            move = (PAINT, test_board.position, test_board.level)
        if move:
            action.append(move)
            chances -= 1
            if goal is not None:
                scores.append(goal.score(sample_board))
    return action, scores


class RandomPlayer(Player):
    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    """A child class of Player to make a random but valid move on the board.
         You must note mutate the given board  parameter """
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        # TODO: Implement Me
        Player.__init__(self, player_id, goal)

        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove

        # TODO: Implement Me
        action, _ = _generate_action(board, 1, self.goal.colour)
        # Up till this point we were
        # applying our moves to a copy of board object
        # Now it's time for us to find the correct block in our board object
        # We use _get_block for that and assemble our move with _create_move()
        move = _create_move(action[0][0],
                            _get_block(board, action[0][1], action[0][2]))
        self._proceed = False  # Must set to False before returning!
        return move


class SmartPlayer(Player):
    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    """A child class of player to make a valid move on the board after choosing
        the highest score random move generating <_difficulty> times.
        You must note mutate the given board  parameter """
    _proceed: bool
    _difficulty: int

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        # TODO: Implement Me
        Player.__init__(self, player_id, goal)
        self._difficulty = difficulty
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove
        actions, score = _generate_action(board, self._difficulty,
                                          self.goal.colour, self.goal)
        current_board_score = self.goal.score(board)
        self._proceed = False  # Must set to False before returning!
        if max(score) < current_board_score:
            return _create_move(PASS, board)
        action = actions[score.index(max(score))]
        return _create_move(action[0], _get_block(board, action[1], action[2]))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
