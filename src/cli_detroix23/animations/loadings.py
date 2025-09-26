"""
IN PICTURE
loadings.py
Aim: loading bars and spinners like `alive_progress`, `tqdm`,...
Utilize the \r escape operator
"""

import time
import sys
from enum import Enum
from typing import Union

class State(Enum):
    READY = 0
    RUNNING = 1
    FINISHED = 2

class Animation:
    """
    Loading animation.
    """
    _i: int
    first_time: float

    state: State

    def __init__(
        self,
        symbols: Union[list[str], str],
        maximum: int,
        span: int = 1, 
        multiple: int = 1,
        empty: str = "█",
        borders: str = "|",
        prefix: str = "Loading: ",
        suffix: str = " ",
        more_counters: list[str] = list()
    ) -> None:
        self._i = 0
        self.first_time: float = 0
        self.state: State = State.READY

        self.symbols: Union[list[str], str] = symbols

        self.max: int = maximum
        self.span: int = span
        self.multiple: int = multiple
        self.empty: str = empty
        
        self.borders: str = borders
        self.prefix: str = prefix
        self.suffix: str = suffix
        
        self.ready_character: str = "..."

        self.counters: dict[str, int] = {counter: 0 for counter in more_counters}


class Bar(Animation):
    """
    Loading bar, child of Animation.
    """
    def __init__(
        self, 
        symbols: str, 
        maximum: int, 
        *, multiple: int = 0,
        empty: str = "░", 
        borders: str = "|",
        prefix: str,
        suffix: str = " ",
        more_counters: list[str] = list(),
    ) -> None:
        super().__init__(
            symbols,
            maximum,
            1,
            multiple,
            empty,
            borders,
            prefix,
            suffix,
            more_counters,
        )
        # For Bar, ensure max > 0
        self.max = self.max if self.max > 0 else 1

        
    def reset(self) -> None:
        """
        Reset the counter. Run this method when using default bars.
        """
        self._i = 0
        self.first_time: float = 0
        self.state = State.READY

    def increment(self, add: int = 1) -> None:
        if self.first_time == 0:
            self.first_time = time.monotonic()
            self.state = State.RUNNING
        
        self._i += add
        progress_bar_symbol: str = self.symbols[0]
        bar: str
        if self.multiple > 0 and self._i <= self.max:
            true_i: int = int(self.multiple * (float(self._i) / float(self.max)))
            bar = (
                progress_bar_symbol * true_i
                + self.empty * (self.multiple - true_i)
            )
        elif self.multiple > 0 and self._i > self.max:
            bar = progress_bar_symbol * self.multiple 
        elif self._i <= self.max:
            bar = (
                progress_bar_symbol * self._i
                + self.empty * (self.max - self._i)
            )
        else:
            bar = progress_bar_symbol * self.max

        template: str = "\r"

        template += self.prefix
        template += self.borders
        template += bar
        template += self.borders
        template += " - "

        percentage: float = self._i / self.max * 100
        template += f"{percentage:.1f}% "
        template += f"{self._i}/{self.max}ops "

        time_elapsed: float = time.monotonic() - self.first_time
        template += f"{time_elapsed:.2f}s "

        template += self.suffix
        template += "\r"

        # Hide cursor
        sys.stdout.write('\x1b[?25l')
        sys.stdout.write(
            template,
        )
        sys.stdout.flush()
    
    def finish(self) -> None:
        """
        Allow to prematurly and ensure the bar to complete.
        Fill the bar on call.
        """
        if self._i < self.max:
            self._i = self.max
        
        self.state = State.FINISHED
        # Show cursor again
        sys.stdout.write('\x1b[?25h')
        self.increment(0)

