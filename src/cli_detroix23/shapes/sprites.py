"""
CLI - Shapes
sprites.py
"""
import maths.maths as maths
import maths.transformations as transformations
import animations.screen as screen
import shapes.base as base

class Sprite(base.Shape):
    sprite: maths.table2D

    def __init__(
        self, 
        support: screen.Screen, 
        position: maths.Vector2D, 
        size: maths.Size,
        sprite: maths.table2D,
        show_center: bool = False
    ) -> None:
        super().__init__(support, position, size, ".", show_center)
        self.sprite = sprite
    
    def draw(self) -> maths.table2D:
        return self.sprite
    

    def rotate(self, angle: int) -> None:
        """
        Implement rotation on self sprite.
        """
        self.sprite = transformations.rotation(self.sprite, angle)


def create_sprite(drawing: str) -> maths.table2D:
    """
    Create a sprite from a body of text, and rotate it 180 degrees.
    """
    table: maths.table2D = base.str_to_table(drawing)
    table = transformations.rotation(table, 180)

    return table


class Exemples:
    Human: maths.table2D = create_sprite(r"""
  @
/###\
 | |
""")
