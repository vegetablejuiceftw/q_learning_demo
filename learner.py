import time
import threading

import world

__author__ = 'philippe'


def do_action(action):
    position = world.player
    delta_score = -world.score
    if action == world.actions[0]:
        world.try_move(0, -1)
    elif action == world.actions[1]:
        world.try_move(0, 1)
    elif action == world.actions[2]:
        world.try_move(-1, 0)
    elif action == world.actions[3]:
        world.try_move(1, 0)
    else:
        return
    new_position = world.player
    delta_score += world.score
    return position, action, delta_score, new_position


def max_q(position):
    x, y = position
    best_value = None
    best_action = None
    for action in world.actions:
        value = Q[(x, y, action)]
        if best_value is None or value > best_value:
            best_value, best_action = value, action
    return best_action, best_value


def inc_q(position, action, alpha, inc):
    key = position[0], position[1], action
    Q[key] = Q[key] * (1 - alpha) + alpha * inc


def run():
    time.sleep(1)
    ttl = 0
    counter = -1
    start = time.time()
    alpha = 0.73
    while True:
        counter += 1
        # Pick the right action
        position = world.player
        max_act, max_val = max_q(position)
        position, action, delta_score, new_position = do_action(max_act)

        # Update Q
        max_act, max_val = max_q(new_position)
        discount = 0.3
        inc_q(position, action, alpha, delta_score + discount * max_val)

        # Check if the game has restarted or packet has timed out
        ttl += 1.0
        if world.restart:
            world.restart_game(Q)
            # print("{}".format(counter / (time.time()-start)))
            print("{}".format(counter), ttl)
            ttl = 1.0

        # Update the learning rate
        alpha = pow(ttl, -0.1)

        # logic_tics_per_second = 240
        # time.sleep(1 / logic_tics_per_second)


def initial_q_table():
    Q = {}
    for i in range(world.grid_size_x):
        for j in range(world.grid_size_y):
            for action in world.actions:
                Q[(i, j, action)] = 0.1

    for position, data in world.specials.items():
        i, j = position
        c, w = data
        for action in world.actions:
            Q[(i, j, action)] = w
    return Q

Q = initial_q_table()

t = threading.Thread(target=run)
t.daemon = True
t.start()
world.start_game()
