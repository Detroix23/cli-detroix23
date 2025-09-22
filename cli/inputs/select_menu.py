# type: ignore[reportPossiblyUnboundVariable]

import sys
import os

UNIX_LIKE: bool = os.name == 'posix'
if UNIX_LIKE:
    import termios
    import tty
else:
    import msvcrt

import base.style as style

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

    def _get_key(self) -> str:
        """
        Get a single keypress from stdin
        """
        if UNIX_LIKE:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                key = sys.stdin.read(1)
                # Handle arrow keys (they send escape sequences)
                if key == '\x1b':  # ESC sequence
                    key += sys.stdin.read(2)
                return key
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        else:  # Windows
            key = msvcrt.getch()
            if key == b'\xe0':  # Special key prefix on Windows
                key += msvcrt.getch()
            return key.decode('utf-8', errors='ignore')

    def _clear_menu(self, num_lines) -> None:
        """
        Clear the menu from terminal
        """
        for _ in range(num_lines):
            sys.stdout.write('\x1b[1A\x1b[2K')  # Move up and clear line
        sys.stdout.flush()
    
    def _draw_menu(self) -> None:
        """
        Draw the menu with current selection highlighted
        """
        print(self.prompt)
        for i, option in enumerate(self.options):
            if i == self.selected_index:
                print(f"{self.select_character}{option}")  # Highlight selected option
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
            # Hide cursor
            sys.stdout.write('\x1b[?25l')
            
            self._draw_menu()
            
            while True:
                key: str = self._get_key()
                
                # Handle arrow keys
                if UNIX_LIKE:
                    if key == '\x1b[A':  # Up arrow
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif key == '\x1b[B':  # Down arrow
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif key == '\r' or key == '\n':  # Enter
                        break
                    elif key == '\x03':  # Ctrl+C
                        raise KeyboardInterrupt
                else:  # Windows
                    if key == 'H':  # Up arrow
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif key == 'P':  # Down arrow
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif key == '\r':  # Enter
                        break
                    elif key == '\x03':  # Ctrl+C
                        raise KeyboardInterrupt
                
                # Clear and redraw menu
                self._clear_menu(len(self.options) + 1)
                self._draw_menu()
        
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