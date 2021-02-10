from quantum_tictactoe.board import Board, InvalidCollapseError
from quantum_tictactoe.tile import Tile
import pytest


def test_board_create():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    assert board.tiles() == tiles
    assert board.entangl_tiles() == []


def test_add_entangle_tile():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    assert board.entangl_tiles() == []
    board.add_entangl_tile(1)
    assert board.entangl_tiles() == [1]


def test_reset_entangle_tiles():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    board.add_entangl_tile(1)
    board.add_entangl_tile(2)
    assert board.entangl_tiles() == [1, 2]
    board.reset_entangl_tiles()
    assert board.entangl_tiles() == []


def test_could_collapse():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    board.add_entangl_tile(1)
    board.add_entangl_tile(2)
    board.tiles()[1].set_move_on_tile('x1')
    board.tiles()[2].set_move_on_tile('x1')
    assert board.could_collapse(1, 'x1') is True


def test_could_collapse_error():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    with pytest.raises(InvalidCollapseError):
        board.could_collapse(1, 'x1')


def test_collapse():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    board.add_entangl_tile(1)
    board.add_entangl_tile(2)
    board.tiles()[1].set_move_on_tile('x1')
    board.tiles()[2].set_move_on_tile('x1')
    board.tiles()[1].set_move_on_tile('y2')
    board.tiles()[2].set_move_on_tile('y2')
    board.collapse(1, 'x1')
    assert board.tiles()[1].is_collapsed() is True
    assert board.tiles()[2].is_collapsed() is True


def test_collapse_error():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    board.add_entangl_tile(1)
    board.add_entangl_tile(2)
    board.tiles()[1].set_move_on_tile('x1')
    board.tiles()[1].set_move_on_tile('x3')
    board.tiles()[2].set_move_on_tile('x1')
    board.tiles()[1].set_move_on_tile('y2')
    board.tiles()[2].set_move_on_tile('y2')
    with pytest.raises(InvalidCollapseError):
        board.collapse(1, 'x3')


def test_analyse_board():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    board.add_entangl_tile(1)
    board.add_entangl_tile(2)
    board.tiles()[1].set_move_on_tile('x1')
    board.tiles()[2].set_move_on_tile('x1')
    board.tiles()[1].set_move_on_tile('y2')
    board.tiles()[2].set_move_on_tile('y2')
    board.collapse(1, 'x1')
    assert board.analyse_board() == ['-', 'x1', 'y2', '-', '-', '-', '-', '-', '-']


def test_analyse_board_empty():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    assert board.analyse_board() == ['-', '-', '-', '-', '-', '-', '-', '-', '-']


def test_win_option_no_winner():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    coll_moves = ['x1', 'x3', 'y2', '-', '-', '-', '-', '-', '-']
    assert board.win_options(coll_moves) == ([], [])


def test_win_option_some_winners():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    coll_moves = ['x3', 'x1', 'x5', 'y2', '-', 'y4', 'y6', 'x7', 'y8']
    assert board.win_options(coll_moves) == (['x1'], [[0, 1, 2]])


def test_is_winner_no_end():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    board.tiles()[0].set_collapsed('x1')
    assert board.is_winner() == (None, [])


def test_is_winner_one_option():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    board.tiles()[0].set_collapsed('x1')
    board.tiles()[1].set_collapsed('x3')
    board.tiles()[2].set_collapsed('x5')
    assert board.is_winner() == ('x', [0, 1, 2])


def test_is_winner_more_options():
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
    assert board.is_winner() == ('y', [3, 4, 5])
