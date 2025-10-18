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

KEYS: Final[list[str]] = ["iflag", "oflag", "cflag", "lflag", "ispeed", "ospeed", "cc"]
# Adapted for Linux. 
CC: Final[list[str]] = [
    "VEOF", "VEOL", "VERASE", "VINTR", "VKILL", "VLNEXT", 
    "VMIN", "VQUIT", "VREPRINT", "VSTART", "VSTATUS", "VSTOP", "VSUSP", "VSWTCH", "VTIME", "VWERASE"
]

def get_settings(file_id: int) -> types.Attr:
    """
    Return terminal attributes.
    """
    return termios.tcgetattr(FILE_ID)

def settings_difference(s1: types.Attr, s2: types.Attr) -> dict[str, tuple[int, int]]:
    """
    Return a dict of Attr differences.
    """
    differences: dict[str, tuple[int, int]] = dict()
    for (index, (e1, e2)) in enumerate(zip(s1, s2)):
        if e1 != e2 and not isinstance(e1, list) and not isinstance(e2, list):
            differences[KEYS[index]] = (int(e1), int(e2)) 

    return differences

def set_to_default() -> None:
    """
    Set back to the original settings the terminal.
    """
    termios.tcsetattr(FILE_ID, termios.TCSANOW, SETTINGS)
    sys.stdout.flush()
    sys.stdin.flush()

def print_attr(settings: types.Attr) -> None:
    """
    Print the given attributes.
    """
    global CC, KEYS

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


def test_present_settings() -> None:
    attrs: Final[types.Attr] = get_settings(FILE_ID)
        
    print("Print test")
    print("Print test")
    print("Print test")
    print("Print test")

    sys.stdout.write("Write test\n")
    sys.stdout.write("Write test\n")
    sys.stdout.write("Write test\n")
    sys.stdout.write("Write test\n")
    sys.stdout.write("Write test\n")

    if SETTINGS != attrs:
        raise ValueError(f"""Settings not matching. 
=> {settings_difference(SETTINGS, attrs)}
=> {get_settings(FILE_ID)}
""")

def main() -> None:
    """
    Main test entry point for this unix script.
    """
    global SETTINGS

    print_attr(SETTINGS)

if __name__ == "__main__":
    main()