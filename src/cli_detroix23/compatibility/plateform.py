"""
CLI - Compatibility
os.py
"""
import os
from typing import Final
from enum import Enum


class Os(Enum):
    """
    Define supported systems.
    """
    WINDOWS = 0
    UNIX = 1

# Current 
OS: Final[Os] = Os.UNIX if os.name == 'posix' else Os.WINDOWS

