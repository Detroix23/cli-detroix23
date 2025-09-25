"""
CLI - Shapes
base.py
Draw basic shapes. Uses the screen script.
"""
import maths.maths as maths
import animations.screen as screen


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

    def __init__(self, position: maths.Vector2D) -> None:
        """
        Initialize an instance of a shape.
        """
        self.position: maths.Vector2D = position
        self.id: int = 0

    def draw(self) -> list[list[str]]:
        """
        Return a 2D table of chars, to draw on the char table. 
        """
        raise DrawError("The `Shape` doesn't implement any draw content.")


class Rectangle(Shape):
    size: maths.Vector2D
    fill: str

    def __init__(
        self, 
        position: maths.Vector2D,
        size: maths.Vector2D,
        fill: str
    ) -> None:
        super().__init__(position)
        self.size: maths.Vector2D = size
        self.fill: str = fill
    
    def draw(self) -> list[list[str]]:
        return [[self.fill] * self.size.x] * self.size.y



# Exemples
class Exemple1(screen.Screen):
    def __init__(
        self, 
        void_char: str = ".", 
        frame_delay: float = 0.1, 
        global_style: str = "", 
        debug: bool = False, 
        deactivate_screen: bool = False
    ) -> None:
        super().__init__(void_char, frame_delay, global_style, debug, deactivate_screen)

        self.rect1 = Rectangle(maths.Vector2D(4, 5), maths.Vector2D(8, 4), '#')

    def drawer(self) -> None:
        self.write_table(self.rect1.draw(), self.rect1.position)

    def updater(self) -> None:
        pass

def run_exemple1() -> None:
    ex1 = Exemple1()

    ex1.run(Exemple1.updater, Exemple1.drawer)

if __name__ == "__main__":
    run_exemple1()


