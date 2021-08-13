
"""
This is a bot for playing Runescape. Specifically, when one has an amount of cake and chocolate in their bank,
this bot will do the dirty work of combining the two to make chocolate cake, which one can then sell on the
Grand Exchange for a tasty profit. It does this by controlling the movement and clicks of the mouse
which, conveniently, is all that is needed to play the game.

Disclaimer: The functions in this script do not work unless the following setup is completed.

Setup:

- Cake in bank slot 1
- Chocolate in bank slot 2
- 'Take x' set to 14 in bank menu
- Empty Inventory
- Stand on the west side of the GE directly opposite the northernmost banker
- Zoom all the way in and reset camera angle by clicking the compass

(there is no simple way around having this setup, unless you find the idea of coding an AI to navigate around
all of these unknowns simple...)
"""

from pynput.mouse import Button, Controller
import time
import random
import math

mouse = Controller()


# top of the banker: (1305, 377)
# bottom of the banker: (1317, 562)
# left side: (1281, 487)
# right side: (1344, 491)
# distance from right click to 'bank banker' is 40
# distance across 'bank banker button is 90

def click(location, xdim, ydim, side):
    # Moves cursor to a random location within 
    # a specified area of a chosen point
    # and left or right clicks

    r1 = random.randint(-xdim, xdim)
    r2 = random.randint(-ydim, ydim)
    r = (r1, r2)

    mouse.position = tuple(map(lambda i, j: i+j, location, r))  # move to location
    time.sleep(0.25 + (r1 / 1000))
    if side == "left":
        mouse.click(Button.left, 1)  # left click
    elif side == "right":
        mouse.click(Button.right, 1)  # right click
    time.sleep(0.5 + (r2 / 1000))

    return

# (1043, 422), (1100, 892)

def enterbank():
    # Enters the bank menu

    click((1075, 650), 10, 25, "left")  # left clicks the board in front of the banker, this opens the bank

    return

# (651, 133) top left corner of bank slot 1
# (672, 155) bottom right corner of bank slot 1

# (661, 147) is the position of the 1st bank slot
# (711, 145) is the position of the 2nd bank slot
# slots are roughly 20x20

# (1054, 62) top left corner of close bank
# (1067, 78) bottom right corner of close bank

def grabcakerecipe():
    # When in the bank menu: takes 14 cake and chocolate bars each (the ingredients for chocolate cake)
    # from the first and second bank slots respectively, and exits the bank

    click((661, 147), 5, 5, "left")  # left click bank slot 1

    click((711, 145), 5, 5, "left")  # left click bank slot 2

    click((1060, 70), 5, 5, "left")  # left click 'close bank'

    return

# (215, 942) top left of make cake button
# (303, 1007) bottom right of make cake button

# (1735, 774) is the position of the 1st inventory slot
# (1821, 882) is the position of the 15th inventory slot
# slots are roughly 20x20

# (1685, 820), (1771, 820) 'use cake' button dimensions

def makecake():
    # With an inventory containing 14 cake in the top slots and 14 chocolate in the bottom,
    # converts those ingredients into 14 chocolate cakes.

    r1 = random.randint(-40, 40)

    click((1735, 774), 5, 5, "right")  # right click inventory slot 1

    p = random.choice([-1, 1])  # randomly chooses -1 or 1
    shift = (r1, 40 + p)
    mouse.position = tuple(map(lambda i, j: i + j, mouse.position, shift))  # move to 'use cake'
    click(mouse.position, 0, 0, "left")  # left click 'use cake'

    click((1821, 882), 5, 5, "left")  # left click inventory slot 15
    time.sleep(0.5)  # gives time for 'make cake' button to appear

    click((260, 970), 40, 30, "left")  # left click 'make cake' button
    time.sleep(17.5)  # gives time for cake to be made

    return


def play():
    # The loop for the entire cake-making process, combining the functions above in order
    # to automatically create a specified number of chocolate cakes.

    k = int(input('How many cakes are you making today? '))  # defines how many times to loop
    k = math.floor(k/14)
    print('Starting up in 5, 4, 3, 2, 1...')
    time.sleep(5)  # gives time to tab into game

    enterbank()
    time.sleep(0.5)

    for i in range(k):

        r1 = random.randint(-10, 10) / 1000

        grabcakerecipe()
        time.sleep(0.25 + r1)

        makecake()
        time.sleep(0.5 + r1)

        enterbank()
        time.sleep(0.5 + r1)

        # this deposits the made chocolate cake into the bank
        click((1735, 774), 5, 5, "left")  # left click inventory slot 1

    return

if __name__ == "__main__":
    play()

