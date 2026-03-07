"""
# CLI - Inputs.
src/cli_detroix23/inputs/windows.py  
"""

from typing import Optional

try: 
    import msvcrt
    
    from cli_detroix23.compatibility import platform
    from cli_detroix23.base import specials
    from cli_detroix23.inputs import keys
    
    def get_key(*, allow_keyboard_interrupt: bool) -> keys.Key:
        """
        Get key at one moment. \n
        Windows only, using `msvcrt`.
        """
        key: bytes = msvcrt.getch()  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
        # Special key prefix on Windows
        if key == specials.WINDOWS:  
            key += msvcrt.getch()
            # debug.debug_print(f"inputs.window.get_key() key: {key}")
        # Ctrl+C.
        elif key == b"\x03" and allow_keyboard_interrupt:
            raise KeyboardInterrupt(f"(X) - Keyboard interrupt while getting key ({repr(key)}).")
        
        key_object: Optional[keys.Key] = None
        
        if key[0] in specials.MSVCRT_GETCH_SPECIALS:
            for default_key in keys.Keys.to_dict().values():
                if key == default_key.key(platform.Os.WINDOWS):
                    key_object = default_key
                    break
            
            if key_object is None:
                raise KeyError(f"(X) Specials key unbound ({repr(key)}).")

        else:
            key_object = keys.Key.new_common(key.decode(encoding='utf-8', errors='strict'))

        return key_object

except ModuleNotFoundError as exception:
    print("(X) inputs.windows Module `msvcrt` not found. Surely wrong OS ?")
    print("Details: \n")
    print(exception)
