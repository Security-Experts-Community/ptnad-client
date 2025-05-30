from typing import Any, Dict, List, Optional

from ptnad.exceptions import PTNADAPIError


class SourcesAPI:
    def __init__(self, client) -> None:
        self.client = client

    def get_sources(self, search: str | None = None, ordering: str | None = None) -> List[Dict[str, Any]]:
        """
        Get a list of storage sources.

        Args:
            search (Optional[str]): Keyword to filter the sources. Search is performed among fields:
                name, description, username, first_name, last_name, middle_name.
            ordering (Optional[str]): Field to sort the results by. Sorting is possible by all fields
                in the schema. For sorting by usernames of users who created the storage, use the
                user__username field. To sort in descending order, add a minus sign before the field
                name (e.g., ordering=-id).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing storage source information.

        Raises:
            PTNADAPIError: If there's an error retrieving the sources.

        """
        url_params = {}
        if search:
            url_params["search"] = search
        if ordering:
            url_params["ordering"] = ordering

        try:
            response = self.client.get("/sources", params=url_params).json()
            return response["results"]
        except PTNADAPIError as e:
            e.operation = "get sources"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get sources: {str(e)}")

    def get_source(self, source_id: int) -> Dict[str, Any]:
        """
        Get information about a specific storage source by its id.

        Args:
            source_id (int): ID of the storage source.

        Returns:
            Dict[str, Any]: Information about the storage source.

        Raises:
            PTNADAPIError: If there's an error retrieving the storage source.

        """
        try:
            response = self.client.get(f"/sources/{source_id}").json()
            return response
        except PTNADAPIError as e:
            e.operation = f"get source {source_id}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get source {source_id}: {str(e)}")
