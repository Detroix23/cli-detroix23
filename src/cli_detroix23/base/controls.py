"""
CLI - Base
controls.py
cf:
    https://en.wikipedia.org/wiki/ANSI_escape_code
"""
import sys

import base.specials as specials
import maths.maths as maths

def up(times: int = 1, flush: bool = False) -> None:
    """
    Print in the console _Arrow up_. \r
    """
    sys.stdout.write(f"{specials.ESC}[{times}A")
    if flush:
        sys.stdout.flush()

def right(times: int = 1, flush: bool = False) -> None:
    """
    Print in the console _Arrow right_. \r
    """
    sys.stdout.write(f"{specials.ESC}[{times}C")
    if flush:
        sys.stdout.flush()

def down(times: int = 1, flush: bool = False) -> None:
    """
    Print in the console _Arrow down_. \r
    """
    sys.stdout.write(f"{specials.ESC}[{times}B")
    if flush:
        sys.stdout.flush()

def left(times: int = 1, flush: bool = False) -> None:
    """
    Print in the console _Arrow left_. \r
    """
    sys.stdout.write(f"{specials.ESC}[{times}D")
    if flush:
        sys.stdout.flush()

def home(flush: bool = False) -> None:
    """
    Print in the console _Home_. \r
    Equivalent to:
    ```python
        goto(maths.Size(1,1))
    ```
    """
    sys.stdout.write(f"{specials.ESC}[H")
    if flush:
        sys.stdout.flush()
        
def fin(flush: bool = False) -> None:
    """
    Print in the console _Fin_. \r
    Equivalent to:
    ```python
        goto_column(1)
    ```
    """
    sys.stdout.write(f"{specials.ESC}[F")
    if flush:
        sys.stdout.flush()

def next_line(times: int = 1,flush: bool = False) -> None:
    """
    Print in the console `<ESC>[E`. \r
    """
    sys.stdout.write(f"{specials.ESC}[{times}E")
    if flush:
        sys.stdout.flush()

def previous_line(times: int = 1, flush: bool = False) -> None:
    """
    Print in the console `<ESC>[F`. \r
    """
    sys.stdout.write(f"{specials.ESC}[{times}F")
    if flush:
        sys.stdout.flush()

def goto_column(x: int, flush: bool = False) -> None:
    """
    Print in the console `<ESC>[<x>G`. \r
    Goto an absolute x; y remains still.
    """
    sys.stdout.write(f"{specials.ESC}[{x}G")
    if flush:
        sys.stdout.flush()

def goto(position: maths.Size, flush: bool = False) -> None:
    """
    Print in the console `<ESC>[<x>;<y>H`.` \r
    Goto a x; y position in the terminal.
    """
    sys.stdout.write(f"{specials.ESC}[{position.x};{position.y}H")
    if flush:
        sys.stdout.flush()

def clear_line(times: int = 1, flush: bool = False) -> None:
    """
    Print in the console `<ESC>[K`. \r
    """
    sys.stdout.write(f"{specials.ESC}[{times}K")
    if flush:
        sys.stdout.flush()

def clear_to_bottom(flush: bool = False) -> None:
    """
    Print in the console `<ESC>[J`.
    Clears to bottom the console. 
    """
    sys.stdout.write(f"{specials.ESC}[J")
    if flush:
        sys.stdout.flush()

def scroll(lines: int, flush: bool = False) -> None:
    """
    Print in the console `<ESC>[<lines>{S/T}`.
    Scrolls the console. Negative `lines` scrolls up, positive scrolls down.
    """
    if lines == 0:
        pass
    elif lines < 0:
        sys.stdout.write(f"{specials.ESC}[{abs(lines)}S")
    else:
        sys.stdout.write(f"{specials.ESC}[{lines}T")

    if flush:
        sys.stdout.flush()

def cursor_save_position(flush: bool = False) -> None:
    """
    Print in the console `<ESC>[s`.
    """  
    sys.stdout.write(f"{specials.ESC}[s")
    if flush:
        sys.stdout.flush()

def cursor_restore_position(flush: bool = False) -> None:
    """
    Print in the console `<ESC>[u`.
    """  
    sys.stdout.write(f"{specials.ESC}[u")
    if flush:
        sys.stdout.flush()

def cursor_show(flush: bool = False) -> None:
    """
    Print in the console `<ESC>[?25h`.
    """  
    sys.stdout.write(f"{specials.ESC}[?25h")
    if flush:
        sys.stdout.flush()

def cursor_hide(flush: bool = False) -> None:
    """
    Print in the console `<ESC>[?25l`.
    """  
    sys.stdout.write(f"{specials.ESC}[?25l")
    if flush:
        sys.stdout.flush()

