"""
CLI - maths
maths.py
Basic maths stuff.
"""
import os

class Vector2D:
    x: int
    y: int
    
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x: int = x
        self.y: int = y

    def __repr__(self) -> str:
        return f"Vector2D(x: int = {self.x}, y: int = {self.y})"

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y} "

    def clone(self) -> 'Vector2D':
        return Vector2D(
            self.x,
            self.y
        )
    
    @staticmethod
    def terminal_size() -> 'Vector2D':
        size: tuple[int, int] = os.get_terminal_size()
        return Vector2D(
            size[0],
            size[1]
        )

    def __eq__(self, target: object) -> bool:
        if isinstance(target, Vector2D):
            return self.x == target.x and self.y == target.y
        else:
            return False