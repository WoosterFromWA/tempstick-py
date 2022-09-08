class TempStickException(Exception):
    """Base class for other exceptions"""

    def __init__(self, message="Generic error"):
        self.message = message
        super().__init__(self.message)


class FilterRemovesRange(TempStickException):
    """Exception raised when provided filter would filter entire range."""

    def __init__(
        self,
        filter=None,
        range=None,
        range_lower=None,
        range_upper=None,
        message="Entire range removed by filter.",
    ):
        self.filter = filter
        self.range = range if range else (range_lower, range_upper)
        self.range_lower = range_lower
        self.range_upper = range_upper
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return "{} -> {}".format(self.filter, self.message)


class ResponseError(Exception):
    def __init__(
        self, type: str, message="Invalid response from target.", *args: object
    ) -> None:
        self.response_type = type
        self.message = message
        super().__init__(self.message)


class InvalidApiKeyError(ResponseError):
    """Exception raised when an invalid API key is used."""

    def __init__(
        self,
        type: str,
        description: str,
        message="Invalid API key used.",
        *args: object
    ) -> None:
        self.description = description
        self.type = type
        self.message = message

        super().__init__(self.type, self.message, *args)

    def __str__(self) -> str:
        # debug_print("type", self.type, self.__name__)
        # print("hello")
        # value = self.message
        value = "{type}|{description} -> {message}".format(
            type=self.type, description=self.description, message=self.message
        )
        return value
