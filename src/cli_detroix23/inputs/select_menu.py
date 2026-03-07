"""
# CLI - Inputs
src/cli_detroix23/inputs/select_menu.py
"""

import sys

from cli_detroix23.compatibility import defaults, debug
from cli_detroix23.base import style, controls
from cli_detroix23.inputs import fetch, keys

class SelectMenu:
    """
    Select with arrow. Most of the code is from Claude.
    """
    options: list[str]
    prompt: str
    selected_index: int

    select_character: str

    def __init__(self, options: list[str], prompt: str = "Select an option:") -> None:
        self.options: list[str] = options
        self.prompt: str = prompt
        self.selected_index: int = 0

        self.select_character: str = "> "

    def _get_key(self) -> keys.Key:
        """
        Get a single keypress from stdin
        """
        return fetch.get()

    def _clear_menu(self, num_lines: int) -> None:
        """
        Clear the menu from terminal, if isn't `ENABLE_DEBUG`.
        """
        if debug.ENABLE_DEBUG:
            return

        for _ in range(num_lines):
            controls.up()
            controls.clear_line(2)  
        sys.stdout.flush()
    
    def _draw_menu(self) -> None:
        """
        Draw the menu with current selection highlighted
        """
        print(self.prompt)
        for index, option in enumerate(self.options):
            if index == self.selected_index:
                # Highlight selected option (style).
                style.printc(
                    f"{self.select_character}{option}",
                    style=style.Color.CYAN + style.Text.BOLD
                ) 
            else:
                print(f"{' ' * len(self.select_character)}{option}")
        # sys.stdout.flush()
    
    def show(self) -> str:
        """
        Display the menu and handle user input.
        Call to display to user.
        Return a string, the chosen index.
        """
        try:
            controls.cursor_hide()

            self._draw_menu()
            
            while True:
                key: keys.Key = self._get_key()
                # Handle arrow keys
                if key == keys.Keys.UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif key == keys.Keys.DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif key == keys.Keys.LINE or key == keys.Keys.RETURN:
                    break
                elif key == keys.Keys.INTERRUPT:
                    raise KeyboardInterrupt(f"{style.Color.YELLOW}{defaults.LOG_INFO}Keyboard Interrupt. {style.END}")      

                # Clear and redraw menu
                self._clear_menu(len(self.options) + 1)
                self._draw_menu()
        except KeyboardInterrupt:
            raise KeyboardInterrupt(f"{style.Color.YELLOW}{defaults.LOG_INFO}Keyboard Interrupt. {style.END}")
        
        finally:
            # Show cursor again
            controls.cursor_show()
            sys.stdout.flush()
        
        return self.options[self.selected_index]


def main() -> None:
    """
    File main.
    """
    menu_options: list[str] = [
        "Hello!",
        "Goodbye",
        "Another"
    ]
    menu = SelectMenu(
        options=menu_options,
        prompt="Main CLI test: "
    )
    sel: str = menu.show()
    print(sel)
