from ptnad.exceptions import PTNADAPIError


class FiltersAPI:
    def __init__(self, client) -> None:
        self.client = client

    def compile(self, user_filter: str) -> str:
        """
        Compile a filter.

        Args:
            user_filter (str): The filter to compile.

        Returns:
            str: The compiled filter string to use in BQL requests.

        Raises:
            PTNADAPIError: If the filter compilation fails.

        """
        data = {
            "user_filter": user_filter
        }

        try:
            response = self.client.post("/filters/compile", json=data).json()
            return response["compiled_filter"]
        except PTNADAPIError as e:
            e.operation = "compile filter"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to compile filter: {str(e)}")