class Spinner(Animation):
    """
    Loading spinner, child of Animation.
    """
    def __init__(
        self, 
        symbols: Union[list[str], str], 
        maximum: int = 0,
        *, span: int = 1, 
        multiple: int = 1,
        finish: str = "█",
        borders: str = "|",
        prefix: str = "Loading: ",
        suffix: str = " ",
        more_counters: list[str] = list()
    ) -> None:
        super().__init__(
            symbols,
            maximum,
            span,
            multiple,
            finish,
            borders,
            prefix,
            suffix,
            more_counters,
        )

    def more_counters(self, more_counters: Union[list[str], str]) -> None:
        """
        Define more counter, after initialization.
        """
        if isinstance(more_counters, list):
            self.counters = {counter: 0 for counter in more_counters}
        else:
            self.counters = {more_counters: 0}

    def reset(self) -> None:
        """
        Reset the counter. Run this method when using default bars.
        """
        self._i = 0
        self.first_time: float = 0
        self.state = State.READY
        # Update custom counters
        self.counters = {key: 0 for key in self.counters.keys()}

    def increment(self, add: int = 1) -> None:
        """
        Progress the bar for 1 tick.
        """
        if self.first_time == 0:
            self.first_time = time.monotonic()
            self.state = State.RUNNING
        
        self._i += add
        i: int = self._i // self.multiple
        
        spinner: str = ""
        for j in range(self.span):
            spinner += self.symbols[(i + j) % len(self.symbols)]
        
        template: str = "\r"

        # Drawing
        template += self.prefix
        template += self.borders
        if self.state == State.FINISHED:
            template += f"{self.empty * self.span}"
        elif self.state == State.READY:
            template += f"{self.ready_character * self.span}"
        else:
            template += spinner
        template += self.borders
        template += " - "

        # Main counter
        if self.max != 0:
            percentage: float = self._i / self.max * 100
            template += f"{percentage:.1f}% "
            template += f"{self._i}/{self.max}ops "
        else:
            template += f"{self._i}ops "

        # Custom counters
        if self.counters:
            for name, count in self.counters.items():
                template += f"{name}: {count} "

        # Time counter
        time_elapsed: float = time.monotonic() - self.first_time
        template += f"{time_elapsed:.2f}s "

        template += self.suffix

        # Hide cursor
        sys.stdout.write('\x1b[?25l')
        sys.stdout.write(
            template,
        )
        sys.stdout.flush()


    
    def __copy__(self) -> 'Spinner':
        copied: 'Spinner' = Spinner(
            self.symbols, 
            self.max, 
            span=self.span, 
            multiple=self.multiple
        )
        copied.reset()
        return copied

    def finish(self) -> None:
        """
        Allow to prematurly and ensure the spinner to complete.
        Set the state to FINISHED, and update one last time.
        """
        if self._i < self.max:
            self._i = self.max

        self.state = State.FINISHED
        # Show cursor again
        sys.stdout.write('\x1b[?25h')
        self.increment(0)

# Default
bars: dict[str, Bar] = {
    "SimpleFull1": Bar(
        "█",
        100,
        prefix="Loading: ",
        multiple=10    
    ),
}
spinners: dict[str, Spinner] = {
    "Bars1": Spinner(
        ["│", "╲", "─", "/"],
        maximum=1000,
        multiple=2,
    ),
    "Wave1": Spinner(
        ["▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂", "▁"],
        span=3,
        multiple=1
    ),
    "Wave2": Spinner(
        ["▂", "▄", "▆", "█", "▆", "▄", "▂", "▁"],
        span=3,
        multiple=1
    ),
    # Box-drawing chars: ▖▗▘▙▚▛▜▝▞▟
    "Solid1": Spinner(
        "▙▚▘▛▞▝▜▚▗▟▞▖"
    ),
    "Solid2": Spinner(
        "▙▌▛▔▜▐▟▁"
    ),
}

def main() -> None:
    run_bars1()
    run_spinners1()


def run_spinners1() -> None:
    b: Spinner = spinners["Wave1"]
    b.reset()

    for _ in range(100):
        b.increment()
        time.sleep(0.1)

    b.finish()
    print()

def run_bars1() -> None:
    a: Bar = bars["SimpleFull1"]
    a.reset()

    for _ in range(100):
        a.increment()
        time.sleep(0.1)

    a.finish()
    print() 

if __name__ == "__main__":
    main()