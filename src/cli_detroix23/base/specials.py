"""
CLI - Style/ Base
specials.py
Special escape characters.
"""

_POSSIBLE_ESC: set[str] = {"\033", "\x1b"}
ESC: str = "\x1b"

NICE_MAP: dict[str, str] = {
    "\x1b": "Escape",
    "\x03": "Keyboard Interrupt",
    " ": "Space",
    "\r": "Carriage return",
    "\n": "Return",
    "\x7f": "Backspace",
    "\x1b[2": "Insert",
    "\x1b[3": "Delete",
    "\x1b[6": "Page down",
    "\x1b[5": "Page up",
    "\x1b[F": "Fin",
    "\x1b[H": "Home",
    "\x1b[A": "Arrow up",
    "\x1b[B": "Arrow down",
    "\x1b[C": "Arrow left",
    "\x1b[D": "Arrow right",
    "\x1b[?25l": "Cursor hide",
    "\x1b[?25h": "Cursor show"
}
