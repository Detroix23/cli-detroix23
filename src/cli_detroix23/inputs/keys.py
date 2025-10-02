# type: ignore[reportPossiblyUnboundVariable]
"""
CLI - Inputs
keys.py
"""
import sys

import compatibility.plateform as plateform
if plateform.OS == plateform.Os.UNIX:
    import termios
    import tty
else:
    import msvcrt

import base.specials as specials

class Key:
    windows: str
    unix: str

    def __init__(self, windows: str, unix: str) -> None:
        self.windows = windows
        self.unix = unix


def get_key(*, allow_keyboard_interrupt: bool = True) -> str:
    """
    Get the user pressed key.
    """
    if plateform.OS == plateform.Os.UNIX:
        fd: int = sys.stdin.fileno()
        old_settings: termios._AttrReturn = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            # Handle arrow keys (escape sequences).
            if key == "\x1b":
                key += sys.stdin.read(2)
            # Ctrl+C.
            elif key == "\x03" and allow_keyboard_interrupt:
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
        # Ctrl+C.
        elif key == b"\x03" and allow_keyboard_interrupt:
            raise KeyboardInterrupt(f"(X) - Keyboard interrupt while getting key ({repr(key)}).")
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