"""
# CLI - Inputs
src/cli_detroix23/inputs/unix.py
"""
import sys
try:
    import tty

    from cli_detroix23.compatibility import unix
    from cli_detroix23.base import specials
    from cli_detroix23.inputs import keys


    def get_key(*, allow_keyboard_interrupt: bool) -> keys.Key:
        """
        Get the current pressed key on Unix systems. \r
        Old settings are stored in `compatibility.unix`.
        Return a key of class `inputs.keys.Key`.
        """
        key: str

        try:
            tty.setraw(unix.FILE_ID)

            # compatibility.unix.test_present_settings()

            key = sys.stdin.read(1)
            # Handle arrow keys (escape sequences).
            if key == specials.ESC:
                key += sys.stdin.read(2)
            # Ctrl+C.
            elif key == "\x03" and allow_keyboard_interrupt:
                raise KeyboardInterrupt(f"(X) - Keyboard interrupt while getting key ({repr(key)}).")

            unix.set_to_default()
            return keys.Key.new_common(key)

        finally:
            unix.set_to_default()
    
except ModuleNotFoundError as exception:
    print("(!) inputs.unix Module `tty` and `termios` not found. Surely wrong OS ?")
    print("Details: \n")
    print(exception)

