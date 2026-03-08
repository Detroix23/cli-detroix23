
from cli_detroix23.animations import screen as screen
from cli_detroix23.maths import maths as maths
from cli_detroix23.shapes import base as base, sprites as sprites

class Example1(screen.Screen):
    rect1: base.Rectangle
    rect_hollow1: base.RectangleHollow
    ell1: base.Ellipse
    sprite1: sprites.Sprite
    
    def __init__(
        self, 
        void_char: str = "'", 
        frame_delay: float = 1, 
        global_style: str = '', 
        debug: bool = False,
        deactivate_screen: bool = False
    ) -> None: ...
    def drawer(self) -> None: ...
    def updater(self) -> None: ...

def run_example1() -> None: ...
