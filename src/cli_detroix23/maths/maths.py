"""
CLI - maths
maths.py
Basic maths stuff.
"""

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
