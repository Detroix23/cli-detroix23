
ESC: str
END: str
DEFAULT: str
OFF_BOLD: str
OFF_ITALIC: str
OFF_UNDERLINE: str

class Style:
    END: str
    DEFAULT: str
    OFF_BOLD: str
    OFF_ITALIC: str
    OFF_UNDERLINE: str
    OFF_BLINK: str
    OFF_INVERSE: str
    OFF_CONCEAL: str
    OFF_CROSS: str
    OFF_FRAME: str
    OFF_OVERLINE: str

    @staticmethod
    def display_all_rendition_subset(range_min: int = 0, range_max: int = 127) -> None: ...

class Text(Style):
    BOLD: str
    ITALIC: str
    UNDERLINE: str
    BLINK: str
    BLINK2: str
    INVISIBLE: str
    THROUGH: str
    DOUBLE_UNDERLINE: str

class Color(Style):
    DIM: str
    DIMMER: str
    BLACK: str
    RED: str
    GREEN: str
    YELLOW: str
    BLUE: str
    MAGENTA: str
    CYAN: str
    LIGHT_RED: str
    LIGHT_GREEN: str
    LIGHT_YELLOW: str
    LIGHT_BLUE: str
    LIGHT_MAGENTA: str
    LIGHT_CYAN: str
    WHITE: str

class Back(Style):
    CONTRAST: str
    BLACK: str
    RED: str
    GREEN: str
    YELLOW: str
    BLUE: str
    MAGENTA: str
    CYAN: str
    GRAY: str
    LIGHT_BLACK: str
    LIGHT_RED: str
    LIGHT_GREEN: str
    LIGHT_YELLOW: str
    LIGHT_BLUE: str
    LIGHT_MAGENTA: str
    LIGHT_CYAN: str
    LIGHT_GRAY: str

def printc(message: str, style: str = '', end: str = '\n') -> None: ...
