"""
CLI - Base
models.py
Easy formatting with premade templates.
Prefixes:
    "$" select
    "#" string input
    "?" boolean input

"""

import base.style as style

def select_gh_style(message: str, start: str = "$", usage: str = "[↑ ↓ - Enter to accept]") -> str:
    """
    Return a nicely formatted prompt message for a select menu.
    """
    return f"{style.Text.BOLD}{style.Color.LIGHT_GREEN}{start}\
{style.Color.WHITE} {message}\
{style.OFF_BOLD}{style.Color.LIGHT_CYAN} {usage}{style.END}"

def input_gh_style(message: str, start: str = "#", usage: str = "", default: str = "") -> str:
    """
    Return a nicely formatted prompt message for an string input.
    Usage is already in [], and default in (), and colon is present.
    """
    string: str = f"{style.Text.BOLD}{style.Color.LIGHT_GREEN}{start}"
    string += f"{style.Color.WHITE} {message}{style.OFF_BOLD}"
    if usage:
        string += f"{style.Color.LIGHT_CYAN} [{usage}]{style.END}"
    if default:
        string += f"{style.Color.LIGHT_CYAN} ({default}){style.END}"
    string += f"{style.Color.WHITE}: {style.END}"

    return string

def bool_gh_style(message: str, start: str = "?", usage: str = "y/ n", default: str = "y") -> str:
    """
    Return a nicely formatted prompt message for a boolean input.
    Usage is already in [], and default in (), and colon is present.
    """
    string: str = f"{style.Text.BOLD}{style.Color.LIGHT_GREEN}{start}"
    string += f"{style.Color.WHITE} {message}{style.OFF_BOLD}"
    if usage:
        string += f"{style.Color.LIGHT_CYAN} [{usage}]{style.END}"
    if default:
        string += f"{style.Color.LIGHT_CYAN} ({default}){style.END}"
    string += f"{style.Color.WHITE}: {style.END}"

    return string