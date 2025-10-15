"""
CLI - Animations
exemples.py
"""
import time
import random
from enum import Enum
from typing import Sequence

import maths.maths as maths
import maths.transformations as transformations
import animations.screen as screen
import base.style as style

class Dropplet:
    """
    Single dropplet for the Matrix's digital rain.
    """
    char: str
    position: maths.Vector2D
    last_chars: list[str]
    frames_to_move: int

    def __init__(self, screen: 'Matrix') -> None:
        self.screen: 'Matrix' = screen
        self.char: str = self._random_char(*self.screen.character_random_range)
        self.position: maths.Vector2D = self._random_position(self.screen)
        self.last_chars: list[str] = []
        self.frames_to_move: int = int(1 / self.screen.frame_delay) // 10

    def _random_char(self, random_min: int, random_max: int) -> str:
        r: int = 0
        blacklist: list[int] = [0, 24, 47, 97, 127, 128, 129, 130, 131, 132, 133, 141, 143, 144, 149, 151, 157, 160, 168, 173, 175, 180, 184]
        r = random.randint(random_min, random_max)
        if r in blacklist:
            r = 42
        return chr(r)

    def _random_position(self, screen: screen.Screen) -> maths.Vector2D:
        return maths.Vector2D(random.randint(0, screen.size.x), 0)

    def update(self) -> None:
        """
        Update the dropplet. Apply gravity.
        """
        # Move, if enough frames.
        if self.screen.frames % self.frames_to_move == 0:
            # Update tail.
            self.last_chars.insert(0, self.char)
            if len(self.last_chars) > random.randint(5, 10):
                self.last_chars.pop()

            # Move 1 tile.
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

class Matrix(screen.Screen):
    digital_rain: list[Dropplet]
    character_random_range: tuple[int, int]
    infos: bool
    start_time: float

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
        self.start_time: float = time.monotonic()
    
    def time_elapsed(self) -> float:
        """
        Return time elapsed from start time to now.
        Float and using time.monotonic().
        """
        d: float = time.monotonic() - self.start_time
        if d > 0:
            return d
        return 1


    def updater(self) -> None:
        # New dropplet
        dropplet_quantity: int = (self.size.x // (45 + int(1 / self.frame_delay) // 10))
        if dropplet_quantity == 0:
            dropplet_quantity = 1
        for _ in range(dropplet_quantity):
            self.digital_rain.append(Dropplet(self))

        # Update each existing dropplet
        new_rain: list[Dropplet] = list()
        for dropplet in self.digital_rain:
            dropplet.update()
            if dropplet.position.y - len(dropplet.last_chars) <= self.size.y:
                new_rain.append(dropplet)
        
        self.digital_rain = new_rain

        # Prevent eventual overflow
        time_of_reset: float = 600
        if self.time_elapsed() > time_of_reset:
            self.start_time = time.monotonic()
            self.frames_reset()


    def drawer(self) -> None:
        cursor: int = 1
        # Draw each existing dropplets.
        for dropplet in self.digital_rain:
            self.write(dropplet.full_tail(), dropplet.position, screen.ReadingWay.DOWN_UP)

        # Infos.
        if self.infos:
            cursor += 1 + self.write(f"fps:{(float(self.frames) / self.time_elapsed()):.0f}", maths.Vector2D(cursor, 0), screen.ReadingWay.LEFT_RIGHT)
            cursor += 1 + self.write(f"table:{self.total_char_table_len()}", maths.Vector2D(cursor, 0), screen.ReadingWay.LEFT_RIGHT)
            cursor += 1 + self.write(f"x:{self.size.x}", maths.Vector2D(cursor, 0), screen.ReadingWay.LEFT_RIGHT)
            cursor += 1 + self.write(f"y:{self.size.y}", maths.Vector2D(cursor, 0), screen.ReadingWay.LEFT_RIGHT)
            cursor += 1 + self.write(f"n:{len(self.digital_rain)}",maths. Vector2D(cursor, 0), screen.ReadingWay.LEFT_RIGHT)

class CellState(Enum):
    DEAD = 0
    ALIVE = 1
    VOID = 2
    

class GameOfLife(screen.Screen):
    board: list[list[CellState]] 
    _to_breed: set[int] = {3}
    _to_survive: set[int] = {2, 3}


    def __init__(
        self, 
        void_char: str = ".", 
        frame_delay: float = 0.1, 
        global_style: str = "", 
        debug: bool = False, 
        deactivate_screen: bool = False
    ) -> None:
        super().__init__(void_char, frame_delay, global_style, debug, deactivate_screen)
        
        self.board = [[CellState.DEAD for _ in range(self.size.x)] for _ in range(self.size.y)]

    def updater(self) -> None:
        new: list[list[CellState]] = list()
        for x, row in enumerate(self.board):
            line: list[CellState] = list()
            for y, state in enumerate(row):
                count: int = self.count_neighbours(maths.Vector2D(x, y))
                if ((state == CellState.ALIVE and count in self._to_survive)
                    or (state == CellState.DEAD and count in self._to_breed)    
                ):
                    line.append(CellState.ALIVE)
                else:
                    line.append(CellState.DEAD)
                    assert count != 3
            new.append(line)
        
        self.board = new

        

    def drawer(self) -> None:
        for y, row in enumerate(self.board):
            for x, state in enumerate(row):
                char: str
                if state == CellState.ALIVE:
                    char = "#"
                elif state == CellState.DEAD:
                    char = "."
                else:
                    char = "?"

                self.write(char, maths.Vector2D(x, y))

    def set_cell(self, coordinates: maths.Size, state: CellState) -> CellState:
        """
        Set the cell at the given `coordinates` to the `state`.
        Return the old state.
        """
        old: CellState = self.board[coordinates.y][coordinates.x]
        self.board[coordinates.y][coordinates.x] = state
        
        return old

    def set_multiple(self, coordinates: Sequence[maths.Size], state: CellState) -> None:
        """
        Set multiple cells, given their `coordinates`, to the `state`.
        """
        for cell in coordinates:
            self.set_cell(cell, state)

    def count_neighbours(self, coordinates: maths.Vector2D) -> int:
        """
        Return the number of neighbours.
        """
        count: int = 0
        for neighbour in transformations.RELATIVE_NEIGHBOURS:
            state: CellState
            x: int = int(neighbour.x + coordinates.x)
            y: int = int(neighbour.y + coordinates.y)
            if (0 <= x < self.size.x
                and 0 <= y < self.size.y
            ):
                state = self.board[y][x]
            else:
                state = CellState.VOID

            if state == CellState.ALIVE:
                count += 1

        return count


def run_matrix() -> None:
    # (48, 49) binary.
	# (32, 132) general.
    screen = Matrix(
        frame_delay=1/27,
        character_random_range=(32, 132),
        infos=True
    )
    
    screen.run(Matrix.updater, Matrix.drawer)

def run_game_of_life() -> None:
    screen = GameOfLife(
        frame_delay=1,
    )

    screen.set_multiple([
        maths.Size(10, 10),
        maths.Size(10, 9),
        maths.Size(9, 9),
    ], CellState.ALIVE)

    screen.run(GameOfLife.updater, GameOfLife.drawer)

def main() -> None:
	run_matrix()


if __name__ == "__main__":
    main()
    