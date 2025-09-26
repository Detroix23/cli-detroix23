"""
CLI - Inputs
inputs.py
"""

import os
import pathlib as path
from typing import Union, Optional

symbol_mode: dict[str, list[str]] = {
        "1": ["1", "en", "encode", "enc"],
        "2": ["2", "de", "decode", "dec"]
    }
symbol_component: dict[str, list[str]] = {
    "0": ["R", "red", "0"], 
    "1": ["G", "green", "1"],
    "2": ["B", "blue", "2"]
}
symbol_bool: dict[str, list[str]] = {
    "0": ["No", "NO", "no", "n", "N"],
    "1": ["Yes", "YES", "yes", "ye", "y", "Y"]
}
   
def list_directory(directory: path.Path) -> None:
    """
    Print the items of the given directory
    """
    print(f"*Files in `{directory}`.*")
    files: list[str] = os.listdir(directory)

    for file in files:
        if file.lower() not in ["readme.md", "readme"]:
            print(f"\t- {file}")
    print()
    return


def input(
    message: str,
    symbols: Union[dict[str, list[str]], list[str], None] = None,
    default: Optional[int] = None,
    must_validate: bool = True,
    allowed_type: type = str,
    error_message: str = "(!) - Incorrect input. Please try again.",
    max_iterations: int = 10000,
) -> str:
    """
    A genral use input sanitaizer that repeats until the user has entered a correct value.
    `Symbols` define the allowed keywords that the user can type. 
        - None (default): no restriction
        - list[str]: Only one keyword for each symbol, itself
        - dict[str, list[str]]: Each symbol can have multiple keywords.
    `Allowed` contains as keys the true machine return symbol and as value the list of all string that corrispond to that key.
    If none, all responses are correct.
    `Default` is the index of the default key of the allowed list.
    """
    valid: bool = False
    true_response: Optional[str] = None 
    i: int = 0
    if isinstance(symbols, list):
        symbols = {symbol: [symbol] for symbol in symbols}

    while not valid and i < max_iterations:
        response: str = input(message).strip()

        if response == "" and default is None:
            pass
        elif symbols is None:
            try:
                allowed_type(response)
            except:
                pass
            else:
                true_response = response
                valid = True
        elif response == "":
            if default is not None:
                true_response = list(symbols.keys())[default]
                valid = True
        else:
            for key, values in symbols.items():
                if response in values:
                    try:
                        allowed_type(response)
                    except:
                        pass
                    else:
                        true_response = key
                        valid = True
        if not valid:
            print(f"{error_message}({response}). ", end="\n")
        i += 1

    if not valid or true_response is None:
        raise ValueError(f"(X) - Can't return an invalid response.")
    print(f"R: `{true_response}`")
    return true_response

def boolean_input(
    message: str,
    default: bool = True, 
    error_message: str = "(!) - Incorrect input. Please try again.",
    max_iterations: int = 10000,
) -> bool:
    """
    A boolean (yes/ no) input sanitaizer that repeats until the user has entered a correct value.
    `Default` is the value returned in case the user just presses Enter.
    """
    valid: bool = False
    true_response: Optional[bool] = None 
    i: int = 0
    symbols: dict[bool, list[str]] = {
        False: ["No", "NO", "no", "n", "N"],
        True: ["Yes", "YES", "yes", "ye", "y", "Y"]
    }

    while not valid and i < max_iterations:
        response: str = input(message).strip()

        if response == "":
            true_response = default
            valid = True
        else:
            for key, values in symbols.items():
                if response in values:
                    true_response = key
                    valid = True
        if not valid:
            print(f"{error_message}({response}). ", end="\n")
        i += 1

    if not valid or true_response is None:
        raise ValueError(f"(X) - Can't return an invalid response.")
    print(f"R: `{true_response}`")
    return true_response



