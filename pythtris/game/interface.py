import pygame
import random
from common import constants


outer_line_color = (255, 255, 255)
inner_line_color = (127, 127, 127)


def visualize_board(board: 'Board', shape: str, x: int = 0, y: int = 0, scale: float = 1):
    surface = pygame.display.get_surface()
    top_left = (x, y)
    box_size = 30 * scale
    font = pygame.font.SysFont(None, 32)

    level_text = font.render(
        'Level: ' + str(board.level), False, (255, 255, 255))
    score_text = font.render(
        'Score: ' + str(board.score), False, (255, 255, 255))
    next_text = font.render('Up Next: ', False, (255, 255, 255))

    level_rect = level_text.get_rect()
    next_rect = next_text.get_rect()
    score_rect = score_text.get_rect()

    level_rect.left = top_left[0]
    level_rect.top = top_left[1] + 10

    score_rect.left = top_left[0]
    score_rect.top = top_left[1] + 40

    next_rect.left = top_left[0]
    next_rect.top = top_left[1] + 70

    surface.blit(level_text, level_rect)
    surface.blit(score_text, score_rect)
    surface.blit(next_text, next_rect)

    for i in range(3):
        for j in range(4):
            pygame.draw.rect(surface, constants.colors[shape],
                             (top_left[0] + box_size * i,
                              top_left[1] + 110 + box_size * j,
                              box_size + 1, box_size + 1), 1)

    pygame.draw.rect(surface,
                     outer_line_color,
                     (top_left[0],
                      top_left[1] + 110,
                      box_size * 3, box_size * 4), 2)

    offset_x = top_left[1]
    for i in range(board.height):
        if i >= 4:
            offset_y = top_left[0] + 120
            for j in range(board.width):
                fill = board.spaces[i][j]
                if fill:
                    for k in constants.values.keys():
                        if board.spaces[i][j] == constants.values[k]:
                            inner_line_color = constants.colors[k]
                else:
                    inner_line_color = (127, 127, 127)
                pygame.draw.rect(surface, inner_line_color,
                                 (offset_y, offset_x, box_size + 1, box_size + 1), not fill)
                offset_y = offset_y + box_size
            offset_x = offset_x + box_size

    pygame.draw.rect(surface,
                     outer_line_color,
                     (top_left[0] + 120,
                         top_left[1],
                         board.width * box_size + 1,
                         (board.height - 4) * box_size + 1), 2)

    pygame.display.flip()


class Board:
    def __init__(self):
        self.height = 24
        self.width = 10
        self.score = 0
        self.level = 0
        self.cleared_lines = 0
        self.spaces = []
        for i in range(self.height):
            self.spaces.append([])
            for j in range(self.width):
                self.spaces[i].append(0)
