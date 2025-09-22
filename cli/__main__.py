"""
main.py
"""

import animations.screen as screen
import inputs.select_menu as select


def main() -> None:
    print("# CLI module for Python, by Detroix23.")
    
    do_screen: bool = False
    do_select: bool = True

    if do_select:
        select.main()

    if do_screen:
        screen.main()


if __name__ == "__main__":
    main()