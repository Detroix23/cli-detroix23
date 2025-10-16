"""
CLI - Inputs
exemples.py
"""
import base.specials as specials
import base.controls as controls
import inputs.keys as keys
import inputs.fetch

def run_basic_keys() -> None:
    """
    Test the getter of key.
    """
    history: list[keys.Key] = list()
    history_length: int = 2

    def append_to_history(hist: list[keys.Key], key: keys.Key) -> None:
        hist.append(key)
        if len(history) > history_length:
            hist.pop(0)

    print("\nGET KEY.", end="\n")
    while True:
        append_to_history(history, inputs.fetch.get())
        
        for key in history:
            mapped: list[str] = specials.filter_map(specials.NICE_MAP, key.key())
            good: bool = inputs.fetch.compare(keys.Keys.DOWN, key)
            print(f"\r{mapped}, key={repr(key)}, good={good}.")
        
        controls.up(len(history))
        controls.clear_to_bottom()

if __name__ == "__main__":
    run_basic_keys()