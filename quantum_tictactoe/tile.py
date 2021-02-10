class Tile:
    """
    Tile class
    Contains array of player and bot moves, entanglement and collapsed move.
    :param array: array of moves, default to empty list
    :type array: list

    :param is_entanglement: returns if tile is entanglement, default to False
    :type is_entanglement: boolean

    :param is_collapsed: returns if tile is collapsed, default to False
    :type is_collapsed: boolean

    """
    def __init__(self, array=None, is_entanglement=False, is_collapsed=False):
        if array is None:
            self._array = []
        else:
            self._array = array
        self._is_entanglement = is_entanglement
        self._is_collapsed = is_collapsed

    def array(self):
        """
        Returns list of moves set on tile
        """
        return self._array

    def remove_move(self, move):
        """
        Removes move from array
        """
        new_array = []
        for mv in self._array:
            if mv != move:
                new_array.append(mv)
        self._array = new_array

    def clear_tile(self):
        """
        Clear all move from tile
        and returns default variables
        """
        self._array = []
        self._is_collapsed = False
        self._is_entanglement = False

    def is_entanglement(self):
        """
        Returns true if tile is in entanglement
        """
        return self._is_entanglement

    def is_collapsed(self):
        """
        Returns true if tile is collapsed
        """
        return self._is_collapsed

    def set_collapsed(self, who):
        """
        Makes tile collapsed and write collapsed move to tile
        """
        self._is_collapsed = True
        self._array = [who, who, who]

    def set_is_entanglement(self, entanglement):
        """
        Makes tile to be or not in entanglement
        """
        self._is_entanglement = entanglement

    def set_move_on_tile(self, who_move):
        """
        Add move to list of moves on choosen tile
        """
        self._array.append(who_move)
