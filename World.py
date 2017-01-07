from tkinter import Tk, Canvas

__author__ = 'philippe'

master = Tk()

triangle_size = 0.1
cell_score_min = -0.2
cell_score_max = 0.2
width = 50
x, y = 5, 5
actions = "up", "down", "left", "right"

board = Canvas(master, width=x * width, height=y * width)
player = 0, y - 1
score = 1
restart = False
walk_reward = -0.04

walls = (1, 1), (1, 2), (2, 1), (2, 2)
specials = (4, 1, "red", -1), (4, 0, "green", 1)
cell_scores = {}


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
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i * width, j * width, (i + 1) * width, (j + 1) * width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i, j)] = temp
    for i, j, c, w in specials:
        board.create_rectangle(i * width, j * width, (i + 1) * width, (j + 1) * width, fill=c, width=1)
    for i, j in walls:
        board.create_rectangle(i * width, j * width, (i + 1) * width, (j + 1) * width, fill="black", width=1)


render_grid()


def set_cell_score(state, action, val):
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255 - green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def try_move(dx, dy):
    global score, restart, player
    if restart:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if 0 <= new_x < x and 0 <= new_y < y and (new_x, new_y) not in walls:
        board.coords(
            me,
            new_x * width + width * 2 / 10,
            new_y * width + width * 2 / 10,
            new_x * width + width * 8 / 10,
            new_y * width + width * 8 / 10
        )
        player = new_x, new_y
    for i, j, c, w in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
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


def restart_game():
    global player, score, restart
    player = 0, y - 1
    score = 1
    restart = False
    board.coords(
        me,
        player[0] * width + width * 2 / 10,
        player[1] * width + width * 2 / 10,
        player[0] * width + width * 8 / 10,
        player[1] * width + width * 8 / 10
    )


def has_restarted():
    return restart


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
