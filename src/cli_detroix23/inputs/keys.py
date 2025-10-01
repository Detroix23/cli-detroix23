# type: ignore[reportPossiblyUnboundVariable]
"""
CLI - Inputs
keys.py
"""
import sys
import os

UNIX_LIKE: bool = os.name == 'posix'
if UNIX_LIKE:
    import termios
    import tty
else:
    import msvcrt

import base.specials as specials

def get_key(*, allow_keyboard_interrupt: bool = True) -> str:

    if UNIX_LIKE:
        fd: int = sys.stdin.fileno()
        old_settings: termios._AttrReturn = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            # Handle arrow keys (escape sequences).
            if key == "\x1b":
                key += sys.stdin.read(2)
            # Ctrl C.
            if key == "\x03" and allow_keyboard_interrupt:
                raise KeyboardInterrupt(f"(X) - Keyboard interrupt while getting key ({repr(key)}).")
            return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    # Windows
    else:  
        key: str = msvcrt.getch()
        # Special key prefix on Windows
        if key == b"\xe0":  
            key += msvcrt.getch()
        return key.decode('utf-8', errors='ignore')
    


def main() -> None:
    """
    Test the getter of key.
    """
    print("GET KEY.", end="\n")
    while True:
        key: str = get_key()
        mapped: list[str] = specials.filter_map(specials.NICE_MAP, key)
        print(mapped, end="\r")

if __name__ == "__main__":
    main()