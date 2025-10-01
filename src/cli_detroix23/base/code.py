"""
CLI - Style/ Base
code.py
"""
from typing import Union

import base.style as base

class Code:
    """
    Describe an or multiple escape code of VT-100 charset.
    """
    string: str
    codes: list[int]

    def __init__(self, string: str = "", codes: list[int] = list()) -> None:
        """
        Create (clean, divide and fuse) a `string`.
        If `codes` is passed, uses them instead.
        """
        self.codes = code_clean_all(string) if not codes else codes
        self.string = code_fuse(self.codes)

    def __str__(self) -> str:
        """
        Print directly the main string, ready to format.
        """
        return self.string
    
    def __repr__(self) -> str:
        """
        Print debug informations, with no formatting.
        """
        return f"Code(string: str = {repr(self.string)}, codes: list[int] = {self.codes})"
    
    def fuse(self, other: 'Code') -> 'Code':
        return Code(codes=self.codes + other.codes)

    def __add__(self, other: object) -> Union[str, 'Code']:
        """
        Handles addition between: \n
            - str -> str \r
            - Code -> Code \r
        """
        if isinstance(other, str):
            return self.string + other
        elif isinstance(other, Code):
            return Code(codes=self.codes + other.codes)
        else:
            raise ValueError(f"(X) - `Code` addiction must be `str` or `Code` ({repr(other)}).")
 

def code_clean(string: str) -> int:
    """
    Return a string cleansed of its first escape character.
    """
    impure: set[str] = {base.ESC, "[", "m"}
    cleaned: str = ""

    for char in string:    
        if char not in impure:
            cleaned += char

    return int(cleaned)

def code_clean_all(string: str) -> list[int]:
    """
    Return a list of str, exploded from a str on each escape character and others. \n
    Use for codes.
    """
    clean: list[int] = list()
    if string:
        splitted: list[str] = string.split(base.ESC)
        if not splitted[0]:
            splitted.pop(0)
        clean = [code_clean(string) for string in splitted]

    return clean

def code_fuse(codes: list[int]) -> str:
    """
    Merges together codes into a multi-style character.
    """
    string: str = base.ESC + "["
    for index, code in enumerate(codes):
        string += str(code)
        if index < len(codes) - 1:
            string += ";"
    string += "m"

    return string
