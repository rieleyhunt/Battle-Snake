from typing import TypedDict


class Coordinate(TypedDict):
    x: int
    y: int


class MoveSafety(TypedDict):
    left: bool
    right: bool
    up: bool
    down: bool


class Snake(TypedDict):
    id: str
    name: str
    health: int
    body: list[Coordinate]
    latency: str
    head: Coordinate
    length: int
    should: str
    squad: str
    customizations: dict[str]


class Board(TypedDict):
    height: int
    width: int
    food: list[Coordinate]
    hazards: list[Coordinate]
    snakes: list[Snake]


class GameDetails(TypedDict):
    id: str
    ruleset: dict[str]
    map: str
    timeout: int
    source: str


class GameState(TypedDict):
    game: GameDetails
    turn: int
    board: Board
    you: Snake
