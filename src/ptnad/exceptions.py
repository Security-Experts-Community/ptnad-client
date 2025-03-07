class PTNADException(Exception):
    """Base exception for all PTNAD-related errors."""

class PTNADAPIError(PTNADException):
    """Exception raised for errors in the API."""
    def __init__(self, message, status_code=None, response=None, operation=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        self.operation = operation

        super().__init__(self.message)

    def __str__(self):
        operation_prefix = f"Failed to {self.operation}. " if self.operation else ""
        base_message = super().__str__()
        return f"{operation_prefix}{base_message}"

class AuthenticationError(PTNADException):
    """Exception raised for authentication errors."""

class ValidationError(PTNADException):
    """Exception raised for validation errors."""
