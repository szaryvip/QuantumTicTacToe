from quantum_tictactoe.tile import Tile


def test_create_tile_with_defaults():
    tile = Tile()
    assert tile.array() == []


def test_create_tile_with_parameters():
    tile = Tile(['x1', 'x1'], True, False)
    assert tile.array() == ['x1', 'x1']
    assert tile.is_entanglement() is True


def test_set_collapsed():
    tile = Tile()
    tile.set_collapsed('x1')
    assert tile.is_collapsed() is True
    assert tile.array() == ['x1', 'x1', 'x1']


def test_set_is_entanglement():
    tile = Tile()
    tile.set_is_entanglement(True)
    assert tile.is_entanglement() is True


def test_set_move_on_tile():
    tile = Tile()
    assert tile.array() == []
    tile.set_move_on_tile('x1')
    assert tile.array() == ['x1']


def test_clear_tile():
    tile = Tile(['x1'], True, True)
    assert tile.array() == ['x1']
    assert tile.is_collapsed() is True
    assert tile.is_entanglement() is True
    tile.clear_tile()
    assert tile.array() == []
    assert tile.is_entanglement() is False


def test_remove_move():
    tile = Tile(['x1'])
    assert tile.array() == ['x1']
    tile.remove_move('x1')
    assert tile.array() == []
