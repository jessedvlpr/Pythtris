import pygame
import random


def visualize_board(board: 'Board', x: int = 0, y: int = 0, scale: float = 1):
    top_left = (x, y)
    box_size = 30 * scale

    outer_line_color = (255, 255, 255)
    inner_line_color = (127, 127, 127)

    surface = pygame.display.get_surface()

    offset_x = top_left[1]
    for i in range(board.height - 4):
        offset_y = top_left[0]
        for j in range(board.width):
            fill = not board.spaces[i][j]
            pygame.draw.rect(surface, inner_line_color,
                             (offset_y, offset_x, box_size, box_size), fill)
            offset_y = offset_y + box_size
        offset_x = offset_x + box_size

    pygame.draw.rect(surface,
                     outer_line_color,
                     (top_left[0],
                         top_left[1],
                         board.width * box_size + 1,
                         (board.height - 4) * box_size + 1), 1)

    pygame.display.flip()


class Board:
    def __init__(self):
        self.height = 24
        self.width = 10
        self.spaces = [[]]
        for i in range(self.height):
            self.spaces.append([])
            for j in range(self.width):
                self.spaces[i].append(0)
