from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse, parse_qs

from ptnad.exceptions import PTNADAPIError


def _normalize_list_param(param: Optional[Union[str, List[str]]]) -> Optional[List[str]]:
    """
    Normalize parameter to list format.

    Args:
        param: Parameter that can be either a string or list of strings

    Returns:
        List of strings or None if param is None
    """
    if param is None:
        return None
    if isinstance(param, str):
        return [param]
    return param


class HostsAPI:
    def __init__(self, client) -> None:
        self.client = client

    def _get_hosts_data(
        self,
        id: Optional[Union[str, List[str]]] = None,
        host: Optional[Union[str, List[str]]] = None,
        type: Optional[Union[str, List[str]]] = None,
        role: Optional[Union[str, List[str]]] = None,
        groups: Optional[Union[str, List[str]]] = None,
        traffic_incoming: Optional[Union[str, List[str]]] = None,
        traffic_outgoing: Optional[Union[str, List[str]]] = None,
        has_redef: Optional[bool] = None,
        comment: Optional[bool] = None,
        ordering: Optional[str] = None,
        history_depth: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Internal method to get the full response from the Hosts API.

        Args:
            id (Optional[Union[str, List[str]]]): Filter by host IDs. Can be a single string or list of strings.
            host (Optional[Union[str, List[str]]]): Filter by host identifiers (id, ip.ip, hostname, user_hostname, dns.dns). Can be a single string or list of strings.
            type (Optional[Union[str, List[str]]]): Filter by host type IDs (filters by both type and user_type). Can be a single string or list of strings.
            role (Optional[Union[str, List[str]]]): Filter by role IDs. Can be a single string or list of strings.
            groups (Optional[Union[str, List[str]]]): Filter by host groups. Can be a single string or list of strings.
            traffic_incoming (Optional[Union[str, List[str]]]): Filter by incoming traffic (protocol, port, banner). Can be a single string or list of strings.
            traffic_outgoing (Optional[Union[str, List[str]]]): Filter by outgoing traffic (protocol, banner). Can be a single string or list of strings.
            has_redef (Optional[bool]): Filter by presence of user-defined overrides (type or roles).
            comment (Optional[bool]): Filter hosts with/without comments.
            ordering (Optional[str]): Field to sort the results by. Sorting is possible by id, ip,
                first_seen, last_seen, has_redef, hostname, comment. To sort in descending order,
                add a minus sign before the field name (e.g., ordering=-last_seen).
            history_depth (Optional[int]): Number of nested document records to return. Default is 5.
                Set to -1 to show all history for all hosts.
            limit (Optional[int]): Maximum number of hosts to return.
            offset (Optional[int]): Number of hosts to skip.

        Returns:
            Dict[str, Any]: Full API response

        Raises:
            PTNADAPIError: If there's an error retrieving the hosts.

        Note:
            By default, hosts are sorted by -last_seen and -id.
            Nested lists (ip, os, dns, server_services, client_services, credentials) are sorted by -last_seen and -id.
        """
        # Normalize parameters to list format
        id = _normalize_list_param(id)
        host = _normalize_list_param(host)
        type = _normalize_list_param(type)
        role = _normalize_list_param(role)
        groups = _normalize_list_param(groups)
        traffic_incoming = _normalize_list_param(traffic_incoming)
        traffic_outgoing = _normalize_list_param(traffic_outgoing)

        url_params = {}

        # Add filter parameters if provided
        if id:
            url_params["id"] = ",".join(id)
        if host:
            url_params["host"] = ",".join(host)
        if type:
            url_params["type"] = ",".join(type)
        if role:
            url_params["role"] = ",".join(role)
        if groups:
            url_params["groups"] = ",".join(groups)
        if traffic_incoming:
            url_params["traffic_incoming"] = ",".join(traffic_incoming)
        if traffic_outgoing:
            url_params["traffic_outgoing"] = ",".join(traffic_outgoing)
        if has_redef is not None:
            url_params["has_redef"] = str(has_redef).lower()
        if comment is not None:
            url_params["comment"] = str(comment).lower()
        if ordering:
            url_params["ordering"] = ordering
        if history_depth is not None:
            url_params["history_depth"] = history_depth
        if limit is not None:
            url_params["limit"] = limit
        if offset is not None:
            url_params["offset"] = offset

        try:
            response = self.client.get("/hosts", params=url_params).json()
            return response
        except PTNADAPIError as e:
            e.operation = "get hosts"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get hosts: {str(e)}")

    def get_hosts(
        self,
        id: Optional[Union[str, List[str]]] = None,
        host: Optional[Union[str, List[str]]] = None,
        type: Optional[Union[str, List[str]]] = None,
        role: Optional[Union[str, List[str]]] = None,
        groups: Optional[Union[str, List[str]]] = None,
        traffic_incoming: Optional[Union[str, List[str]]] = None,
        traffic_outgoing: Optional[Union[str, List[str]]] = None,
        has_redef: Optional[bool] = None,
        comment: Optional[bool] = None,
        ordering: Optional[str] = None,
        history_depth: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get a list of hosts.

        Args:
            id (Optional[Union[str, List[str]]]): Filter by host IDs. Can be a single string or list of strings.
            host (Optional[Union[str, List[str]]]): Filter by host identifiers (id, ip.ip, hostname, user_hostname, dns.dns). Can be a single string or list of strings.
            type (Optional[Union[str, List[str]]]): Filter by host type IDs (filters by both type and user_type). Can be a single string or list of strings.
            role (Optional[Union[str, List[str]]]): Filter by role IDs. Can be a single string or list of strings.
            groups (Optional[Union[str, List[str]]]): Filter by host groups. Can be a single string or list of strings.
            traffic_incoming (Optional[Union[str, List[str]]]): Filter by incoming traffic (protocol, port, banner). Can be a single string or list of strings.
            traffic_outgoing (Optional[Union[str, List[str]]]): Filter by outgoing traffic (protocol, banner). Can be a single string or list of strings.
            has_redef (Optional[bool]): Filter by presence of user-defined overrides (type or roles).
            comment (Optional[bool]): Filter hosts with/without comments.
            ordering (Optional[str]): Field to sort the results by. Sorting is possible by id, ip,
                first_seen, last_seen, has_redef, hostname, comment. To sort in descending order,
                add a minus sign before the field name (e.g., ordering=-last_seen).
            history_depth (Optional[int]): Number of nested document records to return. Default is 5.
                Set to -1 to show all history for all hosts.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing host information.

        Raises:
            PTNADAPIError: If there's an error retrieving the hosts.

        Note:
            By default, hosts are sorted by -last_seen and -id.
            Nested lists (ip, os, dns, server_services, client_services, credentials) are sorted by -last_seen and -id.
        """
        response = self._get_hosts_data(
            id=id,
            host=host,
            type=type,
            role=role,
            groups=groups,
            traffic_incoming=traffic_incoming,
            traffic_outgoing=traffic_outgoing,
            has_redef=has_redef,
            comment=comment,
            ordering=ordering,
            history_depth=history_depth
        )
        return response["results"]

    def get_all_hosts(
        self,
        id: Optional[Union[str, List[str]]] = None,
        host: Optional[Union[str, List[str]]] = None,
        type: Optional[Union[str, List[str]]] = None,
        role: Optional[Union[str, List[str]]] = None,
        groups: Optional[Union[str, List[str]]] = None,
        traffic_incoming: Optional[Union[str, List[str]]] = None,
        traffic_outgoing: Optional[Union[str, List[str]]] = None,
        has_redef: Optional[bool] = None,
        comment: Optional[bool] = None,
        ordering: Optional[str] = None,
        history_depth: Optional[int] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Get all hosts using pagination.

        Args:
            id (Optional[Union[str, List[str]]]): Filter by host IDs. Can be a single string or list of strings.
            host (Optional[Union[str, List[str]]]): Filter by host identifiers (id, ip.ip, hostname, user_hostname, dns.dns). Can be a single string or list of strings.
            type (Optional[Union[str, List[str]]]): Filter by host type IDs (filters by both type and user_type). Can be a single string or list of strings.
            role (Optional[Union[str, List[str]]]): Filter by role IDs. Can be a single string or list of strings.
            groups (Optional[Union[str, List[str]]]): Filter by host groups. Can be a single string or list of strings.
            traffic_incoming (Optional[Union[str, List[str]]]): Filter by incoming traffic (protocol, port, banner). Can be a single string or list of strings.
            traffic_outgoing (Optional[Union[str, List[str]]]): Filter by outgoing traffic (protocol, banner). Can be a single string or list of strings.
            has_redef (Optional[bool]): Filter by presence of user-defined overrides (type or roles).
            comment (Optional[bool]): Filter hosts with/without comments.
            ordering (Optional[str]): Field to sort the results by. Sorting is possible by id, ip,
                first_seen, last_seen, has_redef, hostname, comment. To sort in descending order,
                add a minus sign before the field name (e.g., ordering=-last_seen).
            history_depth (Optional[int]): Number of nested document records to return. Default is 5.
                Set to -1 to show all history for all hosts.
            limit (int): Number of hosts to fetch per request (default: 100).

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing all host information.

        Raises:
            PTNADAPIError: If there's an error retrieving the hosts.

        Note:
            By default, hosts are sorted by -last_seen and -id.
            Nested lists (ip, os, dns, server_services, client_services, credentials) are sorted by -last_seen and -id.
        """
        all_hosts = []
        cursor = None

        while True:
            # Use cursor if available, otherwise start with offset 0
            if cursor:
                response = self._get_hosts_data_with_cursor(
                    id=id,
                    host=host,
                    type=type,
                    role=role,
                    groups=groups,
                    traffic_incoming=traffic_incoming,
                    traffic_outgoing=traffic_outgoing,
                    has_redef=has_redef,
                    comment=comment,
                    ordering=ordering,
                    history_depth=history_depth,
                    limit=limit,
                    cursor=cursor
                )
            else:
                response = self._get_hosts_data(
                    id=id,
                    host=host,
                    type=type,
                    role=role,
                    groups=groups,
                    traffic_incoming=traffic_incoming,
                    traffic_outgoing=traffic_outgoing,
                    has_redef=has_redef,
                    comment=comment,
                    ordering=ordering,
                    history_depth=history_depth,
                    limit=limit
                )

            hosts = response["results"]
            all_hosts.extend(hosts)

            if response["next"] is None:
                break

            # Extract cursor from next URL
            cursor = self._extract_cursor_from_url(response["next"])

        return all_hosts

    def _extract_cursor_from_url(self, url: str) -> Optional[str]:
        """Extract cursor parameter from pagination URL."""
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            return query_params.get("cursor", [None])[0]
        except Exception:
            return None

    def _get_hosts_data_with_cursor(
        self,
        id: Optional[Union[str, List[str]]] = None,
        host: Optional[Union[str, List[str]]] = None,
        type: Optional[Union[str, List[str]]] = None,
        role: Optional[Union[str, List[str]]] = None,
        groups: Optional[Union[str, List[str]]] = None,
        traffic_incoming: Optional[Union[str, List[str]]] = None,
        traffic_outgoing: Optional[Union[str, List[str]]] = None,
        has_redef: Optional[bool] = None,
        comment: Optional[bool] = None,
        ordering: Optional[str] = None,
        history_depth: Optional[int] = None,
        limit: int = 100,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Internal method to get hosts data using cursor-based pagination.
        """
        # Normalize parameters to list format
        id = _normalize_list_param(id)
        host = _normalize_list_param(host)
        type = _normalize_list_param(type)
        role = _normalize_list_param(role)
        groups = _normalize_list_param(groups)
        traffic_incoming = _normalize_list_param(traffic_incoming)
        traffic_outgoing = _normalize_list_param(traffic_outgoing)

        url_params = {}

        # Add filter parameters if provided
        if id:
            url_params["id"] = ",".join(id)
        if host:
            url_params["host"] = ",".join(host)
        if type:
            url_params["type"] = ",".join(type)
        if role:
            url_params["role"] = ",".join(role)
        if groups:
            url_params["groups"] = ",".join(groups)
        if traffic_incoming:
            url_params["traffic_incoming"] = ",".join(traffic_incoming)
        if traffic_outgoing:
            url_params["traffic_outgoing"] = ",".join(traffic_outgoing)
        if has_redef is not None:
            url_params["has_redef"] = str(has_redef).lower()
        if comment is not None:
            url_params["comment"] = str(comment).lower()
        if ordering:
            url_params["ordering"] = ordering
        if history_depth is not None:
            url_params["history_depth"] = history_depth
        url_params["limit"] = limit
        if cursor:
            url_params["cursor"] = cursor

        try:
            response = self.client.get("/hosts", params=url_params).json()
            return response
        except PTNADAPIError as e:
            e.operation = "get hosts"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get hosts: {str(e)}")

    def get_host(self, host_id: str, history_depth: Optional[int] = None) -> Dict[str, Any]:
        """
        Get information about a specific host by its id.

        Args:
            host_id (str): ID of the host.
            history_depth (Optional[int]): Number of nested document records to return. Default is 5.
                Set to -1 to show all history.

        Returns:
            Dict[str, Any]: Information about the host.

        Raises:
            PTNADAPIError: If there's an error retrieving the host information.
        """
        url_params = {}
        if history_depth is not None:
            url_params["history_depth"] = history_depth

        try:
            response = self.client.get(f"/hosts/{host_id}", params=url_params).json()
            return response
        except PTNADAPIError as e:
            e.operation = f"get host {host_id}"
            raise
        except Exception as e:
            raise PTNADAPIError(f"Failed to get host {host_id}: {str(e)}")
