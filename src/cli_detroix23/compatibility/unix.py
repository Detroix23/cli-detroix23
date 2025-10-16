"""
CLI - Compatibility.
terminal_unix.py
cf:
    https://docs.python.org/3/library/termios.html,
    https://manpages.debian.org/trixie/manpages-dev/termios.3.en.html
"""
import sys
import termios
from typing import Final

import compatibility.types as types

FILE_ID: Final[int] = sys.stdin.fileno()
SETTINGS: Final[types.Attr] = termios.tcgetattr(FILE_ID)

def set_to_default() -> None:
    """
    Set back to the original settings the terminal.
    """
    termios.tcsetattr(FILE_ID, termios.TCSANOW, SETTINGS)

def print_attr(settings: types.Attr) -> None:
    """
    Print the given attributes.

    (not in POSIX; 027, ETB, Ctrl-W) Word erase (WERASE). Recognized when ICANON and IEXTEN are set, and then not passed as input. 
    """
    KEYS: Final[list[str]] = ["iflag", "oflag", "cflag", "lflag", "ispeed", "ospeed", "cc"]
    # Adapted for Linux. 
    CC: Final[list[str]] = [
        "VEOF", "VEOL", "VERASE", "VINTR", "VKILL", "VLNEXT", 
        "VMIN", "VQUIT", "VREPRINT", "VSTART", "VSTATUS", "VSTOP", "VSUSP", "VSWTCH", "VTIME", "VWERASE"
    ]

    print("ATTR")
    for i, value in enumerate(settings):
        if i >= len(KEYS):
            pass
        elif isinstance(value, list):
            print(f"- {KEYS[i]}: ")
            for j, arg in enumerate(value):
                if j < len(CC) and isinstance(arg, bytes):
                    print(f"\t* {CC[j]}: {arg} {ord(arg.decode(encoding="utf-8", errors="strict"))}")
                else:
                    print(f"\t* cc-unknown: {arg}")
        else:
            print(f"- {KEYS[i]}: {value}")

    print()


def main() -> None:
    """
    Main test entry point for this unix script.
    """
    global SETTINGS

    print_attr(SETTINGS)

if __name__ == "__main__":
    main()