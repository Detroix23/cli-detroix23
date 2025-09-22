"""
CLI - Base
models.py
Easy formatting with premade templates.
"""

import base.style as style

def select_gh_style(message: str, start: str = "?", usage: str = "[↑ ↓ - Enter to accept]") -> str:
        """
        Return a nicely formatted prompt message
        """
        return f"{style.Text.BOLD}{style.Color.LIGHT_GREEN}{start}\
{style.Color.WHITE} {message}\
{style.OFF_BOLD}{style.Color.LIGHT_CYAN} {usage}{style.END}"