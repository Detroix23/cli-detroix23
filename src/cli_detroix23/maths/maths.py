"""
CLI - maths
maths.py
Basic maths stuff.
"""
import os
import math

import compatibility.types as types

table2D = types.table2D

class Size:
    """
    Simple int structure to store sizes.
    """
    x: int
    y: int

    def __init__(self, x: int = 0, y: int = 0) -> None:
        """
        Initialise with from a pair of x, y.
        """
        self.x: int = x
        self.y: int = y
    
    def area(self) -> int:
        return self.x * self.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    @staticmethod
    def terminal_size() -> 'Size':
        """
        Get the current terminal size as Size class.
        """
        size: tuple[int, int] = os.get_terminal_size()
        return Size(
            size[0],
            size[1]
        )

class Vector2D:
    """
    Float 2D maths vector.
    """
    x: float
    y: float
    
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x: float = x
        self.y: float = y

    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self) -> None:
        magnitude: float = self.magnitude()
        self.x /= magnitude
        self.y /= magnitude

    def __repr__(self) -> str:
        return f"Vector2D(x: int = {self.x}, y: int = {self.y})"

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y} "

    def clone(self) -> 'Vector2D':
        return Vector2D(
            self.x,
            self.y
        )

    def __eq__(self, target: object) -> bool:
        if isinstance(target, Vector2D):
            return self.x == target.x and self.y == target.y
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def both_range(number: int) -> list[int]:
    """
    Return a list of all naturals from -number to number
    """
    return [i - number for i in range(2 * number)]

def middle_range(number: int) -> list[int]:
    """
    Return a list of all naturals from -number / 2 to number / 2 
    """
    return [i - number // 2 for i in range(number)]


def create_table(size: Size, character: str = "") -> table2D:
    """
    Return a 2D table; by default, full of empty strings.
    """
    return [[character for _ in range(size.x)] for _ in range(size.y)]

def create_table_like(model: table2D, character: str = "") -> table2D:
    """
    Return a 2D table that can contain the model; by default, full of empty strings.
    """
    max_y: int = len(model)
    max_x: int = 0
    for row in model:
        if len(row) > max_x:
            max_x = len(row)

    return [[character for _ in range(max_x)] for _ in range(max_y)]