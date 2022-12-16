import __main__ as main
from game import interface
from common import constants


def test_check_collision():
    board = interface.Board()
    board.spaces = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    # test collision at bottom of screen
    assert main.check_collision(down=1) == True
    # test no collision
    assert main.check_collision(down=1) == False
    # test collision to right
    assert main.check_collision(horiz=1) == True
    # test collision to left
    assert main.check_collision(horiz=-1) == True


def test_move_shape():
    board = interface.Board()
    board.spaces = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    shape = [
        [1, 1],
        [1, 1],
    ]

    # test moving shape down
    main.move_shape('down', 1)
    assert board.spaces == [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    # test moving shape right
    main.move_shape('horiz', 1)
    assert board.spaces == [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]


def test_rotate_shape():
    board = interface.Board()
    board.spaces = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    shape = [
        [1, 1],
        [1, 1],
    ]

    # test rotating shape clockwise
    main.rotate_shape(1)
    assert shape == [
        [1, 1],
        [1, 1]
    ]
    # test rotating shape counterclockwise
    main.rotate_shape(-1)
    assert shape == [
        [1, 1],
        [1, 1],
    ]


test_check_collision()
test_move_shape()
test_rotate_shape()
