"""
CLI - Inputs
exemples.py
"""
import base.specials as specials
import inputs.keys as keys
import inputs.fetch

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
        key: keys.Key = inputs.fetch.get()
        mapped: list[str] = specials.filter_map(specials.NICE_MAP, key.key())
        good: bool = inputs.fetch.compare(keys.Keys.DOWN, key)
        print(f"\r{mapped}, key={repr(key)}, good={good}.  ", end="\r")

if __name__ == "__main__":
    run_basic_keys()