"""
CLI - Inputs
arguments.py
"""
import sys
import dataclasses

@dataclasses.dataclass
class Settings:
    """
    All options that can be enabled by arguments.
    """
    args: set[str] = dataclasses.field(default_factory=set[str])
    user_in: bool = False
    choice: str = ""
    enable_debug: bool = False

    def read_arguments(self) -> None:
        """
        Read execution arguments and update the `Settings` instance.
        """
        self.args = set(sys.argv[1:])

        for arg in self.args:
            if arg in {"-d", "--debug"}:
                self.enable_debug = True






