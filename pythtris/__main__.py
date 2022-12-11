import pygame
import time
import random
from game import interface
from common import constants

# initializes the use of the pygame library
pygame.init()

# creates and opens a window 500 pixels by 700 pixels
screen = pygame.display.set_mode((500, 700))
# sets the title of the window
pygame.display.set_caption("Pythtris")

# framerate for how many times the screen should update per second
framerate = 24
# variable for counting how many frames have passed
frame = 0
# variable for how fast the shapes drop down the screen
drop_speed = 10

# variable holding the dict key of a random shape from the shapes dictionary
shape_key = random.choice(list(constants.shapes.keys()))
# another random dict key to show what shape will be coming next
up_next_key = random.choice(list(constants.shapes.keys()))

# variable holing the shape corresponding to the current shape_key
shape = constants.shapes[shape_key].copy()

# width of the current shape, aka the length of the inner list in the dictionary
shape_width = len(shape[0]) - 1
# height of the current shape, aka the length of the outer list in the dictionary
shape_height = len(shape) - 1

# creates a board from the custom Board class in interface.py
# Board is basically a container holding the dimensions, score, level, and other info of the game
board = interface.Board()

# sets the initial x position of the current shape to the middle of the board
pos_x = int(board.width/2) - 1
# sets the initial y position to the top of the screen, 4 places above what is shown to the user
# giving the shape room to appear without being in play
pos_y = 0

