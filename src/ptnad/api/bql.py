from typing import Any, Dict

from ptnad.exceptions import PTNADAPIError, ValidationError


class BQLResponse:
    def __init__(self, result: Any, took: int, total: int, debug: Dict[str, Any] | None = None) -> None:
        self.result = result
        self.took = took
        self.total = total
        self.debug = debug

    def __str__(self) -> str:
        response_dict = {
            "result": self.result,
            "took": self.took,
            "total": self.total
        }
        if self.debug is not None:
            response_dict["debug"] = self.debug
        return str(response_dict)

class BQLAPI:
    def __init__(self, client) -> None:
        self.client = client

    def execute(self, query: str, source: str = "2") -> Any:
        """
        Execute a BQL query on a specific source.

        Args:
            query (str): The BQL query to execute.
            source (str): The identifier of the storage to query. Defaults to "2" (live).

        Returns:
            Any: The result of the query execution.

        Raises:
            PTNADAPIError: If there's an error executing the query.

        """
        try:
            response = self._send_query(query, source)
            return response["result"]
        except PTNADAPIError as e:
            e.operation = "execute BQL query"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to execute BQL query: {str(e)}")

    def execute_raw(self, query: str, source: str = "2") -> BQLResponse:
        """
        Execute a BQL query on a specific source and return the full response.

        Args:
            query (str): The BQL query to execute.
            source (str): The identifier of the storage to query. Defaults to "2" (live).

        Returns:
            BQLResponse: An object containing the query results, execution time, total hits, and debug info.

        Raises:
            PTNADAPIError: If there's an error executing the query.

        """
        try:
            response = self._send_query(query, source)
            return BQLResponse(
                result=response["result"],
                took=response["took"],
                total=response["total"],
                debug=response.get("debug")
            )
        except PTNADAPIError as e:
            e.operation = "execute BQL query"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to execute BQL query: {str(e)}")

    def _send_query(self, query: str, source: str) -> Dict[str, Any]:
        """
        Send a BQL query to the API.

        Args:
            query (str): The BQL query to execute.
            source (str): The identifier of the storage to query.

        Returns:
            Dict[str, Any]: The raw response from the API.

        Raises:
            ValidationError: If the query is invalid or the API returns an error.

        """
        headers = {
            "Content-Type": "text/plain",
            "Referer": self.client.base_url
        }
        response = self.client.post(
            "/bql",
            params={"source": source},
            data=query,
            headers=headers,
            cookies=self.client.session.cookies.get_dict()
        ).json()

        if "error" in response:
            raise ValidationError(response["error"])

        return response
