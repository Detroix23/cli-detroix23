"""
# CLI.
src/cli_detroix23/animations/screen.py

Multi-line updating terminal display.
"""

import os
import sys
import time
import threading
from typing import Callable, Union, Optional, Final
from enum import Enum

from cli_detroix23.compatibility import defaults, debug
from cli_detroix23.maths import maths
from cli_detroix23.base import style, controls
from cli_detroix23.inputs import keys, fetch


class ReadingWay(Enum):
    LEFT_RIGHT = 0
    RIGHT_LEFT = 1
    UP_DOWN = 2
    DOWN_UP = 3


class Screen:
    """
    # Define a whole CLI application.
    See `./animations/examples.py` for example applications.  
    Main method: `run`, taking an `updater` and a `drawer` function.  
    """
    running: bool
    size: maths.Size
    _updater: Callable[[], None]
    """ Raw higher-level updater function. """
    _drawer: Callable[[], None]
    """ Raw higher-level drawer function. """
    _frames: int
    debug: bool
    deactivate_screen: bool
    void_char: str
    frame_delay: float
    global_style: str
    char_table: list[list[str]]
    previous_char_table: list[list[str]]
    read_keys: bool
    _key_information: keys.Info
    activate_threads: bool
    threads: dict[str, threading.Thread]

    def __init__(
        self, 
        void_char: str = ".",
        frame_delay: float = 0.1,
        global_style: str = "",
        debug: bool = False,
        deactivate_screen: bool = False,
        read_keys: bool = False,
        activate_threads: bool = False,
    ) -> None:
        self.running = False
        self.size = maths.Size(*self.update_size())
        self._updater = defaults.NULL_FUNCTION
        self._drawer = defaults.NULL_FUNCTION
        self._frames = 0
        self.debug = debug
        self.deactivate_screen = deactivate_screen
        self.void_char: str = void_char
        self.frame_delay: float = frame_delay
        self.global_style: str = global_style
        self.char_table = self.blank_char_table()
        self.previous_char_table = self.blank_char_table()
        self.read_keys = read_keys
        self._key_information = keys.Info()
        self.activate_threads = activate_threads
        self.threads = dict()

    def start_threads(self) -> int:
        """
        Create and start `keys`, `draw` threads.  
        Returns the number of threads created.

        W.I.P: Extreme lag caused by superposition of reading and writing `stdout`.
        """
        ENABLE: Final[dict[str, bool]] = {
            "keys": self.read_keys,
            "loop": True
        }

        # Threads.
        if ENABLE["keys"]:
            debug.debug_print("Created thread: `keys`.")
            self.threads["keys"] = threading.Thread(
                target=fetch.fetch_target,
                args=(self._key_information,),
            )
            
        if ENABLE["loop"]:
            self.threads["loop"] = threading.Thread(
                target=self._game_loop,
            )
            debug.debug_print("Created thread: `loop`.")

        for name, thread in self.threads.items():
            debug.debug_print(f"Started thread: {name}")
            thread.start()

        return len(self.threads)

    def join_threads(self) -> int:
        """
        Joins all running threads.  

        Return thread count.
        """
        for name, thread in self.threads.items():
            debug.debug_print(f"Joining thread: {name}")
            thread.join()

        return len(self.threads)

    def _draw(self) -> None:
        """
        **Local** draw function for 1 frame, that wraps the `drawer` method.
        """
        # Clear the whole screen.
        if not self.deactivate_screen and not self.debug:
            controls.home()
            # Deactivated because causes the flickering effect.
            #controls.clear_to_bottom()

        debug.debug_print(f"Screen._draw - User draw.")
        self._drawer()

        # Char table
        debug.debug_print(f"Screen._draw - Char table.")
        if self.debug:
            print(f"{repr(self.char_table)}")
        
        if not self.debug and not self.deactivate_screen:
            self.print_char_table()
        
        self.previous_char_table = self.char_table
        self.char_table = self.blank_char_table()
        
        debug.debug_print(f"Screen._draw - Size: {self.size}")
        sys.stdout.flush()
            
        return

    def _update(self) -> None:
        """
        **Local** update function for 1 frame, that wraps the `updater` method.
        """
        # Update.
        self.size = maths.Size(*self.update_size())

        # User updater function.
        self._updater()

        return

    def _game_loop(self) -> None:
        """
        Main game loop, running on thread, on a given FPS.
        """
        while self.running:
            self._update()
            self._draw()

            # Frames
            time.sleep(self.frame_delay)
            self._frames += 1

            if not self.activate_threads and self._key_information.current == keys.Keys.INTERRUPT:
                raise KeyboardInterrupt(f"KeyboardInterrupt. Felt from `Screen.run`.")

        return

    def run(
        self,       
        updater: Callable[[], None], 
        drawer: Callable[[], None],
    ) -> None:
        """
        Screen main loop, using `updater` and `drawer` as functions.
        """
        self._updater = updater
        self._drawer = drawer
        self._frames: int = 0
        self.running = True
        self._key_information.running = True

        if self.activate_threads:
            self.start_threads()

        else:
            try:
                debug.debug_print("Started main loop.")
                self._game_loop()
                
            except KeyboardInterrupt:
                self.running = False
                self._key_information.running = False

                sys.stdout.write("\033[H\033[2J")
                style.printc(f"{defaults.LOG_INFO}Keyboard interrupt. Felt from `Screen.run`.", style.Color.YELLOW)
                sys.stdout.flush()

            finally:
                self.running = False
                self._key_information.running = False

                self.join_threads()

                if os.name == "posix":
                    from cli_detroix23.compatibility import unix
                    
                    debug.debug_print("Screen.run - End: reset CL settings.")
                    unix.set_to_default()

                sys.stdout.flush()

    def update_size(self) -> tuple[int, int]:
        size: tuple[int, int] = os.get_terminal_size()
        return (size[0], size[1])

    @property
    def frames(self) -> int:
        """
        Get the value of `frames`. Semi-private property: read-only.
        """
        return self._frames

    @property
    def pressed_key(self) -> Optional[keys.Key]:
        """
        Get the value of `_current_key`. Read-only.
        """
        return self._key_information.current

    def frames_reset(self) -> None:
        """
        Reset the frame counter to 0.
        """
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
            self.char_table[int(position.y)][int(position.x)] = ' '
        except IndexError:
            style.printc(f"{defaults.LOG_WARNING}Couldn't erase character at {position}: doesn't exist.", style.Color.YELLOW)

    def _write_char(self, char: str, position: maths.Vector2D, styles: str = "") -> None:
        """
        Add a character (len == 1) and its position to the next printed table.
        (0, 0) is the upper left corner.
        """
        raise_on_long_char: bool = False
        warn_on_outside: bool = self.debug
        allow_negative_index: bool = False

        if len(char) > 1 and raise_on_long_char:
            raise ValueError(f"{style.Color.RED}Must be a char: {char}, ({len(char)}).{style.Style.END}")
        if not char:
            # Don't do anything is the char is the empty string.
            # To erase, use `clear_char`.
            return
        if (position.x < 0 or position.y < 0) and not allow_negative_index:
            if warn_on_outside:
                style.printc(f"{defaults.LOG_WARNING}Character {char} ignored at negative position: {position}.", style.Color.YELLOW)
            return

        try:
            if styles:
                self.char_table[int(position.y)][int(position.x)] = styles + char + style.Style.END
            else:
                self.char_table[int(position.y)][int(position.x)] = char
        except IndexError:
            if warn_on_outside:
                style.printc(f"{defaults.LOG_WARNING}Character {char} ignored at {position}.", style.Color.YELLOW)

    def write(self, message: Union[str, list[str]], start: maths.Vector2D, way: ReadingWay = ReadingWay.LEFT_RIGHT, styles: str = "") -> int:
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
                raise ValueError(f"{style.Color.RED}Must be a valid direction (0 - 3): {way}.{style.Style.END}")

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
        Printed in one time for the sake of smoothness, 
        and only if the char table is different or the window size.
        """
        if self.char_table != self.previous_char_table or self.size != maths.Size.terminal_size():
            table: list[str] = list()
            self.char_table[-1].pop()
            for records in self.char_table:
                for char in records:
                    table += self.global_style + char + style.END
                table.append("\n")
            sys.stdout.write("".join(table[:-4]))

    def total_char_table_len(self) -> int:
        total: int = 0
        for record in self.char_table:
            total += len(record)

        return total


if __name__ == "__main__":
    print("See `animations/examples.py`.")
