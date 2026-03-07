"""
# CLI - Inputs
src/cli_detroix23/inputs/examples.py
"""

import sys

from cli_detroix23.base import specials, controls
from cli_detroix23.inputs import keys, fetch

class SysReading:
    running: bool

    def __init__(self) -> None:
        self.running = False

    def run(self) -> None:
        self.running = True

        while self.running:
            print("==========")

            print("sys.stdin:")
            for line in sys.stdin:
                print(f"\t- `{line}`")


def run_sys_reading() -> None:
    print("## Sys reading.")
    sys_reading = SysReading()

    sys_reading.run()

def run_basic_keys() -> None:
    """
    Test the getter of key, by printing an history of the pressed keys.
    """
    history: list[keys.Key] = list()
    history_length: int = 2

    def append_to_history(hist: list[keys.Key], key: keys.Key) -> None:
        hist.append(key)
        if len(history) > history_length:
            hist.pop(0)

    print("\nGET KEY.", end="\n")
    while True:
        append_to_history(history, fetch.get())
        
        for key in history:
            mapped: list[str] = specials.filter_map(specials.NICE_MAP, key.key())
            good: bool = fetch.compare(keys.Keys.DOWN, key)
            print(f"\r{mapped}, key={repr(key)}, good={good}.")
        
        controls.up(len(history))
        controls.clear_to_bottom()

if __name__ == "__main__":
    run_basic_keys()