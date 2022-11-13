import pygame
import time
from game import interface
from game import controller
from common import constants

controller.set_key('K_LEFT', controller.move_left)

screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption("Pythtris")

board = interface.Board()
interface.visualize_board(board, 150, 5, 1.15)

running = True
framerate = 60
while running:
    time.sleep(1/framerate)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
pygame.quit()
