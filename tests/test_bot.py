from quantum_tictactoe.bot import Bot, BotTypeError
from quantum_tictactoe.board import Board
from quantum_tictactoe.tile import Tile
from quantum_tictactoe.game import Game
import pytest


def test_bot_create_easy():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    bot = Bot('easy', board, game)
    assert bot.mode() == 'easy'


def test_bot_create_hard():
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    bot = Bot('hard', board, game)
    assert bot.mode() == 'hard'


def test_bot_move(monkeypatch):
    def one(a):
        return 1
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    bot = Bot('easy', board, game)
    monkeypatch.setattr('quantum_tictactoe.bot.choice', one)
    assert bot.move() == (1, 1)


def test_bot_choose_move(monkeypatch):
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    bot = Bot('easy', board, game)

    def one(a):
        return 1
    monkeypatch.setattr('quantum_tictactoe.bot.choice', one)
    assert bot.choose_move([0, 1, 2, 3, 4, 5]) == 1


def test_bot_collapse(monkeypatch):
    tiles = []
    for _ in range(9):
        tiles.append(Tile())
    board = Board(tiles)
    game = Game(board)
    board.tiles()[1].set_move_on_tile('x1')
    board.tiles()[2].set_move_on_tile('x1')
    board.tiles()[1].set_move_on_tile('x3')
    board.tiles()[2].set_move_on_tile('x3')
    board.add_entangl_tile(1)
    board.add_entangl_tile(2)
    bot = Bot('easy', board, game)

    def one(a):
        return 1
    monkeypatch.setattr('quantum_tictactoe.bot.choice', one)
    assert bot.collapse() == '1,x3'
