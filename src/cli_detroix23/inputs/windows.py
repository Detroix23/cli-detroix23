"""
# CLI - Inputs
src/cli_detroix23/inputs/windows.py  
"""
try: 
    import msvcrt
    
    from cli_detroix23.base import specials
    from cli_detroix23.inputs import keys

    def get_key(*, allow_keyboard_interrupt: bool) -> keys.Key:
        """
        Get key at one moment. \n
        Windows only, using `msvcrt`.
        """
        key: bytes = msvcrt.getch()       # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
        # Special key prefix on Windows
        if key == specials.WINDOWS:  
            key += msvcrt.getch()
            print(f"\ninputs.window.get_key() key: {key}\n")
        # Ctrl+C.
        elif key == b"\x03" and allow_keyboard_interrupt:
            raise KeyboardInterrupt(f"(X) - Keyboard interrupt while getting key ({repr(key)}).")
        
        key_object: keys.Key
        if key[0] in specials.MSVCRT_GETCH_SPECIALS:
            key_object = ...
        else:
            key_object = keys.Key.new_common(key.decode('utf-8', errors='strict'))

        return key_object

except ModuleNotFoundError as exception:
    print("(X) inputs.windows Module `msvcrt` not found. Surely wrong OS ?")
    print("Details: \n")
    print(exception)
