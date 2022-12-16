import pygame
import time
import random
import shelve
from game import interface
from common import constants

# initializes the use of the pygame library
pygame.init()

# creates and opens a window 500 pixels by 700 pixels
screen = pygame.display.set_mode((600, 700))
# sets the title of the window
pygame.display.set_caption("Pythtris")

# variable holding the dict key of a random shape from the shapes dictionary
shape_key = random.choice(list(constants.shapes.keys()))
# another random dict key to show what shape will be coming next
up_next_key = random.choice(list(constants.shapes.keys()))

# variable holing the shape corresponding to the current shape_key
shape = constants.shapes[shape_key].copy()

# width of the current shape, aka the length of the inner list in the dictionary
shape_width = len(shape[0])
# height of the current shape, aka the length of the outer list in the dictionary
shape_height = len(shape)

# creates a board from the custom Board class in interface.py
# Board is basically a container holding the dimensions, score, level, and other info of the game
board = interface.Board()

# sets the initial x position of the current shape to the middle of the board
pos_x = int(board.width/2) - 1
# sets the initial y position to the top of the screen, 4 places above what is shown to the user
# giving the shape room to appear without being in play
pos_y = 0

# counts how many rotations have been done to the shape
rotations = 0


# function to check if there is a collision going to happen
def check_collision(down: int = 1, horiz: int = 0):
    collision = False
    # checks if the shape is within the play area / if it is too far down the screen to drop any more
    if not pos_y + shape_height - 1 < board.height - 1:
        return True
    try:
        # loops through the shape's dictionary
        for i, n in enumerate(shape):
            for j, m in enumerate(n):
                if m:
                    if horiz != -1:
                        # checks if the upcoming space on the board is non-zero (occupied) and
                        # if the checked upcoming space is part of the current shape
                        # triggers the index error if the shape[i + 1] space does not exist
                        if board.spaces[pos_y + i + down][pos_x + j + horiz] != 0 \
                                and shape[i + down][j + horiz] == 0:
                            # if the conditions were met, a collision occurs and sets the variable, and breaks the loop
                            collision = True
                            break
                    else:
                        if board.spaces[pos_y + i + down][pos_x + j + horiz] != 0 \
                                and shape[i + down][j + horiz - shape_width] == 0:
                            # if the conditions were met, a collision occurs and sets the variable, and breaks the loop
                            collision = True
                            break
            # breaks the outer loop if collision occurs
            if collision:
                break
        return collision
    except IndexError:
        # if the shape index error is triggered, assume it is a collision
        return True


# function to hold the code that moves the shape
def move_shape(dir: str = 'down/horiz', val: int = 1):
    global pos_y, pos_x
    if dir.lower() == 'down':
        # 1st for loop: this loop cycles through the shape's dictionary, checking what spaces are supposed
        # to be filled, then causes that space on the board to update it's value to 0
        # effectively clearing the last position of the shape
        for i, n in enumerate(shape):
            for j, m in enumerate(n):
                if m:
                    board.spaces[pos_y + i][pos_x + j] = 0
        # increments/decrements y position, uses divided by abs() in case the value sent to the function
        # was higher than 1 or lower than -1
        pos_y += int(val/abs(val))
        # 2nd for loop: this loop cycles through the shape's dictionary, checking what spaces are supposed
        # to be filled, then causes that space on the board to update it's value to a value other than 0
        # this allows the code to check what spaces are occupied by a shape
        for i, n in enumerate(shape):
            for j, m in enumerate(n):
                if m:
                    board.spaces[pos_y + i][pos_x +
                                            j] = constants.values[shape_key]

    elif dir.lower() == 'horiz':
        # 1st for loop: this loop cycles through the shape's dictionary, checking what spaces are supposed
        # to be filled, then causes that space on the board to update it's value to 0
        # effectively clearing the last position of the shape
        for i, n in enumerate(shape):
            for j, m in enumerate(n):
                if m:
                    board.spaces[pos_y + i][pos_x + j] = 0
        # increments/decrements x position, uses divided by abs() in case the value sent to the function
        # was higher than 1 or lower than -1
        pos_x += int(val/abs(val))
        # 2nd for loop: this loop cycles through the shape's dictionary, checking what spaces are supposed
        # to be filled, then causes that space on the board to update it's value to a value other than 0
        # this allows the code to check what spaces are occupied by a shape
        for i, n in enumerate(shape):
            for j, m in enumerate(n):
                if m:
                    board.spaces[pos_y + i][pos_x +
                                            j] = constants.values[shape_key]
    else:
        raise Exception('Please specify a direction, down/horiz')


# function to hold the code that rotates the shape
def rotate(dir: str = 'cw/ccw'):
    global shape_height, shape_width, pos_x, pos_y, rotations, shape
    if dir.lower() == 'cw':
        rotations += 1
    elif dir.lower() == 'ccw':
        rotations += 3
    else:
        raise Exception('Please specify a rotational direction, cw/ccw')

    # 1st for loop: removes the shape from it's previous position
    for i, n in enumerate(shape):
        for j, m in enumerate(n):
            if m:
                board.spaces[pos_y + i][pos_x + j] = 0

    # creates temporary variable to hold a copy of the shape
    temp = shape.copy()
    # removes the values from the shape list
    shape.clear()

    if rotations % 4 == 0:
        shape = constants.shapes[shape_key].copy()
    elif rotations % 4 == 1:
        for i in range(len(temp[0])):
            shape.append([])
            for j in range(len(temp)):
                if temp[j][i]:
                    shape[i].append(constants.values[shape_key])
                else:
                    shape[i].append(0)
    elif rotations % 4 == 2:
        shape = constants.shapes[shape_key].copy()
        rev_shape = list(reversed(constants.shapes[shape_key].copy()))
        for i in range(len(shape)):
            shape[i] = list(reversed(rev_shape[i].copy()))
    elif rotations % 4 == 3:
        for i in range(len(temp[0])):
            shape.append([])
            for j in range(len(temp)):
                if temp[j][i]:
                    shape[i].append(constants.values[shape_key])
                else:
                    shape[i].append(0)
        rev_shape = list(reversed(shape))
        for i in range(len(shape)):
            shape[i] = list(reversed(rev_shape[i]))
    # resets width and height to match the new rotated shape
    shape_width = len(shape[0])
    shape_height = len(shape)

    # replaces the shape at it's new position
    for i, n in enumerate(shape):
        for j, m in enumerate(n):
            if m:
                board.spaces[pos_y + i][pos_x +
                                        j] = constants.values[shape_key]


