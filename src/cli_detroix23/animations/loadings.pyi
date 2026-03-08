from enum import Enum

class State(Enum):
    READY = 0
    RUNNING = 1
    FINISHED = 2

class Animation:
    _iteration: int
    first_time: float
    state: State
    symbols: list[str] | str
    maximum: int
    span: int
    multiple: int
    empty: str
    borders: str
    prefix: str
    suffix: str
    ready_character: str
    counters: dict[str, int]

    def __init__(
        self, 
        symbols: list[str] | str, 
        maximum: int, 
        span: int = 1, 
        multiple: int = 1, 
        empty: str = '█', 
        borders: str = '|', 
        prefix: str = 'Loading: ', 
        suffix: str = ' ', 
        more_counters: list[str] = ...
    ) -> None: ...

class Bar(Animation):
    def __init__(
        self,
        symbols: str, 
        maximum: int, 
        *, 
        multiple: int = 0, 
        empty: str = '░', 
        borders: str = '|', 
        prefix: str, 
        suffix: str = ' ', 
        more_counters: list[str] = ...
    ) -> None: ...
    def reset(self) -> None: ...
    def increment(self, add: int = 1) -> None: ...
    def finish(self) -> None: ...

class Spinner(Animation):
    def more_counters(self, more_counters: list[str] | str) -> None: ...
    def __init__(
        self, 
        symbols: list[str] | str,
        maximum: int = 0, 
        *,
        span: int = 1, 
        multiple: int = 1, 
        finish: str = '█', 
        borders: str = '|', 
        prefix: str = 'Loading: ', 
        suffix: str = ' ', 
        more_counters: list[str] = ...
    ) -> None: ...
    def reset(self) -> None: ...
    def increment(self, add: int = 1) -> None: ...
    def __copy__(self) -> Spinner: ...
    def finish(self) -> None: ...

bars: dict[str, Bar]
spinners: dict[str, Spinner]

def main() -> None: ...
def run_spinners1() -> None: ...
def run_bars1() -> None: ...
