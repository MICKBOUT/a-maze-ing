from typing import Optional


class PathNotFound(Exception):
    """
    Exception raised when no path is found from the entry point to the exit
    point in the maze.
    """
    def __init__(self, message: str = "Path not found"):
        self.message = message
        super().__init__(self.message)


class MisplaceCell(Exception):
    """
    Exception raised when a key cell is placed on the 42 logo in the maze.
    """
    def __init__(self, message: str = "Key cell place on 42 logo"):
        self.message = message
        super().__init__(self.message)


class ConfigFileError(Exception):
    """
    Exception raised for errors in the configuration file.
    """
    def __init__(self,
                 message: str = "config file",
                 line: Optional[str] = None,
                 line_nb: Optional[int] = None) -> None:
        self.message = "\033[0;31mConfigFileError\033[0m: "
        self.message += message

        if line is not None:
            self.message += f" in '{line}'"

        if line_nb is not None:
            self.message += f" (line {line_nb})"
        super().__init__(self.message)