# framerate for how many times the screen should update per second
framerate = 24
# variable for counting how many frames have passed
frame = 0
# variable for how fast the shapes drop down the screen
drop_speed = 4
# variable to check if game is paused or not
paused = False
# variable to check if game is lost
lost = False
# below is the gameplay loop, an infinite loop that runs while the running variable is true
running = True
# array holding username letters
username = []
while running:
    # uses the time library to wait for 1/framerate seconds
    time.sleep(1/framerate)
    if not paused:
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
            if not check_collision():
                move_shape('down')
            elif check_collision() and pos_y <= 3:
                paused = True
                lost = True
                interface.open_lose(username)
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
                shape_width = len(shape[0])
                shape_height = len(shape)

                # re-sets the position back to the top-middle
                pos_x = int(board.width/2) - 1
                pos_y = 0

                # resets the number of rotations for the shape
                rotations = 0
            # re-sets frames to 0 so the frame counting can recommence
            frame = 0

    # checks through all pygame events currently happening, such as key-presses
    for event in pygame.event.get():

        # checks if the event is a key-press
        if event.type == pygame.KEYDOWN:
            if not paused and not lost:
                # checks if the keypress event is the left-arrow
                if event.key == pygame.K_LEFT:
                    # checks if the shape is within the confines of the board
                    if not check_collision(0, -1) and pos_x > 0:
                        board.spaces[pos_y][pos_x] = 0
                        move_shape('horiz', -1)
                # checks if the key-press event is the right-arrow
                if event.key == pygame.K_RIGHT:
                    # checks if the shape is within the confines of the board
                    if not check_collision(0, 1):
                        board.spaces[pos_y][pos_x] = 0
                        move_shape('horiz', 1)
                # checks if the key-press event is the a key
                if event.key == pygame.K_UP:
                    # checks if the shape is within the confines of the board
                    if pos_x + shape_width - 1 <= board.width - 1 \
                            and pos_x + shape_height - 1 <= board.width - 1 \
                            and pos_x >= 0 and pos_y + shape_width - 1 < board.height \
                            and pos_y + shape_height - 1 <= board.height:
                        rotate('cw')
                # checks if the key-press event is the d key
                if event.key == pygame.K_DOWN:
                    # checks if the shape is within the confines of the board
                    if pos_x + shape_width - 1 <= board.width - 1 \
                            and pos_x + shape_height - 1 <= board.width - 1 \
                            and pos_x >= 0 and pos_y + shape_width - 1 < board.height \
                            and pos_y + shape_height - 1 <= board.height:
                        rotate('ccw')
            # checks if the game has been paused but not lost
            elif paused and not lost:
                # changes the selected button to the menu button
                if event.key == pygame.K_UP:
                    selected = 'menu'
                    interface.open_pause('menu')
                # changes the selected button to the close button
                elif event.key == pygame.K_DOWN:
                    selected = 'close'
                    interface.open_pause('close')
                # activates the selected button
                if event.key == pygame.K_RETURN:
                    if selected == 'menu':
                        running = False
                    elif selected == 'close':
                        running = False
                    else:
                        pass
            # checks if the key-press event is the escape key
            if event.key == pygame.K_ESCAPE:
                # checks if the game isn't paused yet nor lost
                if not paused and not lost:
                    # opens the pause screen
                    interface.open_pause()
                    # pauses the game
                    paused = True
                elif paused and not lost:
                    # unpauses the game
                    paused = False
            # checks if the game is lost
            if lost:
                # checks if backspace is pressed after the game is lost
                if event.key == pygame.K_BACKSPACE:
                    # if username has any letters in it, remove the last one
                    if len(username) > 0:
                        username.pop()
                # checks if the name of the key is a single letter/number
                if len(pygame.key.name(event.key)) == 1:
                    # checks if the amount of letters put so far is less than 4
                    if len(username) < 4:
                        # adds the put letter to the username
                        username.append(pygame.key.name(event.key))
                    else:
                        # removes the last letter
                        username.pop()
                        # replaces the last letter with the put letter
                        username.append(pygame.key.name(event.key))
                # opens the lose screen with the given username inputted
                interface.open_lose(username)
                # checks if the username is filled and the enter key is pressed
                if len(username) == 4 and event.key == pygame.K_RETURN:
                    u = ''.join(username).upper()
                    scores = shelve.open('pythtris/data/score')
                    if not scores.__contains__(u):
                        scores[u] = str(board.score)
                    username.clear()
                    for i in range(len(board.spaces)):
                        board.spaces[i] = [0 for el in board.spaces[i]]
                    board.score = 0
                    board.cleared_lines = 0
                    board.level = 0
                    paused = False
                    lost = False
        # checks if event is quit
        if event.type == pygame.QUIT:
            # stops the while loop
            running = False


# quits and closes the window
pygame.quit()
