"""CSC148 Lab 3: Inheritance

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the implementation of a simple number game.
The key class design feature here is *inheritance*, which is used to enable
different types of players, both human and computer, for the game.
"""
from __future__ import annotations
import random
from typing import Tuple


class NumberGame:
    """A number game for two players.

    A count starts at 0. On a player's turn, they add to the count an amount
    between a set minimum and a set maximum. The player who brings the count
    to a set goal amount is the winner.

    The game can have multiple rounds.

    === Attributes ===
    goal:
        The amount to reach in order to win the game.
    min_step:
        The minimum legal move.
    max_step:
        The maximum legal move.
    current:
        The current value of the game count.
    players:
        The two players.
    turn:
        The turn the game is on, beginning with turn 0.
        If turn is even number, it is players[0]'s turn.
        If turn is any odd number, it is player[1]'s turn.

    === Representation invariants ==
    - self.turn >= 0
    - 0 <= self.current <= self.goal
    - 0 < self.min_step <= self.max_step <= self.goal
    """
    goal: int
    min_step: int
    max_step: int
    current: int
    players: Tuple[Player, Player]
    turn: int

    def __init__(self, goal: int, min_step: int, max_step: int,
                 players: Tuple[Player, Player]) -> None:
        """Initialize this NumberGame.

        Precondition: 0 < min_step <= max_step <= goal
        """
        self.goal = goal
        self.min_step = min_step
        self.max_step = max_step
        self.current = 0
        self.players = players
        self.turn = 0

    def play(self) -> str:
        """Play one round of this NumberGame. Return the name of the winner.

        A "round" is one full run of the game, from when the count starts
        at 0 until the goal is reached.
        """
        while self.current < self.goal:
            self.play_one_turn()
        # The player whose turn would be next (if the game weren't over) is
        # the loser. The one who went one turn before that is the winner.
        winner = self.whose_turn(self.turn - 1)
        winner.game_won(True)
        looser = self.whose_turn(self.turn)
        looser.game_won(False)
        return winner.name

    def whose_turn(self, turn: int) -> Player:
        """Return the Player whose turn it is on the given turn number.
        """
        if turn % 2 == 0:
            return self.players[0]
        else:
            return self.players[1]

    def play_one_turn(self) -> None:
        """Play a single turn in this NumberGame.

        Determine whose move it is, get their move, and update the current
        total as well as the number of the turn we are on.
        Print the move and the new total.
        """
        next_player = self.whose_turn(self.turn)
        amount = next_player.move(
            self.current,
            self.min_step,
            self.max_step,
            self.goal
        )
        self.current += amount
        self.turn += 1

        print(f'{next_player.name} moves {amount}.')
        print(f'Total is now {self.current}.')


# TODO: Write classes Player, RandomPlayer, UserPlayer, and StrategicPlayer.
class Player:
    name: str
    games_played: int
    games_won: int

    def __init__(self, name: str):
        self.name = name
        self.games_played = 0
        self.games_won = 0

    def __str__(self):
        return f'{self.name} played {self.games_played} ' \
               f'and won {self.games_won}'

    def move(self, current: int, min_step: int, max_step: int,
             goal: int) -> int:
        raise NotImplementedError

    def game_won(self, win: bool):
        self.games_played += 1
        if win:
            self.games_won += 1


class RandomPlayer(Player):
    def move(self, current: int, min_step: int, max_step: int,
             goal: int) -> int:
        while current + max_step > goal:
            max_step -= 1
        return random.randint(min_step, max_step)


class UserPlayer(Player):

    def move(self, current: int, min_step: int, max_step: int,
             goal: int) -> int:
        while current + max_step > goal:
            max_step -= 1
        choice = 0
        while choice == 0 or current + choice > goal:
            print(
                f'Enter your move choice between '
                f'{min_step} and {max_step} inclusive')
            choice = int(input())
        return choice


class StrategicPlayer(Player):

    def move(self, current: int, min_step: int, max_step: int,
             goal: int) -> int:
        while current + max_step > goal:
            max_step -= 1
        unsafe_positions = list(range(goal, current, -max_step))
        safe_moves = []
        for i in range(min_step, max_step + 1):
            if i + current <= goal - max_step:
                if (i + current) not in unsafe_positions:
                    safe_moves.append(i)
        if not safe_moves:
            print(f'No safe movies {safe_moves}')
            return goal - current
        else:
            return random.choice(safe_moves)


def make_player(generic_name: str) -> Player:
    """Return a new Player based on user input.

    Allow the user to choose a player name and player type.
    <generic_name> is a placeholder used to identify which player is being made.
    """
    name = input(f'Enter a name for {generic_name}: ')
    # TODO: Create and return some sort of Player.
    choice = 0
    while choice < 1 or choice > 3:
        print("Choose Player Type, input n.o")
        print("1 Random Player")
        print("2 User Player")
        print("3 Strategic Player")
        choice = int(input())
    player: Player
    if choice == 1:
        player = RandomPlayer(name)
    elif choice == 2:
        player = UserPlayer(name)
    else:
        player = StrategicPlayer(name)
    return player


def main() -> None:
    """Play multiple rounds of a NumberGame based on user input settings.
    """
    goal = int(input('Enter goal amount: '))
    minimum = int(input('Enter minimum move: '))
    maximum = int(input('Enter maximum move: '))
    p1 = make_player('p1')
    p2 = make_player('p2')
    while True:
        g = NumberGame(goal, minimum, maximum, (p1, p2))
        winner = g.play()
        print(f'And {winner} is the winner!!!')
        print(p1)
        print(p2)
        again = input('Again? (y/n) ')
        if again != 'y':
            return


if __name__ == '__main__':
    # Uncomment the lines below to check your work using
    # python_ta and doctest.
    import python_ta

    # python_ta.check_all(config={
    #     'extra-imports': ['random'],
    #     'allowed-io': [
    #         'main',
    #         'make_player',
    #         'move',
    #         'play_one_turn'
    #     ]
    # })
    # import doctest
    # doctest.testmod()

    # Uncomment the following line to run the number game.
    main()
