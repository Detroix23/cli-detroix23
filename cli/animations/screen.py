"""
CLI - Terminal
screen.py
Multi-line updating terminal display.
"""

import os
import time
import random
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
        frame_delay: float = 0.1,
        global_style: str = "",
        debug: bool = False,
        deactivate_screen: bool = False
    ) -> None:
        self.size: Vector2D = Vector2D(*self.update_size())
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
                    print("", end="\033[H\033[3J")
                
                # Update.
                self.size: Vector2D = Vector2D(*self.update_size())

                # User functions.
                self.updater(self)
                self.drawer(self)

                # Char table
                if self.debug:
                    print(fr"{self.char_table}")
                if not (self.debug or self.deactivate_screen):
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
        return [
            [self.void_char for _ in range(self.size.x)] 
            for _ in range(self.size.y)
        ]

    def _write_char(self, char: str, position: Vector2D, styles: str = "") -> None:
        """
        Add a character (len == 1) and its position to the next printed table.
        (0, 0) is the upper left corner.
        """
        raise_on_long_char: bool = False
        warn_on_outside: bool = self.debug

        if len(char) > 1 and raise_on_long_char:
            raise ValueError(f"{style.Color.RED}(X) - Must be a char: {char}, ({len(char)}).{style.Style.END}")
        try:
            if styles:
                self.char_table[position.y][position.x] = styles + char + style.Style.END
            else:
                self.char_table[position.y][position.x] = char

        except:
            if warn_on_outside:
                style.printc(f"(!) - Character {char} ignored at {position}.", style.Color.YELLOW)

    def write(self, message: str | list[str], start: Vector2D, way: ReadingWay = ReadingWay.LEFT_RIGHT, styles: str = "") -> int:
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

            if isinstance(message, str):
                for index, letter in enumerate(message):
                    self._write_char(
                        letter,
                        Vector2D(
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
                        Vector2D(
                            start.x + index * shift.x,
                            start.y + index * shift.y
                        ),
                        styles
                    )
        
        return len(message)

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
        print(table[:-5], end="")

    def total_char_table_len(self) -> int:
        total: int = 0
        for record in self.char_table:
            total += len(record)

        return total


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


class Dropplet:
    char: str
    position: Vector2D
    last_chars: list[str]

    def __init__(self, screen: 'Matrix') -> None:
        self.screen: 'Matrix' = screen
        self.char: str = self._random_char(*self.screen.character_random_range)
        self.position: Vector2D = self._random_position(self.screen)
        self.last_chars: list[str] = []

    def _random_char(self, random_min: int, random_max: int) -> str:
        r: int = 0
        blacklist: list[int] = [0, 24, 47, 97, 127, 128, 129, 130, 131, 132, 133, 141, 143, 144, 149, 151, 157, 160, 168, 173, 175, 180, 184]
        r = random.randint(random_min, random_max)
        if r in blacklist:
            r = 42
        return chr(r)

    def _random_position(self, screen: Screen) -> Vector2D:
        return Vector2D(random.randint(0, screen.size.x), 0)

    def update(self) -> None:
        """
        Update the dropplet. Apply gravity.
        """
        self.last_chars.insert(0, self.char)
        if len(self.last_chars) > random.randint(5, 10):
            self.last_chars.pop()

        self.position.y += 1
        self.char = self._random_char(*self.screen.character_random_range)

    def full_tail(self) -> list[str]:
        """
        Return the string list of all character (current and tail's) formated.
        """
        tail: list[str] = [f"{style.Text.BOLD}{self.char}{style.END}"]
        for index, char in enumerate(self.last_chars):
            if index < len(self.last_chars) // 2:
                tail.append(f"{style.Color.LIGHT_GREEN}{char}{style.END}")
            else:
                tail.append(f"{style.Color.GREEN}{char}{style.END}")

        return tail

class Matrix(Screen):
        digital_rain: list[Dropplet]

        def __init__(
            self,
            frame_delay: float,
            character_random_range: tuple[int, int] = (40, 127),
            infos: bool = False
        ) -> None:
            super().__init__(
                frame_delay=frame_delay,
                void_char=" ",
                global_style=style.Back.BLACK,
                debug=False,
                deactivate_screen=False
            )
            self.digital_rain: list[Dropplet] = list()
            self.character_random_range: tuple[int, int] = character_random_range
            self.infos: bool = infos
        
        def updater(self) -> None:
            # New dropplet
            for _ in range(self.size.x // 50 + 1):
                self.digital_rain.append(Dropplet(self))

            # Update each existing dropplet
            new_rain: list[Dropplet] = list()
            for dropplet in self.digital_rain:
                dropplet.update()
                if dropplet.position.y - len(dropplet.last_chars) <= self.size.y:
                    new_rain.append(dropplet)
            
            self.digital_rain = new_rain


        def drawer(self) -> None:
            cursor: int = 1
            # Draw each existing dropplets.
            for dropplet in self.digital_rain:
                self.write(dropplet.full_tail(), dropplet.position, ReadingWay.DOWN_UP)

            # Infos.
            if self.infos:
                cursor += 1 + self.write(f"frames: {self.frames}", Vector2D(cursor, 0), ReadingWay.LEFT_RIGHT)
                cursor += 1 + self.write(f"table: {self.total_char_table_len()}", Vector2D(cursor, 0), ReadingWay.LEFT_RIGHT)
                cursor += 1 + self.write(f"x: {self.size.x}", Vector2D(cursor, 0), ReadingWay.LEFT_RIGHT)
                cursor += 1 + self.write(f"y: {self.size.y}", Vector2D(cursor, 0), ReadingWay.LEFT_RIGHT)
                cursor += 1 + self.write(f"n: {len(self.digital_rain)}", Vector2D(cursor, 0), ReadingWay.LEFT_RIGHT)




def main_test() -> None:
	# (48, 49) binary.
	# (32, 132) general.
    screen = Matrix(
        frame_delay=0.08,
        character_random_range=(32, 132),
        infos=True
    )
    screen.run(Matrix.updater, Matrix.drawer)

if __name__ == "__main__":
    main_test()
    
