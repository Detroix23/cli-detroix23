import dataclasses

@dataclasses.dataclass
class Settings:
    args: set[str] = dataclasses.field(default_factory=set[str])
    user_in: bool = False
    choice: str = ""
    enable_debug: bool = False
    
    def read_arguments(self) -> None: ...
