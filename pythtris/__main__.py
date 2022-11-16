import pygame
import time
import random
from game import interface
from common import constants

pygame.init()

screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption("Pythtris")

framerate = 24
frame = 0

shape_key = random.choice(list(constants.shapes.keys()))
up_next_key = random.choice(list(constants.shapes.keys()))

shape = constants.shapes[shape_key].copy()

shape_width = len(shape[0]) - 1
shape_height = len(shape) - 1

board = interface.Board()

pos_x = int(board.width/2) - 1
pos_y = 0

running = True
while running:
    time.sleep(1/framerate)
    frame += 1
    screen.fill(0)
    interface.visualize_board(board, shape_key, up_next_key, 30, 5, 1.15)
    if frame >= framerate/(10 + board.level):
        able = True
        if pos_y + shape_height < board.height - 1:
            for i, n in enumerate(shape):
                for j, m in enumerate(n):
                    if m:
                        board.spaces[pos_y + i][pos_x + j] = 0
            pos_y += 1
            for i, n in enumerate(shape):
                for j, m in enumerate(n):
                    if m:
                        board.spaces[pos_y + i][pos_x +
                                                j] = constants.values[shape_key]
        else:
            line_count = 0
            for i in range(len(board.spaces)):
                if not (0 in board.spaces[i]):
                    line_count += 1
                    board.cleared_lines += 1
                    board.spaces[i] = [0 for el in board.spaces[i]]
                    for j in range(len(board.spaces) - (len(board.spaces) - i), 0, -1):
                        board.spaces[j] = board.spaces[j - 1].copy()
            if board.cleared_lines >= board.level * 10 + 10:
                board.cleared_lines = board.cleared_lines - \
                    (board.level * 10 + 10)
                board.level += 1
            if line_count == 1:
                board.score += 40 * (board.level + 1)
            if line_count == 2:
                board.score += 100 * (board.level + 1)
            if line_count == 3:
                board.score += 300 * (board.level + 1)
            if line_count == 4:
                board.score += 1200 * (board.level + 1)

            shape_key = up_next_key
            up_next_key = random.choice(list(constants.shapes.keys()))

            shape = constants.shapes[shape_key].copy()

            shape_width = len(shape[0]) - 1
            shape_height = len(shape) - 1

            pos_x = int(board.width/2) - 1
            pos_y = 0

        frame = 0

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if pos_x <= 9 and pos_x > 0 and pos_y > 3 and board.spaces[pos_y][pos_x - 1] == 0:
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x + j] = 0
                    pos_x -= 1
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x +
                                                        j] = constants.values[shape_key]

            if event.key == pygame.K_RIGHT:
                if pos_x + shape_width < 9 and pos_x >= 0 and pos_y > 3 and board.spaces[pos_y][pos_x + 1 + shape_width] == 0:
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x + j] = 0
                    pos_x += 1
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x +
                                                        j] = constants.values[shape_key]

            if event.key == pygame.K_a:
                if pos_x + shape_width <= 9 and pos_x + shape_height <= 9 and pos_x >= 0:
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x + j] = 0
                    temp = shape.copy()
                    shape.clear()
                    for i in range(len(temp[0])):
                        shape.append([])
                        for j in range(len(temp)):
                            if temp[j][i]:
                                shape[i].append(1)
                            else:
                                shape[i].append(0)
                    shape_width = len(shape[0]) - 1
                    shape_height = len(shape) - 1
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x +
                                                        j] = constants.values[shape_key]

            if event.key == pygame.K_d:
                if pos_x + shape_width <= 9 and pos_x + shape_height <= 9 and pos_x >= 0:
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x + j] = 0
                    temp = shape.copy()
                    shape.clear()
                    for i in range(len(temp[0])):
                        shape.append([])
                        for j in range(len(temp)):
                            if temp[j][i]:
                                shape[i].append(1)
                            else:
                                shape[i].append(0)
                    shape_width = len(shape[0]) - 1
                    shape_height = len(shape) - 1
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x +
                                                        j] = constants.values[shape_key]

            if event.key == pygame.K_ESCAPE:
                running = False
pygame.quit()
