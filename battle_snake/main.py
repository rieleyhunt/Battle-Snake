# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

from utility import *
from matrix import MoveMatrix


# from move_checking import *
# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Tiernan, Ian, Saurabh, and Rieley", 
        "color": "#454ADE",  # TODO: Choose color
        "head": "do-sammy",  # TODO: Choose head
        "tail": "do-sammy",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: GameState) -> typing.Dict:

    # We've included code to prevent your Battlesnake from moving backwards
    me: Snake = game_state["you"]

    valid_move_matrix = MoveMatrix(game_state["board"]["width"], game_state["board"]["height"])

    for snek in game_state["board"]["snakes"]:

        for coord in snek["body"]:
            valid_move_matrix.set(coord["x"], coord["y"], False)

    # for hazard in game_state.board.hazards:
    #     valid_move_matrix[hazard.y][hazard.x] = False

    move_safety: MoveSafety = {
        "up": valid_move_matrix.get(me["head"]["x"], me["head"]["y"] + 1),
        "down": valid_move_matrix.get(me["head"]["x"], me["head"]["y"] - 1),
        "left": valid_move_matrix.get(me["head"]["x"] - 1, me["head"]["y"]),
        "right": valid_move_matrix.get(me["head"]["x"] + 1, me["head"]["y"]),
    }

    target_food = nearest_food(game_state["board"]["food"], me["head"])
    direction = decide_direction(me, valid_move_matrix, target_food)

    print(f"MOVE {game_state['turn']}: ", end="")
    print(f"{direction['move']}")
    return direction


def nearest_food(foods: list[Coordinate], head_pos: Coordinate) -> Coordinate:  # find closest food
    distances: list[tuple[int, Coordinate]] = [
        (((food_pos["x"] - head_pos["x"]) ** 2 + (food_pos["y"] - head_pos["y"]) ** 2), food_pos) for food_pos in foods
    ]

    return min(distances, key=lambda tup: tup[0])[1]  # get the coordinate that corresponds to the minimum distance
    

def decide_direction(me: Snake, move_matrix: MoveMatrix, food_pos: Coordinate) -> dict["move", str]:
    dx = food_pos["x"] - me["head"]["x"]
    dy = food_pos["y"] - me["head"]["y"]

    move: typing.Optional[dict["move": str]]

    if abs(dx) > abs(dy):     # prioritise the longer component to travel first
        # try to move on the x-axis
        move = try_move_x(dx, me, move_matrix)

        if move is None:
            move = try_move_y(dy, me, move_matrix)

        if move is None:
            move = try_move_random(me, move_matrix) # if we cannot move toward the food

    else:      # we need to try moving along the y axis first
        move = try_move_y(dy, me, move_matrix)
        
        if move is None:
            move = try_move_x(dx, me, move_matrix)
        
        if move is None:
            move = try_move_random(me, move_matrix) # if we cannot move toward the food

    return move


def try_move_x(dx: int, me: Snake, move_matrix: MoveMatrix) -> typing.Optional[typing.Dict["move", str]]:
    if dx > 0:  # if we have to move right
        if move_matrix.get(me["head"]["x"] + 1, me["head"]["y"]):  # if we can legally move right
            return {"move": "right"}
    else:       # if we have to move left
        if move_matrix.get(me["head"]["x"] - 1, me["head"]["y"]):  # if we can legally move left
            return {"move": "left"}


def try_move_y(dy: int, me: Snake, move_matrix: MoveMatrix) -> typing.Optional[typing.Dict["move", str]]:
    if dy > 0:  # if we have to move up
        if move_matrix.get(me["head"]["x"], me["head"]["y"] + 1):  # if we can legally move up
            return {"move": "up"}
    else:       # if we have to move down
        if move_matrix.get(me["head"]["x"], me["head"]["y"] - 1):  # if we can legally move down
            return {"move": "down"}


def try_move_random(me: Snake, move_matrix: MoveMatrix) -> dict["move", str]:
    directions: MoveSafety = {
        "up": move_matrix.get(me["head"]["x"], me["head"]["y"] + 1),
        "down": move_matrix.get(me["head"]["x"], me["head"]["y"] - 1),
        "left": move_matrix.get(me["head"]["x"] - 1, me["head"]["y"]),
        "right": move_matrix.get(me["head"]["x"] + 1, me["head"]["y"]),
    }

    valid_directions = []
    all_directions = []
    for direction, can_do in directions.items():
        all_directions.append(direction)
        if can_do:
            valid_directions.append(direction)
    
    if len(valid_directions) > 0:
        return {"move": random.choice(valid_directions)}
    else:
        return {"move": random.choice(all_directions)}  # just fuckin send it bud


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
 