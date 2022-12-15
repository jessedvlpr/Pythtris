# dictionary holding lists of either 1 or 0, 1 being a filled block, 0 being an empty space
# the number of lists is the height of the space, and the number of integers in each list is the width
shapes = {
    'St':   [
        [1, 1, 1, 1]
    ],
    'Sk':   [
        [0, 1, 1],
        [1, 1, 0]
    ],
    'Z':    [
        [1, 1, 0],
        [0, 1, 1]
    ],
    'Sq':   [
        [1, 1],
        [1, 1]
    ],
    'T':    [
        [1, 1, 1],
        [0, 1, 0]
    ],
    'L':    [
        [1, 0],
        [1, 0],
        [1, 1]
    ],
    'J':    [
        [0, 1],
        [0, 1],
        [1, 1]
    ]
}
# dictionary holding the values of each shape, the value will be held by the space on the board
values = {
    'St':   100,
    'Sk':   200,
    'Z':    300,
    'Sq':   400,
    'T':    500,
    'L':    600,
    'J':    700
}
# dictionary holding the color values for each shape
colors = {
    'St':   (255, 255, 255),
    'Sk':   (255, 64, 64),
    'Z':    (255, 64, 255),
    'Sq':   (127, 127, 255),
    'T':    (64, 255, 64),
    'L':    (255, 255, 0),
    'J':    (0, 127, 255)
}
