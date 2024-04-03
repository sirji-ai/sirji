class MessageValidationError(Exception):
    """Exception raised for errors in the input message format."""

    def __init__(self, message="Invalid message format"):
        self.message = message
        super().__init__(self.message)


class MessageParsingError(Exception):
    """Exception raised for errors in parsing the message contents."""

    def __init__(self, message="Error parsing message"):
        self.message = message
        super().__init__(self.message)
