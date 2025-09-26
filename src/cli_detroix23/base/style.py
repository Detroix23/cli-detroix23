"""
CLI - Terminal
style.py
"""
import os


# Escape character. \033, \x1b
ESC: str = "\x1b"

# Shortcuts
END: str = ESC + '[0m'
DEFAULT: str = ESC + '[10m'
OFF_BOLD: str = ESC + '[22m'
OFF_ITALIC: str = ESC + '[23m'
OFF_UNDERLINE: str = ESC + '[24m'

class Style:
    """
    Color codes for the terminal, from the Select Graphic Rendition subset.
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
    BOLD = ESC + '[1m'
    ITALIC = ESC + '[3m'
    UNDERLINE = ESC + '[4m'
    BLINK = ESC + '[5m'
    BLINK2 = ESC + '[6m'
    INVISIBLE = ESC + '[8m'
    THROUGHT = ESC + '[9m'
    DOUBLE_UNDERLINE = ESC + '[21m'

class Color(Style):
    """
    Foreground text colors.
    More info:
        - https://github.com/termstandard/colors
    """
    DIM = ESC + '[2m'
    DIMMER = ESC + '[37m'

    BLACK = ESC + '[30m'
    RED = ESC + '[31m'
    GREEN = ESC + '[32m'
    YELLOW = ESC + '[33m'
    OKBLUE = ESC + '[34m'
    MAGENTA = ESC + '[35m'
    CYAN = ESC + '[36m'
    LIGHT_RED = ESC + '[91m'
    LIGHT_GREEN = ESC + '[92m'
    LIGHT_YELLOW = ESC + '[93m'
    LIGHT_OKBLUE = ESC + '[94m'
    LIGHT_MAGENTA = ESC + '[95m'
    LIGHT_CYAN = ESC + '[96m'
    WHITE = ESC + '[97m'


class Back(Style):
    """
    Background colors.
    """
    CONTRAST = ESC + '[7m'

    BLACK = ESC + '[40m'
    RED = ESC + '[41m'
    GREEN = ESC + '[42m'
    YELLOW = ESC + '[43m'
    BLUE = ESC + '[44m'
    MAGENTA = ESC + '[45m'
    CYAN = ESC + '[46m'
    GRAY = ESC + '[47m'
    LIGHT_BLACK = ESC + '[100m'
    LIGHT_RED = ESC + '[101m'
    LIGHT_GREEN = ESC + '[102m'
    LIGHT_YELLOW = ESC + '[103m'
    LIGHT_BLUE = ESC + '[104m'
    LIGHT_MAGENTA = ESC + '[105m'
    LIGHT_CYAN = ESC + '[106m'
    LIGHT_GRAY = ESC + '[107m'


def printc(message: str, style: str = "", end: str = "\n") -> None:
    """
    Print a string, using an optional style for the whole line and an end character.
    Automatically put a style END.
    """
    string: str = style + message + Style.END
    print(string, end=end)
    
    return

def main() -> None:
    Style.display_all_rendition_subset()

    printc(f"█████████████", Color.DIM)
    printc(f"█████████████", Color.DIMMER)

if __name__ == "__main__":
    main()
