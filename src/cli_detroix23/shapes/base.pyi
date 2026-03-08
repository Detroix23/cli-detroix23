from cli_detroix23.compatibility import (
    defaults as defaults,
    types as types,
)
from cli_detroix23.animations import screen as screen
from cli_detroix23.maths import maths as maths

class DrawError(Exception):
    message: str

    def __init__(self, message: str) -> None: ...


class Shape:
    position: maths.Vector2D
    id: int
    support: screen.Screen
    size: maths.Size
    fill: str
    show_center: bool
    
    def __init__(
        self, 
        support: screen.Screen, 
        position: maths.Vector2D, 
        size: maths.Size, 
        fill: str, 
        show_center: bool = False
    ) -> None: ...
    def draw(self) -> types.Table2D: ...
    def shift(self, step: maths.Vector2D, loop: bool = True) -> None: ...
    def loop_position(self) -> None: ...


class Rectangle(Shape):
    fill: str

    def __init__(
        self, 
        support: screen.Screen, 
        position: maths.Vector2D,
        size: maths.Size, 
        fill: str, 
        show_center: bool = False
    ) -> None: ...
    def draw(self) -> types.Table2D: ...


class RectangleHollow(Shape):
    fill: str
    border_size: int

    def __init__(
        self, 
        support: screen.Screen, 
        position: maths.Vector2D, 
        size: maths.Size, 
        fill: str, 
        border_size: int, 
        show_center: bool = False
    ) -> None: ...
    def draw(self) -> types.Table2D: ...


class Ellipse(Shape):
    def __init__(
        self, 
        support: screen.Screen, 
        position: maths.Vector2D, 
        size: maths.Size, 
        fill: str, 
        show_center: bool = False
    ) -> None: ...
    def draw(self) -> types.Table2D: ...

def str_to_table(text: str) -> types.Table2D: ...
def squarify_table(table: types.Table2D, fill: str = '') -> None: ...
