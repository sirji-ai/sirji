class MessageMissingPropertyError(Exception):
    """Exception raised for errors in the input message format."""

    def __init__(self, message="Message does not contain required property"):
        self.message = message
        super().__init__(self.message)

class MessageUnRecognizedActionError(Exception):
    """Exception raised for errors in the input message format."""

    def __init__(self, message="Action is not recognized"):
        self.message = message
        super().__init__(self.message)

class MessageIncorrectFormatError(Exception):
    """Exception raised for errors in the input message format."""

    def __init__(self, message="Message must start and end with ***"):
        self.message = message
        super().__init__(self.message)

class MessageLengthConstraintError(Exception):
    """Exception raised for errors in the input message format."""

    def __init__(self, message="Message does not meet the minimum length requirement"):
        self.message = message
        super().__init__(self.message)

class MessageMultipleActionError(Exception):
    """Exception raised for errors in the input message format."""

    def __init__(self, message="Message contains more than one ACTION keyword"):
        self.message = message
        super().__init__(self.message)