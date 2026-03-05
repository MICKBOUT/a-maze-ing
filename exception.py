class PathNotFound(Exception):
    def __init__(self, message: str = "Path not found"):
        self.message = message
        super().__init__(self.message)
