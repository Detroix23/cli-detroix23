"""
CLI - Terminal
screen.py
Multi-line updating terminal display.
"""

import os
import time
from typing import Callable
from enum import Enum

import base.style as style

class Vector2D:
    x: int
    y: int
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x: int = x
        self.y: int = y

    def __repr__(self) -> str:
        return f"Vector2D(x: int = {self.x}, y: int = {self.y})"

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y} "

class ReadingWay(Enum):
    LEFT_RIGHT = 0
    RIGHT_LEFT = 1
    UP_DOWN = 2
    DOWN_UP = 3

class Screen:
    size: Vector2D
    updater: Callable[..., None] | None
    drawer: Callable[..., None] | None
    _frames: int
    char_table: list[list[str]]

    def __init__(
        self, 
        void_char: str = ".",
        frame_delay: float = 0.1
    ) -> None:
        self.size: Vector2D = Vector2D(*self.update_size())
        self.updater: Callable[..., None] | None = None
        self.drawer: Callable[..., None] | None = None
        self._frames: int = 0
        self.void_char: str = void_char
        self.char_table: list[list[str]] = self.blank_char_table()
        self.frame_delay: float = frame_delay

    def run(
        self,       
        updater: Callable[..., None], 
        drawer: Callable[..., None],
    ) -> None:
        """
        Screen main loop, using `updater` and `drawer` as functions.
        """
        self.updater = updater
        self.drawer = drawer
        self._frames: int = 0

        running: bool = True

        print("\033[H\033[2J", end="")
        try:
            while running:
                # Clear the whole screen.
                print("\033[H\033[2J", end="")
                print("\033[H\033[3J", end="")
                
                # Update.
                self.size: Vector2D = Vector2D(*self.update_size())

                # User functions.
                self.updater(self)
                self.drawer(self)

                # Char table
                self.print_char_table()
                self.char_table = self.blank_char_table()

                # Frames
                time.sleep(self.frame_delay)
                self._frames += 1

        except KeyboardInterrupt:
            print("\033[H\033[2J", end="")
            style.printc("(!) - Keyboard interrupt.", style.Color.YELLOW)


    def update_size(self) -> tuple[int, int]:
        size: tuple[int, ...] = tuple(os.get_terminal_size())
        return size[0], size[1]

    @property
    def frames(self) -> int:
        return self._frames

    def blank_char_table(self) -> list[list[str]]:
        """
        Return the default char table state.
        """
        return [[self.void_char for _ in range(self.size.x)] for _ in range(self.size.y - 1)]

    def write_char(self, char: str, position: Vector2D, styles: str) -> None:
        """
        Add a character (len == 1) and its position to the next printed table.
        (0, 0) is the upper left corner.
        """
        if len(char) > 1:
            raise ValueError(f"{style.Color.RED}(X) - Must be a char: {char}, ({len(char)}).{style.Style.END}")
        try:
            self.char_table[position.y][position.x] = styles + char + style.Style.END
        except:
            # style.printc(f"(!) - Character {char} ignored at {position}.", style.Color.YELLOW)
            pass

    def write(self, message: str, start: Vector2D, way: ReadingWay = ReadingWay.LEFT_RIGHT, styles: str = "") -> None:
        """
        Write whole words in the char table.
        Follow the reading `way`.
        """
        shift: Vector2D
        if way == ReadingWay.LEFT_RIGHT:
            shift = Vector2D(1, 0)
        elif way == ReadingWay.RIGHT_LEFT:
            shift = Vector2D(-1, 0)
        elif way == ReadingWay.DOWN_UP:
            shift = Vector2D(0, -1)
        elif way == ReadingWay.UP_DOWN:
            shift = Vector2D(0, 1)
        else:
            raise ValueError(f"{style.Color.RED}(X) - Must be a valid direction (0 - 3): {way}.{style.Style.END}")


        for index, letter in enumerate(message):
            self.write_char(
                letter,
                Vector2D(
                    start.x + index * shift.x,
                    start.y + index * shift.y
                ),
                styles
            )


    def print_char_table(self) -> None:
        """
        When all chars are written, print the table that covers the whole screen.
        """
        for records in self.char_table:
            for char in records:
                print(char, end="")
        print()




class Custom1(Screen):
        def __init__(self) -> None:
            super().__init__()
            self.hello: int = 0

        def updater(self) -> None:
            if str(self.frames)[0] == "0": 
                self.hello += 1 
            self.hello -= 1

        def drawer(self) -> None:
            

            print(self.size)
            print(self.frames)
            print(self.hello)

class Matrix(Screen):
        def __init__(self) -> None:
            super().__init__()
            self.hello: int = 0

        def updater(self) -> None:
            pass

        def drawer(self) -> None:
            self.write(f"frames: {self.frames}", Vector2D(0, 0))

def main_test() -> None:

    screen = Matrix()
    print(Matrix.updater, Matrix.drawer)
    screen.run(Matrix.updater, Matrix.drawer)

if __name__ == "__main__":
    main_test()
    