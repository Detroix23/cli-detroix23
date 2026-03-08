"""
# CLI - Shapes.
src/cli_detroix23/shapes/sprites.py
"""

from cli_detroix23.compatibility import types
from cli_detroix23.maths import maths, transformations
from cli_detroix23.animations import screen
from cli_detroix23.shapes import base

class Sprite(base.Shape):
    sprite: types.Table2D

    def __init__(
        self, 
        support: screen.Screen, 
        position: maths.Vector2D, 
        size: maths.Size,
        sprite: types.Table2D,
        show_center: bool = False
    ) -> None:
        super().__init__(support, position, size, ".", show_center)
        self.sprite = sprite
    
    def draw(self) -> types.Table2D:
        return self.sprite
    

    def rotate(self, angle: int) -> None:
        """
        Implement rotation on self sprite.
        """
        self.sprite = transformations.simple_rotation(self.sprite, angle)


def create_sprite(drawing: str) -> types.Table2D:
    """
    Create a sprite from a body of text, and rotate it 180 degrees.
    """
    table: types.Table2D = base.str_to_table(drawing)
    base.squarify_table(table)
    table = transformations.simple_rotation(table, 180)

    return table


class Examples:
    Human: types.Table2D = create_sprite(r"""
  @
/###\
 | |
""")
    Block1: types.Table2D = create_sprite(r"""
@#
$O
""")
