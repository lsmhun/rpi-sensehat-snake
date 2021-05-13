#!/usr/bin/python3
from sense_hat import SenseHat
from time import sleep
from random import randint

sense = SenseHat()


# Variables ---------------------------

snake = [[2, 4], [3, 4], [4, 4]]
snake_color = (0, 0, 255)
veg_color = (255, 0, 0)
vegetables = []
max_veg_number = 3

score = 0
is_dead = False

blank_color = (0, 0, 0)

# These directions are defined in sense lib (lowercase)
# up, down, left, right

direction = 'right'
SPEED = 0.5


# Functions ---------------------------

def draw_snake():
    for pix in snake:
        sense.set_pixel(pix[0], pix[1], snake_color)


def new_location_for_veg():
    x = randint(0, 7)
    y = randint(0, 7)
    return [x, y]


def make_veg():
    global vegetables
    global max_veg_number

    # randint(1, 5) > 4 --> it is for slow down vegetables creation
    if len(vegetables) >= max_veg_number or randint(1, 5) > 4:
        return

    new_veg = new_location_for_veg()
    while new_veg in snake:
        new_veg = new_location_for_veg()

    vegetables.append(new_veg)
    sense.set_pixel(new_veg[0], new_veg[1], veg_color)


def wrap(pix):
    # Wrap x coordinate
    if pix[0] > 7:
        pix[0] = 0
    if pix[0] < 0:
        pix[0] = 7

    # Wrap y coordinate
    if pix[1] < 0:
        pix[1] = 7
    if pix[1] > 7:
        pix[1] = 0

    return pix


def move():
    global vegetables
    global score
    global is_dead
    global direction
    global snake

    # Find the last and first items in the slug list
    last = snake[-1]
    first = snake[0]
    next = list(last)  # Create a copy of the last item

    if direction == 'right':
        next[0] = last[0] + 1
    elif direction == 'left':
        next[0] = last[0] - 1
    elif direction == 'down':
        next[1] = last[1] + 1
    elif direction == 'up':
        next[1] = last[1] - 1
    next = wrap(next)

    is_removeable = True
    if next in vegetables:
        vegetables.remove(next)
        is_removeable = False
        score += 1

    if next in snake:
        is_dead = True

    # Add this pixel at the end of the slug list
    snake.append(next)

    # Set the new pixel to the slug's colour
    sense.set_pixel(next[0], next[1], snake_color)

    # Set the first pixel in the slug list to blank
    sense.set_pixel(first[0], first[1], blank_color)

    # Remove the first pixel from the list
    if is_removeable == True:
        snake.remove(first)


def joystick_moved(event):
    global direction
    global is_dead

    # no revert direction allowed
    if event.direction == 'up' and direction == 'down' \
        or event.direction == 'down' and direction == 'up' \
        or event.direction == 'left' and direction == 'right' \
        or event.direction == 'right' and direction == 'left':
        return

    if event.direction != 'middle':
        direction = event.direction
    elif is_dead == True:
        reset()


def reset():
    global direction
    global snake
    global vegetables
    global score
    global is_dead
    sense.clear()

    del snake[:]
    snake = [[2, 4], [3, 4], [4, 4]]
    direction = 'right'
    vegetables = []
    score = 0
    is_dead = False
    draw_snake()


def dead_face():
    P = (10, 255, 10)
    O = (0, 0, 0)
    logo = [
    O, O, O, O, O, O, O, O,
    O, P, O, P, O, P, O, P,
    O, O, P, O, O, O, P, O,
    O, P, O, P, O, P, O, P,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, P, P, P, P, P, P, P,
    O, O, O, O, O, O, O, O,
    ]
    return logo

def dead():
    global score
    sense.show_message('Score: ' + str(score))
    sense.set_pixels(dead_face())


# Main program ------------------------

reset()
sense.stick.direction_any = joystick_moved
while True:
    # You can reset the game with pushing middle button
    while is_dead == False:
        move()
        make_veg()
        if is_dead == True:
            dead()
        sleep(SPEED)
    sleep(SPEED)
