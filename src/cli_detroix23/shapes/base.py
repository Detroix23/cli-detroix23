"""
CLI - Shapes
base.py
Draw basic shapes. Uses the screen script.
"""
import maths.maths as maths
import animations.screen as screen


table2D = list[list[str]]

class DrawError(Exception):
    """
    Raised when an error occurs when drawing a shape.
    """
    message: str

    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(message)

    def __repr__(self) -> str:
        return f"(X) - DrawError: {self.message}."
        
    def __str__(self) -> str:
        return f"(X) - DrawError: {self.message}."


class Shape:
    """
    Define the base of any shape.
    Has position, unique id. 
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

    def draw(self) -> table2D:
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

    @staticmethod
    def create_table(size: maths.Size, character: str = "") -> table2D:
        """
        Return a 2D table; by default, full of empty strings.
        """
        return [[character for _ in range(size.x)] for _ in range(size.y)]


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
    
    def draw(self) -> table2D:
        table: table2D = Shape.create_table(self.size, self.fill)

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
            raise ValueError(f"(X) - The border size must be 0 (filled) or more ({border_size}).")

        super().__init__(support, position, size, fill, show_center)
        self.border_size: int = border_size
    
    def draw(self) -> table2D:
        if self.border_size == 0:
            return [[self.fill] * self.size.x] * self.size.y
        else:
            table: table2D = list()
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

    def draw(self) -> table2D:
        size_x: int = self.size.x // 2
        size_y: int = self.size.y // 2
        table: table2D = Shape.create_table(maths.Size(self.size.x + 1, self.size.y + 1))
        
        for y in maths.both_range(size_y + 1):
            for x in maths.both_range(size_x + 1):
                if ((x * x) / (size_x * size_x)) + ((y * y) / (size_y * size_y)) <= 1:
                    table[y + size_y][x + size_x] = self.fill
        
        if self.show_center:
            table[size_y][size_x] = "0" 
        
        return table


# Exemples
class Exemple1(screen.Screen):
    def __init__(
        self, 
        void_char: str = "'", 
        frame_delay: float = 0.3, 
        global_style: str = "", 
        debug: bool = False, 
        deactivate_screen: bool = False
    ) -> None:
        super().__init__(void_char, frame_delay, global_style, debug, deactivate_screen)

        self.rect1 = Rectangle(self, maths.Vector2D(4, 5), maths.Size(8, 4), "#", True)
        self.hrect1 = RectangleHollow(self, maths.Vector2D(7, 8), maths.Size(9, 6), "@", 2, True)
        self.ell1 = Ellipse(self, maths.Vector2D(10, 10), maths.Size(8, 8), "$", True)

    def drawer(self) -> None:
        self.write_table(self.rect1.draw(), self.rect1.position)
        self.write_table(self.hrect1.draw(), self.hrect1.position)
        self.write_table(self.ell1.draw(), self.ell1.position)

    def updater(self) -> None:
        self.hrect1.shift(maths.Vector2D(0, 1))

def run_exemple1() -> None:
    ex1 = Exemple1()

    ex1.run(Exemple1.updater, Exemple1.drawer)

if __name__ == "__main__":
    run_exemple1()
