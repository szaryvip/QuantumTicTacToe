class InvalidCollapseError(Exception):
    pass


class Board:
    """
    Board class. Contains all tiles in game and list of tiles in entanglement
    :param tiles: Tiles in game
    :type tiles: list

    :param entangl_tiles: Tiles in entanglement, default is empty list
    :type entangl_tiles: list

    """
    def __init__(self, tiles: list):
        self._tiles = tiles
        self._entangl_tiles = []

    def tiles(self):
        """
        Returns list of tiles in game.
        """
        return self._tiles

    def show_board(self):
        """
        Returns string represent of board which could be print in terminal
        """
        display = ''
        for row in [0, 3, 6]:
            for column in range(0, 3):
                tile = self._tiles[column+row]
                wall = ' | ' if column in [0, 1] else '\n'
                in_tile = '' if not tile.is_entanglement() else '*'
                for index, element in enumerate(tile.array()):
                    coma = '' if index == 0 else ', '
                    in_tile += f'{coma}{element}'
                display += f'{in_tile:^{24}}{wall}'
            line_len = 78
            floor = '-'*line_len if row in [0, 3] else ''
            display += floor
            display += '\n'
        return display

    def entangl_tiles(self):
        """
        Returns list of tiles numbers which are in entanglement
        """
        return self._entangl_tiles

    def add_entangl_tile(self, tile):
        """
        Add number of tile which is in entanglement
        and set tile entanglemet to True
        """
        self._entangl_tiles.append(tile)
        self._tiles[tile].set_is_entanglement(True)

    def reset_entangl_tiles(self):
        """
        Reset list of tiles in entanglemet
        """
        for tile in self._entangl_tiles:
            self._tiles[tile].set_is_entanglement(False)
        self._entangl_tiles = []

    def could_collapse(self, tile, what_collapse):
        """
        Returns if choosen move could collapse
        """
        can_collapse = False
        if tile not in self._entangl_tiles:
            raise InvalidCollapseError('You could collapse only tiles with *')
        for entile in self._entangl_tiles:
            if entile != tile:
                if what_collapse in self._tiles[entile].array():
                    can_collapse = True
        return can_collapse

    def collapse(self, tile, what_collapse):
        """
        Changes tiles state to collapsed if its possible
        """
        if self.could_collapse(tile, what_collapse):
            ctile = self._tiles[tile]
            moves_to_collapse = []
            for move in ctile.array():
                if move not in moves_to_collapse and move != what_collapse:
                    moves_to_collapse.append(move)
            ctile.set_collapsed(what_collapse)
            for move in moves_to_collapse:
                for tile in self._tiles:
                    if move in tile.array():
                        for an_move in tile.array():
                            not_repeat = an_move not in moves_to_collapse
                            if not_repeat and an_move != move:
                                moves_to_collapse.append(an_move)
                        tile.set_collapsed(move)
        else:
            raise InvalidCollapseError("""Cannot collapse it.
You must choose move which is on two tiles in entanglement""")

    def analyse_board(self):
        """
        Analyses the board,
        returns list of collapsed tiles,
        if tile is not collapsed append "-" to list
        """
        coll_moves = []
        for tile_number in range(9):
            if self._tiles[tile_number].is_collapsed():
                move = self._tiles[tile_number].array()[0]
                coll_moves.append(move)
            else:
                coll_moves.append('-')
        return coll_moves

    def win_options(self, coll_moves):
        """
        Create list of winning options and tiles and returns it
        """
        win_options = []
        win_tiles = []
        if coll_moves[0][0] == coll_moves[1][0] == coll_moves[2][0]:
            if coll_moves[0] != '-':
                win = coll_moves[0][0] + min(coll_moves[0][1], coll_moves[1][1], coll_moves[2][1])
                win_options.append(win)
                win_tiles.append([0, 1, 2])
        if coll_moves[0][0] == coll_moves[3][0] == coll_moves[6][0]:
            if coll_moves[0] != '-':
                win = coll_moves[0][0] + min(coll_moves[0][1], coll_moves[3][1], coll_moves[6][1])
                win_options.append(win)
                win_tiles.append([0, 3, 6])
        if coll_moves[0][0] == coll_moves[4][0] == coll_moves[8][0]:
            if coll_moves[0] != '-':
                win = coll_moves[0][0] + min(coll_moves[0][1], coll_moves[4][1], coll_moves[8][1])
                win_options.append(win)
                win_tiles.append([0, 4, 8])
        if coll_moves[1][0] == coll_moves[4][0] == coll_moves[7][0]:
            if coll_moves[1] != '-':
                win = coll_moves[1][0] + min(coll_moves[1][1], coll_moves[4][1], coll_moves[7][1])
                win_options.append(win)
                win_tiles.append([1, 4, 7])
        if coll_moves[2][0] == coll_moves[5][0] == coll_moves[8][0]:
            if coll_moves[2] != '-':
                win = coll_moves[2][0] + min(coll_moves[2][1], coll_moves[5][1], coll_moves[8][1])
                win_options.append(win)
                win_tiles.append([2, 5, 8])
        if coll_moves[3][0] == coll_moves[4][0] == coll_moves[5][0]:
            if coll_moves[3] != '-':
                win = coll_moves[3][0] + min(coll_moves[3][1], coll_moves[4][1], coll_moves[5][1])
                win_options.append(win)
                win_tiles.append([3, 4, 5])
        if coll_moves[6][0] == coll_moves[7][0] == coll_moves[8][0]:
            if coll_moves[6] != '-':
                win = coll_moves[6][0] + min(coll_moves[6][1], coll_moves[7][1], coll_moves[8][1])
                win_options.append(win)
                win_tiles.append([6, 7, 8])
        if coll_moves[2][0] == coll_moves[4][0] == coll_moves[6][0]:
            if coll_moves[2] != '-':
                win = coll_moves[2][0] + min(coll_moves[2][1], coll_moves[4][1], coll_moves[6][1])
                win_options.append(win)
                win_tiles.append([2, 4, 6])
        return win_options, win_tiles

    def is_winner(self):
        """
        If there is a winner, function returns
        who is it and winning tiles. If there is no winner, returns unknown
        """
        coll_moves = self.analyse_board()
        not_collapsed = coll_moves.count('-')
        win_options, win_tiles = self.win_options(coll_moves)
        if len(win_options) == 1:
            return win_options[0][0], win_tiles[0]
        elif len(win_options) > 1:
            min_opt = 40
            winner = ''
            winner_tiles = []
            for opt in win_options:
                if int(opt[1]) < min_opt:
                    min_opt = int(opt[1])
            for (opt, tiles) in zip(win_options, win_tiles):
                if int(opt[1]) == min_opt:
                    winner = opt[0]
                    winner_tiles = tiles
            return winner, winner_tiles
        elif win_options == [] and (not_collapsed == 0 or not_collapsed == 1):
            return 'unknown', []
        else:
            return None, []
