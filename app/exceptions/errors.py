class InputIsNotAlphabet(Exception):
    """raise when received input is not an alphabet"""

    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)


class TemporarilySuspendService(Exception):
    """raise when cannot connect 3rd party: Free Dictionary API"""

    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)


class NotFound(Exception):
    """raise when not found"""

    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)


class FileExists(Exception):
    """raise when file exist"""

    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)


class AlreadyProcessed(Exception):
    """raise when something have processed"""

    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)
