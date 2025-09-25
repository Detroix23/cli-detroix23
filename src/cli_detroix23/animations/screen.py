"""
CLI - Terminal
screen.py
Multi-line updating terminal display.
"""

import os
import sys
import time
from typing import Callable
from enum import Enum

import maths.maths as maths
import base.style as style



class ReadingWay(Enum):
    LEFT_RIGHT = 0
    RIGHT_LEFT = 1
    UP_DOWN = 2
    DOWN_UP = 3

class Screen:
    size: maths.Vector2D
    updater: Callable[..., None] | None
    drawer: Callable[..., None] | None
    _frames: int
    char_table: list[list[str]]

    def __init__(
        self, 
        void_char: str = ".",
        frame_delay: float = 0.1,
        global_style: str = "",
        debug: bool = False,
        deactivate_screen: bool = False
    ) -> None:
        self.size: maths.Vector2D = maths.Vector2D(*self.update_size())
        self.updater: Callable[..., None] | None = None
        self.drawer: Callable[..., None] | None = None
        self._frames: int = 0
        self.debug: bool = debug
        self.deactivate_screen: bool = deactivate_screen

        self.void_char: str = void_char
        self.frame_delay: float = frame_delay
        self.global_style: str = global_style

        self.char_table: list[list[str]] = self.blank_char_table()


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

        try:
            # Main loop
            while running:
                # Clear the whole screen.
                if not (self.deactivate_screen or self.debug):
                    # print("\033[H\033[2J", end="")
                    sys.stdout.write("\033[H\033[3J")
                    sys.stdout.flush()


                # Update.
                self.size: maths.Vector2D = maths.Vector2D(*self.update_size())

                # User functions.
                self.updater(self)
                self.drawer(self)

                # Char table
                if self.debug:
                    print(fr"{self.char_table}")
                if not (self.debug or self.deactivate_screen):
                    self.print_char_table()
                self.char_table = self.blank_char_table()
                sys.stdout.flush()
                

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
        """
        Get the value of frames. Semi-private proprety: read-only.
        """
        return self._frames

    def frames_reset(self) -> None:
        self._frames = 0

    def blank_char_table(self) -> list[list[str]]:
        """
        Return the default char table state.
        """
        return [
            [self.void_char for _ in range(self.size.x)] 
            for _ in range(self.size.y)
        ]

    def clear_char(self, position: maths.Vector2D) -> None:
        try:
            self.char_table[position.y][position.x] = ' '
        except IndexError:
            style.printc(f"(!) - Couldn't erase character at {position}: inexistant.", style.Color.YELLOW)

    def _write_char(self, char: str, position: maths.Vector2D, styles: str = "") -> None:
        """
        Add a character (len == 1) and its position to the next printed table.
        (0, 0) is the upper left corner.
        """
        raise_on_long_char: bool = False
        warn_on_outside: bool = self.debug
        allow_negative_index: bool = False

        if len(char) > 1 and raise_on_long_char:
            raise ValueError(f"{style.Color.RED}(X) - Must be a char: {char}, ({len(char)}).{style.Style.END}")
        if not char:
            # Don't do anything is the char is the empty string.
            # To erase, use `clear_char`.
            return
        if (position.x < 0 or position.y < 0) and not allow_negative_index:
            if warn_on_outside:
                style.printc(f"(!) - Character {char} ignored at negative position: {position}.", style.Color.YELLOW)
            return

        try:
            if styles:
                self.char_table[position.y][position.x] = styles + char + style.Style.END
            else:
                self.char_table[position.y][position.x] = char
        except IndexError:
            if warn_on_outside:
                style.printc(f"(!) - Character {char} ignored at {position}.", style.Color.YELLOW)

    def write(self, message: str | list[str], start: maths.Vector2D, way: ReadingWay = ReadingWay.LEFT_RIGHT, styles: str = "") -> int:
        """
        Write whole words in the char table.
        Follow the reading `way`.
        Returns the length of the written message.
        """
        if not message:
            pass
        elif len(message) == 1 and isinstance(message, str):
            self._write_char(message, start, styles)
        elif len(message) == 1 and isinstance(message, list):
            self._write_char(message[0], start, styles)
        else:
            shift: maths.Vector2D
            if way == ReadingWay.LEFT_RIGHT:
                shift = maths.Vector2D(1, 0)
            elif way == ReadingWay.RIGHT_LEFT:
                shift = maths.Vector2D(-1, 0)
            elif way == ReadingWay.DOWN_UP:
                shift = maths.Vector2D(0, -1)
            elif way == ReadingWay.UP_DOWN:
                shift = maths.Vector2D(0, 1)
            else:
                raise ValueError(f"{style.Color.RED}(X) - Must be a valid direction (0 - 3): {way}.{style.Style.END}")

            if isinstance(message, str):
                for index, letter in enumerate(message):
                    self._write_char(
                        letter,
                        maths.Vector2D(
                            start.x + index * shift.x,
                            start.y + index * shift.y
                        ),
                        styles
                    )
            else:
                # print(f"MESSAGE: {message}")
                for index, composition in enumerate(message):
                    # print(f"\nc: {composition}", end="")
                    self._write_char(
                        composition,
                        maths.Vector2D(
                            start.x + index * shift.x,
                            start.y + index * shift.y
                        ),
                        styles
                    )
        
        return len(message)

    def write_table(self, table: list[list[str]], position: maths.Vector2D, way: ReadingWay = ReadingWay.LEFT_RIGHT, styles: str = "") -> None:
        """
        Write a whole 2D table to the char table from the top-left corner, starting on position.
        """
        cursor_position: maths.Vector2D = position.clone()
        for row in table:
            self.write(row, cursor_position, way, styles)
            cursor_position.y -= 1
        


    def print_char_table(self) -> None:
        """
        When all chars are written, print the table that covers the whole screen.
        Printed in one time for the sake of smoothness.
        """
        table: str = ""
        self.char_table[-1].pop()
        for records in self.char_table:
            for char in records:
                table += self.global_style + char + style.END
            table += "\n"
        sys.stdout.write(table[:-5])

    def total_char_table_len(self) -> int:
        total: int = 0
        for record in self.char_table:
            total += len(record)

        return total


if __name__ == "__main__":
    print("See `animations/exemples.py`.")