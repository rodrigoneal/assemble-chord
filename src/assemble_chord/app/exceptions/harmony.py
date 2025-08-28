class SambaProgressionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NotaInvalidaError(Exception):
    def __init__(self, message):
        super().__init__(message)
