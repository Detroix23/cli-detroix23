"""
# CLI - Base.
src/cli_detroix23/base/style.py

Reference for ANSI character codes and styles.

_This file is supposed to be neutral, with only Python dependencies_
"""

import os

ESC: str = "\x1b"
"""
Escape special characters that allows styles.  
Possibles codes:
- `\\033`;
- `\\x1b`;
- `\\e` (Windows);
- `\\e0` (Windows);
"""

# Shortcuts
END: str = ESC + '[0m'
DEFAULT: str = ESC + '[10m'
OFF_BOLD: str = ESC + '[22m'
OFF_ITALIC: str = ESC + '[23m'
OFF_UNDERLINE: str = ESC + '[24m'


class Style:
    """
    Color codes for the terminal, reference for the Select Graphic Rendition subset. 

    More info:
    - https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences.
    - https://en.wikipedia.org/wiki/ANSI_escape_code
    """
    END: str = ESC + '[0m'
    DEFAULT: str = ESC + '[10m'
    OFF_BOLD: str = ESC + '[22m'
    OFF_ITALIC: str = ESC + '[23m'
    OFF_UNDERLINE: str = ESC + '[24m'
    OFF_BLINK: str = ESC + '[25m'
    OFF_INVERSE: str = ESC + '[27m'
    OFF_CONCEAL: str = ESC + '[28m'
    OFF_CROSS: str = ESC + '[29m'
    OFF_FRAME: str = ESC + '[54m'
    OFF_OVERLINE: str = ESC + '[55m'

    @staticmethod
    def display_all_rendition_subset(range_min: int = 0, range_max: int = 127) -> None:
        size: tuple[int, int] = os.get_terminal_size()
        char_count: int = 0
        for i in range(range_min, range_max):
            text: str = f"Text {i}."
            char_count += len(text) + 2
            if char_count > size[0] and len(text) <= size[0]:
                print()
                char_count = 0
            else:
                print(f"(\033[{i}m{text}{Style.END})", end="")
        print()


class Text(Style):
    """
    Text weight and style.
    """
    BOLD: str = ESC + '[1m'
    ITALIC: str = ESC + '[3m'
    UNDERLINE: str = ESC + '[4m'
    BLINK: str = ESC + '[5m'
    BLINK2: str = ESC + '[6m'
    INVISIBLE: str = ESC + '[8m'
    THROUGHT: str = ESC + '[9m'
    DOUBLE_UNDERLINE: str = ESC + '[21m'


class Color(Style):
    """
    Foreground text colors.
    More info:
        - https://github.com/termstandard/colors
    """
    DIM: str = ESC + '[2m'
    DIMMER: str = ESC + '[37m'
    BLACK: str = ESC + '[30m'
    RED: str = ESC + '[31m'
    GREEN: str = ESC + '[32m'
    YELLOW: str = ESC + '[33m'
    OKBLUE: str = ESC + '[34m'
    MAGENTA: str = ESC + '[35m'
    CYAN: str = ESC + '[36m'
    LIGHT_RED: str = ESC + '[91m'
    LIGHT_GREEN: str = ESC + '[92m'
    LIGHT_YELLOW: str = ESC + '[93m'
    LIGHT_OKBLUE: str = ESC + '[94m'
    LIGHT_MAGENTA: str = ESC + '[95m'
    LIGHT_CYAN: str = ESC + '[96m'
    WHITE: str = ESC + '[97m'


class Back(Style):
    """
    Background colors.
    """
    CONTRAST: str = ESC + '[7m'
    BLACK: str = ESC + '[40m'
    RED: str = ESC + '[41m'
    GREEN: str = ESC + '[42m'
    YELLOW: str = ESC + '[43m'
    BLUE: str = ESC + '[44m'
    MAGENTA: str = ESC + '[45m'
    CYAN: str = ESC + '[46m'
    GRAY: str = ESC + '[47m'
    LIGHT_BLACK: str = ESC + '[100m'
    LIGHT_RED: str = ESC + '[101m'
    LIGHT_GREEN: str = ESC + '[102m'
    LIGHT_YELLOW: str = ESC + '[103m'
    LIGHT_BLUE: str = ESC + '[104m'
    LIGHT_MAGENTA: str = ESC + '[105m'
    LIGHT_CYAN: str = ESC + '[106m'
    LIGHT_GRAY: str = ESC + '[107m'



def printc(message: str, style: str = "", end: str = "\n") -> None:
    """
    Print a string, using an optional style for the whole line and an end character.
    Automatically put a style END.
    """
    string: str = style + message + Style.END
    print(string, end=end)
    
    return

if __name__ == "__main__":
    print("cf. Examples.")
