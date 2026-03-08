from cli_detroix23.compatibility import types as types
from cli_detroix23.animations import screen as screen
from cli_detroix23.maths import maths as maths, transformations as transformations
from cli_detroix23.shapes import base as base

class Sprite(base.Shape):
    sprite: types.Table2D

    def __init__(
        self, 
        support: screen.Screen, 
        position: maths.Vector2D, 
        size: maths.Size, 
        sprite: types.Table2D, 
        show_center: bool = False
    ) -> None: ...
    def draw(self) -> types.Table2D: ...
    def rotate(self, angle: int) -> None: ...


class Examples:
    Human: types.Table2D
    Block1: types.Table2D


def create_sprite(drawing: str) -> types.Table2D: ...
