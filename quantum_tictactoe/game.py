from quantum_tictactoe.bot import Bot, BotTypeError
from quantum_tictactoe.tile import Tile
from quantum_tictactoe.board import Board, InvalidCollapseError
import sys


class InvalidMoveError(Exception):
    pass


class Game:
    """
    Game class. Contains board in game and variables to manage the game.
    :param board: board in game
    :type board: Board

    :param entanglement: default to false, contains if game is in entanglement
    :type entanglement: boolean

    :param basic: contains if game is in basic mode, default to true
    :type basic: boolean

    :param _first_move: contains true if it is player's first move
    :type _first_move: boolean

    :param _last_tile: number of last used tile
    :type last_tile: int default ''

    :param _last_move: last move on board
    :type _last_move: str

    :param _finished: contains info if game is finished, default to false
    :type _finished: boolean

    :param _game_result: contains info about game result
    :type _game_result: str

    :param _counter: contains round number, default to 1
    :type _counter: int
    """
    def __init__(self, board):
        self.board = board
        self.entanglement = False
        self.basic = True
        self._first_move = True
        self._last_tile = ''
        self._last_move = ''
        self._finished = False
        self._game_result = ''
        self._counter = 1

    def is_first_move(self):
        """
        Returns if it's player's first move
        """
        return self._first_move

    def set_first_move(self, first):
        """
        Change _first_move value
        """
        if first is True or first is False:
            self._first_move = first

    def last_tile(self):
        """
        Returns number of last used tile
        """
        return self._last_tile

    def set_last_tile(self, last):
        """
        Sets number of last used tile
        """
        self._last_tile = last

    def last_move(self):
        """
        Returns last move
        """
        return self._last_move

    def set_last_move(self, last):
        """
        Sets _last_move value
        """
        self._last_move = last

    def is_finished(self):
        """
        Returns true if game is finished, other false
        """
        return self._finished

    def set_finished(self):
        """
        Sets _finished to True
        """
        self._finished = True

    def game_result(self):
        """
        Returns game result
        """
        return self._game_result

    def counter(self):
        """
        Returns _counter
        """
        return self._counter

    def increase_counter(self):
        """
        Increase _counter by 1
        """
        self._counter += 1

    def clear_game(self):
        """
        Reset default parameters for game instance
        """
        self.entanglement = False
        self.basic = True
        self._first_move = True
        self._last_tile = ''
        self._last_move = ''
        self._finished = False
        self._game_result = ''
        self._counter = 1
        for tile in self.board.tiles():
            tile.clear_tile()

    def move_is_correct(self, tile, new_move):
        """
        Returns false when choosen tile is collapsed
        or when it's second move on the same tile in turn
        """
        if tile.is_collapsed():
            return False
        if int(new_move) == self._last_tile and not self._first_move:
            return False
        return True

    def whos_move(self):
        """
        Returns move to opposite site and add number of round to player move.
        """
        if 'x' in self._last_move:
            return f'y{int(self._counter)}'
        else:
            return f'x{int(self._counter)}'

    def move(self, new_move):
        """
        Set move on choosen tile.
        Returns chosen tile number
        """
        if new_move not in range(0, 9):
            raise InvalidMoveError('Tiles are numbering from 0 to 8')
        tile = self.board.tiles()[new_move]
        if self.move_is_correct(tile, new_move):
            tile.set_move_on_tile(self.whos_move())
        else:
            raise InvalidMoveError('You cannot place your move here')
        self._last_tile = new_move
        return new_move

    def rec_entanglement(self, tile_move, last_move):
        """
        If board is in entanglement changes game state.
        """
        for index, tile in enumerate(self.board.tiles()):
            if last_move in tile.array() and index != tile_move:
                if index == self._last_tile:
                    self.board.add_entangl_tile(index)
                    self.entanglement = True
                    self.basic = False
                    break
                for move in tile.array():
                    if move != last_move:
                        self.board.add_entangl_tile(index)
                        self.rec_entanglement(index, move)

    def is_entanglement(self):
        """
        Checks entanglement and returns True if game is in entanglement.
        """
        for index, tile in enumerate(self.board.tiles()):
            if index != self._last_tile and self._last_move in tile.array():
                for move in tile.array():
                    if move != self._last_move:
                        self.board.add_entangl_tile(index)
                        self.rec_entanglement(index, move)
                        if self.entanglement is True:
                            return True
        self.board.reset_entangl_tiles()
        return False

    def game_entanglement(self):
        """
        Changes game state when game is entanglement
        """
        if self.is_entanglement():
            self.entanglement = True
            self.basic = False
        else:
            self.entanglement = False
            self.basic = True

    def game_collapse(self, bot, bot_mode, collapse=''):
        """
        Needs info with tile and move to collapse, split answer,
        collapse board and sets state of the game
        """
        who_choose = 'X' if 'y' in self._last_move else 'Y'
        if bot_mode != 'none' and who_choose == 'Y':
            collapse = bot.collapse()
        tile_number, what_collapse = collapse.split(',')
        self.board.collapse(int(tile_number), what_collapse)
        self.entanglement = False
        self.basic = True

    def is_game_end(self):
        """
        Check board result and change _finished or not
        and assign string
        with info of winner to self._game_result.
        Returns True if game is finished
        """
        winner = self.board.is_winner()[0]
        if winner == 'x':
            self._game_result = 'Player X wins'
            self.set_finished()
            return True
        elif winner == 'y':
            self._game_result = 'Player Y wins'
            self.set_finished()
            return True
        elif winner == 'unknown':
            self._game_result = 'Draw'
            self.set_finished()
            return True
        else:
            self._finished = False
            return False

    def play(self):
        """
        Main loop of the game in terminal version
        """
        bot_selected = False
        while not bot_selected:
            try:
                bot_mode = input('Choose bot mode (none/easy/hard): ')
                bot = Bot(bot_mode, self.board, self)
                bot_selected = True
            except BotTypeError as err:
                print(err)
        while not self._finished:
            while self.basic:
                try:
                    if bot_mode != 'none' and 'x' in self._last_move:
                        self._last_tile = bot.move()[1]
                        self._last_move = self.whos_move()
                        self._counter += 1
                        self.game_entanglement()
                    else:
                        if self._first_move:
                            print(self.board.show_board())
                            new_move = int(input(f'Your move {self.whos_move()[0]}: '))
                            self.move(new_move)
                            self._first_move = False
                        else:
                            print(self.board.show_board())
                            new_move = int(input(f'Your move {self.whos_move()[0]}: '))
                            self.move(new_move)
                            self._last_move = self.whos_move()
                            self._counter += 1
                            self._first_move = True
                            self.game_entanglement()
                except InvalidMoveError as err:
                    print(err)
                except ValueError:
                    print("Don't use letters. Use digits from 0 to 8.")
            if self.entanglement:
                try:
                    print(self.board.show_board())
                    who_choose = 'X' if 'y' in self._last_move else 'Y'
                    if bot_mode == 'none' or who_choose == 'X':
                        description = f'Player {who_choose} choose'
                        description += ' what will collapse(tile_number,what_collapse): '
                        collapse = input(description)
                        self.game_collapse(bot, bot_mode, collapse)
                    else:
                        self.game_collapse(bot, bot_mode)
                    self.board.reset_entangl_tiles()
                except InvalidCollapseError as err:
                    print(err)
            self.is_game_end()
        print(self.board.show_board())
        print(self._game_result)


def main():
    tiles = []
    for i in range(0, 9):
        tiles.append(Tile())
    myboard = Board(tiles)
    game = Game(myboard)
    game.play()


if __name__ == '__main__':
    main()
