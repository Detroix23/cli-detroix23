"""
# CLI - Shapes.
src/cli_detroix23/shapes/base.py

Draw basic shapes. Uses the screen script.
"""

from cli_detroix23.compatibility import defaults, types
from cli_detroix23.maths import maths
from cli_detroix23.animations import screen

class DrawError(Exception):
    """
    Raised when an error occurs when drawing a shape.
    """
    message: str

    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(message)

    def __repr__(self) -> str:
        return f"{defaults.LOG_ERROR}DrawError: {self.message}."
        
    def __str__(self) -> str:
        return f"{defaults.LOG_ERROR}DrawError: {self.message}."


class Shape:
    """
    Define the base of any shape.
    Has:
    - `position`: `Vector2D`;
    - `id`: `int`, must be unique; 
    """
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
    ) -> None:
        """
        Initialize an instance of a shape.
        """
        self.position = position
        self.id = 0
        self.support = support
        self.size = size
        self.fill = fill
        self.show_center = show_center

    def draw(self) -> types.Table2D:
        """
        Return a 2D table of chars, to draw on the char table. 
        """
        raise DrawError("The `Shape` doesn't implement any draw content.")

    def shift(self, step: maths.Vector2D, loop: bool = True) -> None:
        """
        Shift the position.
        """
        self.position.x += step.x
        self.position.y += step.y
        if loop:
            self.loop_position()

    def loop_position(self) -> None:
        self.position.x %= self.support.size.x + self.size.x
        self.position.y %= self.support.size.y + self.size.y



class Rectangle(Shape):
    """
    A rectangle.
    """
    fill: str

    def __init__(
        self, 
        support: screen.Screen,
        position: maths.Vector2D,
        size: maths.Size,
        fill: str,
        show_center: bool = False
    ) -> None:
        super().__init__(support, position, size, fill, show_center)
    
    def draw(self) -> types.Table2D:
        table: types.Table2D = maths.create_table(self.size, self.fill)

        if self.show_center:
            table[self.size.y // 2][self.size.x // 2] = "0"

        return table


class RectangleHollow(Shape):
    """
    A hollow rectangle with a border size.
    """
    fill: str
    border_size: int

    def __init__(
        self,
        support: screen.Screen,
        position: maths.Vector2D,
        size: maths.Size,
        fill: str,
        border_size: int,
        show_center: bool = False,
    ) -> None:
        if border_size < 0:
            raise ValueError(f"The border size must be 0 (filled) or more ({border_size}).")

        super().__init__(support, position, size, fill, show_center)
        self.border_size: int = border_size
    
    def draw(self) -> types.Table2D:
        if self.border_size == 0:
            return [[self.fill] * self.size.x] * self.size.y
        else:
            table: types.Table2D = list()
            for y in range(self.size.y):
                if self.border_size <= y < self.size.y - self.border_size:
                    table.append(
                        [self.fill] * self.border_size + [''] * (self.size.x - 2 * self.border_size) + [self.fill] * self.border_size
                    )
                else:
                    table.append([self.fill] * self.size.x)
            
            if self.show_center:
                table[self.size.y // 2][self.size.x // 2] = "0"

            return table
                    

class Ellipse(Shape):
    """
    An ellipse fitting in size.
    Find the points solving x ** 2 / size.x ** 2 + y ** 2 / size.y ** 2 == 1
    """
    def __init__(
        self, 
        support: screen.Screen, 
        position: maths.Vector2D, 
        size: maths.Size,
        fill: str,
        show_center: bool = False,
    ) -> None:
        super().__init__(support, position, size, fill, show_center)

    def draw(self) -> types.Table2D:
        size_x: int = self.size.x // 2
        size_y: int = self.size.y // 2
        table: types.Table2D = maths.create_table(maths.Size(self.size.x + 1, self.size.y + 1))
        
        for y in maths.both_range(size_y + 1):
            for x in maths.both_range(size_x + 1):
                if ((x * x) / (size_x * size_x)) + ((y * y) / (size_y * size_y)) <= 1:
                    table[y + size_y][x + size_x] = self.fill
        
        if self.show_center:
            table[size_y][size_x] = "0" 
        
        return table


def str_to_table(text: str) -> types.Table2D:
    """
    Transform a string, using the line break, to a 2D table.
    """
    line_breaks: set[str] = {"\n", "\r"}
    blank_chars: set[str] = {" "}

    cursor: int = 0
    table: types.Table2D = list()
    line: list[str] = list()
    while cursor < len(text):
        # Line break
        if cursor < len(text) and text[cursor] in line_breaks:        
            if line:
                table.append(line)
            line = list()
        elif text[cursor] in blank_chars:
            line.append('') 
        else:
            line.append(text[cursor])

        cursor += 1

    if line:
        table.append(line)

    return table


def squarify_table(table: types.Table2D, fill: str = "") -> None:
    """
    Ensure that all sub-list, records are of the same length. \n
    Returns None but modify by reference the table.
    """
    # Find maximum.
    width: int = 0
    for row in table:
        if len(row) > width:
            width = len(row)
    
    # Modify by reference the row.
    for row in table:
        for _ in range(width - len(row)):
            row.append(fill)

    return

if __name__ == "__main__":
    print("See `examples.py`.")
