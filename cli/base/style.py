"""
CLI - Terminal
style.py
"""

# Shortcuts
END: str = '\033[0m'
DEFAULT: str = '\033[10m'
OFF_BOLD: str = '\033[22m'
OFF_ITALIC: str = '\033[23m'
OFF_UNDERLINE: str = '\033[24m'

class Style:
    """
    Color codes for the terminal, from the Select Graphic Rendition subset.
    More info: 
        - https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences.
        - https://en.wikipedia.org/wiki/ANSI_escape_code
    """
    END: str = '\033[0m'
    DEFAULT: str = '\033[10m'
    OFF_BOLD: str = '\033[22m'
    OFF_ITALIC: str = '\033[23m'
    OFF_UNDERLINE: str = '\033[24m'
    OFF_BLINK: str = '\033[25m'
    OFF_INVERSE: str = '\033[27m'
    OFF_CONCEAL: str = '\033[28m'
    OFF_CROSS: str = '\033[29m'
    OFF_FRAME: str = '\033[54m'
    OFF_OVERLINE: str = '\033[55m'

    @staticmethod
    def display_all_rendition_subset(range_min: int = 0, range_max: int = 127) -> None:
        for i in range(range_min, range_max):
            print(f"(\033[{i}m Text {i}. {Style.END})", end="")
            if i % 12 == 0 and i != 0:
                print()
        print()

class Text(Style):
    """
    Text weight and style.
    """
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    BLINK2 = '\033[6m'
    INVISIBLE = '\033[8m'
    THROUGHT = '\033[9m'
    DOUBLE_UNDERLINE = '\033[21m'

class Color(Style):
    """
    Foreground text colors.
    More info:
        - https://github.com/termstandard/colors
    """
    DIM = '\033[2m'
    DIMMER = '\033[37m'

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    OKBLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_OKBLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'


class Back(Style):
    """
    Background colors.
    """
    CONTRAST = '\033[7m'

    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    GRAY = '\033[47m'
    LIGHT_BLACK = '\033[100m'
    LIGHT_RED = '\033[101m'
    LIGHT_GREEN = '\033[102m'
    LIGHT_YELLOW = '\033[103m'
    LIGHT_BLUE = '\033[104m'
    LIGHT_MAGENTA = '\033[105m'
    LIGHT_CYAN = '\033[106m'
    LIGHT_GRAY = '\033[107m'


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
