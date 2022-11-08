import time
import pygame as pg

(width, height) = (400, 600)

screen = pg.display.set_mode((width, height))

pg.display.flip()

running = True

while running:
    time.sleep(1/60)
    for event in pg.event.get():
        if event.type == pg.quit:
            running = False
