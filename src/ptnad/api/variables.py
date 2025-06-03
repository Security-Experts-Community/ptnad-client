from typing import Any, Dict, List, Optional

from ptnad.exceptions import PTNADAPIError, ValidationError


class VariablesAPI:
    def __init__(self, client) -> None:
        self.client = client

    def create_group(self, name: str, type: str = "ip", value: str | None = None,
                     comment: str | None = None) -> Dict[str, Any]:
        """
        Create a new group of hosts or ports.

        Args:
            name (str): Name of the group.
            type (str): Type of the group ('port' or 'ip', 'ip' by default).
            value (Optional[str]): Value of the group (empty string by default).
            comment (Optional[str]): Comment for the group.

        Returns:
            Dict[str, Any]: Information about the created group.

        Raises:
            ValidationError: If the input parameters are invalid.
            PTNADAPIError: If there's an error creating the group.

        Note:
            Changes are saved during commit, which should be performed by using the apply_changes()
            method from the signatures.

        """
        if type not in ["port", "ip"]:
            msg = "Type must be 'port' or 'ip'."
            raise ValidationError(msg)

        data = {
            "name": name,
            "type": type
        }
        if value is not None:
            data["value"] = value
        if comment is not None:
            data["comment"] = comment

        try:
            response = self.client.post("/variables", json=data).json()
            return response
        except PTNADAPIError as e:
            e.operation = "create group"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to create group: {str(e)}")

    def get_groups(self, search: str | None = None) -> List[Dict[str, Any]]:
        """
        Get all Rules using pagination.

        Args:
            search (Optional[str]): Keyword to filter the groups (search in name, value, comment).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing all group information.

        Raises:
            PTNADAPIError: If there's an error retrieving the group.

        """
        url_params = {}
        if search:
            url_params["search"] = search

        try:
            response = self.client.get("/variables", params=url_params).json()
            return response["results"]
        except PTNADAPIError as e:
            e.operation = "get groups"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get groups: {str(e)}")


    def get_group(self, group_id: int) -> Dict[str, Any]:
        """
        Get information about a specific group by its id.

        Args:
            group_id (int): id of the group.

        Returns:
            Dict[str, Any]: Information about the group.

        Raises:
            PTNADAPIError: If there's an error retrieving the group.

        """
        try:
            response = self.client.get(f"/variables/{group_id}").json()
            return response
        except PTNADAPIError as e:
            e.operation = f"get group {group_id}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get group {group_id}: {str(e)}")

    def update_group(self, group_id: int, value: str | None = None, comment: str | None = None) -> Dict[str, Any]:
        """
        Update a group variable.

        Args:
            group_id (int): id of the group to update.
            value (Optional[str]): Value of the group.
            comment (Optional[str]): Comment for the group.

        Returns:
            Dict[str, Any]: Updated information about the group.

        Raises:
            ValidationError: If neither value nor comment is provided.
            PTNADAPIError: If there's an error updating the group.

        Note:
            Changes are saved during commit, which should be performed by using the apply_changes()
            method from the signatures.

        """
        data = {}
        if value is not None:
            data["value"] = value
        if comment is not None:
            data["comment"] = comment

        if not data:
            raise ValidationError("At least one of 'value' or 'comment' must be provided")

        try:
            response = self.client.patch(f"/variables/{group_id}", json=data).json()
            return response
        except PTNADAPIError as e:
            e.operation = f"update group {group_id}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to update group {group_id}: {str(e)}")

    def delete_group(self, group_id: int) -> bool:
        """
        Delete a group variable.

        Args:
            group_id (int): id of the group to delete.

        Returns:
            bool: True if commit is required, False otherwise.

        Raises:
            PTNADAPIError: If there's an error deleting the group.

        Note:
            Changes are saved during commit, which should be performed by using the apply_changes()
            method from the signatures.

        """
        commit_required = True
        try:
            response = self.client.delete(f"/variables/{group_id}")
            if response.status_code == 204:
                commit_required = False
        except PTNADAPIError as e:
            e.operation = f"delete group {group_id}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to delete group {group_id}: {str(e)}")

        return commit_required

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about Variables (IP/Port Groups).

        Returns:
            Dict[str, Any]: Statistics about Variables.

        Raises:
            PTNADAPIError: If there's an error retrieving the statistics.

        """
        try:
            response = self.client.get("/variables/stats").json()
            return response
        except PTNADAPIError as e:
            e.operation = "get Variables statistics"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get variables statistics: {str(e)}")
