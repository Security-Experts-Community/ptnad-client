import re
from typing import Any, Dict, List, Union

from ptnad.exceptions import PTNADAPIError, ValidationError


class RepListsAPI:
    def __init__(self, client) -> None:
        self.client = client

    def _get_lists_data(self, search: str | None = None, ordering: str | None = None,
                        limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Internal method to get the full response from the Replists API.

        Args:
            search (Optional[str]): Keyword to filter the lists by name, description, or vendor name.
            ordering (Optional[str]): Field to sort the results by (id, name, color, type, created, modified, items_count, description, vendor__name). Use prefix '-' for descending order.
            limit (int): Maximum number of lists to return.
            offset (int): Number of lists to skip.

        Returns:
            Dict[str, Any]: Full API response

        Raises:
            PTNADAPIError: If there's an error retrieving the lists.

        """
        params = {}
        if search:
            params["search"] = search
        if ordering:
            params["ordering"] = ordering
        params["limit"] = limit
        params["offset"] = offset

        try:
            response = self.client.get("/replists", params=params).json()
            return response
        except PTNADAPIError as e:
            e.operation = "get reputation lists"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get reputation lists: {str(e)}")

    def get_lists(self, search: str | None = None, ordering: str | None = None,
                  limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get a list of reputation lists.

        Args:
            search (Optional[str]): Keyword to filter the lists by name, description, or vendor name.
            ordering (Optional[str]): Field to sort the results by (id, name, color, type, created, modified, items_count, description, vendor__name). Use prefix '-' for descending order.
            limit (int): Maximum number of lists to return (default: 100).
            offset (int): Number of lists to skip (default: 0).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing reputation list information.

        Raises:
            PTNADAPIError: If there's an error retrieving the lists.

        """
        response = self._get_lists_data(search, ordering, limit, offset)
        return response["results"]

    def get_all_lists(self, search: str | None = None, ordering: str | None = None,
                      limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all reputation lists using pagination.

        Args:
            search (Optional[str]): Keyword to filter the lists by name, description, or vendor name.
            ordering (Optional[str]): Field to sort the results by (id, name, color, type, created, modified, items_count, description, vendor__name). Use prefix with '-' for descending order.
            limit (int): Number of lists to fetch per request (default: 100).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing all reputation list information.

        Raises:
            PTNADAPIError: If there's an error retrieving the lists.

        """
        all_lists = []
        offset = 0

        while True:
            response = self._get_lists_data(search, ordering, limit, offset)
            lists = response["results"]
            all_lists.extend(lists)

            if response["next"] is None:
                break

            offset += limit

        return all_lists

    @staticmethod
    def _is_valid_slug(name: str) -> bool:
        """
        Check if the given name is a valid slug.

        A valid slug consists of letters, numbers, underscores or hyphens.
        """
        return bool(re.match(r"^[a-zA-Z0-9_-]+$", name))

    def create_list(self, name: str, type: str, color: str, description: str | None = None,
                    content: Union[str, List[str], None] = None, external_key: str | None = None) -> Dict[str, Any]:
        """
        Create a new reputation list.

        Args:
            name (str): Name of the reputation list. Must be a valid slug (letters, numbers, underscores, hyphens).
            type (str): Type of the reputation list ('ip', 'dn', 'uri', or 'md5').
            color (str): Color code for the reputation list ('0' to '7').
            description (Optional[str]): Description of the reputation list.
            content (Optional[Union[str, List[str]]]): Content of the reputation list. Can be a string or a list of strings that will be joined with newlines.
            external_key (Optional[str]): External key for the reputation list.

        Returns:
            Dict[str, Any]: Information about the created reputation list.

        Raises:
            ValidationError: If the input parameters are invalid.
            PTNADAPIError: If there's an error creating the list.

        """
        if not self._is_valid_slug(name):
            raise ValidationError("Name must be a valid slug consisting of letters, numbers, underscores or hyphens.")

        data = {
            "name": name,
            "type": type,
            "color": color,
        }
        if description:
            data["description"] = description
        if content:
            # Convert list of strings to newline-separated string if needed
            if isinstance(content, list):
                data["content"] = "\n".join(content)
            else:
                data["content"] = content
        if external_key:
            data["external_key"] = external_key

        try:
            response = self.client.post("/replists", json=data)
            if response.status_code == 201:
                return response.json()
            error_message = response.json() if response.headers.get("Content-Type") == "application/json" else response.text
            raise PTNADAPIError(f"Failed to create reputation list. Status code: {response.status_code}. Error: {error_message}")
        except PTNADAPIError as e:
            e.operation = "create reputation list"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to create reputation list: {str(e)}")


    def get_list(self, list_id: int) -> Dict[str, Any]:
        """
        Get information about a specific reputation list.

        Args:
            list_id (int): ID of the reputation list.

        Returns:
            Dict[str, Any]: Information about the reputation list.

        Raises:
            PTNADAPIError: If there's an error retrieving the list.

        """
        try:
            response = self.client.get(f"/replists/{list_id}").json()
            return response
        except PTNADAPIError as e:
            e.operation = f"get reputation list {list_id}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get reputation list {list_id}: {str(e)}")

    def update_list(self, list_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update a reputation list.

        Args:
            list_id (int): ID of the reputation list to update.
            **kwargs: Fields to update (color, name, type, description, content).

        Returns:
            Dict[str, Any]: Updated information about the reputation list.

        Raises:
            PTNADAPIError: If there's an error updating the list.

        """
        try:
            response = self.client.patch(f"/replists/{list_id}", json=kwargs).json()
            return response
        except PTNADAPIError as e:
            e.operation = f"update reputation list {list_id}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to update reputation list {list_id}: {str(e)}")

    def delete_list(self, list_id: int) -> None:
        """
        Delete a reputation list.

        Args:
            list_id (int): ID of the reputation list to delete.

        Raises:
            PTNADAPIError: If there's an error deleting the reputation list.

        """
        try:
            response = self.client.delete(f"/replists/{list_id}")
            if response.status_code != 204:
                raise PTNADAPIError(f"Failed to delete reputation list {list_id}: {response.text}")
        except PTNADAPIError as e:
            e.operation = f"delete reputation list {list_id}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to delete reputation list {list_id}: {str(e)}")

    def add_dynamic_list_item(self, external_key: str, value: str, attributes: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Add an item to a dynamic reputation list.

        Args:
            external_key (str): External key of the reputation list.
            value (str): Value to add to the list.
            attributes (Optional[Dict[str, Any]]): Additional attributes for the item.

        Returns:
            Dict[str, Any]: Information about the added item.

        Raises:
            PTNADAPIError: If there's an error adding the item.

        """
        try:
            response = self.client.post(f"/replists/dynamic/{external_key}/{value}", json=attributes or {})
            if response.status_code in (200, 201):
                return response.json()
            raise PTNADAPIError(f"Failed to add item to reputation list {external_key}: {response.text}")
        except PTNADAPIError as e:
            e.operation = f"add item to reputation list {external_key}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to add item to reputation list {external_key}: {str(e)}")

    def remove_item(self, external_key: str, value: str) -> None:
        """
        Remove an item from a dynamic reputation list.

        Args:
            external_key (str): External key of the reputation list.
            value (str): Value to remove from the reputation list.

        Raises:
            PTNADAPIError: If there's an error removing the item.

        """
        try:
            response = self.client.delete(f"/replists/dynamic/{external_key}/{value}")
            if response.status_code != 204:
                raise PTNADAPIError(f"Failed to remove item from reputation list {external_key}: {response.text}")
        except PTNADAPIError as e:
            e.operation = f"remove item from reputation list {external_key}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to remove item from reputation list {external_key}: {str(e)}")

    def get_dynamic_list_items(self, external_key: str, ordering: str | None = None) -> List[Dict[str, Any]]:
        """
        Get items from a dynamic reputation list.

        Args:
            external_key (str): External key of the reputation list.
            ordering (Optional[str]): Field to sort the results by (value or modified).

        Returns:
            List[Dict[str, Any]]: List of items in the reputation list.

        Raises:
            PTNADAPIError: If there's an error retrieving the items.

        """
        params = {}
        if ordering:
            params["ordering"] = ordering

        try:
            response = self.client.get(f"/replists/dynamic/{external_key}", params=params).json()
            return response["results"]
        except PTNADAPIError as e:
            e.operation = f"get items from reputation list {external_key}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get items from reputation list {external_key}: {str(e)}")

    def bulk_add_items(self, external_key: str, items: List[Dict[str, Any]]) -> None:
        """
        Add multiple items to a dynamic reputation list.

        Args:
            external_key (str): External key of the reputation list.
            items (List[Dict[str, Any]]): List of items to add, each item should have 'value' and optionally 'attrs'.

        Raises:
            PTNADAPIError: If there's an error adding the items.

        """
        try:
            self.client.post(f"/replists/dynamic/{external_key}/_bulk", json=items)
        except PTNADAPIError as e:
            e.operation = f"bulk add items to reputation list {external_key}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to bulk add items to reputation list {external_key}: {str(e)}")

    def bulk_delete_items(self, external_key: str, values: List[str]) -> None:
        """
        Delete multiple items from a dynamic reputation list.

        Args:
            external_key (str): External key of the reputation list.
            values (List[str]): List of values to delete from the list.

        Raises:
            PTNADAPIError: If there's an error deleting the items.

        """
        try:
            response = self.client.post(f"/replists/dynamic/{external_key}/_delete", json=values)
            if response.status_code != 204:
                raise PTNADAPIError(f"Failed to bulk delete items from reputation list {external_key}: {response.text}")
        except PTNADAPIError as e:
            e.operation = f"bulk delete items from reputation list {external_key}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to bulk delete items from reputation list {external_key}: {str(e)}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about reputation lists.

        Returns:
            Dict[str, Any]: Statistics about reputation lists.

        Raises:
            PTNADAPIError: If there's an error retrieving the statistics.

        """
        try:
            response = self.client.get("/replists/stats").json()
            return response
        except PTNADAPIError as e:
            e.operation = "get reputation lists statistics"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get reputation lists statistics: {str(e)}")
