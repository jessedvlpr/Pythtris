import pygame
import random
from common import constants


def visualize_board(board: 'Board', shape: str, up_next: str, x: int = 0, y: int = 0, scale: float = 1):
    # gets the surface of the currently displayed window
    surface = pygame.display.get_surface()

    # sets inner and outer line colors to white and grey respectively
    outer_line_color = (255, 255, 255)
    inner_line_color = (127, 127, 127)

    # sets the top left of the visualization to a tuple holding the specified x and y positions
    top_left = (x, y)

    # sets the size of the boxes to 30 multiplied by the specified scale multiplier
    box_size = 30 * scale

    # sets the font of screen text to the default system font
    font = pygame.font.SysFont(None, 32)

    # renders 3 texts for level, score, and up next displays
    level_text = font.render(
        'Level: ' + str(board.level), False, (255, 255, 255))
    score_text = font.render(
        'Score: ' + str(board.score), False, (255, 255, 255))
    next_text = font.render('Up Next: ', False, (255, 255, 255))

    # gets the rect bounds for each text, for the ability to mutate the positions and such
    level_rect = level_text.get_rect()
    next_rect = next_text.get_rect()
    score_rect = score_text.get_rect()

    # changes the position of each of the texts to their appropriate spots on screen
    level_rect.left = top_left[0]
    level_rect.top = top_left[1] + 10

    score_rect.left = top_left[0]
    score_rect.top = top_left[1] + 40

    next_rect.left = top_left[0]
    next_rect.top = top_left[1] + 100

    # adds the text to the surface
    surface.blit(level_text, level_rect)
    surface.blit(score_text, score_rect)
    surface.blit(next_text, next_rect)

    # creates a 3x4 box to hold the up_next shape
    for i in range(3):
        for j in range(4):
            # try is for checking if the shape's dimensions fall out of the bounds of the for loops
            try:
                # if the spot lining up with i and j is not a 0 in the shape, then fill the relative box
                if constants.shapes[up_next][j][i]:
                    pygame.draw.rect(surface, constants.colors[up_next],
                                     (top_left[0] + box_size * i,
                                     top_left[1] + 130 + box_size * j,
                                     box_size + 1, box_size + 1), 0)
                # if the lining up spot is a 0, trigger the index error to re-use the code
                else:
                    [][-1]  # hacky solution to trigger IndexError
            # if the lining up spot is neither a 0 or a 1, it is off the grid entirely, then fill the spot with
            # an empty box
            except IndexError:
                pygame.draw.rect(surface, inner_line_color,
                                 (top_left[0] + box_size * i,
                                  top_left[1] + 130 + box_size * j,
                                  box_size + 1, box_size + 1), 1)

    # adds a border around the up next box
    pygame.draw.rect(surface,
                     outer_line_color,
                     (top_left[0],
                      top_left[1] + 130,
                      box_size * 3, box_size * 4), 2)

    # sets the y-offset to the provided y position
    offset_y = top_left[1]

    # loops through the board objects height
    for i in range(board.height):
        # executes code only after the 3rd row is passed
        if i >= 4:
            # sets the x-offset to the provided x position, plus a boundary given for the left-most ui
            offset_x = top_left[0] + 120

            # loops through the board objects width
            for j in range(board.width):

                # variable holding the value of board space, to determine if the space should be filled or empty
                fill = board.spaces[i][j]
                # if the space should be filled, checks through the values dictionary and matches the value to
                # the shape on the screen, then makes the fill-color into the respective shape's color in constants.py
                if fill:
                    for k in constants.values.keys():
                        if board.spaces[i][j] == constants.values[k]:
                            inner_line_color = constants.colors[k]
                # if the space should not be filled, set the color back to grey
                else:
                    inner_line_color = (127, 127, 127)
                # draw each space with the calculated color and fill boolean (0 = false, other = true)
                pygame.draw.rect(surface, inner_line_color,
                                 (offset_x, offset_y, box_size + 1, box_size + 1), not fill)

                # pushes the x-offset ahead by the width of a box
                offset_x = offset_x + box_size
            # pushes the y-offset ahead by the width of a box
            offset_y = offset_y + box_size

    # creates a border around the 10x20 board
    pygame.draw.rect(surface,
                     outer_line_color,
                     (top_left[0] + 120,
                         top_left[1],
                         board.width * box_size + 1,
                         (board.height - 4) * box_size + 1), 2)

    # sends the updated info to the screen
    pygame.display.flip()


# Board class to hold the information about the game
class Board:
    def __init__(self):
        self.height = 24
        self.width = 10
        self.score = 0
        self.level = 0
        self.cleared_lines = 0
        self.spaces = []

        # creates a 24x10 board to play the game on
        for i in range(self.height):
            self.spaces.append([])
            for j in range(self.width):
                self.spaces[i].append(0)
