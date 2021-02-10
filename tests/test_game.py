from quantum_tictactoe.game import Game, InvalidMoveError
from quantum_tictactoe.board import Board
from quantum_tictactoe.tile import Tile
from quantum_tictactoe.bot import Bot
import pytest


def test_game_create():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    assert game.board == board
    assert game.entanglement is False
    assert game.basic is True
    assert game.is_first_move() is True
    assert game.last_tile() == ''
    assert game.last_move() == ''
    assert game.is_finished() is False
    assert game.game_result() == ''
    assert game.counter() == 1


def test_game_making_changes():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    game.set_first_move(False)
    assert game.is_first_move() is False
    game.set_last_tile(2)
    assert game.last_tile() == 2
    game.set_last_move('x1')
    assert game.last_move() == 'x1'
    game.set_finished()
    assert game.is_finished() is True
    game.increase_counter()
    assert game.counter() == 2


def test_game_clear():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    game.set_first_move(False)
    game.set_last_tile(2)
    game.set_last_move('x1')
    game.set_finished()
    game.increase_counter()
    game.clear_game()
    assert game.is_first_move() is True
    assert game.last_tile() == ''
    assert game.last_move() == ''
    assert game.is_finished() is False
    assert game.game_result() == ''
    assert game.counter() == 1


def test_move_is_correct():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    game.set_first_move(False)
    game.set_last_tile(2)
    tile = game.board.tiles()[1]
    assert game.move_is_correct(tile, 1) is True


def test_move_is_not_correct_same_tile():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    game.set_first_move(False)
    game.set_last_tile(1)
    tile = game.board.tiles()[1]
    assert game.move_is_correct(tile, 1) is False


def test_move_is_not_correct_collapsed_tile():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    tile = game.board.tiles()[1]
    tile.set_collapsed('x1')
    assert game.move_is_correct(tile, 1) is False


def test_whos_move_x():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    game.set_last_move('y1')
    game.increase_counter()
    assert game.whos_move() == 'x2'


def test_whos_move_y():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    game.set_last_move('x1')
    game.increase_counter()
    assert game.whos_move() == 'y2'


def test_move_correct():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    assert game.move(1) == 1
    assert game.last_tile() == 1


def test_move_wrong_number():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    with pytest.raises(InvalidMoveError):
        game.move(9)


def test_is_entanglement():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    board.tiles()[1].set_move_on_tile('x1')
    board.tiles()[2].set_move_on_tile('x1')
    board.tiles()[1].set_move_on_tile('x3')
    board.tiles()[2].set_move_on_tile('x3')
    game.set_last_move('x3')
    game.set_last_tile(2)
    assert game.is_entanglement() is True


def test_is_not_entanglement():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    board.tiles()[1].set_move_on_tile('x1')
    board.tiles()[2].set_move_on_tile('x1')
    board.tiles()[1].set_move_on_tile('x3')
    board.tiles()[3].set_move_on_tile('x3')
    game.set_last_move('x3')
    game.set_last_tile(1)
    assert game.is_entanglement() is False


def test_game_entanglement():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    assert game.entanglement is False
    assert game.basic is True
    board.tiles()[1].set_move_on_tile('x1')
    board.tiles()[2].set_move_on_tile('x1')
    board.tiles()[1].set_move_on_tile('x3')
    board.tiles()[2].set_move_on_tile('x3')
    game.set_last_move('x3')
    game.set_last_tile(2)
    game.game_entanglement()
    assert game.entanglement is True
    assert game.basic is False


def test_game_collapse_player():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    bot = Bot('easy', board, game)
    assert board.tiles()[1].is_collapsed() is False
    assert board.tiles()[2].is_collapsed() is False
    board.tiles()[1].set_move_on_tile('x1')
    board.tiles()[2].set_move_on_tile('x1')
    board.tiles()[1].set_move_on_tile('y2')
    board.tiles()[2].set_move_on_tile('y2')
    game.set_last_move('y2')
    game.set_last_tile(2)
    collapse = '1,x1'
    game.game_entanglement()
    game.game_collapse(bot, 'easy', collapse)
    assert board.tiles()[1].is_collapsed() is True
    assert board.tiles()[2].is_collapsed() is True


def test_game_collapse_bot():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    bot = Bot('easy', board, game)
    assert board.tiles()[1].is_collapsed() is False
    assert board.tiles()[2].is_collapsed() is False
    board.tiles()[1].set_move_on_tile('x1')
    board.tiles()[2].set_move_on_tile('x1')
    board.tiles()[1].set_move_on_tile('x3')
    board.tiles()[2].set_move_on_tile('x3')
    game.set_last_move('x3')
    game.set_last_tile(2)
    game.game_entanglement()
    game.game_collapse(bot, 'easy')
    assert board.tiles()[1].is_collapsed() is True
    assert board.tiles()[2].is_collapsed() is True


def test_is_game_end():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    board.tiles()[0].set_collapsed('x1')
    board.tiles()[1].set_collapsed('x3')
    board.tiles()[2].set_collapsed('x5')
    game = Game(board)
    assert game.is_game_end() is True


def test_is_game_end_more_options():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    board.tiles()[0].set_collapsed('x7')
    board.tiles()[1].set_collapsed('x3')
    board.tiles()[2].set_collapsed('x5')
    board.tiles()[3].set_collapsed('y2')
    board.tiles()[4].set_collapsed('y4')
    board.tiles()[5].set_collapsed('y6')
    game = Game(board)
    assert game.is_game_end() is True


def test_is_not_game_end():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    assert game.is_game_end() is False
