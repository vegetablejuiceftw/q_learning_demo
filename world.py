from tkinter import Tk, Canvas
from random import randint, seed

__author__ = 'philippe'

seed("Cupcakes")

master = Tk()

triangle_size = 0.1
width = 25
size = 18
grid_size_x, grid_size_y = size, size
actions = "up", "down", "left", "right"

board = Canvas(master, width=grid_size_x * width, height=grid_size_y * width)
player = 0, 0
score = 1
restart = False
walk_cost = -0.04

walls = {(randint(0, grid_size_x - 1), randint(0, grid_size_y - 1)) for _ in range(grid_size_x * grid_size_y // 6)}
walls.discard((0, 0))
specials = {(grid_size_x - 1, grid_size_y - 1): ("green", 1)}
specials.update({(randint(0, grid_size_x - 1), randint(0, grid_size_y - 1)): ("red", -1) for _ in range(size // 2)})
triangles = {}


def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i + 0.5 - triangle_size) * width, (j + triangle_size) * width,
                                    (i + 0.5 + triangle_size) * width, (j + triangle_size) * width,
                                    (i + 0.5) * width, j * width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i + 0.5 - triangle_size) * width, (j + 1 - triangle_size) * width,
                                    (i + 0.5 + triangle_size) * width, (j + 1 - triangle_size) * width,
                                    (i + 0.5) * width, (j + 1) * width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i + triangle_size) * width, (j + 0.5 - triangle_size) * width,
                                    (i + triangle_size) * width, (j + 0.5 + triangle_size) * width,
                                    i * width, (j + 0.5) * width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i + 1 - triangle_size) * width, (j + 0.5 - triangle_size) * width,
                                    (i + 1 - triangle_size) * width, (j + 0.5 + triangle_size) * width,
                                    (i + 1) * width, (j + 0.5) * width,
                                    fill="white", width=1)


def render_grid():
    for i in range(grid_size_x):
        for j in range(grid_size_y):
            board.create_rectangle(i * width, j * width, (i + 1) * width, (j + 1) * width, fill="white", width=1)
            for action in actions:
                triangles[(i, j, action)] = create_triangle(i, j, action)
    for position, data in specials.items():
        i, j = position
        c, w = data
        board.create_rectangle(i * width, j * width, (i + 1) * width, (j + 1) * width, fill=c, width=1)
    for i, j in walls:
        board.create_rectangle(i * width, j * width, (i + 1) * width, (j + 1) * width, fill="black", width=1)


def move_me(new_x, new_y):
    global player
    size = 0.6
    start, end = width * (1 - size) / 2, width * (1 + size) / 2
    board.coords(
        me,
        new_x * width + start,
        new_y * width + start,
        new_x * width + end,
        new_y * width + end
    )
    player = new_x, new_y


def try_move(dx, dy):
    global score, restart
    new_x, new_y = player[0] + dx, player[1] + dy
    score += walk_cost

    if 0 <= new_x < grid_size_x and 0 <= new_y < grid_size_y and (new_x, new_y) not in walls:
        move_me(new_x, new_y)

    if (new_x, new_y) in specials:
        c, w = specials[(new_x, new_y)]
        score -= walk_cost
        score += w
        if score > 0:
            print("Success! score: ", score)
        else:
            print("Fail! score: ", score)
        restart = True
        return


def call_up():
    try_move(0, -1)


def call_down():
    try_move(0, 1)


def call_left():
    try_move(-1, 0)


def call_right():
    try_move(1, 0)


def restart_game(scores):
    global player, score, restart
    player = 0, 0
    score = 1
    restart = False
    move_me(*player)

    redraw_action_weights(scores or {})


def redraw_action_weights(scores, cache={}):
    for key, triangle in triangles.items():
        value = scores[key]
        if value == cache.get(key):
            continue
        cache[key] = value
        green = int(min((value + 1) * 128 + 16, 255))
        red = 255 - green + 16
        color = "#{:x}{:x}00".format(red, green)
        board.itemconfigure(triangle, fill=color)


render_grid()

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(
    player[0] * width + width * 2 / 10,
    player[1] * width + width * 2 / 10,
    player[0] * width + width * 8 / 10,
    player[1] * width + width * 8 / 10,
    fill="orange",
    width=1,
    tag="me"
)

board.grid(row=0, column=0)


def start_game():
    master.mainloop()
