"""
CLI - Shapes
exemples.py
"""
import maths.maths as maths
import animations.screen as screen
import shapes.base as base
import shapes.sprites as sprites

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

        self.rect1 = base.Rectangle(self, maths.Vector2D(4, 5), maths.Size(8, 4), "#", True)
        self.hrect1 = base.RectangleHollow(self, maths.Vector2D(7, 8), maths.Size(9, 6), "@", 2, True)
        self.ell1 = base.Ellipse(self, maths.Vector2D(10, 10), maths.Size(8, 8), "$", True)
        self.sprt1 = sprites.Sprite(self, maths.Vector2D(20, 20), maths.Size(10, 10), sprites.Exemples.Human)
        self.sprt1.rotate(90)

    def drawer(self) -> None:
        self.write_table(self.rect1.draw(), self.rect1.position)
        self.write_table(self.hrect1.draw(), self.hrect1.position)
        self.write_table(self.ell1.draw(), self.ell1.position)
        self.write_table(self.sprt1.draw(), self.sprt1.position)

    def updater(self) -> None:
        self.hrect1.shift(maths.Vector2D(0, 1))

def run_exemple1() -> None:
    base.str_to_table("""
Hello world!
Another line...
For the sprite!
""")

    ex1 = Exemple1()

    ex1.run(Exemple1.updater, Exemple1.drawer)

if __name__ == "__main__":
    run_exemple1()