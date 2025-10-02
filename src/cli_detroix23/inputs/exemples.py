"""
CLI - Inputs
exemples.py
"""
import base.specials as specials
import inputs.keys as keys

def run_basic_keys() -> None:
    """
    Test the getter of key.
    """
    print()

    k1 = keys.Key("Arrow up", "\x1b[A", "\x1b[A")
    print(f"({k1.get()})")
    print(repr(k1))

    print()

    print("\nGET KEY.", end="\n")
    while True:
        key: str = keys.get_key()
        mapped: list[str] = specials.filter_map(specials.NICE_MAP, key)
        print(mapped, end="\r")

if __name__ == "__main__":
    run_basic_keys()