"""
# CLI - Shapes.
src/cli_detroix23/shapes/examples.py
"""
from cli_detroix23.maths import maths
from cli_detroix23.animations import screen
from cli_detroix23.shapes import base, sprites

# Examples.
class Example1(screen.Screen):
    def __init__(
        self, 
        void_char: str = "'", 
        frame_delay: float = 1, 
        global_style: str = "", 
        debug: bool = False, 
        deactivate_screen: bool = False
    ) -> None:
        super().__init__(
            void_char, 
            frame_delay, 
            global_style, 
            debug,
            deactivate_screen,
            read_keys=True
        )

        self.rect1 = base.Rectangle(self, maths.Vector2D(4, 5), maths.Size(8, 4), "#", True)
        self.rect_hollow1 = base.RectangleHollow(self, maths.Vector2D(7, 8), maths.Size(9, 6), "@", 2, True)
        self.ell1 = base.Ellipse(self, maths.Vector2D(10, 10), maths.Size(8, 8), "$", True)
        self.sprite1 = sprites.Sprite(self, maths.Vector2D(20, 20), maths.Size(10, 10), sprites.Examples.Human)

    def drawer(self) -> None:
        self.write_table(self.rect1.draw(), self.rect1.position)
        self.write_table(self.rect_hollow1.draw(), self.rect_hollow1.position)
        self.write_table(self.ell1.draw(), self.ell1.position)
        self.write_table(self.sprite1.draw(), self.sprite1.position)

        if self.pressed_key is not None:
            self.write(f"Key={self.pressed_key.get()}", maths.Vector2D(self.size.x // 2, self.size.y // 2))

    def updater(self) -> None:
        self.rect_hollow1.shift(maths.Vector2D(0, 1))
        if self.frames % 2 == 0:
           self.sprite1.rotate(90)

        # Keys. Now native to `Screen`.
        # self.key = keys.get_key()


def run_example1() -> None:
    base.str_to_table("""
Hello world!
Another line...
For the sprite!
""")

    ex1 = Example1(
        frame_delay=1,
    )

    ex1.run(Example1.updater, Example1.drawer)

if __name__ == "__main__":
    run_example1()
