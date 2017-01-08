from tkinter import Tk, Canvas
from random import randint, seed

__author__ = 'philippe'

seed("Cupcakes")

master = Tk()

triangle_size = 0.1
width = 25
size = 19
grid_size_x, grid_size_y = size, size
actions = "up", "down", "left", "right"

board = Canvas(master, width=grid_size_x * width, height=grid_size_y * width)
player = 0, 0
score = 1
restart = False
walk_cost = -0.04
triangles = {}

walls = set()

specials = {}
for _ in range(grid_size_x * grid_size_y // 5):
    specials[(randint(0, grid_size_x - 1), randint(0, grid_size_y - 1))] = ["green", 1, None, None]
specials = {key: value for key, value in specials.items() if key not in walls}


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
        color = data[0]
        specials[position][3] = board.create_rectangle(
            i * width, j * width,
            (i + 1) * width,
            (j + 1) * width,
            fill=color,
            width=1
        )

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


def try_move(dx, dy, game_counter):
    global score, restart
    score += walk_cost
    new_x, new_y = player[0] + dx, player[1] + dy
    key = new_x, new_y

    if key in specials:
        color, value, reset, rect = specials[key]
        if not reset or key not in walls or reset < game_counter:
            score += value - walk_cost
            specials[key][2] = game_counter + randint(500, 1000)

            color = "red"
            specials[key][0] = color
            board.itemconfigure(rect, fill=color)

            walls.add(key)
            restart = True

    if 0 <= new_x < grid_size_x and 0 <= new_y < grid_size_y and key not in walls:
        move_me(new_x, new_y)


def update_specials(game_counter):
    for key, data in specials.items():
        color, value, reset, rect = data

        if reset and reset < game_counter and key in walls:
            walls.discard(key)
            color = "green"
            specials[key][0] = color
            board.itemconfigure(rect, fill=color)


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
