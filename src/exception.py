class PathNotFound(Exception):
    def __init__(self, message: str = "Path not found"):
        self.message = message
        super().__init__(self.message)


class ConfigFileError(Exception):
    def __init__(self,
                 message: str = "config file",
                 line: str = None,
                 line_nb: int = None):
        self.message = "ConfigFileError: "
        self.message += message

        if line is not None:
            self.message += f" in '{line}'"
        super().__init__(self.message)

        if line_nb is not None:
            self.message += f" (line {line_nb})"
        super().__init__(self.message)
