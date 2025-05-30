from typing import Any, Dict, List

from ptnad.exceptions import PTNADAPIError


class SignaturesAPI:
    def __init__(self, client) -> None:
        self.client = client

    def get_classes(self, search: str | None = None, ordering: str | None = None, **filters) -> List[Dict[str, Any]]:
        """
        Get a list of signature classes.

        Args:
            search (Optional[str]): Keyword to filter the classes.
            ordering (Optional[str]): Field to sort the results by.
            **filters: Additional filters (name, title, priority).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing signature class information.

        Raises:
            PTNADAPIError: If there's an error retrieving the classes.

        """
        params = {k: v for k, v in filters.items() if v is not None}
        if search:
            params["search"] = search
        if ordering:
            params["ordering"] = ordering

        try:
            response = self.client.get("/signatures/classes", params=params).json()
            return response["results"]
        except PTNADAPIError as e:
            e.operation = "get signature classes"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get signature classes: {str(e)}")

    def _get_rules_data(self, search: str | None = None, ordering: str | None = None,
                           limit: int = 100, offset: int = 0, **filters) -> Dict[str, Any]:
        """
        Internal method to get the full response from the Signatures API.

        Args:
            search (Optional[str]): Keyword to filter the rules.
            ordering (Optional[str]): Field to sort the results by.
            limit (int): Maximum number of rules to return.
            offset (int): Number of rules to skip.
            **filters: Additional filters. Available filters:
                sid: Filter by sid (can be a single value or a list)
                sid__gte: sid greater than or equal to
                sid__lt: sid less than
                vendor: Filter by vendor name (can be a single value or a list)
                enabled: Filter by enabled status (true or false)
                has_redef: Filter by has_redef status (true or false)
                has_exceptions: Filter by has_exceptions status (true or false)
                priority: Filter by priority (if priority=4, finds all rules with priority>=4)
                cls: Filter by class name (can be a single value or a list)
                diff: Filter by rule changes, valid values (can be a list): added (+), updated (*), removed (-), unchanged (=). Available in PT NAD 12.2+
                has_error: Filter by has_error status (true or false)
                client: Search for IP address in src_adr and dst_adr
                server: Search for IP address in src_adr and dst_adr

        Returns:
            Dict[str, Any]: Full API response

        Raises:
            PTNADAPIError: If there's an error retrieving the rules.

        """
        # Separate pagination, search and ordering parameters from filters
        url_params = {}
        if search:
            url_params["search"] = search
        if ordering:
            url_params["ordering"] = ordering
        url_params["limit"] = limit
        url_params["offset"] = offset

        # Extract filter parameters
        filter_params = {k: v for k, v in filters.items() if v is not None}

        # If we have filters, send them in the JSON payload
        if filter_params:
            try:
                response = self.client.get("/signatures/rules", params=url_params, json={"filter": filter_params}).json()
                return response
            except PTNADAPIError as e:
                e.operation = "get Rules"
                raise
            except Exception as e:
                raise PTNADAPIError(f"Failed to get Rules: {str(e)}")
        else:
            # No filters, use regular GET request
            try:
                response = self.client.get("/signatures/rules", params=url_params).json()
                return response
            except PTNADAPIError as e:
                e.operation = "get Rules"
                raise
            except Exception as e:
                raise PTNADAPIError(f"Failed to get Rules: {str(e)}")

    def get_rules(self, search: str | None = None, ordering: str | None = None,
                  limit: int = 100, offset: int = 0, **filters) -> List[Dict[str, Any]]:
        """
        Get a list of Rules.

        Args:
            search (Optional[str]): Keyword to filter the rules.
            ordering (Optional[str]): Field to sort the results by.
            limit (int): Maximum number of rules to return (default: 100).
            offset (int): Number of rules to skip (default: 0).
            **filters: Additional filters. Available filters:
                sid: Filter by sid (can be a single value or a list)
                sid__gte: sid greater than or equal to
                sid__lt: sid less than
                vendor: Filter by vendor name (can be a single value or a list)
                enabled: Filter by enabled status (true or false)
                has_redef: Filter by has_redef status (true or false)
                has_exceptions: Filter by has_exceptions status (true or false)
                priority: Filter by priority (if priority=4, finds all rules with priority>=4)
                cls: Filter by class name (can be a single value or a list)
                diff: Filter by rule changes, valid values (can be a list): added (+), updated (*), removed (-), unchanged (=). Available in 12.2+
                has_error: Filter by has_error status (true or false)
                client: Search for IP address in src_adr and dst_adr
                server: Search for IP address in src_adr and dst_adr

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing Rule information.

        Raises:
            PTNADAPIError: If there's an error retrieving the rules.

        """
        response = self._get_rules_data(search, ordering, limit, offset, **filters)
        return response["results"]

    def get_rule(self, rule_id: int) -> Dict[str, Any]:
        """
        Get information about a specific Rule.

        Args:
            rule_id (int): sid of the Rule.

        Returns:
            Dict[str, Any]: Information about the Rule.

        Raises:
            PTNADAPIError: If there's an error retrieving the rule.

        """
        try:
            response = self.client.get(f"/signatures/rules/{rule_id}").json()
            return response
        except PTNADAPIError as e:
            e.operation = f"get Rule {rule_id}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get rule {rule_id}: {str(e)}")

    def update_rule(self, rule_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update a Rule.

        Args:
            rule_id (int): ID of the Rule to update.
            **kwargs: Fields to update (enabled, action, msg, etc.).

        Returns:
            Dict[str, Any]: Updated information about the Rule.

        Raises:
            PTNADAPIError: If there's an error updating the rule.

        """
        try:
            response = self.client.patch(f"/signatures/rules/{rule_id}", json=kwargs).json()
            return response
        except PTNADAPIError as e:
            e.operation = f"update Rule {rule_id}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to update Rule {rule_id}: {str(e)}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about Rules.

        Returns:
            Dict[str, Any]: Statistics about Rules.

        Raises:
            PTNADAPIError: If there's an error retrieving the statistics.

        """
        try:
            response = self.client.get("/signatures/stats").json()
            return response
        except PTNADAPIError as e:
            e.operation = "get Rules statistics"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get Rules statistics: {str(e)}")

    def apply_changes(self) -> Dict[str, str]:
        """
        Apply changes made to Rules and commit them to sensors.

        Returns:
            Dict[str, str]: A dictionary with the hashsum of the package.

        Raises:
            PTNADAPIError: If there's an error applying the changes.

        """
        try:
            response = self.client.post("/signatures/commit").json()
            if "hashsum" in response:
                return response
            if "fatal_error" in response or "other_errors" in response:
                errors = []
                if response.get("fatal_error"):
                    errors.append(response["fatal_error"])
                if response.get("other_errors"):
                    errors.extend(response["other_errors"])
                raise PTNADAPIError(f"Failed to commit signature changes: {', '.join(errors)}")
            return response
        except PTNADAPIError as e:
            e.operation = f"commit signature changes: {', '.join(errors)}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to apply Rule changes: {str(e)}")

    def revert_changes(self) -> None:
        """
        Revert changes made to Rules.

        Raises:
            PTNADAPIError: If there's an error reverting the changes.

        """
        try:
            self.client.post("/signatures/rollback")
        except PTNADAPIError as e:
            e.operation = "revert Rule changes"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to revert Rule changes: {str(e)}")
