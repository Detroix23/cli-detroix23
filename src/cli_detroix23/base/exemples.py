"""
CLI - Base / Style.
exemples.py
"""
import base.style as style
import base.code as code

def main() -> None:
    style.Style.display_all_rendition_subset()

    print(f"1: {code.code_clean(style.Color.BLACK)}.")
    print(f"2: {code.code_clean_all(style.Color.BLACK + style.END)}.")

    c1 = code.Code(style.Text.BOLD + style.Color.CYAN)
    print(f"c1-add: {c1 + 'A' + style.END}.")
    print(f"c1-repr: {repr(c1)}.")
    c2 = code.Code(style.Text.BLINK2 + style.Back.GRAY)
    print(f"c2-repr: {repr(c2)}.")

    c3: code.Code = c1.fuse(c2)
    print(f"c3-add: {c3 + 'A' + style.END}.")
    print(f"c3-repr: {repr(c3)}.")


    style_attributes: dict[str, str] = {
        key: value for key, value in style.Style.__dict__.items() 
        if not key.startswith("__")
        if isinstance(value, str)
    }
    print("\n", style_attributes)

    style.printc(f"█", style.Color.DIM)
    style.printc(f"█", style.Color.DIMMER)


if __name__ == "__main__":
    main()