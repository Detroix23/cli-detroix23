"""
CLI - Inputs
select_menu.py
"""
import sys

import compatibility.plateform as plateform
import base.style as style
import inputs.keys as keys

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
        return keys.get_key()

    def _clear_menu(self, num_lines: int) -> None:
        """
        Clear the menu from terminal
        """
        for _ in range(num_lines):
            # Move up and clear line
            sys.stdout.write('\x1b[1A\x1b[2K')  
        sys.stdout.flush()
    
    def _draw_menu(self) -> None:
        """
        Draw the menu with current selection highlighted
        """
        print(self.prompt)
        for i, option in enumerate(self.options):
            if i == self.selected_index:
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
        Return a string, the choosen index.
        """
        try:
            # Hide cursor.
            sys.stdout.write('\x1b[?25l')

            self._draw_menu()
            
            while True:
                key: keys.Key = self._get_key()
                # Handle arrow keys
                if plateform.OS == plateform.Os.UNIX:
                    if key == '\x1b[A':  # Up arrow
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif key == '\x1b[B':  # Down arrow
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif key == '\r' or key == '\n':  # Enter
                        break
                    elif key == '\x03':  # Ctrl+C
                        raise KeyboardInterrupt(f"{style.Color.YELLOW}(!) - Keyboard Interrupt. {style.END}")

                elif plateform.OS == plateform.Os.WINDOWS:  
                    if key == 'H':  # Up arrow
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif key == 'P':  # Down arrow
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif key == '\r':  # Enter
                        break
                    elif key == '\x03':  # Ctrl+C
                        raise KeyboardInterrupt(f"{style.Color.YELLOW}(!) - Keyboard Interrupt. {style.END}")
                else:
                    raise OSError(f"(X) - SelectMenu.show - Unsupported OS ({plateform.OS}).")            


                # Clear and redraw menu
                self._clear_menu(len(self.options) + 1)
                self._draw_menu()
        except KeyboardInterrupt:
            raise KeyboardInterrupt(f"{style.Color.YELLOW}(!) - Keyboard Interrupt. {style.END}")
        
        finally:
            # Show cursor again
            sys.stdout.write('\x1b[?25h')
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
    sel = menu.show()
    print(sel)