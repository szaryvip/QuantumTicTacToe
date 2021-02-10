from random import choice


class BotTypeError(Exception):
    pass


class Bot:
    """
    Bot class
    Contains mode and board to play
    :param mode: bot mode
    :type mode: str

    :param board: Board to play
    :type board: Board

    :param game: Game in play
    :type game: Game
    """
    def __init__(self, mode, board, game):
        # if mode == 'hard':
        #     raise BotTypeError('Hard bot is not available yet')
        if mode not in ['none', 'easy', 'hard']:
            err = 'You must choose bot type between none/easy/hard'
            raise BotTypeError(err)
        self._mode = mode
        self._board = board
        self._game = game

    def mode(self):
        """
        Returns bot mode
        """
        return self._mode

    def move(self):
        """
        Returns tuple of choosen tiles to set move on
        """
        available_tiles = []
        for tile_num in range(9):
            is_coll = self._board.tiles()[tile_num].is_collapsed()
            if not is_coll:
                available_tiles.append(tile_num)
        if self._mode == 'easy':
            tile_to_move_1 = self.choose_move(available_tiles)
            available_tiles.remove(tile_to_move_1)
            tile_to_move_2 = self.choose_move(available_tiles)
        elif self._mode == 'hard':
            tile_to_move_1 = self.choose_move(available_tiles)
            available_tiles.remove(tile_to_move_1)
            available_tiles_2 = []
            for index, tile in enumerate(self._board.tiles()):
                if tile.array() == []:
                    available_tiles_2.append(index)
            tiles_with_y = self.tiles_y()
            if len(available_tiles_2) > 0:
                tile_to_move_2 = self.choose_move(available_tiles_2)
            elif len(tiles_with_y) > 0:
                tile_to_move_2 = self.choose_move(tiles_with_y)
            else:
                tile_to_move_2 = self.choose_move(available_tiles)
        return tile_to_move_1, tile_to_move_2

    def tiles_y(self):
        """
        Returns list of tiles numbers with bot moves only
        """
        only_y = []
        for index, tile in enumerate(self._board.tiles()):
            only = True
            for move in tile.array():
                if 'x' in move:
                    only = False
            if only:
                only_y.append(index)
        return only_y

    def choose_move(self, available_tiles):
        """
        Chooses and returns tile to move from avaiable_tiles
        Makes move
        """
        tile_to_move = choice(available_tiles)
        move = self._game.whos_move()
        self._board.tiles()[tile_to_move].set_move_on_tile(move)
        return tile_to_move

    def collapse(self):
        """
        Choices what move on which tile will collapse.
        Returns string: tile_number,move_to_collapse
        """
        available_tiles = self._board.entangl_tiles()
        if self._mode == 'easy' or self._mode == 'hard':
            while True:
                tile_nr = choice(available_tiles)
                num_of_moves = len(self._board.tiles()[tile_nr].array())
                move_to_collapse = choice(range(num_of_moves))
                move_to_collapse = self._board.tiles()[tile_nr].array()[move_to_collapse]
                if self._board.could_collapse(tile_nr, move_to_collapse):
                    return f'{tile_nr},{move_to_collapse}'
        elif self._mode == 'hard':
            pass