# below is the gameplay loop, an infinite loop that runs while the running variable is true
running = True
while running:
    # uses the time library to wait for 1/framerate seconds
    time.sleep(1/framerate)
    # increments the current frame
    frame += 1
    # clears the screen visuals
    screen.fill(0)
    # adds the visualized board to the screen, using the board variable, current shape key, next shape key,
    # position numbers, and scale of the screen elements
    interface.visualize_board(board, shape_key, up_next_key, 30, 5, 1.15)

    # checks if current frame is more than the framerate divided by the drop speed and level
    # this causes the shapes to fall down the screen less frequently than the screen updates
    # as well, it increases the speed of the drops as level progresses
    if frame >= framerate/(drop_speed + board.level):
        collision = False
        # checks if the shape is within the play area / if it is too far down the screen to drop any more
        if not pos_y + shape_height < board.height - 1:
            collision = True
        # trys for index error
        try:
            # loops through the shape's dictionary
            for i, n in enumerate(shape):
                for j, m in enumerate(n):
                    if m:
                        # checks if the upcoming space on the board is non-zero (occupied) and
                        # if the checked upcoming space is part of the current shape
                        # triggers the index error if the shape[i + 1] space does not exist
                        if board.spaces[pos_y + i + 1][pos_x + j] != 0 and \
                                shape[i + 1][j] == 0:
                            # if the conditions were met, a collision occurs and breaks out of inner loop
                            collision = True
                            break
                # break out of outer loop
                if collision:
                    break
        except IndexError:
            # if the shape index error is triggered, assume it is a collision
            collision = True
        if not collision:
            # 1st for loop: this loop cycles through the shape's dictionary, checking what spaces are supposed
            # to be filled, then causes that space on the board to update it's value to 0
            # effectively clearing the last position of the shape
            for i, n in enumerate(shape):
                for j, m in enumerate(n):
                    if m:
                        board.spaces[pos_y + i][pos_x + j] = 0
            pos_y += 1
            # 2nd for loop: this loop cycles through the shape's dictionary, checking what spaces are supposed
            # to be filled, then causes that space on the board to update it's value to a value other than 0
            # this allows the code to check what spaces are occupied by a shape
            for i, n in enumerate(shape):
                for j, m in enumerate(n):
                    if m:
                        board.spaces[pos_y + i][pos_x +
                                                j] = constants.values[shape_key]
        else:
            # variable to check how many lines were cleared in a single move, should be max of 4
            line_count = 0
            # loops through every row of the board
            for i in range(len(board.spaces)):
                # checks if there isn't a 0 within the row, meaning if all spaces are filled by a shape
                if not (0 in board.spaces[i]):
                    # increments line count
                    line_count += 1
                    # increments total lines cleared for the current level
                    board.cleared_lines += 1
                    # replaces all values in the row to 0
                    board.spaces[i] = [0 for el in board.spaces[i]]
                    # loops through the rows above the cleared row, then moves them all down a position
                    for j in range(len(board.spaces) - (len(board.spaces) - i), 0, -1):
                        board.spaces[j] = board.spaces[j - 1].copy()
            # checks if the number of cleared lines is enough to increase the level
            if board.cleared_lines >= board.level * 10 + 10:
                # lowers the amount of lines cleared
                board.cleared_lines = board.cleared_lines - \
                    (board.level * 10 + 10)
                board.level += 1
            # checks if the amount of lines cleared in the previous move was 1, increases score by 40 * (level+1)
            if line_count == 1:
                board.score += 40 * (board.level + 1)
            # checks if the amount of lines cleared in the previous move was 2, increases score by 100 * (level+1)
            elif line_count == 2:
                board.score += 100 * (board.level + 1)
            # checks if the amount of lines cleared in the previous move was 3, increases score by 300 * (level+1)
            elif line_count == 3:
                board.score += 300 * (board.level + 1)
            # checks if the amount of lines cleared in the previous move was 4, increases score by 1200 * (level+1)
            elif line_count == 4:
                board.score += 1200 * (board.level + 1)
            # this should be impossible
            else:
                pass
            # sets current shape_key to the previously up_next key
            shape_key = up_next_key
            # assigns a new random shape_key to be up next
            up_next_key = random.choice(list(constants.shapes.keys()))

            # sets the current shape to the corresponding shape of the new shape key
            shape = constants.shapes[shape_key].copy()

            # re-sets the width and height to match the new shape
            shape_width = len(shape[0]) - 1
            shape_height = len(shape) - 1

            # re-sets the position back to the top-middle
            pos_x = int(board.width/2) - 1
            pos_y = 0
        # re-sets frames to 0 so the frame counting can recommence
        frame = 0

    # checks through all pygame events currently happening, such as key-presses
    for event in pygame.event.get():

        # checks if the event is a key-press
        if event.type == pygame.KEYDOWN:

            # checks if the keypress event is the left-arrow
            if event.key == pygame.K_LEFT:

                # checks if the shape is within the confines of the board
                if pos_x <= 9 and pos_x > 0 and pos_y > 3 and board.spaces[pos_y][pos_x - 1] == 0:

                    # 1st for loop: removes the shape from it's previous position
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x + j] = 0
                    # decrements x position, moving the shape to the left
                    pos_x -= 1

                    # 2nd for loop: adds the shape back to the board in it's new position
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x +
                                                        j] = constants.values[shape_key]

            # checks if the key-press event is the right-arrow
            if event.key == pygame.K_RIGHT:

                # checks if the shape is within the confines of the board
                if pos_x + shape_width < 9 and pos_x >= 0 and pos_y > 3 and board.spaces[pos_y][pos_x + 1 + shape_width] == 0:

                    # 1st for loop: removes the shape from it's previous position
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x + j] = 0
                    # increments x position, moving the shape to the right
                    pos_x += 1

                    # 2nd for loop: adds the shape back to the board in it's new position
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x +
                                                        j] = constants.values[shape_key]

            # checks if the key-press event is the a key
            if event.key == pygame.K_a:

                # checks if the shape is within the confines of the board
                if pos_x + shape_width <= board.width - 1 \
                    and pos_x + shape_height <= board.width - 1 \
                    and pos_x >= 0 and pos_y + shape_width < board.height \
                        and pos_y + shape_height <= board.height:

                    # 1st for loop: removes the shape from it's previous position
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x + j] = 0

                    # creates temporary variable to hold a copy of the shape
                    temp = shape.copy()
                    # removes the values from the shape list
                    shape.clear()

                    # below for loop is effectively swapping the shape's height and width with each-other
                    # as well as the values held in the positions of height and width

                    # cycles through the temp variable's width
                    for i in range(len(temp[0])):
                        # appends a new list to the height
                        shape.append([])

                        # cycles through the temp variable's height
                        for j in range(len(temp)):
                            # appends a value to the width
                            if temp[j][i]:
                                shape[i].append(1)
                            else:
                                shape[i].append(0)

                    # resets width and height to match the new rotated shape
                    shape_width = len(shape[0]) - 1
                    shape_height = len(shape) - 1

                    # replaces the shape at it's new position
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x +
                                                        j] = constants.values[shape_key]

            # checks if the key-press event is the d key
            if event.key == pygame.K_d:

                # checks if the shape is within the confines of the board
                if pos_x + shape_width <= board.width - 1 \
                    and pos_x + shape_height <= board.width - 1 \
                    and pos_x >= 0 and pos_y + shape_width < board.height \
                        and pos_y + shape_height <= board.height:

                    # 1st for loop: removes the shape from it's previous position
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x + j] = 0

                    # creates temporary variable to hold a copy of the shape
                    temp = shape.copy()
                    # removes the values from the shape list
                    shape.clear()

                    # below for loop is effectively swapping the shape's height and width with each-other
                    # as well as the values held in the positions of height and width

                    # cycles through the temp variable's width
                    for i in range(len(temp[0])):
                        # appends a new list to the height
                        shape.append([])

                        # cycles through the temp variable's height
                        for j in range(len(temp)):
                            # appends a value to the width
                            if temp[j][i]:
                                shape[i].append(1)
                            else:
                                shape[i].append(0)

                    # resets width and height to match the new rotated shape
                    shape_width = len(shape[0]) - 1
                    shape_height = len(shape) - 1

                    # replaces the shape at it's new position
                    for i, n in enumerate(shape):
                        for j, m in enumerate(n):
                            if m:
                                board.spaces[pos_y + i][pos_x +
                                                        j] = constants.values[shape_key]

        # checks if event is quit
        if event.type == pygame.QUIT:
            # stops the while loop
            running = False

# quits and closes the window
pygame.quit()
